/*
 * main.c
 *
 *  Created on: Apr 21, 2022
 *      Author: daro
 */


#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <inttypes.h>
#include <math.h>

#define DR_WAV_IMPLEMENTATION
#include "dr_wav.h"
#include "fixmath.h"
#include "FFT.h"
#include "types.h"

#define N 64
#define EXP 6
#define TUNING 19
clock_t start, end;

void encoder(int16_t *samples, unsigned short size, uint16_t * output, uint64_t nSamples)
{
	uint64_t block_idx = 0;
	uint64_t sample_idx = 0;
	lcomplex twiddle[EXP];
	lcomplex temp_output[size];

	fft_init(twiddle, EXP);

	start = clock();

	for(block_idx = 0; block_idx < nSamples; block_idx+=N)
	{
		for(sample_idx = 0; sample_idx < size; sample_idx++)
		{
			temp_output[sample_idx].re = (samples[block_idx + sample_idx]<<16);
			temp_output[sample_idx].im = 0;
		}

		fft(temp_output, EXP, twiddle, 1);

		for(sample_idx = 0; sample_idx < size/2; sample_idx++)
		{
			uint16_t val1 = 0x00ff&(((temp_output[sample_idx].re+32768)>>TUNING)+128);
			uint16_t val2 = 0x00ff&(((temp_output[sample_idx].im+32768)>>TUNING)+128);
			output[block_idx/2 + sample_idx] = ((val1)<<8) | (val2);
		}
	}

	end = clock();

	printf("TIME ENCODING: %f\n", (double)(end-start)/CLOCKS_PER_SEC);
}



void decoder(uint16_t *coefficients, unsigned short size, int16_t * output, uint64_t nSamples)
{
	uint16_t block_idx = 0;
	uint16_t sample_idx = 0;
	lcomplex twiddle[EXP];
	lcomplex temp_output[size];

    //initialize FFT

	fft_init(twiddle, EXP);

	start = clock();

	for(block_idx = 0; block_idx < nSamples/2; block_idx+=N/2)
	{
		temp_output[0].re = ((int32_t)((0xff00&coefficients[0])>>8)-128)<<TUNING;
		temp_output[0].im = ((int32_t)((0x00ff&coefficients[0])-128))<<TUNING;

		temp_output[N/2].re = 0;
		temp_output[N/2].im = 0;

		for(sample_idx = 1; sample_idx < size/2; sample_idx++)
		{
			temp_output[sample_idx].re = ((int32_t)((0xff00&coefficients[block_idx + sample_idx])>>8)-128)<<TUNING;
			temp_output[sample_idx].im = ((int32_t)((0x00ff&coefficients[block_idx + sample_idx])-128))<<TUNING;

			temp_output[N-sample_idx].re = ((int32_t)((0xff00&coefficients[block_idx + sample_idx])>>8)-128)<<TUNING;
			temp_output[N-sample_idx].im = -((int32_t)((0x00ff&coefficients[block_idx + sample_idx])-128))<<TUNING;
		}


		ifft(temp_output, EXP, twiddle, 0);

		//scaling the output
		for(sample_idx = 0; sample_idx < size; sample_idx++)
		{
			output[block_idx*2 + sample_idx] = 0xffff&(temp_output[sample_idx].re+32768)>>16;
		}
	}

	end = clock();

	printf("TIME DECODING: %f\n", (double)(end-start)/CLOCKS_PER_SEC);
}


int main()
{

	drwav wav;
	drwav wav_out;

	drwav_init_file(&wav, "test_audio.wav", NULL);

	uint64_t samplesLength = wav.totalPCMFrameCount;
	uint64_t len = (uint64_t)(ceil((double)samplesLength/64)*64);
	int16_t* pSampleData = (int16_t*)malloc((size_t)len * wav.channels * sizeof(int16_t));
	uint16_t* enc_output = (uint16_t*)malloc((size_t)(len/2) * wav.channels * sizeof(uint16_t));
	int16_t* dec_output = (int16_t*)malloc((size_t)len * wav.channels * sizeof(int16_t));

	drwav_read_pcm_frames_s16(&wav, wav.totalPCMFrameCount, pSampleData);

	drwav_uninit(&wav);

	encoder(pSampleData, N, enc_output, len);

	decoder(enc_output, N, dec_output, len);

	drwav_data_format format;
	format.container = drwav_container_riff;
	format.format = DR_WAVE_FORMAT_PCM;
	format.channels = 1;
	format.sampleRate = 8000;
	format.bitsPerSample = 16;

	drwav_init_file_write(&wav_out,"wav_out.wav",&format,NULL);

	drwav_write_pcm_frames(&wav_out,samplesLength,dec_output);


	return 0;
}











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

#include "types.h"

#define N 64
#define EXP 6
#define TUNING 19
clock_t start, end;

#include <NE10.h>


void encoder(int16_t *samples, unsigned short size, uint16_t * output, uint64_t nSamples)
{
	//LOAD SAMPLES TO REAL PART OF INPUT
	uint16_t block_idx = 0;
	uint16_t sample_idx = 0;

	ne10_fft_cpx_int32_t* src = (ne10_fft_cpx_int32_t*) NE10_MALLOC(N * sizeof(ne10_fft_cpx_int32_t)); // A source array of input data
	ne10_fft_cpx_int32_t* dst = (ne10_fft_cpx_int32_t*) NE10_MALLOC(N * sizeof(ne10_fft_cpx_int32_t));
	ne10_fft_cfg_int32_t cfg;

	start = clock();
    //initialize FFT

	cfg = ne10_fft_alloc_c2c_int32_neon(N);

	for(block_idx = 0; block_idx < nSamples; block_idx+=N)
	{
		for(sample_idx = 0; sample_idx < size; sample_idx++)
		{
			src[sample_idx].r = (samples[block_idx + sample_idx]<<16);
			src[sample_idx].i = 0;
		}

		//execute FFT block of samples

		ne10_fft_c2c_1d_int32_neon(dst,src,cfg,0,1);

		//report only the lower half of the result
		for(sample_idx = 0; sample_idx < size/2; sample_idx++)
		{
			uint16_t val1 = 0x00ff&(((dst[sample_idx].r+32768)>>TUNING)+128);
			uint16_t val2 = 0x00ff&(((dst[sample_idx].i+32768)>>TUNING)+128);
			output[block_idx/2 + sample_idx] = ((val1)<<8) | (val2);
		}

	}
	    //report only the lower half of the result
	//printf("max %"PRId32 "\n",maxval>>TUNING);
	end = clock();
	printf("TIME ENCODING: %f\n", (double)(end-start)/CLOCKS_PER_SEC);
}

void decoder(uint16_t *coefficients, unsigned short size, int16_t * output,  uint64_t nSamples)
{
	//Mirror result of RFFT

	uint16_t block_idx = 0;
	uint16_t sample_idx = 0;

	ne10_fft_cpx_int32_t* src = (ne10_fft_cpx_int32_t*) NE10_MALLOC(N * sizeof(ne10_fft_cpx_int32_t)); // A source array of input data
	ne10_fft_cpx_int32_t* dst = (ne10_fft_cpx_int32_t*) NE10_MALLOC(N * sizeof(ne10_fft_cpx_int32_t));
	ne10_fft_cfg_int32_t cfg;

	cfg = ne10_fft_alloc_c2c_int32_neon(N);
    //initialize FFT
	start = clock();

		for(block_idx = 0; block_idx < nSamples/2; block_idx+=N/2)
		{
			src[0].r = ((int32_t)((0xff00&coefficients[0])>>8)-128)<<TUNING;
			src[0].i = ((int32_t)((0x00ff&coefficients[0])-128))<<TUNING;

			src[N/2].r = 0;
			src[N/2].i = 0;

			for(sample_idx = 1; sample_idx < size/2; sample_idx++)
			{
				src[sample_idx].r = ((int32_t)((0xff00&coefficients[block_idx + sample_idx])>>8)-128)<<TUNING;
				src[sample_idx].i = ((int32_t)((0x00ff&coefficients[block_idx + sample_idx])-128))<<TUNING;

				src[N-sample_idx].r = ((int32_t)((0xff00&coefficients[block_idx + sample_idx])>>8)-128)<<TUNING;
				src[N-sample_idx].i = -((int32_t)((0x00ff&coefficients[block_idx + sample_idx])-128))<<TUNING;
			}

		//execute FFT block of samples

			ne10_fft_c2c_1d_int32_neon(dst,src,cfg,1,0);

		//ifft(values, EXP, twiddle, 1);

			for(sample_idx = 0; sample_idx < size; sample_idx++)
			{
				output[block_idx*2 + sample_idx] = 0xffff&(dst[sample_idx].r+32768)>>16;
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

	drwav_init_file_write(&wav_out,"neon_wav_out.wav",&format,NULL);

	drwav_write_pcm_frames(&wav_out,samplesLength,dec_output);

	return 0;
}











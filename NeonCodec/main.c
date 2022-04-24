/*
 * main.c
 *
 *  Created on: Apr 21, 2022
 *      Author: daro
 */

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include "types.h"
#include "FFT.h"
#include "fixedPoint.h"
#include <string.h>
#include <inttypes.h>
#include <time.h>
#include <NE10.h>

//uint16_t EXP = 4;

#define N 64
#define EXP 6
#define length 24960
complex twiddle[EXP];
complex output_vector[N/2];

clock_t start, end;


#define ARRAY_GUARD_LEN      4


void encoder(int16_t *samples, unsigned short size, uint16_t * output)
{
	//LOAD SAMPLES TO REAL PART OF INPUT
	unsigned short i;
	unsigned short idx_block;
	//complex values[N];
	ne10_fft_cpx_int16_t* src = (ne10_fft_cpx_int16_t*) NE10_MALLOC(N * sizeof(ne10_fft_cpx_int16_t)); // A source array of input data
	ne10_fft_cpx_int16_t* dst = (ne10_fft_cpx_int16_t*) NE10_MALLOC(N * sizeof(ne10_fft_cpx_int16_t));
	ne10_fft_cfg_int16_t cfg;

	start = clock();
    //initialize FFT
	//fft_init(twiddle, EXP);

	for(idx_block = 0; idx_block < length; idx_block += N)
	{
		for (i = 0; i<N; i++)
		{
			//values[i].re = samples[idx_block + i];
			src[i].r =(ne10_int16_t) samples[idx_block + i];
			src[i].i =(ne10_int16_t) 0x0000;
		}

		//execute FFT block of samples
		cfg = ne10_fft_alloc_c2c_int16 (N);

		ne10_fft_c2c_1d_int16(dst,src,cfg,0,0);

		//report only the lower half of the result
		for(i = 0; i < N/2; i++)
				{
					if(dst[i].r < 0) dst[i].r = 0x0080 | ((-dst[i].r/6) &0x00ff);

					else if(dst[i].r > 0) dst[i].r = (dst[i].r/6) & 0x00ff;

					if(dst[i].i < 0) dst[i].i = 0x0080 | ((-dst[i].i/6) &0x00ff);

					else if(dst[i].i > 0) dst[i].i = (dst[i].i/6) & 0x00ff;
					output[i+(idx_block>>1)] = (((uint16_t)((dst[i].r) & 0x00ff)) << 8) | ((uint16_t)((dst[i].i) & 0x00ff)); //quantization
				}

	}
	    //report only the lower half of the result
	end = clock();
	printf("TIME ENCODING: %f\n", (double)(end-start)/CLOCKS_PER_SEC);
}

void decoder(uint16_t *coefficients, unsigned short size, int16_t * output)
{
	//Mirror result of RFFT

	unsigned short i,idx_block;
	ne10_fft_cpx_int16_t* src = (ne10_fft_cpx_int16_t*) NE10_MALLOC(N * sizeof(ne10_fft_cpx_int16_t)); // A source array of input data
	ne10_fft_cpx_int16_t* dst = (ne10_fft_cpx_int16_t*) NE10_MALLOC(N * sizeof(ne10_fft_cpx_int16_t));
	ne10_fft_cfg_int16_t cfg;

    //initialize FFT
	start = clock();

	for (idx_block = 0; idx_block<length/2; idx_block+=(N/2))
	{
		for (i = 0; i<N/2; i++)
				{
					//printf("%d \n ", coefficients[i+idx_block]);
					if((coefficients[i+idx_block] & 0x8000) == 0x8000)
					{
						src[i].r = -((int16_t)(coefficients[i+idx_block]>>8)&0x007f)*6;
						src[N-i-1].r = -((int16_t)(coefficients[i+idx_block]>>8)&0x007f)*6;
					}

					else
					{
						src[i].r = ((int16_t)(coefficients[i+idx_block]>>8)&0x007f)*6;
						src[N-i-1].r = ((int16_t)(coefficients[i+idx_block]>>8)&0x007f)*6;
					}

					if((coefficients[i+idx_block] & 0x0080) == 0x0080)
					{
						src[i].i = -((int16_t)(coefficients[i+idx_block])&0x007f)*6;
						src[N-i-1].i = -((int16_t)(coefficients[i+idx_block])&0x7f)*6;
					}
					else
					{
						src[i].i = (((int16_t)(coefficients[i+idx_block])&0x7f)*6);
						src[N-i-1].i = (((int16_t)(coefficients[i+idx_block])&0x7f)*6);
					}

				}
		//execute FFT block of samples

		cfg = ne10_fft_alloc_c2c_int16 (N);
		ne10_fft_c2c_1d_int16(dst,src,cfg,1,0);

		//ifft(values, EXP, twiddle, 1);

		for (i = 0; i<N; i++)
		{
			output[i+(idx_block*2)] = dst[i].r;
		}
	}
	end = clock();
	printf("TIME DECODING: %f\n", (double)(end-start)/CLOCKS_PER_SEC);
}


int main()
{
	//int n;

	//printf("aaaa");
	FILE * stream = fopen("decoder2.txt", "r");
	FILE * fp_stream_enc = fopen("neon_encoder.txt", "w+");
	FILE * fp_stream_dec = fopen("neon_decoder.txt", "w+");

	int16_t samples[length];
	int16_t final[length];
	uint16_t out[length/2] = {0};
	//while()

	ne10_init();

	for(int i = 0; i<length;i++)
	{
		fscanf(stream, "%" SCNd16, &samples[i]);
	}

	encoder(samples, 64, out);

	for(int i = 0; i<length/2;i++)
	{
		fprintf(fp_stream_enc,"%u\n", out[i]);
	}

	fclose(fp_stream_enc);

	decoder(out, 64, final);

	for(int i = 0; i<length;i++)
	{
		fprintf(fp_stream_dec,"%d\n", final[i]);
	}

	fclose(fp_stream_dec);

	fclose(stream);



	return 0;
}











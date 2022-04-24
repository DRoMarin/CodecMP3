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


//uint16_t EXP = 4;

#define N 64
#define EXP 6
#define length 24960
complex twiddle[EXP];
complex output_vector[N/2];

clock_t start, end;



void encoder(int16_t *samples, unsigned short size, uint16_t * output)
{
	//LOAD SAMPLES TO REAL PART OF INPUT
	unsigned short i;
	unsigned short idx_block;
	complex values[N];

	start = clock();
    //initialize FFT
	fft_init(twiddle, EXP);

	for(idx_block = 0; idx_block < length; idx_block += N)
	{
		for (i = 0; i<N; i++)
		{
			values[i].re = samples[idx_block + i];
			values[i].im = 0x0000;
		}

		//execute FFT block of samples
		fft(values, EXP, twiddle, 1);

		//report only the lower half of the result
		for(i = 0; i < N/2; i++)
		{
			output[i+(idx_block>>1)] = (((uint16_t)((values[i].re/416) & 0x00ff)) << 8) | ((uint16_t)((values[i].im/416) & 0x00ff)); //quantization

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
	complex values[N] = {0};

    //initialize FFT
	start = clock();
	fft_init(twiddle, EXP);

	for (idx_block = 0; idx_block<length/2; idx_block+=(N/2))
	{
		for (i = 0; i<N/2; i++)
		{
			//printf("%d \n ", coefficients[i+idx_block]);
			values[i].re = (((int16_t)(coefficients[i+idx_block]>>8))*416);
			values[i].im = (((int16_t)(coefficients[i+idx_block] & 0x00ff))*416);
		    values[(N-i-1)].re = (((int16_t)(coefficients[i+idx_block]>>8))*416);
			values[(N-i-1)].im = -(((int16_t)(coefficients[i+idx_block] & 0x00ff))*416);
		}
		//execute FFT block of samples
		ifft(values, EXP, twiddle, 1);

		for (i = 0; i<N; i++)
		{
			output[i+(idx_block*2)] = values[i].re;
		}
	}
	end = clock();
	printf("TIME DECODING: %f\n", (double)(end-start)/CLOCKS_PER_SEC);
}


int main()
{
	//int n;

	//printf("aaaa");
	FILE * stream = fopen("decoder.txt", "r");
	FILE * fp_stream_enc = fopen("fp_encoder.txt", "w+");
	FILE * fp_stream_dec = fopen("fp_decoder.txt", "w+");

	int16_t samples[length];
	int16_t final[length];
	uint16_t out[length/2] = {0};
	//while()

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











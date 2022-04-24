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
#include <inttypes.h>
//#include <math.h>

//uint16_t EXP = 4;

#define N 64
#define EXP 6
#define length 24960
complex twiddle[EXP];
complex output_vector[N/2];

void encoder(int16_t *samples, unsigned short size, complex * output)
{
	//LOAD SAMPLES TO REAL PART OF INPUT
	unsigned short i;
	unsigned short idx_block;
	complex values[N];

    //initialize FFT
	fft_init(twiddle, EXP);

	for(idx_block = 0; idx_block < length; idx_block += N){
		for (i = 0; i<N; i++)
		{
			values[i].re = samples[idx_block + i];
			values[i].im = 0x0000;
		}

		//execute FFT block of samples
		fft(values, EXP, twiddle, 0);

		for(i = 0; i < N/2; i++)
		{
			output[i+(idx_block>>1)] = values[i];
		}

	}
	    //report only the lower half of the result
		//TO-DO quantization
	//}
}

void decoder(complex *coefficients, unsigned short size, int16_t * output)
{
	//Mirror result of RFFT
	//TO-DO RE-SCALE BACK

	unsigned short i,idx_block;
	complex values[N] = {0};

    //initialize FFT

	fft_init(twiddle, EXP);

	for (idx_block = 0; idx_block<length/2; idx_block+=(N/2))
	{
		for (i = 0; i<N/2; i++)
		{
			//printf("%d --- %d \n ", idx_block + i, N-i-1);
			values[i] = coefficients[i+idx_block];
		    values[(N-i-1)].re = coefficients[i+idx_block].re;
			values[(N-i-1)].im = -coefficients[i+idx_block].im;
		}
		//execute FFT block of samples
		ifft(values, EXP, twiddle, 0);

		for (i = 0; i<N; i++)
		{
			output[i+(idx_block<<1)] = values[i].re;
		}
	}


}

int main()
{
	//int n;

	//printf("aaaa");
	FILE * stream = fopen("testing.txt", "r");

	int16_t samples[length];
	int16_t final[length];
	complex out[length/2] = {0};
	//while()

	for(int i = 0; i<length/145;i++)
	{
		fscanf(stream, "%" SCNd16, &samples[i]);

		printf("%d \n", samples[i]);
	}

	encoder(samples, 64, out);

	//for(int i = 0; i<64;i++)
	//{
		//printf("%d + j*%d\n", out[i].re, out[i].im);
	//}

	decoder(out, 64, final);

	for(int i = 0; i<64;i++)
	{
		printf("%d \n", out[i]);
	}

	fclose(stream);


    //RE SCALING AND RECOVERY

	//int arr_csv[n];

	return 0;
}
//double pi = 3.1415926535897;










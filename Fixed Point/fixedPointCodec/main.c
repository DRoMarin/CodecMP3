/*
 * main.c
 *
 *  Created on: Apr 21, 2022
 *      Author: daro
 */

#include <stdint.h>
#include "types.h"
#include "FFT.h"
#include "fixedPoint.h"
//#include <math.h>

//uint16_t EXP = 4;

#define N 64
#define EXP 6
#define lenght 1000
complex twiddle[EXP];
complex output_vector[N/2];

void encoder(int16_t *samples, unsigned short size, complex * output)
{
	//LOAD SAMPLES TO REAL PART OF INPUT
	unsigned short i;
	complex values[lenght];

	for (i = 0; i<N; i++)
	{
		values[i].re = samples[i];
		values[i].im = 0x0000;
	}
    //initialize FFT
	fft_init(twiddle, EXP);

	//execute FFT block of samples
	for(i = 0; i< lenght; i+=N)
	{
		fft(values, EXP, twiddle, 1);
	}

    //report only the lower half of the result
	//TO-DO quantization
	for(i = 0; i < lenght/2; i++)
	{
		output[i] = values[i];
	}
}

void decoder(complex *coefficients, unsigned short size, int16_t * output)
{
	//Mirror result of RFFT
	//TO-DO RE-SCALE BACK

	unsigned short i;
	complex values[lenght];

	for (i = 0; i<N/2; i++)
	{
		values[i] = coefficients[i];
		values[lenght-i].re = coefficients[i].re;
		values[lenght-i].im = fp_sub(0x0000, coefficients[i].im);
	}

    //initialize FFT
	fft_init(twiddle, EXP);

	//execute FFT block of samples
	for(i = 0; i< lenght; i+=N)
	{
		fft(values, EXP, twiddle, 1);
	}

	for(i = 0; i < lenght; i++){
		output[i] = values[i].re;
	}
}

int main()
{
	return 0;
}
//double pi = 3.1415926535897;










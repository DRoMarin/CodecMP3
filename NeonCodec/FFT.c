
#include "types.h"
#include "FFT.h"
#include "fixedPoint.h"
#include <stdint.h>
#include <math.h>


double pi = 3.1415926535897;
#define SFT16 16

//Qs0.15 for twiddle
void fft_init(complex *W, short EXP)
{
	unsigned short L,LE,LE1;

	for(L=1; L<=EXP; L++)
	{
		LE = 1<<L;
		LE1 = LE>>1;
		W[L-1].re = (int)((0x7fff*cos(pi/LE1))+0.5);
		W[L-1].im = -(int)((0x7fff*sin(pi/LE1))+0.5);
	}
}

void bit_rev(complex *X, short EXP)
{
	unsigned short i,j,k;
	unsigned short N = 1 << EXP;
	unsigned short N2 = N>>1;
	complex temp;
	for (j = 0, i = 1; i < N-1; i++)
	{
		k = N2;
		while(k<=j)
		{
			j -= k;
			k >>= 1;
		}
		j += k;

		if (i<j)
		{
			temp = X[j];
			X[j] = X[i];
			X[i] = temp;
		}
	}
}

void fft(complex * X, unsigned short EXP, complex * W, unsigned short SCALE){
	complex temp;
	lcomplex ltemp;
	complex U;
	unsigned short i, j;
	unsigned short id;
	unsigned short N = 1<<EXP;
	unsigned short L;
	unsigned short LE;
	unsigned short LE1;

	unsigned short scale = SCALE;

	bit_rev(X,EXP);

	for(L=1; L <= EXP; L++){

		LE = 1<<L;
		LE1 = LE>>1;
		U.re = 0x7fff;
		U.im = 0;

		for (j = 0; j < LE1; j++)
		{
			for(i = j; i < N; i += LE)
			{
				id = i + LE1;
				ltemp.re = lfp_mul(X[id].re,	U.re);
				temp.re  = lfp_smas(ltemp.re, 	X[id].im, U.im)>>SFT16;
				temp.re  = fp_add(temp.re, 		1)>>scale;
				//temp.re = (X[id].re*U.re - X[id].im*U.im)*scale;

				ltemp.im = lfp_mul(X[id].im, 	U.re);
				temp.im  = lfp_smac(ltemp.im, 	X[id].re, U.im)>>SFT16;
				temp.im  = fp_add(temp.im, 		1)>>scale;
				//temp.im = (X[id].im*U.re + X[id].re*U.im)*scale;

				X[id].re = fp_sub(X[i].re>>scale, 	temp.re);
				X[id].im = fp_sub(X[i].im>>scale, 	temp.im);
				//X[id].re = X[i].re*scale - temp.re;
				//X[id].im = X[i].im*scale - temp.im;
				X[i].re  = fp_add(X[i].re>>scale, 	temp.re);
				X[i].im  = fp_add(X[i].im>>scale, 	temp.im);
				//X[i].re = X[i].re*scale + temp.re;
				//X[i].im = X[i].im*scale + temp.im;
			}

			ltemp.re = lfp_mul(U.re, W[L-1].re);
			ltemp.re = lfp_smas(ltemp.re, U.im,	W[L-1].im);
			//temp.re = U.re*W[L-1].re - U.im*W[L-1].im;

			ltemp.im = lfp_mul(U.re, W[L-1].im);
			ltemp.im = lfp_smac(ltemp.im, U.im,	W[L-1].re);
			//U.im = U.re*W[L-1].im - U.im*W[L-1].re;

			U.re = ltemp.re>>SFT16;
			U.im = ltemp.im>>SFT16;
			//U.re = temp.re;
		}
	}
}


void ifft(complex * X, unsigned short EXP, complex * W, unsigned short SCALE){

	unsigned short N;
	unsigned short i;
	complex temp;
	N = 1<<EXP;
	//compute FFT

	fft(X, EXP, W, SCALE);
	//reverse X[1] through X[N-1] and append to X[0]

	for(i = 1; i<N/2; i++){
		temp 	=	X[i];
		X[i] 	= 	X[N-i];
		X[N-i] 	= 	temp;
	}
	for(i = 0; i < N; i++){
		X[i].re = X[i].re>>EXP;//>>EXP;
	}

}



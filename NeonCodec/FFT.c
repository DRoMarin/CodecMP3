
#include "types.h"
#include "FFT.h"
#include "fixmath.h"

#include <stdint.h>
#include <math.h>
#include <inttypes.h>

double pi = 3.1415926535897;
#define SFT16 16

//FFT algorithm with Q16

void fft_init(lcomplex *W, short EXP)
{
	unsigned short L,LE,LE1;

	for(L=1; L<=EXP; L++)
	{
		LE = 1<<L;
		LE1 = LE>>1;
		W[L-1].re = (int)((0xffff*cos(pi/LE1))+0.5);

		W[L-1].im = -(int)((0xffff*sin(pi/LE1))+0.5);
	}
}

void bit_rev(lcomplex *X, short EXP)
{
	unsigned short i,j,k;
	unsigned short N = 1 << EXP;
	unsigned short N2 = N>>1;
	lcomplex temp;
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

void fft(lcomplex * X, unsigned short EXP, lcomplex * W, unsigned short SCALE){
	lcomplex temp;
	lcomplex U;
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
		U.re = 0x0000ffff;
		U.im = 0;

		for (j = 0; j < LE1; j++)
		{
			for(i = j; i < N; i += LE)
			{
				id = i + LE1;

				temp.re = fix16_ssub(fix16_smul(X[id].re,U.re),fix16_smul(X[id].im,U.im))>>scale;
																		//temp.re = (X[id].re*U.re - X[id].im*U.im)*scale;

				temp.im = fix16_sadd(fix16_smul(X[id].im,U.re),fix16_smul(X[id].re,U.im))>>scale;
																		//temp.im = (X[id].im*U.re + X[id].re*U.im)*scale;

				X[id].re = fix16_ssub(X[i].re>>scale,temp.re);
				X[id].im = fix16_ssub(X[i].im>>scale,temp.im);
																		//X[id].re = X[i].re*scale - temp.re;
																		//X[id].im = X[i].im*scale - temp.im;

				X[i].re = fix16_sadd(X[i].re>>scale,temp.re);
				X[i].im = fix16_sadd(X[i].im>>scale,temp.im);
																		//X[i].re = X[i].re*scale + temp.re;
																		//X[i].im = X[i].im*scale + temp.im;
			}

			temp.re = fix16_ssub(fix16_smul(U.re,W[L-1].re),fix16_smul(U.im,W[L-1].im));
			U.im = fix16_sadd(fix16_smul(U.re,W[L-1].im),fix16_smul(U.im,W[L-1].re));
			U.re = temp.re;

			//temp.re = U.re*W[L-1].re - U.im*W[L-1].im;

			//U.im = U.re*W[L-1].im - U.im*W[L-1].re;

			//U.re = temp.re;
		}
	}
}


void ifft(lcomplex * X, unsigned short EXP, lcomplex * W, unsigned short SCALE){

	unsigned short N;
	unsigned short i;
	lcomplex temp;
	N = 1<<EXP;

	//compute FFT

	fft(X, EXP, W, SCALE);

	//reverse X[1] through X[N-1] and append to X[0]; then scale
	for(i = 1; i<N/2; i++){
		temp 	=	X[i];
		X[i] 	= 	X[N-i];
		X[N-i] 	= 	temp;
	}
}



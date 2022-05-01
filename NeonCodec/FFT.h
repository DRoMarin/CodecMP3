/*
 * FFT.h
 *
 *  Created on: Apr 21, 2022
 *      Author: daro
 */

#ifndef FFT_H_
#define FFT_H_

#include "types.h"

void fft_init(lcomplex * W, short EXP);

void bit_rev(lcomplex * X, short EXP);

void fft(lcomplex * X, unsigned short EXP, lcomplex * W, unsigned short SCALE);

void ifft(lcomplex * X, unsigned short EXP, lcomplex * W, unsigned short SCALE);

#endif /* FFT_H_ */

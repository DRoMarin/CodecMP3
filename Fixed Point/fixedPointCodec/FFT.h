/*
 * FFT.h
 *
 *  Created on: Apr 21, 2022
 *      Author: daro
 */

#ifndef FFT_H_
#define FFT_H_

#include "types.h"

void fft_init(complex * W, short EXP);

void bit_rev(complex * X, short EXP);

void fft(complex * X, unsigned short EXP, complex * W, unsigned short SCALE);

void ifft(complex * X, unsigned short EXP, complex * W, unsigned short SCALE);

#endif /* FFT_H_ */

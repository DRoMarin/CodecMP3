/*
 * fixedPoint.c
 *
 *  Created on: Apr 22, 2022
 *      Author: daro
 */

#include <stdint.h>
#include "fixedPoint.h"

int16_t fp_add(int16_t src1, int16_t src2)
{
	int16_t out = 0x7fff*src1 + 0x7fff*src2;

	return out;
}

int16_t fp_sub(int16_t src1, int16_t src2)
{
	int16_t out = 0x7fff*src1 - 0x7fff*src2;

	return out;
}

int32_t lfp_mul(int16_t src1, int16_t src2)
{
	int32_t out = (int32_t) src1 * (int32_t) src2;

	return out;
}

int32_t lfp_smas(int32_t src1, int16_t src2, int16_t src3)
{
	int32_t out = src1 * ((int32_t) src2 - (int32_t) src3);

	return out;
}


int32_t lfp_smac(int32_t src1, int16_t src2, int16_t src3)
{
	int32_t out = src1 * ((int32_t) src2 + (int32_t) src3);

	return out;
}



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
	int32_t out = (uint32_t)src1 + (uint32_t)src2;
	if (out > 32767) out = 32767;
	else if (out <  -32768) out = -32768;

	return (int16_t) out;
}

int16_t fp_sub(int16_t src1, int16_t src2)
{
	int32_t out = (uint32_t)src1 - (uint32_t)src2;
		if (out > 32767) out = 32767;
		else if (out <  -32768) out = -32768;

		return (int16_t) out;
}

int32_t lfp_mul(int16_t src1, int16_t src2)
{
	int32_t out = (int32_t) src1 * (int32_t) src2;

	return out;
}

int32_t lfp_smas(int32_t src1, int16_t src2, int16_t src3)
{
	int32_t out = src1 - ((int32_t) src2 * (int32_t) src3);

	return out;
}


int32_t lfp_smac(int32_t src1, int16_t src2, int16_t src3)
{
	int32_t out = src1 + ((int32_t) src2 * (int32_t) src3);

	return out;
}



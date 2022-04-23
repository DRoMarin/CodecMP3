/*
 * fixedPoint.h
 *
 *  Created on: Apr 22, 2022
 *      Author: daro
 */

#ifndef FIXEDPOINT_H_
#define FIXEDPOINT_H_

#include <stdint.h>

int16_t fp_add(int16_t src1, int16_t src2);
int16_t fp_sub(int16_t src1, int16_t src2);
int32_t lfp_mul(int16_t src1, int16_t src2);
int32_t lfp_smas(int32_t src1, int16_t src2, int16_t src3);
int32_t lfp_smac(int32_t src1, int16_t src2, int16_t src3);
#endif /* FIXEDPOINT_H_ */

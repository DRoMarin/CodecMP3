################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../libfixmath/fix16.c \
../libfixmath/fix16_exp.c \
../libfixmath/fix16_sqrt.c \
../libfixmath/fix16_str.c \
../libfixmath/fix16_trig.c \
../libfixmath/fract32.c \
../libfixmath/uint32.c 

O_SRCS += \
../libfixmath/fix16.o \
../libfixmath/fix16_exp.o \
../libfixmath/fix16_sqrt.o \
../libfixmath/fix16_str.o \
../libfixmath/fix16_trig.o \
../libfixmath/fract32.o \
../libfixmath/uint32.o 

OBJS += \
./libfixmath/fix16.o \
./libfixmath/fix16_exp.o \
./libfixmath/fix16_sqrt.o \
./libfixmath/fix16_str.o \
./libfixmath/fix16_trig.o \
./libfixmath/fract32.o \
./libfixmath/uint32.o 

C_DEPS += \
./libfixmath/fix16.d \
./libfixmath/fix16_exp.d \
./libfixmath/fix16_sqrt.d \
./libfixmath/fix16_str.d \
./libfixmath/fix16_trig.d \
./libfixmath/fract32.d \
./libfixmath/uint32.d 


# Each subdirectory must supply rules for building sources it contributes
libfixmath/%.o: ../libfixmath/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: Cross GCC Compiler'
	arm-linux-gnueabihf-gcc -I"/home/daro/eclipse-workspace/NeonCodec/NE10" -I"/home/daro/eclipse-workspace/NeonCodec/libfixmath" -O3 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '



 #include<stdio.h>
#include<stdint.h>
#include<immintrin.h>
#define ADD(chi, alpha) { \
  _i_asm__ __volatile__ ("add %[src], %[dest];" : [dest] "+r" (chi) : [src] "r" (alpha)); \
};
int main(void){int chi=0;int alpha=1;ADD(chi,alpha); return 0;};
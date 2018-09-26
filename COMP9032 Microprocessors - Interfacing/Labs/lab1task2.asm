;
; lab1task2.asm
;
; Created: 1/08/2018 4:34:44 PM
; Author : z5145114
;


; Replace with your application code

.include "m2560def.inc"  
.def a =r16              ; define a to be register r16  
.def n =r17              ; define b to be register r17
clr r0                   ; clr r0
clr r1                   ; clr r1

.macro loop              ;loop n: excute (sum[r1:r0]+1)*a[r16]
                         ;which is equal to a+a^2+a^3+...+a^n
   dec @0                ;n: loop count dec

   inc r0                ;16-bit int add 1
   brcc carry0               ;if carry cleared, do nothing
   inc r1                    ;else, sunH inc 1
   carry0:                   ;do nothing
      nop
	                     ;16-bit * 8-bit
   mov r18,r0                ;mov low of sum into r18
   mul r1,a                  ;mul a and high of sum
   mov r19,r0                ;mov low result1 to r19
   mul r18,a                 ;mul a and low of sum
   add r1,r19                ;add high of result2 with r19(lower bit of result1)
.endmacro

nloop:                   ;loop control
   loop n  
   cpi n,0               ;compare n with 0
   breq end                  ;if equal, jmp to end
   rjmp nloop                ;else, return to nloop
    
end:
   rjmp end 

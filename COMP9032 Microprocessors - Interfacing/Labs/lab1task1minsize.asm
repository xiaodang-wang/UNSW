;
; AssemblerApplication1.asm
;
; Created: 8/08/2018 7:04:05 PM
; Author : xiaodan wang z5145114
;


; Replace with your application code
.include "m2560def.inc"  
.def a =r16              ; define a to be register r16  
.def b =r17              ; define b to be register r17  


loop:                    ;loop cycle
   cp a,b                ;compare a and b
   breq end              ;  branch1: a = b -> end
   brlo bgta             ;  branch2: a < b -> bgta: b = b - a
   sub a,b               ;  branch3: a > b -> a = a - b 
   rjmp loop             ;repeat loop

bgta:                    ;if b is greater than a
   sub b,a               ;b = b - a
   rjmp loop             ;repeat loop

end:
   rjmp end

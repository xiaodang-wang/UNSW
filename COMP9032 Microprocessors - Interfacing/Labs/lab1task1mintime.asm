;
; lab1.asm
;
; Created: 1/08/2018 4:02:57 PM
; Author : xiaodan wang z5145114
;
; minimum code size


; Replace with your application code


.include "m2560def.inc"  
.def a =r16            ; define a to be register r16  
.def b =r17            ; define b to be register r17  


loop1:                 ;loop cycle
   cp a,b              ;compare a and b
   breq end            ;  branch1: a = b -> end
   brlo bgta           ;  branch2: a < b -> bgta: b = b - a
   sub a,b             ;  branch3: a > b -> a = a - b   

   cp a,b              ;repeat loop 2nd time
   breq end
   brlo bgta
   sub a,b

   cp a,b              ;repeat 3rd
   breq end
   brlo bgta
   sub a,b

   cp a,b              ;repeat 4th
   breq end
   brlo bgta
   sub a,b

   cp a,b              ;repeat 5th
   breq end
   brlo bgta
   sub a,b

   cp a,b              ;repeat 6th
   breq end
   brlo bgta
   sub a,b
   rjmp loop1          ;repeat the big loop

bgta:                  ;if b is greater than a
   sub b,a             ;b = b - a

   cp a,b              ;1st repeation
   breq end
   brlo bgta
   sub a,b

   cp a,b              ;2nd repeation
   breq end
   brlo bgta
   sub a,b

   cp a,b              ;3rd repeation
   breq end
   brlo bgta
   sub a,b

   cp a,b              ;4th repeation
   breq end
   brlo bgta
   sub a,b

   cp a,b              ;5th repeation
   breq end
   brlo bgta
   sub a,b

   cp a,b              ;6th repeation
   breq end
   brlo bgta
   sub a,b
   rjmp loop1          ;repeat the big loop

end:
   rjmp end

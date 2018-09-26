.include "m2560def.inc"

.def countH = r17
.def countL = r16
.def count2 = r19
.def i = r20
.def temp = r21
.def flag = r22
.def iH = r25
.def iL = r24

.equ loop_count = 5		;50000
.equ loop_count2 = 3	;39
.equ pattern1 = 0x0f
.equ pattern2 = 0xf0
.equ pattern3 = 0xaa

	rjmp reset
.org int0addr
	rjmp ext_int0
.org int1addr
	jmp ext_int1


.macro Delay	
	ldi countL,low(loop_count)
	ldi countH,high(loop_count)
	clr iH
	clr iL
loop:				; 7 * loop_count + 4 + 2(out&ldi)  400010cc
	cp iL,countL		;1
	cpc iH,countH		;1
	brsh done			;1
	adiw iH:iL,1		;2
	rjmp loop			;2
done:
.endmacro


.macro oneSecondDelay
	ldi count2,loop_count2
	clr i
loop2:
	Delay			; 400010 cc
	cp i,count2
	brsh done2
	inc i
	rjmp loop2
done2:
.endmacro


reset:
	ser temp		;set portc as output
	out ddrc, temp

	ldi temp, (2<<isc00)|(2<<isc10)	;2=0b10,falling edge
	sts eicra, temp

	in temp, eimsk	;enable int0 and int1
	ori temp, (1<<int0)|(1<<int1)
	out eimsk, temp

	sei				;set global interrupt
	jmp main

ext_int0:
	;prologue
	push temp		;save temp
	in temp, sreg	;save sreg
	push temp
	;body
ext_int0_loop:
	cpi flag, 1
	breq end_ext_int0
	rjmp ext_int0_loop
	;epilogue
end_ext_int0:
	pop temp
	out sreg, temp
	pop temp
	reti


ext_int1:
	ldi flag, 1
	reti


main:
	clr flag
patternloop:
	ldi r18, pattern1	; pattern 1
	out portc, r18
	oneSecondDelay
	ldi r18, pattern2	; pattern 2
	out portc, r18
	oneSecondDelay
	ldi r18, pattern3	; pattern 3
	out portc, r18
	oneSecondDelay
	rjmp patternloop


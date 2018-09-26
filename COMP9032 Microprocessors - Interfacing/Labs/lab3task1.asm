.include"m2560def.inc"
.equ loop_count = 65535
.equ loop_count2 = 
.def iH = r25
.def iL = r24
.def countH = r17
.def countL = r16
.def count2 = r19
.def i = r20

.macro Delay	
	ldi countL,low(loop_count)
	ldi countH,high(loop_count)
	clr iH
	clr iL
loop:				; 8 * loop_count + 4 + 2(out&ldi)  400010cc
	cp iL,countL		;1
	cpc iH,countH		;1
	brsh done			;1
	adiw iH:iL,1		;2
	sbic pinD,1		;1 check if 0 bit of pind is clear
	rjmp loop		;2 if yes, skip
	rjmp halt
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


; main part
	clr r18
	out ddrD,r18	; set portd for input
	ser r18
	out ddrc,r18	; set portc for output

patternloop:
	ldi r18,0xaa	; pattern 1
	out portc,r18
	oneSecondDelay
	ldi r18,0xff	; pattern 2
	out portc,r18
	oneSecondDelay
	ldi r18,0x0f	; pattern 3
	out portc,r18
	oneSecondDelay
	rjmp patternloop  

halt:
	sbic pinD,1			;1 check if 0 bit of pind is clear
	rjmp patternloop		;2 if yes, skip; or countinue pattern loop
	rjmp halt			; keep halt

end:
	rjmp end
; z5145114
.include"m2560def.inc"

.def zero = r25

; left shift for 16-bits
.macro left_shift
	LSL @0
	ROL @1
.endmacro

; right shift for 16-bits
.macro right_shift
	LSR	@1
	ROR @0
.endmacro

.cseg
main:
	ldi zh, high(dividend<<1)	; z <- *dividend, gets byte address of dividend
	ldi zl, low(dividend<<1)
	lpm r16, z+			; r17:r16 = dividend
	lpm r17, z
	ldi zh, high(divisor<<1)	; z <- *divisor, gets byte address of divisor 
	ldi zl, low(divisor<<1)
	lpm r18, z+			; r19:r18 = divisor
	lpm r19, z
	rcall posdiv			; call function posdiv()
					; parameter int dividend and int divisor, stored in r17:r16 and r19:r18
					; return int n, stored in r21:r20
	ldi zh, high(quotient)		; z <- *quotient, gets byte address of qoutient
	ldi zl, low(quotient)
	st z+, r20			; store qoutient into data memory		
	st z, r21
end:
	rjmp end

dividend: .dw 24000		; set dividend
divisor: .dw 50			; set divisor

posdiv:
	;Prologue		
	push yl			; frame pointer
	push yh
	push zero		; conflict registers
	in yl, spl		; reserve space for local variable
	in yh, sph
	sbiw y,8		; 4 int, 8 bytes
	out sph, yh
	out spl, yl
	;End of prologue

	;Function body
	clr r20			; r21:r20 = quotient = 0
	clr r21
	ldi r22, 0x01		; r23:r22 = bit_position = 1
	clr r23
loop1:
	cp r18, r16		; compare lower byte of divisor and dividend
	cpc r19, r17		; compare lower byte of divisor and dividend with carry
	brsh loop2			; if dividend > divisor, end loop1
	sbrc r19, 7		; if !(divisor & 0x8000) (the 7th bit of r19 is cleared):
	rjmp loop2			; then go in loop1 or jump to loop2
	left_shift r18, r19		; divisor = divisor << 1
	left_shift r22, r23		; bit_position = bit_position << 1
	rjmp loop1
loop2:
	cp r22, zero		; compare lower byte of bit_position and zero
	cpc r23, zero		; compare lower byte of bit_position and zero with carry
	breq end1		; if bit_position > 0 then go in loop2 or jump to end
	cp r16, r18		; compare lower byte of divisor and dividend	
	cpc r17, r19		; compare lower byte of divisor and dividend with carry
	brlo ifnot			; if dividend < divisor, jump ifnot
	sub r16, r18		;dividend = dividend - divisor
	sbc r17, r19
	add r20, r22		;quotient = quotient + bit_position
	adc r21, r23
ifnot:
	right_shift r18, r19	;divisor = divisor >> 1
	right_shift r22, r23	;bit_position = bit_position >> 1
	rjmp loop2
	;End of function body

	;Epilogue
end1:	
	adiw y,8
	out sph, yh
	out spl, yl
	pop zero
	pop yh
	pop yl
	ret
	;End of Epilogue

.dseg
quotient: .byte 2

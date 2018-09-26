; z5145114

.include"m2560def.inc"
.def ten = r16			; set r16 as ten(10)		
.def zero = r17			; set r17 as zero(0)
.def c = r20			; set r20 char c
.equ size = 5			; size of char *s

.cseg

main:
	ldi ten,10		; ten = 10		
	clr zero		; zero = 0
	ldi zl,LOW(s<<1)	; z <- *s, gets byte address of s
	ldi zh,HIGH(s<<1)
	rcall atoi		; call function atoi()
				; parameter char *s, stored in z
				; return int n, stored in x
	ldi yl,LOW(number)	; y <- *number, gets byte address of s
	ldi yh,HIGH(number)
	st y+,xh		; store n into data memory
	st y,xl

end:	rjmp end

s:	.db "12345",0		; char *s[] = "12345"

atoi:
	;Prologue
	push yl			; frame pointer
	push yh
	push r16		; conflict registers
	push r17
	in yl, spl		; reserve space for local variable
	in yh, sph
	sbiw y, 6		; address a = 2 bytes, char i = 1 byte, char c = 1 byte, int n = 2 bytes
	out spl, yl
	out sph, yh
	std y+1, zl		; pass parameters
	std y+2, zh		
	;End of prologue

	;Function body
	clr xl			; n = x
	clr xh				
loop:
	lpm c,z+		; load char into c
	cpi c, 48		; compare c with '0'
	brlo end1			; if lower, end loop
	cpi c, 57		; compare c with '9'
	brsh end1			; if higer, end loop
	subi c, 0x30		; c - '0'
	; r22:r21 = n * 10
	mul xh,ten		; higher byte of x * 10
	cp r1,zero		; if the higher byte of result is not zero:
	brne end1			; overflow, end loop
	mov r22,r0		; save the lower byte of result in r22
	mul xl,ten		; then do the lower byte mul
	add r22,r1		; add r22 with higher byte of result
	brcs end1			; if carry is set, overflow, end loop
	mov r21,r0		; sabe the lower byte of result in r21
	; n = r22:r21 + c
	add r21,c		; add lower byte of n with c
	adc r22,zero		; add higher byte of n with carry
	brcs end1			; if carry set, overflow, end loop
	mov xl,r21		; move the result into x
	mov xh,r22
	; n = n * 10 + c - 48, done
	rjmp loop

end1:
	;Epilogue
	adiw y, 6
	out sph, yh
	out spl, yl
	pop r17
	pop r16
	pop yh
	pop yl
	ret
	;End of epilogue

.dseg
number:	.byte 2			; int number

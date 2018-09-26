.include "m2560def.inc"
	
.def row = r16			; current row number
.def col = r17			; current column number
.def rmask = r18		; mask for current row
.def cmask = r19		; mask for current column
.def temp1 = r20		
.def temp2 = r21
.def b = r22			; register for b
.def c = r23			; register for c
.def flag = r24			; register for * flag
.def ten = r25

.equ loop_count = 10000
.equ loop_count2 = 40

.equ PORTFDIR = 0xF0		; use PortF for input/output from keypad: PF7-4, output Col, PF3-0, input Row
.equ INITCOLMASK = 0xEF		; scan from the leftmost column, the value to mask output
.equ INITROWMASK = 0x01		; scan from the bottom row
.equ ROWMASK = 0x0F			; low four bits are output from the keypad. This value mask the high 4 bits.


.macro Delay				; Delay for 0.2 sec
	ldi ZL, loop_count2
	clr ZH
loop2:
	cp ZH, ZL
	brsh done2
	inc ZH
	rjmp delay1
delay1:
	ldi XL,low(loop_count)
	ldi XH,high(loop_count)
	clr YH
	clr YL
loop:				; 8 * loop_count + 4 + 2(out&ldi)  400010cc
	cp YL,XL		;1
	cpc YH,XH		;1
	brsh done			;1
	adiw YH:YL,1		;2
	rjmp loop		;2 if yes, skip
done:
	rjmp loop2
done2:
.endmacro

RESET:
	ldi temp1, PORTFDIR			; columns are outputs, rows are inputs
	out	DDRF, temp1				; PORTF for input/output from keypad: PF7-4, output Col, PF3-0, input Row
	ser temp1					; PORTC is outputs
	out DDRC, temp1			

	clr flag
	clr b
	clr c
	ldi ten, 10

main:
	ldi cmask, INITCOLMASK		; initial column mask, from leftmost column
	clr	col						; initial column
colloop:
	cpi col, 4
	breq main					; col loop end
	out	PORTF, cmask			; set column to mask value (one column off)

	ldi temp1, 0xFF
delay1:
	dec temp1
	brne delay1

	in temp1, PINF				; read PORTF
	andi temp1, ROWMASK
	cpi temp1, 0x0F				; check if any rows are on
	breq nextcol
								; if yes, find which row is on
	ldi rmask, INITROWMASK		; initialise row check, from bottom row
	clr	row						; initial row
rowloop:
	cpi row, 4
	breq nextcol
	mov temp2, temp1
	and temp2, rmask			; check masked bit
	breq convert 				; if bit is clear, convert the bitcode
	inc row						; else move to the next row
	lsl rmask					; shift the mask to the next bit
	jmp rowloop

nextcol:
	lsl cmask					; else get new mask by shifting and 
	inc col						; increment column value
	jmp colloop					; and check the next column

convert:
	cpi col, 3				; if column is 3 we have a letter
	breq letters				
	cpi row, 3				; if row is 3 we have a symbol or 0
	breq symbols

	cpi flag, 1					; if * was pressed:
	breq getc						; put in c
	; get pressed number in temp2
	mov temp2, row			; otherwise we have a number in 1-9
	lsl temp2
	add temp2, row				; temp1 = row * 3
	add temp2, col				; add the column address to get the value
	inc temp2					; get the real number
	; b = b * 10 + temp2
	mul b, ten				; b * 10
	mov b, r0				; put result in b
	add b, temp2			; add temp2
	out PORTC, b			; write value to PORTC
	Delay
	jmp main

getc:						; similar to above, just replace b with c
	mov temp2, row				; otherwise we have a number in 1-9
	lsl temp2
	add temp2, row				; temp1 = row * 3
	add temp2, col				; add the column address to get the value
	inc temp2
	; b = b * 10 + temp2
	mul c, ten				; c * 10
	mov c, r0				; put result in c
	add c, temp2			; add temp2
	out PORTC, c			; write value to PORTC
	Delay
	jmp main

letters:					; do nothing and return to main
	jmp main

symbols:
	cpi col, 0					; check if we have a star
	breq star
	cpi col, 1					; or if we have zero
	breq zero					
	;ldi temp1, '#'				; if not we have hash
	jmp calculate
star:						; if we got star:
	ldi flag, 1					; change the flag to 1
	ldi temp1, 0xff				; flash once
	;out PORTC, temp1			; write value to PORTC
	;Delay
	jmp main
zero:					; if we got zero:
	cpi flag, 1				; if * was pressed:
	breq getczero				; put zero in c
							; * not pressed, b = b*10
	ldi temp1, 0			
	mul b, ten
	mov b, r0
	out PORTC, b			; write value to PORTC
	Delay
	jmp main

getczero:				; c = c * 10
	ldi temp1, 0
	mul c, ten
	mov c, r0
	out PORTC, b			; write value to PORTC
	Delay
	jmp main

calculate:				; calculate a = b * c
	mul b, c
	mov temp1, r1			; if high bits of result is not 0:
	cpi temp1, 0
	brne overflow				; overflow
	mov temp1, r0			; otherwise, output low bits
	out PORTC, temp1		; write value to PORTC
	Delay
	jmp end					; end

overflow:			; over flow
	ldi temp2, 3		; count for 3 times

flash:					; flash once
	ldi temp1, 0xFF		; all on
	out PORTC, temp1		
	Delay
	Delay
	Delay

	ldi temp1, 0x00		; all off
	out PORTC, temp1
	Delay
	Delay
	Delay

	dec temp2			; count--
	cpi temp2, 0		; if count == 0
	breq end				; end
	rjmp flash			; otherwise, flash again 

end:
	rjmp end


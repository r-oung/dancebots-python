/**
******************************************************************************
* @file    MP3DanceBot.c
* @author  Philipp Reist
* @author  Raymond Oung 
* @version V1.0
* @date    11/03/2012
* @brief   MP3DanceBot v1.0 Firmware for ATTiny 261A - 861A
*
* FUSE CONFIG ****************************************************************
* Extended byte: 0xFF
* High byte:     0xDF
* Low byte:      0xE2
******************************************************************************
* Copyright (C) 2011 - 2019 mint & pepper
*
* This program is free software: you can redistribute it and/or modify it
* under the terms of the GNU General Public License as published by the Free
* Software Foundation, either version 3 of the License, or (at your option)
* any later version.
*
* This program is distributed in the hope that it will be useful, but WITHOUT
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
* FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
* more details.
*
* You should have received a copy of the GNU General Public License along with
* this program. If not, see <https://www.gnu.org/licenses/>.
*/ 

#include <avr/sleep.h>
#include <avr/wdt.h> 
#include "avr/io.h"
#include "avr/interrupt.h"
#include "inttypes.h"

/** @addtogroup MP3DANCEBOT_Private_Defines
  * @{
  */ 
#define	__AVR_ATtiny261__ 	1
#define OSCSPEED	8000000 // [Hz]

// MOTOR DEFINES
// macros to set motors driving forward/backward
#define SETFWDR() {PORTB &= ~_BV(PB0); PORTB |= _BV(PB2);}
#define SETFWDL() {PORTA &= ~_BV(PA0); PORTA |= _BV(PA1);}
#define SETBWDR() {PORTB &= ~_BV(PB2); PORTB |= _BV(PB0);}
#define SETBWDL() {PORTA &= ~_BV(PA1); PORTA |= _BV(PA0);}

// motor duty-cycle registers
#define MOTL	OCR1B
#define MOTR	OCR1A

// MESSAGE DEFINES
// bit and reset thresholds (obtained using generateTestData.m in Matlab files)
#define RESET 	5805 // threshold for RESET pulse. If timer ticks > RESET, reset is detected
#define DTONE	3367 // If timer ticks between RESET and DTONE, a high bit is read
					 // Below DTONE, a zero is read out

// define message length and forward/backward code
#define LMSG	24	// total message length [bits]
#define LMOTL	8   // bit which indicates the end of MOTL [bit]
#define LMOTR	16  // bit which indicates the end of MOTR [bit]

typedef enum {
	MSG_STATE_MOTL = 0,
	MSG_STATE_MOTR,
	MSG_STATE_LED,
	MSG_STATE_SET
} msg_state_t;
/**
  * @}
  */ 


/** @addtogroup MP3DANCEBOT_Private_Function_Prototypes
  * @{
  */ 
void GPIO_Init(void);
void TIMER_Init(void);
uint8_t convDCtoOCR(uint8_t dc);
void setMotors(uint8_t cmdL, uint8_t cmdR);
void setLED(uint8_t msg);
/**
  * @}
  */ 

/** @addtogroup MP3DANCEBOT_Private_Variables
  * @{
  */ 
/**
  * @}
  */ 


/**
* @brief Initialize GPIO
* @param None
* @retval None
*/
void GPIO_Init(void)
{	
	//		  76543210
	PORTA = 0b00000000; // all outputs, except PA4 (DATA)
	DDRA =  0b11101111;
	
	//		  76543210
	PORTB = 0b00000000; // all outputs, except PB7 (RESET)
	DDRB =  0b01111111;
}

/**
* @brief Initialize Timer Peripheral
* @param None
* @retval None
*/
void TIMER_Init(void)
{	
	// set 16-bit timer: counter 0, enable input capture, and noise canceling
	TCCR0A |= (_BV(TCW0) | _BV(ICEN0) | _BV(ICNC0));
	// set trigger on falling edge
	TCCR0A &= ~(_BV(ICES0));
	// set prescaler to 8 = 1 MHz timer clock
	TCCR0B |= _BV(CS00);
	TCCR1B |= _BV(CS10); // set timer-1 prescaler to 512 to get 50Hz PWM signal
	TIMSK  |= _BV(TICIE0);

	// LEFT MOTOR: PWM-1
	OCR1A = 0x00; // initialize compare to 0% duty-cycle
	TCCR1A |= (_BV(PWM1A) | _BV(COM1A1)); // set output to inverted fast-PWM mode, 
										  // low on compare match, set on 0 of counter
	
	// RIGHT MOTOR: PWM-2
	OCR1B = 0x00; // initialize compare to 0% duty-cycle
	TCCR1A |= (_BV(PWM1B) | _BV(COM1B1)); // set output to inverted fast-PWM mode, 
									      // low on compare match, set on 0 of counter
										  
	// initialize motor directions
	SETFWDR()
	SETFWDL()
}

/**
* @brief Interrupt Service Routine for incoming Data
*	     Messages are time-modulated, i.e. like Morse code (1-long; 0-short)
*        Packet: [START | 7-bits MOTOR-LEFT SPEED | 1-bit MOTOR-LEFT DIRECTION
*						  7-bits MOTOR-RIGHT SPEED | 1-bit MOTOR-RIGHT DIRECTION
*						  8-bits LED]			  
* @brief I don't want to understand this --Ray
* @param None
* @retval None
*/
ISR(TIMER0_CAPT_vect, ISR_BLOCK)
{
	static uint8_t msgState = MSG_STATE_MOTL;
	static uint8_t bitCnt = 0u; // maximum is LMSG
	
	static uint8_t msgML = 0u;
	static uint8_t msgMR = 0u;
	static uint8_t msgLED = 0u;

	static uint16_t t0 = 0u;
	uint16_t t = 0u;
	uint16_t dt = 0u;

	// toggle capture event edge
	if(TCCR0A & _BV(ICES0))
	{
		TCCR0A &= ~(_BV(ICES0)); // if the register value is set, toggle to zero
	}
	else
	{
		TCCR0A |= _BV(ICES0);
	}

	// read out current timer value
	t = OCR0A;
	t |= ((uint16_t) OCR0B << 8);
	
	// measure elapsed time
	// take care of buffer overflow
	if(t > t0)
	{
		dt = t - t0;
	}
	else
	{
		dt = 0xFFFF + t - t0 + 1;
	}
	t0 = t; // save time to buffer

	// reset message buffer if RESET has been hit
	if(dt > RESET)
	{
		bitCnt = 0u;
		msgML = 0u;
		msgMR = 0u;		
		msgLED = 0u;
		msgState = MSG_STATE_MOTL;
	}
	else
	{
		// reading a valid message
		if(dt < RESET && (bitCnt < LMSG))
		{
			// there are 3 states: MOTOR-LEFT | MOTOR-RIGHT | LED
			switch(msgState)
			{
				case MSG_STATE_MOTL:
				{
					if(dt > DTONE)
					{
						msgML |= _BV(bitCnt); // 1
					}
					else
					{
						msgML &= ~(_BV(bitCnt)); // 0
					}
					
					if(++bitCnt >= LMOTL) // go to the next state
					{
						msgState = MSG_STATE_MOTR;
					}				
					break;
				}
				case MSG_STATE_MOTR:
				{
					if(dt > DTONE)
					{
						msgMR |= _BV(bitCnt-LMOTL); // 1
					}
					else
					{
						msgMR &= ~(_BV(bitCnt-LMOTL)); // 0
					}
					
					if(++bitCnt >= LMOTR) // go to the next state
					{
						msgState = MSG_STATE_LED;
					}
					break;
				}			
				case MSG_STATE_LED:
				{
					if(dt > DTONE)
					{
						msgLED |= _BV(bitCnt-LMOTR); // 1
					}
					else
					{
						msgLED &= ~(_BV(bitCnt-LMOTR)); // 0
					}
					
					if(++bitCnt >= LMSG) // we're done reading all states, yay!
					{
						setLED(msgLED);
						setMotors(msgML, msgMR);
						wdt_reset(); // reset watchdog
					}
					break;
				}			
				default:
				break;
			}					
		}
	}
}

/**
* @brief Convert duty-cycle to OCR value
* @param dc Duty-cycle [0-100]
* @retval OCR value [0-255]
*/
#define DC_OFFSET 175.0f // motor offset (motors won't run until they hit this value)
uint8_t convDCtoOCR(uint8_t dc)
{
	static const float inc = (255.0f-DC_OFFSET)/100.0f;

	return (uint8_t)(inc*dc + DC_OFFSET);
}

/**
* @brief Set motor direction and speed
* @param cmdL Duty-cycle [0-100]
* @param cmdR Duty-cycle [0-100]
* @retval None
*/
void setMotors(uint8_t cmdL, uint8_t cmdR)
{
	uint8_t val;
	
	// LEFT MOTOR
	val = 0u; // reset
	if(cmdL & 0x80) {SETBWDL()} else {SETFWDL()} // set direction
	if(cmdL & 0x7F) {val = convDCtoOCR(cmdL & 0x7F);} // set speed					
	MOTL = val;
	
	// RIGHT MOTOR								
	val = 0u; // reset
	if(cmdR & 0x80) {SETBWDR()} else {SETFWDR()} // set direction									
	if(cmdR & 0x7F) {val = convDCtoOCR(cmdR & 0x7F);} // set speed
	MOTR = val;						
}

/**
* @brief Set LEDs
* @param cmd 8-bit LED command; each bit represents the state of that LED
* @retval None
*/
void setLED(uint8_t cmd)
{
	if(cmd & 0x01) {PORTA |= _BV(PA2);} else {PORTA &= ~(_BV(PA2));} // LED0
	if(cmd & 0x02) {PORTA |= _BV(PA3);} else {PORTA &= ~(_BV(PA3));} // LED1
	if(cmd & 0x04) {PORTA |= _BV(PA5);} else {PORTA &= ~(_BV(PA5));} // LED2
	if(cmd & 0x08) {PORTA |= _BV(PA6);} else {PORTA &= ~(_BV(PA6));} // LED3
	if(cmd & 0x10) {PORTB |= _BV(PB4);} else {PORTB &= ~(_BV(PB4));} // LED4
	if(cmd & 0x20) {PORTB |= _BV(PB6);} else {PORTB &= ~(_BV(PB6));} // LED5
	if(cmd & 0x40) {PORTA |= _BV(PA7);} else {PORTA &= ~(_BV(PA7));} // LED6
	if(cmd & 0x80) {PORTB |= _BV(PB5);} else {PORTB &= ~(_BV(PB5));} // LED7
}

/**
* @brief Main
* @param None
* @retval None
*/
int main()
{
	// initialize GPIO
	GPIO_Init();
	
	// initialize TIMERS
	TIMER_Init();
	
	// initialize WATCHDOG
	wdt_enable(WDTO_500MS); // turn the motors off if there is no incoming data,
						    // shut down if no music is playing
	
	// set interrupts
	sei();

	// loop forever!
	while (1);
}
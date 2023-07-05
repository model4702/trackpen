/*
  LiquidCrystal Library - Hello World by DIY Hacking
  -Arvind Sanjeev, Dec 2014
 
 Demonstrates the use a 20x4 LCD display.  The LiquidCrystal
 library works with all LCD displays that are compatible with the 
 Hitachi HD44780 driver. There are many of them out there, and you
 can usually tell them by the 16-pin interface.
 
 This sketch prints some sample text to the LCD
 and shows the time.
 
 Check out: http://diyhacking.com/arduino-lcd-tutorial for
 the connection diagrams.
 
 Library originally added 18 Apr 2008
 by David A. Mellis
 library modified 5 Jul 2009
 by Limor Fried (http://www.ladyada.net)
 example added 9 Jul 2009
 by Tom Igoe
 modified 22 Nov 2010
 by Tom Igoe
 
 This example code is in the public domain.

 http://www.arduino.cc/en/Tutorial/LiquidCrystal
 */

// include the library code:
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

void setup() {
  // set up the LCD's number of columns and rows: 
  lcd.begin(20, 4);
  // Print a message to the LCD.
  lcd.setCursor(4,0);
  lcd.print("DIY Hacking");
}

void loop() {
  // set the cursor to column 0, line 1
  // (note: line 1 is the second row, since counting begins with 0):
  lcd.setCursor(4, 1);
  lcd.print("Arduino-LCD");
  lcd.setCursor(6,2);
  lcd.print("Tutorial");
  // print the number of seconds since reset:
  
  lcd.setCursor(6,3);
  lcd.print("Time: ");
  lcd.print(millis()/1000);
}

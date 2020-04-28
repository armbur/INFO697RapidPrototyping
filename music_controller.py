from microbit import *
import music
import random
import speech

LCD_I2C_ADDR=39

class LCD1620():
    def __init__(self):
        self.buf = bytearray(1)
        self.BK = 0x08
        self.RS = 0x00
        self.E = 0x04
        self.setcmd(0x33)
        sleep(5)
        self.send(0x30)
        sleep(5)
        self.send(0x20)
        sleep(5)
        self.setcmd(0x28)
        self.setcmd(0x0C)
        self.setcmd(0x06)
        self.setcmd(0x01)
        self.version='1.0'

    def setReg(self, dat):
        self.buf[0] = dat
        i2c.write(LCD_I2C_ADDR, self.buf)
        sleep(1)

    def send(self, dat):
        d=dat&0xF0
        d|=self.BK
        d|=self.RS
        self.setReg(d)
        self.setReg(d|0x04)
        self.setReg(d)

    def setcmd(self, cmd):
        self.RS=0
        self.send(cmd)
        self.send(cmd<<4)

    def setdat(self, dat):
        self.RS=1
        self.send(dat)
        self.send(dat<<4)

    def clear(self):
        self.setcmd(1)

    def backlight(self, on):
        if on:
            self.BK=0x08
        else:
            self.BK=0
        self.setcmd(0)

    def on(self):
        self.setcmd(0x0C)

    def off(self):
        self.setcmd(0x08)

    def shl(self):
        self.setcmd(0x18)

    def shr(self):
        self.setcmd(0x1C)

    def char(self, ch, x=-1, y=0):
        if x>=0:
            a=0x80
            if y>0:
                a=0xC0
            a+=x
            self.setcmd(a)
        self.setdat(ch)

    def puts(self, s, x=0, y=0):
        if len(s)>0:
            self.char(ord(s[0]),x,y)
            for i in range(1, len(s)):
                self.char(ord(s[i]))

lcd=LCD1620()

# used these images during testing of led - currently not being used.
images_a = [Image.HEART]
images_b = [Image.HAPPY]
images_x = [Image.YES]

# music.get_tempo() function that will return for you a tuple consisting of the bpm and ticks.
music.set_tempo(bpm=240, ticks=4)

# C4:4 - This means the note C from octave 4, or middle C, played for 4 ticks.
#tune_button_a = ['F#4:4','G4:4','A4:4']
tune_button_a = ['G3:4', 'D5:4']
tune_button_b = ['G3:4', 'D#5:4']
tune_button_x = ['F#4:4']
tune_button_z = ['G4:4','A4:4']

# pin0 = passive buzzer
# pin1 = digital buzzer
# pin3 = joystick x axis - currently not being used in code
# pin10 = joystick y axis - currently not being used in code
# pin4 = joystick button - currently not being used in code
# pin8 = digital push button
# pin12 = Crash sensor

# pin0.write_digital(1) = green light on
# pin0.write_digital(0) = green light off
# pin1.write_digital(1) = yellow light on
# pin1.write_digital(0) = yellow light off
# pin2.write_digital(1) = red light on
# pin2.write_digital(0) = red light off

while True:
    if (button_a.is_pressed()):
        music.play(tune_button_a, pin16, False, False)
        lcd.clear()
        lcd.puts('You played:', 0 ,0)
        lcd.puts(str(tune_button_a), 0 ,5)
        sleep(500)
        lcd.clear()
    elif (button_b.is_pressed()):
        music.play(tune_button_b, pin16, False, False)
        lcd.clear()
        lcd.puts('You played:', 0 ,0)
        lcd.puts(str(tune_button_b), 0 ,5)
        sleep(500)
        lcd.clear()
    elif pin8.read_digital() == 0:
        music.play(tune_button_x, pin1, False, False)
        lcd.clear()
        lcd.puts('You played:', 0 ,0)
        lcd.puts(str(tune_button_x), 0 ,5)
        sleep(500)
        lcd.clear()
    elif pin12.read_digital() == 0:
        music.play(tune_button_z, pin1, False, False)
        lcd.clear()
        lcd.puts('You played:', 0 ,0)
        lcd.puts(str(tune_button_z), 0 ,5)
        sleep(500)
        lcd.clear()

    else:
        display.clear()

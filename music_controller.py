from microbit import *
import music
import random
import speech

# --- Microbit configuration guide---

# pin0 = passive buzzer
# pin14 = digital buzzer
# pin2 = joystick x axis
# pin1 = joystick y axis
# pin5 = crash push button
# pin8 = digital push button
# pin12 = digital push button
# pin16 = digital push button


# pin16.write_digital(1) = red light on
# pin16.write_digital(0) = red light off



# --- LCD CODE START ---
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
# --- LCD CODE END ---


# --- VARIABLES USED IN PROGRAM---
# used these images during testing of led - currently not being used.
images_a = [Image.HEART]
images_b = [Image.HAPPY]
images_x = [Image.YES]

# Music notes for buttons
# C4:4 - This means the note C from octave 4, or middle C, played for 4 ticks.
#tune_button_a = ['F#4:4','G4:4','A4:4']
tune_button_a = ['G3:4', 'D5:4']
tune_button_b = ['G3:4', 'D#5:4']
tune_button_c = ['G4:4','A4:4']
tune_button_d = ['A4:4']

pitch_emulator_on = False


while True:

# Welcome message output to LCD Screen    
    lcd.puts('Welcome to', 0 ,0)
    lcd.puts('Music Controller', 0 ,5)

# --- PITCH EMULATOR CODE START ---
# code below turns on pitch emulator and prints status to LCD Screen
# plays a note on repeat and you can use the joystick to change the pitch

    if button_a.is_pressed():
        pitch_emulator_on = True
        pitch_note = 1500
        pitch_rate = 100
        lcd.puts('Pitch Mode: ON', 0 ,0)
        lcd.puts('                ', 0 ,5)
    while pitch_emulator_on:
        joyy = pin1.read_analog()
        joyx = pin2.read_analog()
        music.pitch(pitch_note, pitch_rate)

# code below controls the pitch.
# Move joystick up = higher pitch
# Move joystick down = lower pitch
        if joyy < 765:
            pitch_note += 100
        if joyy > 901:
            pitch_note -= 100

        if pin16.read_digital() == 0:
            pitch_rate += 10
        if pin8.read_digital() == 0:
            pitch_rate -= 10

# the code below is a pitch min and max as the buzzer 
# cannot play pitches above/below a certain range
# this code is to prevent the program from erroring out
        if pitch_note > 2999:
            pitch_note = 3000
        if pitch_note < 199:
            pitch_note = 200

# code below turns off pitch emulator and prints status to LCD Screen             
        if pin12.read_digital() == 0:
            pitch_emulator_on = False
            lcd.puts('Pitch Mode: OFF', 0 ,0)
            lcd.puts('                ', 0 ,5)
            sleep(1000)
            lcd.clear()
    
    sleep(100)
# --- PITCH EMULATOR CODE END ---

# --- PUSH BUTTON TO PLAY NOTES CODE START ---
    if pin8.read_digital() == 0:
        music.play(tune_button_a, pin14, False, False)
        lcd.clear()
        lcd.puts('You played:', 0 ,0)
        lcd.puts(str(tune_button_a), 0 ,5)
        sleep(800)
        lcd.clear()
    if pin12.read_digital() == 0:
        music.play(tune_button_b, pin14, False, False)
        lcd.clear()
        lcd.puts('You played:', 0 ,0)
        lcd.puts(str(tune_button_b), 0 ,5)
        sleep(800)
        lcd.clear()
    if pin16.read_digital() == 0:
        music.play(tune_button_c, pin14, False, False)
        lcd.clear()
        lcd.puts('You played:', 0 ,0)
        lcd.puts(str(tune_button_c), 0 ,5)
        sleep(800)
        lcd.clear()

# --- PUSH BUTTON TO PLAY NOTE CODE START ---

    else:
        display.clear()

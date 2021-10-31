# LIFEDECK V1.0
# PROJECT STARTED HALLOWEEN 2021
# CURRENT FEATURES ARE ABILITY TO RAISE AND LOWER HP VALUES
# WHEN HP REACHES 0, DISPLAY GAME OVER MESSAGE

from machine import I2C, Pin
import time
from pico_i2c_lcd import I2cLcd

# Set base hp values
p1_hp = 40
p2_hp = 40

# Empty array to hold LCD displays
lcds = []

# Empty array to hold buttons
buttons = [] # TODO create set_up_buttons, physically create 3 more buttons

p1_up_btn = Pin(15, Pin.IN, Pin.PULL_UP)

def set_up_lcds(lcds): # Find and set LCD display addresses    
    i2c_1 = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    i2c_2 = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)

    I2C_ADDR_1 = i2c_1.scan()[0]
    I2C_ADDR_2 = i2c_2.scan()[0]
    
    lcd_1 = I2cLcd(i2c_1, I2C_ADDR_1, 2, 16)
    lcd_2 = I2cLcd(i2c_2, I2C_ADDR_2, 2, 16) 
    
    lcds.append(lcd_1)
    lcds.append(lcd_2)
    
    return lcds

def display_version():
    for lcd in lcds:
        lcd.putstr("LifeDeck V1.0")
        
    time.sleep(2)

    for lcd in lcds:
        lcd.clear()

def init_display_hp(p1_hp):
    for lcd in lcds:
        lcd.putstr(f"P1: {p1_hp}")

def display_hp(lcd, p1_hp):
    lcd.putstr(f"P1: {p1_hp}")

def change_hp():
    global p1_hp
    if(p1_up_btn.value()) == 0:
        p1_hp -= 1
        for lcd in lcds:
            lcd.clear()
        for lcd in lcds:
            display_hp(lcd, p1_hp)
        time.sleep(0.5)
        
def game_over(p1_hp):
    if(p1_hp == 0):
        for lcd in lcds:
            lcd.clear()
            lcd.putstr("GAME OVER")
        time.sleep(1)
        exit()
        #lcd.clear()


set_up_lcds(lcds)
display_version()
init_display_hp(p1_hp)


while True:
    change_hp()
    game_over(p1_hp)
    


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
buttons = []



def set_up_lcds(lcds): # Find and set LCD display addresses    
    i2c_1 = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    i2c_2 = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)

    I2C_ADDR_1 = i2c_1.scan()[0]
    I2C_ADDR_2 = i2c_2.scan()[0]
    
    lcd_1 = I2cLcd(i2c_1, I2C_ADDR_1, 2, 16)
    lcd_2 = I2cLcd(i2c_2, I2C_ADDR_2, 2, 16) 
    
    lcds.extend((lcd_1, lcd_2))
    
    return lcds


def set_up_buttons(buttons):
    p1_up_btn = Pin(12, Pin.IN, Pin.PULL_UP)
    p1_down_btn = Pin(13, Pin.IN, Pin.PULL_UP)
    p2_up_btn = Pin(14, Pin.IN, Pin.PULL_UP)
    p2_down_btn = Pin(15, Pin.IN, Pin.PULL_UP)
    
    buttons.extend((p1_up_btn, p1_down_btn, p2_up_btn, p2_down_btn))
    
    return buttons


def display_version():
    for lcd in lcds:
        lcd.putstr("LifeDeck V1.0")
        
    time.sleep(2)

    for lcd in lcds:
        lcd.clear()


def init_display_hp(p1_hp, p2_hp):
    for lcd in lcds:
        lcd.clear()
        lcd.putstr(f"P1: {p1_hp}  P2: {p2_hp}")


def display_hp(lcd, p1_hp, p2_hp):
    lcd.putstr(f"P1: {p1_hp}  P2: {p2_hp}")


def update_hp_display(p1_hp, p2_hp):  
    for lcd in lcds:
        lcd.clear()
    for lcd in lcds:
        display_hp(lcd, p1_hp, p2_hp)
    time.sleep(0.5)
        
        

def change_hp(buttons):
    global p1_hp, p2_hp
    
    if(buttons[0].value() == 0):
        p1_hp += 1
        update_hp_display(p1_hp, p2_hp)
    elif(buttons[1].value() == 0):
        p1_hp -= 1
        update_hp_display(p1_hp, p2_hp)
    elif(buttons[2].value() == 0):
        p2_hp += 1
        update_hp_display(p1_hp, p2_hp)
    elif(buttons[3].value() ==0):
        p2_hp -= 1
        update_hp_display(p1_hp, p2_hp)


def game_over(lcds, p1_hp, p2_hp):
    if(p1_hp == 0 or p2_hp == 0):
        for lcd in lcds:
            lcd.clear()
            lcd.putstr("GAME OVER")
        time.sleep(0.5)
        for lcd in lcds:
            lcd.move_to(0,1)
        if(p1_hp == 0):
            lcds[0].putstr("YOU LOSE")
            lcds[1].putstr("YOU WIN")
        elif(p2_hp == 0):
            lcds[0].putstr("YOU WIN")
            lcds[1].putstr("YOU LOSE")
        time.sleep(3)
        exit() # Not a proper stop, but stops the program anyway.



set_up_lcds(lcds)
set_up_buttons(buttons)
display_version()
init_display_hp(p1_hp, p2_hp)


while True:
    change_hp(buttons)
    game_over(lcds, p1_hp, p2_hp)
 
# LIFEDECK V1.0
# PROJECT STARTED HALLOWEEN 2021
# ALLOWS FOR TWO PLAYER MTG GAMES WITH EITHER 20 OR 40 STARTING LIFE


from machine import I2C, Pin
import time
from pico_i2c_lcd import I2cLcd

# Empty array to hold LCD displays
lcds = []

# Empty array to hold buttons
buttons = []

running = False
selecting = False


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


def set_starting_hp():
    for lcd in lcds:
        lcd.clear()
    lcds[0].putstr('Starting life?')
    lcds[0].move_to(0,1)
    lcds[0].putstr ("20 40")
    lcds[1].putstr('Waiting for')
    lcds[1].move_to(0,1)
    lcds[1].putstr('Player 1')
    
    selecting = True
    while selecting:
        if(buttons[0].value()) == 0:
           p1_hp = 20
           p2_hp = 20
           selecting = False
           start_game(p1_hp, p2_hp)
        elif(buttons[1].value()) == 0:
            p1_hp = 40
            p2_hp = 40
            selecting = False
            start_game(p1_hp, p2_hp)


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


def update_hp_display(p1_hp, p2_hp):  
    for lcd in lcds:
        lcd.clear()
        
    for lcd in lcds:
        lcd.putstr(f"P1: {p1_hp}  P2: {p2_hp}")
        
    time.sleep(0.5)

       
def start_game(p1_hp, p2_hp):    
    init_display_hp(p1_hp, p2_hp)
    game_loop(p1_hp, p2_hp)


def game_loop(p1_hp, p2_hp):
    running = True
    
    while running:
        if(buttons[0].value()) == 0:
            p1_hp += 1
            update_hp_display(p1_hp, p2_hp)
        elif(buttons[1].value()) == 0:
            p1_hp -= 1
            update_hp_display(p1_hp, p2_hp)
        elif(buttons[2].value()) == 0:
            p2_hp += 1
            update_hp_display(p1_hp, p2_hp)
        elif(buttons[3].value()) == 0:
            p2_hp -= 1
            update_hp_display(p1_hp, p2_hp)
        
        game_over(running, p1_hp, p2_hp)
        

def restart_game(selecting):    
    for lcd in lcds:
        lcd.clear()
        
    lcds[0].putstr('Play again?')
    lcds[0].move_to(0,1)
    lcds[0].putstr('Yes No')
    lcds[1].putstr('Waiting for')
    lcds[1].move_to(0,1)
    lcds[1].putstr('Player 1')
        
    while selecting:       
        if(buttons[0].value()) == 0:
           set_starting_hp()
        elif(buttons[1].value()) == 0:
            for lcd in lcds:
                lcd.clear()
                lcd.putstr('Goodbye')
            selecting = False
            quit()


def game_over(running, p1_hp, p2_hp): 
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
        
        running = False
        selecting = True
        restart_game(selecting)


set_up_lcds(lcds)
set_up_buttons(buttons)
display_version()
set_starting_hp()


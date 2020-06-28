# Create back button
# this is a test
import pygame
import sys 
import time
from random import randint, random
import os

pygame.init()

# Display
WIDTH = 750
HEIGHT = 768
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
IMG_TIME = 3
full_screen = True

pygame.display.set_caption("Hand Cricket!")
clock = pygame.time.Clock()

# Load images
intro_imgs = list()
for i in range(1, 6):
    img = pygame.image.load(os.path.join("images", f"intro_{i}.jpg"))
    img = pygame.transform.scale(img, (WIDTH, HEIGHT))
    intro_imgs.append(img)

batting_imgs = list()
for i in range(1, 4):
    img = pygame.image.load(os.path.join("images", f"batting_{i}.jpg"))
    img = pygame.transform.scale(img, (WIDTH, HEIGHT))
    batting_imgs.append(img)

bowling_imgs = list()
for i in range(1, 5):
    img = pygame.image.load(os.path.join("images", f"bowling_{i}.jpg"))
    img = pygame.transform.scale(img, (WIDTH, HEIGHT))
    bowling_imgs.append(img)

toss_img = pygame.image.load(os.path.join("images", "toss.jpg"))
toss_img = pygame.transform.scale(toss_img, (WIDTH, HEIGHT))

victory_img = pygame.image.load(os.path.join("images", "victory.jpg"))
victory_img = pygame.transform.scale(victory_img, (WIDTH, HEIGHT))

loss_img = pygame.image.load(os.path.join("images", "loss.jpg"))
loss_img = pygame.transform.scale(loss_img, (WIDTH, HEIGHT))

mid_game_img = pygame.image.load(os.path.join("images", "mid_game.jpg"))
mid_game_img = pygame.transform.scale(mid_game_img, (WIDTH, HEIGHT))

draw_img = pygame.image.load(os.path.join("images", "draw.jpg"))
draw_img = pygame.transform.scale(draw_img, (WIDTH, HEIGHT))

out_img = pygame.image.load(os.path.join("images", "out.jpg"))
out_img = pygame.transform.scale(out_img, (WIDTH, HEIGHT))

settings_img = pygame.image.load(os.path.join("images", "settings.jpg"))
settings_img = pygame.transform.scale(settings_img, (WIDTH, HEIGHT))

mute_icon = pygame.image.load(os.path.join("images", "mute.jpg"))

unmute_icon = pygame.image.load(os.path.join("images", "unmute.jpg"))


# Load music
pygame.mixer.init()
pygame.mixer.music.load("sound\\BG_song.mp3")

# Volume
with open("volume.txt", 'r') as vol_file:
    vol_percent = int(vol_file.read())
change_vol = False
base_vol = 0.24
muted = False

# Fonts
button_font = pygame.font.SysFont("comicsans", 20)
score_font = pygame.font.SysFont("comicsans", 35)
toss_font = pygame.font.SysFont("comicsans", 50)

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (247, 244, 22)
BLUE = (28, 69, 235)
GREY = (68, 71, 69)

# Score
user_total = 0
comp_total = 0
user_batting = None
first_innings = True
memory = dict()
TOTAL_WICKETS = 1
user_wickets = 0
comp_wickets = 0

events = None

def reset():
    global user_batting, user_total, comp_total, first_innings, memory, events, user_wickets, comp_wickets
    user_total = 0
    comp_total = 0
    user_batting = None
    first_innings = True
    memory = dict()
    events = None
    user_wickets = 0
    comp_wickets = 0

def button_icon(icon, x, y, w, h):
    global events, window
    mouse = pygame.mouse.get_pos()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                return True # icon pressed
    
    icon = pygame.transform.scale(icon, (w, h))
    window.blit(icon, (x, y))


def mute_buttons():
    global muted, window

    icon_side = 20
    if muted:
        pressed = button_icon(unmute_icon, 0, 0, icon_side, icon_side)
        if pressed:
            muted = False
            pygame.mixer.music.set_volume(base_vol * vol_percent / 100)
    else:
        pressed = button_icon(mute_icon, 0, 0, icon_side, icon_side)
        if pressed:
            muted = True
            pygame.mixer.music.set_volume(0)


def text_objects(text, font, colour, pos):
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.center = pos
    window.blit(text_surface, text_rect)

def button(text, x, y, w, h, colour, active_colour, action=None):
    global events
    mouse = pygame.mouse.get_pos()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(window, active_colour, (x-4, y-4, w+10, h+10))
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and action is not None:
                action()
                return True # Button pressed

    else:
        pygame.draw.rect(window, colour, (x, y, w, h))

    text_objects(text, button_font, BLACK, ((x + (w // 2)), (y + (h // 2))))

def update_score():
    global user_total, comp_total, user_wickets, comp_wickets
    # User
    text_objects(f"Your score: {user_total}", score_font, YELLOW,((WIDTH-140), 50))
    text_objects(f"Wickets: {user_wickets}", score_font, RED, ((WIDTH-140), 90))
    # Computer
    text_objects(f"Opponent score: {comp_total}", score_font, BLUE, (140, 50))
    text_objects(f"Wickets: {comp_wickets}", score_font, GREEN, (140, 90))

def draw():
    for i in range(0, 2):
            for j in range(1, 4):
                value = (i*3) + j
                button(str(value), WIDTH-(210 - (j-1)*70), 210 + (i*70), 50, 50, RED, GREEN, lambda: get_input(value))
    
    button("0", WIDTH-140, 350, 50, 50, RED, GREEN, lambda: get_input(0))

def event_check():
    global events

    for event in events:
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                if full_screen:
                    window = pygame.display.set_mode((WIDTH, HEIGHT-100))
                    full_screen = False


def toss():
    global events, window, full_screen
    value = random()
    start_time = time.time()
    while True:
        events = pygame.event.get()
        event_check()
        
        window.blit(toss_img, (0, 0))
        mute_buttons()
        if value > 0.5:
            text_objects("You have won the toss!", toss_font, GREEN,((WIDTH//2), 50))
            text_objects("Choose to:", toss_font, RED,(WIDTH//2, HEIGHT//2 - 75))
            bat = button("Bat", 50, HEIGHT//2 + 20, 100, 50, RED, GREEN, lambda:toss_result(True))
            bowl = button("Bowl", WIDTH-150, HEIGHT//2 + 20, 100, 50, RED, GREEN, lambda:toss_result(False))
            if bat or bowl:
                break
        else:
            text_objects("The opponent has won the toss!", toss_font, RED, ((WIDTH//2), 50))
            if value >= 0.25:
                text_objects("The opponent chose to bat first", toss_font, GREEN, (WIDTH//2, HEIGHT//2 - 75))
                toss_result(False)
            else:
                text_objects("The opponent chose to bowl first!", toss_font, GREEN, (WIDTH//2, HEIGHT//2 - 75))
                toss_result(True)
            if time.time() - start_time > 3:
                break

        button("Home", WIDTH-200, HEIGHT-150, 100, 50, GREEN, RED, game_intro)
        button("EXIT", WIDTH-400, HEIGHT-150, 100, 50, GREEN, RED, quit_game)

        pygame.display.update()
        clock.tick(15)

def toss_result(ub):
    global user_batting
    user_batting = ub

def get_input(num):
    global user_batting, user_total, comp_total, first_innings, memory, user_wickets, comp_wickets, TOTAL_WICKETS, full_screen
    value = randint(0, 6)
    memory["comp_input"] = value
    if user_batting:
        if num != value:
            user_total += num
            if not first_innings and user_total > comp_total:
                memory["user_won"] = True
        else:
            user_wickets += 1
            display_out()
            if first_innings:
                if user_wickets + 1 >= TOTAL_WICKETS:
                    user_batting = False
                    first_innings = False
                    memory["user_total"] = user_total
            else:
                if user_total == comp_total and user_wickets + 1 >= TOTAL_WICKETS:
                    memory["draw"] = True
                elif user_total < comp_total and user_wickets + 1 >= TOTAL_WICKETS:
                    memory["user_won"] = False
    else:
        if num != value:
            comp_total  += value
            if not first_innings and comp_total > user_total:
                memory["user_won"] = False
        else:
            comp_wickets += 1
            display_out()
            if first_innings:
                if comp_wickets + 1 >= TOTAL_WICKETS:
                    user_batting = True
                    first_innings = False
                    memory["comp_total"] = comp_total
            else:
                if user_total == comp_total and comp_wickets + 1 >= TOTAL_WICKETS:
                    memory["draw"] = True
                elif user_total > comp_total and comp_wickets + 1 >= TOTAL_WICKETS:
                    memory["user_won"] = True

def display_out():
    global events, window, full_screen
    start_time = time.time()

    while time.time() - start_time < 3:
        events = pygame.event.get()
        event_check()
        
        window.blit(out_img, (0, 0))

        mute_buttons()

        text_objects("It is Out!", toss_font, RED, (WIDTH//2, HEIGHT//2))

        pygame.display.update()


def quit_game():
    pygame.quit()
    sys.exit()

def end_game(user_won, draw=False):
    global events, window, full_screen
    while True:
        events = pygame.event.get()
        event_check()

        if draw:
            window.blit(draw_img, (0, 0))
            text_objects("It is a draw!", toss_font, BLACK,(WIDTH//2, HEIGHT//2))
        else:
            if user_won:
                window.blit(victory_img, (0, 0))
                text_objects("You have won!", toss_font, GREEN, (WIDTH//2, HEIGHT//2))
            else:
                window.blit(loss_img, (0, 0))
                text_objects("You have lost!", toss_font, RED, (WIDTH//2, HEIGHT//2))
        
        mute_buttons()
        
        button("Play again!", WIDTH-200, HEIGHT-150, 100, 50, RED, GREEN, game)
        button("EXIT", WIDTH-400, HEIGHT-150, 100, 50, GREEN, RED, quit_game)

        pygame.display.update()
        clock.tick(15)

def mid_game(runs, user_batting):
    global events, window, full_screen
    i = 0
    while True:
        events = pygame.event.get()
        event_check()
        for event in events:
            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                game_loop()
                return
        
        window.blit(mid_game_img, (0, 0))

        mute_buttons()

        if user_batting:
            text_objects(f"You have scored {runs} runs.", score_font, YELLOW, (WIDTH//2, 125))
            text_objects(f"The opponent requires {runs+1} runs to win.", score_font, BLACK, (WIDTH//2, 350))
        else:
            text_objects(f"The opponent scored {runs} runs.", score_font, YELLOW, (WIDTH//2, 125))
            text_objects(f"You require {runs+1} runs to win.", score_font, BLACK, (WIDTH//2, 350))

        if i % 2 == 0:
            text_objects(f'Press "ENTER" key to continue!', score_font, RED,(WIDTH//2, 450))

        button("Home", WIDTH-200, HEIGHT-150, 100, 50, GREEN, RED, game_intro)
        button("EXIT", WIDTH-400, HEIGHT-150, 100, 50, GREEN, RED, quit_game)

        i += 1
        pygame.display.update()
        clock.tick(15)
        

def game():
    reset()
    toss()
    game_loop()

def update():
    global memory 
    for key, value in memory.items():
            if key == "comp_input":
                text = text_objects(f"Computer chose {value}.", score_font, BLACK,(165, 280))
                pygame.display.update(text)
            elif key == "user_won":
                if value:
                    end_game(value)
                    break
                else:
                    end_game(value)
                    break
            elif key == "user_total":
                mid_game(value, True)
                break
            elif key == "comp_total":
                mid_game(value, False)
                break
            elif key == "draw":
                end_game(False, True)  
                break

def set_vol():
    global events, window, full_screen, vol_percent, change_vol, muted

    vol_bar_x = (WIDTH//2) - 60
    vol_bar_y = (HEIGHT//2) - 150

    while True:
        events = pygame.event.get()
        event_check()

        window.blit(settings_img, (0, 0))

        mute_buttons()

        mouse_x, mouse_y = pygame.mouse.get_pos() 

        if not muted:
            if vol_bar_x + 100 > mouse_x > vol_bar_x and vol_bar_y + 15 > mouse_y > vol_bar_y:
                left_click = pygame.mouse.get_pressed()[0]
                if left_click:
                    vol_percent = mouse_x - vol_bar_x 
                    change_vol = True

        pygame.draw.rect(window, WHITE, (vol_bar_x, vol_bar_y, 100, 15))

        if not muted:
            pygame.draw.rect(window, BLUE, (vol_bar_x, vol_bar_y, vol_percent, 15))
        else:
            pygame.draw.rect(window, GREY, (vol_bar_x, vol_bar_y, vol_percent, 15))

        text_objects("Background music:", button_font, YELLOW, (vol_bar_x - 75, vol_bar_y + 7))

        button("Home", WIDTH-200, HEIGHT-150, 100, 50, GREEN, RED, game_intro) 
        button("EXIT", WIDTH-400, HEIGHT-150, 100, 50, GREEN, RED, quit_game)
        # Create back button

        if change_vol and not muted:
            pygame.mixer.music.set_volume(base_vol * vol_percent / 100)
            # Save changes
            with open("volume.txt", 'w') as vol_file:
                vol_file.write(str(vol_percent))
            change_vol = False

        pygame.display.update()
        clock.tick(15)

def set_wickets():
    global events, window, full_screen

    while True:
        pass

def settings():
    global events, window, full_screen

    while True:
        events = pygame.event.get()
        event_check()

        window.blit(settings_img, (0, 0))
        mute_buttons()
        
        button("Volume", (WIDTH//2) -50, (HEIGHT//2) - 120, 100, 50, YELLOW, GREEN, set_vol)
        button("Wickets", (WIDTH//2) - 50, (HEIGHT//2) - 60, 100, 50, YELLOW, GREEN, set_wickets)

        button("Home", WIDTH-200, HEIGHT-150, 100, 50, GREEN, RED, game_intro) 
        button("EXIT", WIDTH-400, HEIGHT-150, 100, 50, GREEN, RED, quit_game)

        pygame.display.update()
        clock.tick(15)


def game_loop():
    global memory, events, user_batting, window, full_screen
    memory = dict()
    start_time = time.time()
    img_count = 0
    running = True
    
    while running:
        events = pygame.event.get()
        event_check()

        if user_batting:
            if time.time() - start_time > IMG_TIME:
                img_count = img_count + 1 if img_count < len(batting_imgs) - 1 else 0
                start_time = time.time()
            # Background image every 3 seconds
            window.blit(batting_imgs[img_count], (0, 0))
        else:
            if time.time() - start_time > IMG_TIME:
                img_count = img_count + 1 if img_count < len(bowling_imgs) - 1 else 0
                start_time = time.time()
            # Background image every 3 seconds
            window.blit(bowling_imgs[img_count], (0, 0))

        update()
        mute_buttons()
        draw()    

        button("Home", WIDTH-200, HEIGHT-150, 100, 50, GREEN, RED, game_intro) 
        button("EXIT", WIDTH-400, HEIGHT-150, 100, 50, GREEN, RED, quit_game)   
        
        update_score()

        pygame.display.update()
        clock.tick(15)

def game_intro():
    global events, window, full_screen, vol_percent
    start_time = time.time()
    img_count = 0
    intro = True

    while intro:
        events = pygame.event.get()
        event_check()
                
        if time.time() - start_time > IMG_TIME:
            img_count = img_count + 1 if img_count < len(intro_imgs) - 1 else 0
            start_time = time.time()
        # Background image every 3 seconds
        window.blit(intro_imgs[img_count], (0, 0))

        mute_buttons()

        text_objects("HAND CRICKET", toss_font, YELLOW, (WIDTH//2, 70))

        button("START", (WIDTH//2) - 50, (HEIGHT//2) - 60, 100, 50, RED, GREEN, game)
        button("SETTINGS", (WIDTH//2) - 50, HEIGHT//2, 100, 50, YELLOW, BLUE, settings)
        button("QUIT", (WIDTH//2) - 50, (HEIGHT//2) + 60, 100, 50, GREEN, RED, quit_game)    

        pygame.display.update()
        clock.tick(15)

if __name__ == "__main__":
    pygame.mixer.music.set_volume(base_vol * vol_percent / 100)
    pygame.mixer.music.play(loops=-1, start=0)
    game_intro()




    

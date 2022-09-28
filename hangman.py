import math
import pygame
import random

from english_words import english_words_lower_alpha_set
from googletrans import Translator

pygame.init()

# setup display
WIDTH = 800
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

# fonts
font_size = 30
game_font = pygame.font.Font("freesansbold.ttf", font_size)
title_font = pygame.font.Font("freesansbold.ttf", 50)

# load images
images = []
for i in range(7):
    image = pygame.image.load("Hangman_images/hangman" + str(i) + ".png")
    images.append(image)

# menu buttons
menu_buttons = []
button_height = 100
button_width = 150

# button variables
RADIUS = 20
GAP = 15


# game variables
hangman_status = 0



# colors
bg_color = pygame.Color('grey25')
light_grey = (200, 200, 200)


def draw():
    screen.fill(bg_color)

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = game_font.render(display_word, True, light_grey)
    screen.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(screen, light_grey, (x, y), RADIUS, 3)
            text = game_font.render(ltr, True, light_grey)
            screen.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    screen.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def draw_menu():
    screen.fill(bg_color)

    # draw options
    launch_game = "Play!"
    launch_text = game_font.render(launch_game, True, light_grey)
    screen.blit(launch_text, (WIDTH / 2 - launch_text.get_width()/2, HEIGHT / 2 - button_height*1.15))

    exit_game = "Exit"
    exit_text = game_font.render(exit_game, True, light_grey)
    screen.blit(exit_text, (WIDTH / 2 - exit_text.get_width()/2, HEIGHT / 2 + button_height/1.15))

    # draw options buttons
    play_button = pygame.Rect(WIDTH / 2 - button_width/2, HEIGHT / 2 - button_height*1.5, button_width, button_height)
    menu_buttons.append(play_button)
    pygame.draw.rect(screen, light_grey, play_button, 1)
    exit_button = pygame.Rect(WIDTH / 2 - button_width / 2, HEIGHT / 2 + button_height/2, button_width, button_height)
    menu_buttons.append(exit_button)
    pygame.draw.rect(screen, light_grey, exit_button, 1)

    pygame.display.update()


def display_message(message):
    pygame.time.delay(1000)
    screen.fill(bg_color)
    text = game_font.render(message, True, light_grey)
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    text_word = game_font.render("The word was " + word, True, light_grey)
    screen.blit(text_word, (
        WIDTH / 2 - text_word.get_width() / 2, HEIGHT / 2 - text_word.get_height() / 2 + text_word.get_height() * 2))
    pygame.display.update()
    pygame.time.delay(3000)


def reset_game():
    global hangman_status, translator, english_word, word, guessed, letters, start_x, start_y
    hangman_status = 0

    translator = Translator()
    english_word = random.choice(list(english_words_lower_alpha_set))
    word = list(translator.translate(english_word, dest='fr').text.upper())
    print(''.join(word))
    for i in range (len(word)):
      match word[i]:
        case 'É':
          word[i]='E'
        case 'È':
          word[i]='E'
        case 'Ê':
          word[i]='E'
        case 'Ë':
          word[i]='E'
        case 'À':
          word[i]='A'
        case 'Â':
          word[i]='A'
        case 'Î':
          word[i]='I'
        case 'Ï':
          word[i]='I'
        case 'Û':
          word[i]='U'
        case 'Ô':
          word[i]='O'
        case 'Ö':
          word[i]='O'
    word = ''.join(word)
    print(word)
    guessed = []

    letters = []
    start_x = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
    start_y = 400
    A = 65
    for i in range(26):
        x = start_x + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = start_y + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])


def main():
    # setup game loop
    global clock
    run = True
    reset_game()

    global hangman_status
    while run:

        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                run = False
            if game_event.type == pygame.MOUSEBUTTONDOWN:
                game_m_x, game_m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - game_m_x) ** 2 + (y - game_m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            display_message("You WON!")
            run = False

        if hangman_status == 6:
            display_message("You LOST!")
            run = False

        clock.tick(FPS)


menu_run = True

while menu_run:
    FPS = 60
    clock = pygame.time.Clock()
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            for button in menu_buttons:
                if button.collidepoint(m_x, m_y):
                    if button.y < HEIGHT/2:
                        main()
                        break
                    else:
                        menu_run = False
    clock.tick(FPS)
pygame.quit()





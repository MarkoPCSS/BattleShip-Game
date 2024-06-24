#Name: Marko Kosoric, Ali Kawaja, Gurpal Johal
#Date: June 24th, 2024
#Program Name: Culminating - Battleships
#Purpose: To make a Battleship game with pygame that has data persistance.


#imports
import random
from random import randint
import time
import os
import pygame, sys
from button import Button
import database


#Basic Grid Setup and System
pygame.init()
bounds = (400,450)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("Battleship")
timer = pygame.time.Clock()
fps = 60
grid = [[0]*10 for n in range(10)]
width = 40
ship_positions = []
count = 0
font_one = pygame.font.SysFont('comicsans',60, True)
shots_left = 60

#Colours
LIGHT_BLUE = (173,216,230)
BlUE = (0,0,255)
BLACK = (0 , 0 , 0)
RED = (255 , 0 , 0)
GREEN = (0 , 255 , 0)
win_screen = 0
# Returns Press-Start-2P in the desired size
def get_font(size): 
    return pygame.font.Font("font.ttf", size)

#checks if ship can be placed, if not return false, if it can then it will place the ship and put the the values in the ship_positions array.
def validate_and_place_ship(start_row, end_row, start_col, end_col):
  global grid
  global ship_positions
  
  #Checks if it is empty space: if not, returns false.
  all_valid = True
  for r in range(start_row, end_row):
    for c in range(start_col, end_col):
      if grid[r][c] != 0:
        all_valid = False
        break
  
  #Will only activate once all valid is true.
  if all_valid == True:
    ship_positions.append([start_row, end_row, start_col, end_col])
    for r in range(start_row, end_row):
      for c in range(start_col, end_col):
        grid[r][c] = 1
  return all_valid

#Determines position of ship squares based on what direction is chosen.
def try_to_place_ship_on_grid(row, col, direction, length):
  grid_size = 10
  
  start_row, end_row, start_col, end_col = row, row + 1, col, col + 1
  
  if direction == "left":
    if col - length < 0:
      return False
    start_col = col - length + 1
  
  elif direction == "right":
    if col + length >= grid_size:
      return False
    end_col = col + length
  
  elif direction == "up":
    if row - length < 0:
      return False
    start_row = row - length + 1
  
  elif direction == "down":
    if row + length >= grid_size:
      return False
    end_row = row + length
  
  return validate_and_place_ship(start_row, end_row, start_col, end_col)

#Draws grid and and tries placing ships until 5 ships are placed that meet the criteria of the try_to_place_ship_on_grid_function.
def draw_grid():
  x,y= 0,0
  #Draws grid.
  grid = [[0]*10 for n in range(10)]
  for row in grid:
    for col in row:
      pygame.draw.rect(window, BLACK, pygame.Rect(x, y, 40, 40),  2)
      x = x + width
      pygame.display.flip()
    y = y + width    
    x = 0
  #Ship variables
  num_of_ships_placed = 0
  num_of_ships = 5
  
  ship_positions = [[]]
  ship_size_number = 0
  #Tries placing ships until 5 ships are placed that meet the criteria of the try_to_place_ship_on_grid_function.
  while num_of_ships_placed != num_of_ships:
    random_row = random.randint(0, 9)
    random_col = random.randint(0, 9)
    direction = random.choice(["left", "right", "up", "down"])
    size = [2,3,3,4,5]
    ship_size = size[ship_size_number]
    
    if try_to_place_ship_on_grid(random_row, random_col, direction, ship_size):
      num_of_ships_placed += 1 
      ship_size_number += 1
  
#Prints how many shots the player has left.        
def shotsleft():
  global shots_left
  window.fill(LIGHT_BLUE, rect=(0,400,400,50))
  SHOTS_LEFT_TEXT = get_font(10).render(str(shots_left) + "/60 Shots Left", True, BLACK)
  window.blit(SHOTS_LEFT_TEXT, [10,410])
  MISS_TEXT = get_font(10).render("Miss:", True, BLACK)
  window.blit(MISS_TEXT, [10,430])
  window.fill((0,0,255), rect=(60,430, 10,10))
  HIT_TEXT = get_font(10).render("Hit:", True, BLACK)
  window.blit(HIT_TEXT, [345,430])
  window.fill(RED, rect=(385,430, 10,10))
  

#draws the grid and determines colour based on if grid has a ship, does not have a ship, or has not been clicked yet.
def ship_location():
  x,y= 0,0
  #window.fill(LIGHT_BLUE, rect=(0,400,400,50))
  #SHOTS_LEFT_TEXT = get_font(10).render(str(shots_left) + "/60 Shots Left", True, BLACK)
  #SHOTS_LEFT_RECT = SHOTS_LEFT_TEXT.get_rect(center=(100, 425))
  for row in grid:
    for col in row:
      #Ship locations.
      #if col == 1:
        #pygame.draw.rect(window, BLACK, pygame.Rect(x, y, 40, 40),  2)
        #pygame.draw.rect(window, BLACK, pygame.Rect(x+1, y+1, 38, 38))
      #Ship has been hit.
      if col == 3:
        pygame.draw.rect(window, BLACK, pygame.Rect(x, y, 40, 40),  2)
        pygame.draw.rect(window, RED, pygame.Rect(x+1, y+1, 38, 38))
      #No ship has been hit.
      elif col == 4:
        pygame.draw.rect(window, BLACK, pygame.Rect(x, y, 40, 40),  2)
        pygame.draw.rect(window, BlUE, pygame.Rect(x+1, y+1, 38, 38))
      else:
        pygame.draw.rect(window, BLACK, pygame.Rect(x, y, 40, 40),  2)
      x = x + width
      pygame.display.flip()
    y = y + width    
    x = 0

#Fills in background.
def background():
  window.fill(LIGHT_BLUE)
  pygame.display.flip()

#if all parts of a ship have been shot it is sunk and we later increment the sinking sequence
def check_for_ship_sunk(row, col):
  global ship_positions
  global grid
  
  for position in ship_positions:
    start_row = position[0]
    end_row = position[1]
    start_col = position[2]
    end_col = position[3]

    if start_row <= row <= end_row and start_col <= col <= end_col:
      #ship has been found, now checks if it has sunk
      for r in range(start_row, end_row):
        for c in range(start_col, end_col):
          if grid[r][c] != "3":
            return False
  
  return True

              
#If the left mouse button has been hit, takes the x and y coordinate of the mosue position, divides it by 40 to correspond with the array, sees if there is a ship or not on that square and returns a colour. Also subtracts a shot from the shots left counter if a square is cliked.  
def shoot():
  global shots_left
  #Mouse variables.
  mouse = pygame.mouse.get_pos()
  left_click = pygame.mouse.get_pressed()[0]
  
  if left_click == True and mouse[1]<=399: 
    a,b = int(mouse[0]/40), int(mouse[1]/40)
    if grid[b][a] == 1:
      grid[b][a] = 3
      shots_left -= 1
      game_over_check()
      if check_for_ship_sunk(a,b):
        print("hi")
      else:
        print("no")
    elif grid[b][a] == 0:
      grid[b][a] = 4
      shots_left -= 1
      game_over_check()
  return shots_left

#Displays game over screen once the game is over.
def game_over_screen(win_screen):
  database_highscore = database.read_file()
  global shot_left
  #If players has completed the game in less shots than the number in database, calls the write_table function.
  if 60 - shots_left < int(database_highscore[0][0]):
    database.write_table(shots_left)
  while True:
      #Fills background
      window.fill(LIGHT_BLUE)

      MENU_MOUSE_POS = pygame.mouse.get_pos()
      #If the requirements to win the game are met, "You Win" and highscore is printed.
      if win_screen == 1:
        MENU_TEXT = get_font(32).render("You Win", True, BLACK)
        MENU_RECT = MENU_TEXT.get_rect(center=(200, 100))
        BESTSCORE_TEXT = get_font(10).render("HIGHSCORE:" + database_highscore[0][0] ,True, RED)
        BESTSCORE_RECT = BESTSCORE_TEXT.get_rect(center=(200, 130))
        window.blit(BESTSCORE_TEXT, BESTSCORE_RECT)
      #If the requirements to win the game are not met, "You Lose" is printed.
      if win_screen == 2:
        MENU_TEXT = get_font(32).render("You Lose", True, BLACK)
        MENU_RECT = MENU_TEXT.get_rect(center=(200, 100))
        BESTSCORE_TEXT = get_font(10).render("HIGHSCORE:" + database_highscore[0][0] ,True, RED)
        BESTSCORE_RECT = BESTSCORE_TEXT.get_rect(center=(200, 130))
        window.blit(BESTSCORE_TEXT, BESTSCORE_RECT)
      #If players has completed the game in less shots than the number in database, prints "NEW HIGHSCORE!".
      if 60 - shots_left < int(database_highscore[0][0]):
        HIGHSCORE_TEXT = get_font(10).render("NEW HIGHSCORE!", True, RED)
        HIGHSCORE_RECT = HIGHSCORE_TEXT.get_rect(center=(200, 130))
        window.blit(HIGHSCORE_TEXT, HIGHSCORE_RECT)
        
      #Button variables. Calls button function to create button.
      INFO_BUTTON = Button(image=pygame.image.load("rsz_2play_rect.png"), pos=(200, 180), 
                          text_input="INFO", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
      QUIT_BUTTON = Button(image=pygame.image.load("rsz_2play_rect.png"), pos=(200, 280), 
                          text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
      #Displays text and button and changes colour if cursor hovers over the button.
      window.blit(MENU_TEXT, MENU_RECT)
      for button in [INFO_BUTTON, QUIT_BUTTON]:
          button.changeColor(MENU_MOUSE_POS)
          button.update(window)
      #If the game is quit, then the program stops.
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
          #If button is clicked then calls functions.
          if event.type == pygame.MOUSEBUTTONDOWN:
              if INFO_BUTTON.checkForInput(MENU_MOUSE_POS):
                  info_choice = 2
                  info(info_choice)
              if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                  pygame.quit()
                  sys.exit()

      pygame.display.update()
#Checks if game shoud be over.  
def game_over_check():
  global win_screen
  global shots_left
  count = 0
  x,y= 0,0
  #If there are seventeen 3 values in the array, the game ends and the player wins.
  for row in grid:
   for col in row:
    if col == 3:
      count += 1
    x = x + width
  y = y + width    
  x = 0
  if count == 17:
    win_screen = 1
    game_over_screen(win_screen)
    return count
  #If player runs out of shots, game ends and player loses.
  elif shots_left == 0:
    win_screen = 2
    game_over_screen(win_screen)
  return win_screen

#Displays instructions of the game.
def info(info_choice):
  global win_screen
  while True:
    #loads instructions image
    instructions_background = pygame.image.load("instructions.png").convert()
    window.blit(instructions_background, (0, 0))
    MENU_MOUSE_POS = pygame.mouse.get_pos()
    #Button variables. Calls button function to create button.
    BACK_BUTTON = Button(image=pygame.image.load("rsz_2play_rect.png"), pos=(200, 390), 
                          text_input="BACK", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
    #Changes colour if cursor hovers over the button.
    for button in [BACK_BUTTON]:
          button.changeColor(MENU_MOUSE_POS)
          button.update(window)
    #If the game is quit, then the program stops.
    for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
          #If button is clicked then calls functions.
          if event.type == pygame.MOUSEBUTTONDOWN:
              #If the info screen was called from main menu, info_choice will be set to 1 which will make it so the back button leads to the main menu. Same for if the info screen was called from the game over screen but with 2.
              if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                if info_choice == 1:
                  main_menu()
                elif info_choice == 2:
                  game_over_screen(win_screen)
    #Updates display.
    pygame.display.update()

#Displays pause screen.
def pause():
  while True:
      #Fills background.
      window.fill(LIGHT_BLUE)

      MENU_MOUSE_POS = pygame.mouse.get_pos()
      #displays "Paused"
      PAUSE_TEXT = get_font(50).render("Paused", True, BLACK)
      PAUSE_RECT = PAUSE_TEXT.get_rect(center=(200, 150))
      window.blit(PAUSE_TEXT, PAUSE_RECT)
      #Button variables. Calls button function to create button.
      BACK_BUTTON = Button(image=pygame.image.load("rsz_2play_rect.png"), pos=(200, 330), 
                            text_input="BACK", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
      #Changes colour if cursor hovers over the button.
      for button in [BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)
      #If the game is quit, then the program stops.
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #If button is clicked then calls functions.
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_game()
      pygame.display.update()



def main_menu():
  database_highscore = database.read_file()
  while True:
      #Fills background.
      window.fill(LIGHT_BLUE)

      MENU_MOUSE_POS = pygame.mouse.get_pos()
      #Text variables.
      MENU_TEXT = get_font(32).render("Battleship", True, BLACK)
      MENU_RECT = MENU_TEXT.get_rect(center=(200, 50))

      HIGHSCORE_TEXT = get_font(10).render("Highscore:" + database_highscore[0][0], True, RED)
      HIGHSCORE_RECT = HIGHSCORE_TEXT.get_rect(center=(200,75))
      #Button variables. Calls button function to create button.
      PLAY_BUTTON = Button(image=pygame.image.load("rsz_2play_rect.png"), pos=(200, 130), 
                          text_input="PLAY", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
      INFO_BUTTON = Button(image=pygame.image.load("rsz_2play_rect.png"), pos=(200, 230), 
                          text_input="INFO", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
      QUIT_BUTTON = Button(image=pygame.image.load("rsz_2play_rect.png"), pos=(200, 330), 
                          text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
      #Displays text and button and changes colour if cursor hovers over the button.
      window.blit(MENU_TEXT, MENU_RECT)
      window.blit(HIGHSCORE_TEXT, HIGHSCORE_RECT)
      #Changes colour if cursor hovers over the button.
      for button in [PLAY_BUTTON, INFO_BUTTON, QUIT_BUTTON]:
          button.changeColor(MENU_MOUSE_POS)
          button.update(window)
      #If the game is quit, then the program stops.
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
          #If button is clicked then calls functions.
          if event.type == pygame.MOUSEBUTTONDOWN:
              if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                  start_function()
                  main_game()
              if INFO_BUTTON.checkForInput(MENU_MOUSE_POS):
                  info_choice = 1
                  info(info_choice)
              if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                  pygame.quit()
                  sys.exit()
      #Updates the screen.
      pygame.display.update()
#Functions required to start the game
def start_function():
  background()
  draw_grid()
#Runs the game.
def main_game():
  background()
  while True:
      #Refreshes the screen 60 times per second.
      timer.tick(60)
      ship_location()
      shotsleft()
      shoot()
      #If space is clicked, pause screen appears.
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            pause()
        #If games is quit, then quits the game.
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.quit() 
  
  
  
      
      pygame.display.flip()
  pygame.quit()

database_highscore = database.read_file()
main_menu()
  

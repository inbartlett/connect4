import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.chip = image
        self.turn = True
        self.image = self.chip
        self.rect = self.image.get_rect(center = (167, chip_hover_height))

    def myTurn(self):
        if(self.turn):
            self.image = self.chip
        else:
            self.image = blank_surface

    def update(self):
        self.myTurn()


class BoardandGUI(pygame.sprite.Sprite):
    def __init__(self, p1_chip, p2_chip):
        super().__init__()
        self.image = pygame.image.load("board_elements/boards/default_board.png").convert_alpha()
        self.rect = self.image.get_rect(center = (w/2, gl), bottom = gl)
        self.p1 = pygame.sprite.GroupSingle(Player(p1_chip))
        self.p2 = pygame.sprite.GroupSingle(Player(p2_chip))
        self.slots = [[0] * 7 for i in range(6)]
        self.slot_rects = []
        self.place_rects = []
        self.winner = None
        self.chip_sound = pygame.mixer.Sound("audio/chip_drop.mp3")
        self.bg_music = pygame.mixer.music.load("audio/bg_music.mp3")
        self.setup_board(p1_chip, p2_chip)
    

    def setup_board(self, p1_chip, p2_chip): # fills board row-first with blank surfaces starting from the bottom left. Fills row above board with clickable surfaces for each column. returns the slots as a 2d list, and the places as a list.
        # self.p1.sprite.add(Player(p1_chip))
        self.p1.sprite.turn = True

        # self.p2.sprite.add(Player(p2_chip))
        self.p2.sprite.turn = False
        self.p2.sprite.image = blank_surface

        pygame.mixer.music.play(-1)

        for y in range(497, 497 - 75*6, -75):
            row_list = []
            for x in range(167, 167 + 85*7, 85):
                if len(self.place_rects) < 7:
                    self.place_rects.append(Red.get_rect(center = (x, chip_hover_height)))
                row_list.append(Red.get_rect(center = (x, y)))
            self.slot_rects.append(row_list)

    def check_winner(self): # checks if there is a winner. draws a line over the win and  returns winner if there is one, else returns None.
        cat = 0
        for y in range(len(self.slot_rects)):
            for x in range(len(self.slot_rects[y])):
                if self.slots[y][x] != 0: # if there is a chip in the slot, check if there is a winner
                    cat += 1
                    if x < 4: # check if there is a winner in the row
                        if self.slots[y][x] == self.slots[y][x+1] == self.slots[y][x+2] == self.slots[y][x+3]:
                            self.winner = "Player 1" if self.slots[y][x] == self.p1.sprite.chip else "Player 2"
                            return (y,x), "r"
                    if y < 3: # check if there is a winner in the column
                        if self.slots[y][x] == self.slots[y+1][x] == self.slots[y+2][x] == self.slots[y+3][x]:
                            self.winner = "Player 1" if self.slots[y][x] == self.p1.sprite.chip else "Player 2"
                            return (y,x), "c"
                    if y < 3 and x < 4: # check if there is a winner in the right diagonal
                        if self.slots[y][x] == self.slots[y+1][x+1] == self.slots[y+2][x+2] == self.slots[y+3][x+3]:
                            self.winner = "Player 1" if self.slots[y][x] == self.p1.sprite.chip else "Player 2"
                            return (y,x), "rd"
                    if y > 2 and x < 4: # check if there is a winner in the left diagonal
                        if self.slots[y][x] == self.slots[y-1][x+1] == self.slots[y-2][x+2] == self.slots[y-3][x+3]:
                            self.winner = "Player 1" if self.slots[y][x] == self.p1.sprite.chip else "Player 2"
                            return (y,x), "ld"
        if cat == 42:
            self.winner = "cat"
        return None, None

    def winning_line(self, pos, d): # draws a line over the winning line
        slot_y = pos[0]
        slot_x = pos[1]
        start = self.slot_rects[slot_y][slot_x]
        line_width = 10
        self.draw_guiandslots(screen) # redraw the chips so the line is on top

        if d == "r":
            pygame.draw.line(screen, text_color, (start.left, start.centery), (self.slot_rects[slot_y][slot_x+3].right, self.slot_rects[slot_y][slot_x+3].centery), line_width)
        elif d == "c":
            pygame.draw.line(screen, text_color, (start.centerx, start.bottom), (self.slot_rects[slot_y+3][slot_x].centerx, self.slot_rects[slot_y+3][slot_x].top), line_width)
        elif d == "rd":
            pygame.draw.line(screen, text_color, (start.left, start.bottom), (self.slot_rects[slot_y+3][slot_x+3].right, self.slot_rects[slot_y+3][slot_x+3].top), line_width)
        elif d == "ld":
            pygame.draw.line(screen, text_color, (start.left, start.top), (self.slot_rects[slot_y-3][slot_x+3].right, self.slot_rects[slot_y-3][slot_x+3].bottom), line_width)
            
    def update_board(self): # adds chips to the board.
        mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5, 10, 10)
        collided = mouse_rect.collidelist(self.place_rects)

        if collided != -1: # if place rect selected
            for y in range(len(self.slot_rects)):
                for x in range(len(self.slot_rects[y])):
                    if self.place_rects[collided].centerx != self.slot_rects[y][x].centerx or self.slots[y][x] != 0: # fill the slot that the mouse is in the same column as
                        continue 
                    if self.p1.sprite.turn:
                        self.p1.sprite.turn = False
                        p = self.p1.sprite
                        self.p2.sprite.turn = True
                    else: # if self.p2's turn, fill with yellow
                        self.p1.sprite.turn = True
                        p = self.p2.sprite
                        self.p2.sprite.turn = False
                    self.slots[y][x] = p.sprite.image
                    p.rect.center = (167, chip_hover_height)
                    self.chip_sound.play(loops=0)
                    return self.check_winner()

        for z in range(len(self.slot_rects)): # check if slot rect is selected
            collided = mouse_rect.collidelist(self.slot_rects[z])
            if collided == -1: # if slot rect is selected, fill first available slot in the same column
                continue
            for y in range(len(self.slot_rects)):
                for x in range(len(self.slot_rects[y])):
                    # print(self.slot_rects[1][0], collided)
                    if self.slot_rects[y][collided].centerx != self.slot_rects[y][x].centerx or self.slots[y][x] != 0:
                        continue
                    if self.p1.sprite.turn: # if self.p1's turn, fill with red
                        self.p1.sprite.turn = False
                        p = self.p1
                        self.p2.sprite.turn = True
                    else: # if self.p2's turn, fill with yellow
                        self.p1.sprite.turn = True
                        p = self.p2
                        self.p2.sprite.turn = False
                    self.slots[y][x] = p.sprite.image
                    p.sprite.rect.center = (167, chip_hover_height)
                    self.chip_sound.play(loops=0)
                    return self.check_winner()
        return None, None
        
    def eventloop(self):
        global gaming, resume, in_menu, events
        for event in events: #action loop
            if event.type == pygame.QUIT: # close game manually
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button_rect.collidepoint(pygame.mouse.get_pos()):
                    # resume = False
                    in_menu = 1
                    pygame.mixer.pause()
                    break
                elif help_button_rect.collidepoint(pygame.mouse.get_pos()):
                    # resume = False
                    in_menu = 2
                    pygame.mixer.music.pause()
                    return
                elif pygame.Rect(pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5, 10, 10).collidelist(self.place_rects) != -1 or (pygame.mouse.get_pos()[0] > self.rect.left and pygame.mouse.get_pos()[0] < self.rect.right): # click a valid space         
                    where, direction = self.update_board()
                    if not self.winner:
                        continue
                    
                    self.p1.sprite.turn = False
                    self.p2.sprite.turn = False # stop input and don't render chip hover
                    self.p1.sprite.update()
                    self.p2.sprite.update()

                    if self.winner == "cat":
                        win_text = font.render("It's a draw!", True, text_color)
                    else:
                        win_text = font.render(self.winner + " wins!", True, text_color)
                        self.winning_line(where, direction) # important to draw before rendering win_text because function redraws the background. draws the line over the winning chips

                    screen.blit(win_text, win_text.get_rect(center = (w/2, self.rect.top - 25)))
                    gaming = False
                    return
                
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pos()[0] <= self.place_rects[-1].right: # move chip with mouse
                for x in range(len(self.place_rects)): # check if mouse is in a place rect and move chip to that rect
                    if pygame.mouse.get_pos()[0] < self.place_rects[x].left:
                        return # if mouse is before the current place rect, should have already found a spot prior, so return
                    elif pygame.mouse.get_pos()[0] > self.place_rects[x].right:
                        continue

                    if self.p1.sprite.turn:
                        self.p1.sprite.rect.center = (self.place_rects[x].centerx, self.place_rects[x].centery)
                    else:
                        self.p2.sprite.rect.center = (self.place_rects[x].centerx, self.place_rects[x].centery)
                    break

    def draw_guiandslots(self, screen):
        screen.blit(background, (0, 0))
        screen.blit(menu_button, menu_button_rect)
        screen.blit(help_button, help_button_rect)
        for i in range(len(self.slots)):
            for j in range(len(self.slots[i])):
                if self.slots[i][j] != 0:
                    screen.blit(self.slots[i][j], self.slot_rects[i][j])
        screen.blit(self.image, self.rect)
        self.p1.draw(screen)
        self.p2.draw(screen)

    def update(self):
        self.p1.sprite.update()
        self.p2.sprite.update()
        self.draw_guiandslots(screen)
        self.eventloop()


pygame.init()
pygame.display.set_caption("Connect 4")

# Set up the window
w, h = 850, 600
gl = h-5
chip_hover_height = 40
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()
font = pygame.font.Font("font/junegull.ttf", 50)
text_color = (255, 255, 255)
blank_surface = pygame.image.load("environments/blank.png").convert_alpha()

# Title screen
title = font.render("Connect 4", True, text_color)
title_rect = title.get_rect(center = (w/2, 140))
play_button = font.render("Play!", True, text_color)
play_button_rect = play_button.get_rect(center = (w/2, title_rect.bottom + 200))
coin_anim_image = pygame.image.load("board_elements/coins/spinning.gif/spin_anim1.png").convert_alpha()
coin_anim_rect = pygame.Rect(title_rect.left + title_rect.width/2 -42, title_rect.bottom + 25, 84, 86)
coin_anim = 1

# Game screen
Red = pygame.image.load("board_elements/coins/Red.png").convert_alpha()
Yellow = pygame.image.load("board_elements/coins/Yellow.png").convert_alpha()
# player1 = pygame.sprite.GroupSingle()
# player1.add(Player("Red", Red))
# player2 = pygame.sprite.GroupSingle()
# player2.add(Player("Yellow", Yellow))


# UI elements
menu_button = pygame.image.load("ui/menu_button.png").convert_alpha()
menu_button_rect = menu_button.get_rect(topleft = (10, 10))
game_menu = pygame.image.load("ui/game_menu.png").convert_alpha()
game_menu_rect = game_menu.get_rect(center = (w/2 - 2, h/2 + 11)) # 525 x 400
return_button_rect = pygame.Rect(350, 265, 150, 50)
quit_button_rect = pygame.Rect(350, 360, 150, 50)
help_button = pygame.image.load("ui/help_button.png").convert_alpha()
help_button_rect = help_button.get_rect(topright = (w-10, 10))
help_menu = pygame.image.load("ui/help_menu.png").convert_alpha()
help_menu_rect = game_menu_rect.copy()
exit_menu_button_rect = pygame.Rect(game_menu_rect.right - 54, game_menu_rect.top + 3, 39, 39)

board = []
# Game status
gaming = False
resume = True
in_menu = 0 # 0 = F, 1 = menu, 2 = help

while True:
    events = pygame.event.get()
    if gaming and not in_menu:

        if coin_anim != 1:
            coin_anim = 1
   
        background = pygame.image.load("environments/coffee_shop.png").convert()
        # screen.blit(background, (0, 0))

        board.sprite.update()

                          
    # game paused or ended
    else:
        if board and board.sprite.winner != None: # game ended
            for event in events:
                if event.type == pygame.QUIT: # close window manually
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_RETURN]:
                    board.sprite.winner = None
                    pygame.mixer.music.stop()
                    break
        elif in_menu:
            pygame.mixer.music.pause()
            for event in events:
                if event.type == pygame.QUIT: # close window manually
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN: # click on menu buttons
                    if exit_menu_button_rect.collidepoint(pygame.mouse.get_pos()) or (in_menu == 1 and return_button_rect.collidepoint(pygame.mouse.get_pos())):
                        in_menu = 0
                        # resume = True
                        pygame.mixer.music.unpause()
                        break
                    elif in_menu == 1 and quit_button_rect.collidepoint(pygame.mouse.get_pos()):
                        in_menu = 0
                        # resume = True
                        gaming = False
                        pygame.mixer.music.stop()
                        break

            if in_menu == 1: # game menu
                screen.blit(game_menu, game_menu_rect)
            elif in_menu == 2: # help menu
                screen.blit(help_menu, help_menu_rect) 

            screen.blit(blank_surface, exit_menu_button_rect) # both menus have the same exit button
        else: # title screen
            for event in events:
                if event.type == pygame.QUIT: # close window manually
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if help_button_rect.collidepoint(pygame.mouse.get_pos()):
                        in_menu = 2
                        break
                    elif play_button_rect.collidepoint(pygame.mouse.get_pos()) and not in_menu:
                        gaming = True
                        board = pygame.sprite.GroupSingle()
                        board.add(BoardandGUI(Red, Yellow))

            background = pygame.image.load("ui/title_menu.png").convert()
            screen.blit(background, (0, 0))
            screen.blit(help_button, help_button_rect)
            screen.blit(title, title_rect)
            screen.blit(play_button, play_button_rect)
            pygame.draw.rect(screen, (0, 121, 230), pygame.Rect(play_button_rect.left-10, play_button_rect.top, play_button_rect.width + 20, play_button_rect.height), 2, 20)
            if coin_anim <= 9.5:
                if coin_anim == -1:
                    coin_anim = 1
                coin_anim_image = pygame.image.load(f"board_elements/coins/spinning.gif/spin_anim{int(coin_anim)}.png").convert_alpha()
                coin_anim += 0.08
            # else:
            #     coin_anim = 1
            screen.blit(coin_anim_image, coin_anim_rect)


    # Update the screen and wait for a clock tick
    pygame.display.update()
    clock.tick(60)
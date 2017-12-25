#-*- coding: cp949 -*-

import pygame, sys, copy, time, random
from pygame.locals import *

WHITE = pygame.Color(255,255,255)            #R, G, B
BLACK = pygame.Color(0,0,0)
BLUE = pygame.Color(0,0,255)
GREEN = pygame.Color(0,255,0)
RED = pygame.Color(255,0,0)
GRAY = pygame.Color(100,100,100)
LIGHT_BLUE = pygame.Color(150,190,255)
DARK_BLUE = pygame.Color(0,0,120)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800

if SCREEN_WIDTH > SCREEN_HEIGHT:
    SQUARE_LEN = int(SCREEN_HEIGHT/12)
elif SCREEN_HEIGHT >= SCREEN_WIDTH:
    SQUARE_LEN = int(SCREEN_WIDTH/12)

X_MARGIN = (SCREEN_WIDTH - SQUARE_LEN * 8)/2
Y_MARGIN = (SCREEN_HEIGHT - SQUARE_LEN * 8)/2
# 보드 칸 수 : 8x8
BOARD_LEN = SQUARE_LEN * 8
BOARD_SIZE = (X_MARGIN,Y_MARGIN,BOARD_LEN,BOARD_LEN)

SLIDER_WIDTH = 70
SLIDER_HEIGHT = 50

BASIC_FONT_SIZE = 15

TARGET_FPS = 30                 # 초당 프레임 수

def main():                     # global vars ; pygame의 모듈을 사용한 변수들 선언
    global SCREEN, BASIC_FONT, clock, BACKGROUND, SLIDER_HOR, SLIDER_VER,\
           CHIP_1, CHIP_2, CHIP_3, CHIP_4, WIN_1, WIN_2, WIN_3, WIN_4, DRAW, NEW_GAME, EXIT_GAME,\
           HOW_MANY, CHOOSE_1, CHOOSE_2, CHOOSE_3, HOW_TO_BUTTON, HOW_TO_EXIT, HOW_TO_PLAY

    pygame.init()

    # Set up the Window Screen,Font
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Welcome to the Pixel Board Game!')

    BASIC_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)
    # Set up the Background
    BACKGROUND = pygame.image.load('Gotham 2.jpg')
    # Set up the Slider
    SLIDER_VER = pygame.image.load('Slider_White 2.png')
    SLIDER_HOR = pygame.transform.rotate(SLIDER_VER, 270)
    # Set up the Chip
    CHIP_1 = pygame.image.load('chip 1.png')
    CHIP_2 = pygame.image.load('chip 2.png')
    CHIP_3 = pygame.image.load('chip 3.png')
    CHIP_4 = pygame.image.load('chip 4.png')
    # Set up the Win / Draw text
    WIN_1 = pygame.image.load('win1.png')
    WIN_2 = pygame.image.load('win2.png')
    WIN_3 = pygame.image.load('win3.png')
    WIN_4 = pygame.image.load('win4.png')
    DRAW = pygame.image.load('draw.png')
    NEW_GAME = pygame.image.load('newgame.png')
    EXIT_GAME = pygame.image.load('exit.png')
    # Set up the people choosing
    HOW_MANY = pygame.image.load('howmany.png')
    CHOOSE_1 = pygame.image.load('choose1.png')
    CHOOSE_2 = pygame.image.load('choose2.png')
    CHOOSE_3 = pygame.image.load('choose3.png')
    # Set up the 'How to play?'
    HOW_TO_PLAY = pygame.image.load('how to play.png')
    HOW_TO_EXIT = pygame.image.load('exit button.png')
    HOW_TO_BUTTON = pygame.image.load('how to play button.png')

    clock = pygame.time.Clock()

    while True:
        ret_val = runGame()
        pygame.quit()
        sys.exit(ret_val)

def runGame():                  # 게임 실행 함수
    global SCREEN, clock, BACKGROUND, SLIDER_HOR, SLIDER_VER, SLIDER_X, SLIDER_Y, SAVE_LOC,\
           SLIDER_DX, SLIDER_DY, WIN_1, WIN_2, WIN_3, WIN_4, DRAW, NEW_GAME, EXIT_GAME, \
           HOW_MANY, CHOOSE_1, CHOOSE_2, CHOOSE_3, HOW_TO_BUTTON, HOW_TO_EXIT, HOW_TO_PLAY,\
           turn_str, turn_color,\
           TURN_NUM, SLIDER_BEFX, SLIDER_BEFY, SLIDER_CHANGE, PEOPLE_NUM, SAVE_MOVE  # TurnMoving() 변수

    # default postion of SLIDER_HOR  : SLDIER_D#
    SLIDER_DX = X_MARGIN + (SQUARE_LEN - SLIDER_HEIGHT)/2 + SQUARE_LEN * 3
    SLIDER_DY = Y_MARGIN + (SQUARE_LEN - SLIDER_HEIGHT)/2 + SQUARE_LEN * 3
    SLIDER_X = SLIDER_BEFX = SLIDER_DX
    SLIDER_Y = SLIDER_BEFY = SLIDER_DY
    drawSliderHor(SLIDER_X)
    drawSliderVer(SLIDER_Y)
    SLIDER_CHANGE = 'hor'

    SAVE_MOVE = []           # 칩 위치 기록.  (player_num, x_position, y_position)

    # determine the Next turn
    TURN_NUM = 0  # 지금은 2명 = 0,1. 나중엔 0~3. 순서 정하기.
    drawBackground()
    HOW_MANY_SURF = HOW_MANY.get_rect()
    HOW_MANY_SURF.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    CHOOSE_1_SURF = CHOOSE_1.get_rect()
    CHOOSE_1_SURF.center = (SCREEN_WIDTH/2-200, SCREEN_HEIGHT/2+150)
    CHOOSE_2_SURF = CHOOSE_2.get_rect()
    CHOOSE_2_SURF.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2+150)
    CHOOSE_3_SURF = CHOOSE_3.get_rect()
    CHOOSE_3_SURF.center = (SCREEN_WIDTH/2+200, SCREEN_HEIGHT/2+150)
    HOW_TO_BUTTON_SURF = HOW_TO_BUTTON.get_rect()
    HOW_TO_BUTTON_SURF.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    PEOPLE_NUM = 0
    while True:
        CheckForQuit()
        # choose how many people in game
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if CHOOSE_1_SURF.collidepoint((mousex, mousey)):
                    PEOPLE_NUM = 2
                elif CHOOSE_2_SURF.collidepoint((mousex, mousey)):
                    PEOPLE_NUM = 3
                elif CHOOSE_3_SURF.collidepoint((mousex, mousey)):
                    PEOPLE_NUM = 4
                elif HOW_TO_BUTTON_SURF.collidepoint((mousex, mousey)):
                    drawHowToPlay()
        SCREEN.blit(HOW_MANY, HOW_MANY_SURF)
        SCREEN.blit(CHOOSE_1, CHOOSE_1_SURF)
        SCREEN.blit(CHOOSE_2, CHOOSE_2_SURF)
        SCREEN.blit(CHOOSE_3, CHOOSE_3_SURF)
        SCREEN.blit(HOW_TO_BUTTON, HOW_TO_BUTTON_SURF)
        clock.tick(TARGET_FPS)
        pygame.display.update()
        if PEOPLE_NUM != 0:
            break

    drawBoard()

    # start game - initial statement.
    SAVE_MOVE.append((0, SLIDER_X, SLIDER_Y))

    if PEOPLE_NUM == 2:
        SAVE_MOVE.append((1, SLIDER_X + SQUARE_LEN, SLIDER_Y + SQUARE_LEN))
    elif PEOPLE_NUM == 3:
        SAVE_MOVE.append((1, SLIDER_X + SQUARE_LEN, SLIDER_Y))
        SAVE_MOVE.append((2, SLIDER_X + SQUARE_LEN, SLIDER_Y + SQUARE_LEN))
    elif PEOPLE_NUM == 4:
        SAVE_MOVE.append((1, SLIDER_X + SQUARE_LEN, SLIDER_Y))
        SAVE_MOVE.append((2, SLIDER_X + SQUARE_LEN, SLIDER_Y + SQUARE_LEN))
        SAVE_MOVE.append((3, SLIDER_X, SLIDER_Y + SQUARE_LEN))

    while True :
        # Player 차례
        while TurnMoving() != 'C':
            # 슬라이더 움직임 & 턴 바꿈
            # 움직임 갱신
            drawBackground()
            drawText('This turn is player{} : {}'.format(turn_str,turn_color), (10,70),LIGHT_BLUE)
            drawBoard()
            drawSliderHor(SLIDER_X)
            drawSliderVer(SLIDER_Y)
            drawButton(SLIDER_CHANGE)
            if isValidMove_C(SLIDER_X, SLIDER_Y) == True:
                drawSliderMark()
            else:
                drawSliderMark(False)
            drawBoardLine()
            for i in range(len(SAVE_MOVE)):         # 칩 위치 저장 후 모두 그리기
                deterChipColor(SAVE_MOVE[i][0], SAVE_MOVE[i][1],SAVE_MOVE[i][2])
            clock.tick(TARGET_FPS)
            pygame.display.update()             # display를 다 짜고 한 번에 업데이트.
            CheckForQuit()

        if DecisionWin() == True or DecisionDraw() == False:
            break

        # AI 차례
        drawBackground()
        drawText('This turn is player{} : {}'.format(turn_str,turn_color), (10,70),LIGHT_BLUE)
        drawBoard()
        drawSliderHor(SLIDER_X)
        drawSliderVer(SLIDER_Y)
        drawButton(SLIDER_CHANGE)
        drawBoardLine()
        for i in range(len(SAVE_MOVE)):         # 칩 위치 저장 후 모두 그리기
            deterChipColor(SAVE_MOVE[i][0], SAVE_MOVE[i][1],SAVE_MOVE[i][2])
        clock.tick(TARGET_FPS)
        pygame.display.update()             # display를 다 짜고 한 번에 업데이트.

        AI_1 = Computer_AI_Hard()
        if AI_1 != False:
            SAVE_MOVE.append((TURN_NUM, AI_1[0], AI_1[1]))
            TURN_NUM += 1
            if TURN_NUM == PEOPLE_NUM :
                TURN_NUM = 0

        SLIDER_X = SLIDER_BEFX = AI_1[0]
        SLIDER_Y = SLIDER_BEFY = AI_1[1]

        for i in range(len(SAVE_MOVE)):         # 칩 위치 저장 후 모두 그리기
            deterChipColor(SAVE_MOVE[i][0], SAVE_MOVE[i][1],SAVE_MOVE[i][2])
        pauseUntil = time.time() + 0.5
        while time.time() < pauseUntil:
            continue
        pygame.display.update()
        if DecisionWin() == True or DecisionDraw() == False:
            break

    for i in range(len(SAVE_MOVE)):         # 칩 위치 저장 후 모두 그리기
        deterChipColor(SAVE_MOVE[i][0], SAVE_MOVE[i][1],SAVE_MOVE[i][2])

    TEXT_WIDTH = 700
    TEXT_HEIGHT = 200
    TEXT_POS = ((SCREEN_WIDTH-TEXT_WIDTH)/2, (SCREEN_HEIGHT-TEXT_HEIGHT)/2)

    NEW_GAME_SUR = NEW_GAME.get_rect()
    NEW_GAME_SUR.center = (SCREEN_WIDTH/2 - 200, SCREEN_HEIGHT/2 +150)

    EXIT_GAME_SUR = EXIT_GAME.get_rect()
    EXIT_GAME_SUR.center = (SCREEN_WIDTH/2 + 200, SCREEN_HEIGHT/2 +150)

    if DecisionDraw() == False:
        SCREEN.blit(DRAW, TEXT_POS)

    if DecisionWin() == True:
        if SAVE_MOVE[-1][0] == 0:
            SCREEN.blit(WIN_1, TEXT_POS)
        elif SAVE_MOVE[-1][0] == 1:
            SCREEN.blit(WIN_2, TEXT_POS)
        elif SAVE_MOVE[-1][0] == 2:
            SCREEN.blit(WIN_3, TEXT_POS)
        else:
            SCREEN.blit(WIN_4, TEXT_POS)
    exit_alarm = drawText_Center('Close after 2 seconds',(SCREEN_WIDTH/2,SCREEN_HEIGHT/2+60),GRAY)
    pauseUntil = time.time() + 2
    pygame.display.update()
    while time.time() < pauseUntil:
        continue

    if DecisionDraw() == False:
        return 2
    elif DecisionWin() == True:
        if SAVE_MOVE[-1][0] == 0:
            return 1
        else:
            return 3
'''
    while True:
        # new game or exit? choose it!
        CheckForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if NEW_GAME_SUR.collidepoint((mousex,mousey)):
                    return True
                elif EXIT_GAME_SUR.collidepoint((mousex,mousey)):
                    return False

        SCREEN.blit(NEW_GAME, NEW_GAME_SUR)
        SCREEN.blit(EXIT_GAME, EXIT_GAME_SUR)
        clock.tick(TARGET_FPS)
        pygame.display.update()
'''

def DecisionWin():              # 게임 승패 조건
    global SAVE_MOVE, PEOPLE_NUM, CONT_CHIP, LCT_CHIP

    LCT_CHIP = [] 		# COLLECT_CHIP; now turn player's
    NOW_MOVE = SAVE_MOVE[-1]
    ard = SQUARE_LEN	# around.

    xb = NOW_MOVE[1]-ard
    x = NOW_MOVE[1]
    xa = NOW_MOVE[1]+ard

    yb = NOW_MOVE[2]-ard
    y = NOW_MOVE[2]
    ya = NOW_MOVE[2]+ard

    CONT_CHIP = [[xb,yb], [x,yb], [xa,yb], [xa,y], [xa,ya], [x,ya], [xb,ya], [xb,y],\
    			[xb-ard, yb-ard], [x,yb-ard], [xa+ard, yb-ard], [xa+ard,y],\
    			[xa+ard,ya+ard], [x, ya+ard], [xb-ard,ya+ard], [xb-ard,y],\
                [xb-2*ard,yb-2*ard], [x,yb-2*ard], [xa+2*ard,yb-2*ard], [xa+2*ard,y],\
                [xa+2*ard,ya+2*ard],[x,ya+2*ard],[xb-2*ard,ya+2*ard],[xb-2*ard,y]]  # CONTINIOUS_CHIP
                #~8
                #~12
                #~16
                #~20
                #~24
    for i in range(len(SAVE_MOVE)):
    	if SAVE_MOVE[i][0] == NOW_MOVE[0]:
    		LCT_CHIP.append(list(SAVE_MOVE[i][1:]))

    if PEOPLE_NUM != 4:
        for i in range(4):
            if CONT_CHIP[i] in LCT_CHIP:#2연속
                if CONT_CHIP[i+4] in LCT_CHIP:#3연속
                    if CONT_CHIP[i+12] in LCT_CHIP:#4연속
                        return True
                    elif CONT_CHIP[i+8] in LCT_CHIP:#4연속
                        return True
                elif (CONT_CHIP[i+8] in LCT_CHIP) and (CONT_CHIP[i+16] in LCT_CHIP):#3-4연속
                    return True
        for i in range(4,8):
            if CONT_CHIP[i] in LCT_CHIP:
                if (CONT_CHIP[i+8] in LCT_CHIP) and (CONT_CHIP[i+16] in LCT_CHIP):
                    return True

    elif PEOPLE_NUM == 4:
        for i in range(4):
        	if CONT_CHIP[i] in LCT_CHIP:
        		if CONT_CHIP[i+4] in LCT_CHIP:
        			return True
        		elif CONT_CHIP[i+8] in LCT_CHIP:
        			return True
        for i in range(4,8):
        	if CONT_CHIP[i] in LCT_CHIP:
        		if CONT_CHIP[i+8] in LCT_CHIP:
        			return True
    return False

def DecisionDraw():             # 게임 무승부 조건
    global SAVE_MOVE, PEOPLE_NUM, SLIDER_X, SLIDER_Y, SLIDER_DX, SLIDER_DY, ALL_POS_POS

    ALL_POS_POS = []        # All possible position : 칩을 둘 수 있는 모든 좌표 ( 칩 유무는 상관없음 & 십자모양 )

    for i in range(8):
        ALL_POS_POS.append([SAVE_MOVE[-1][1] , SLIDER_DY -(-i+3)*SQUARE_LEN])
        ALL_POS_POS.append([SLIDER_DX -(-i+3)*SQUARE_LEN , SAVE_MOVE[-1][2]])

    for i in range(len(ALL_POS_POS)):
        if isValidMove_C(ALL_POS_POS[i][0], ALL_POS_POS[i][1]):
            return True
    return False

def Computer_AI():
    global SAVE_MOVE, PEOPLE_NUM, ALL_POS_POS, LCT_CHIP
    #LCT_CHIP : 바로 이전 player의 모든 좌표를 get.
    #OPPO_1 : 특정 플레이어(player 1)의 모든 좌표를 get. -> 필요없으면 후에 삭제.
    ALL_VALID_POS = []      # 칩을 둘 수 있는 모든 좌표 get
    OPPO_1 = []             # 상대 팀(player 1)의 모든 좌표를 get
    MINE = []               # 나(AI : player 2)의 모든 좌표를 get

    for i in range(len(SAVE_MOVE)):
        if SAVE_MOVE[i][0] == 0:
            OPPO_1.append([SAVE_MOVE[i][1],SAVE_MOVE[i][2]])
    for i in range(len(SAVE_MOVE)):
        if SAVE_MOVE[i][0] == 1:
            MINE.append([SAVE_MOVE[i][1],SAVE_MOVE[i][2]])
    for i in range(len(ALL_POS_POS)):
        if isValidMove_C(ALL_POS_POS[i][0], ALL_POS_POS[i][1]) == True:
            ALL_VALID_POS.append([ALL_POS_POS[i][0], ALL_POS_POS[i][1]])

    ard = SQUARE_LEN	# around.
    xb = OPPO_1[-1][0]-ard
    x = OPPO_1[-1][0]
    xa = OPPO_1[-1][0]+ard

    yb = OPPO_1[-1][1]-ard
    y = OPPO_1[-1][1]
    ya = OPPO_1[-1][1]+ard

    CONT_CHIP = [[xb,yb], [x,yb], [xa,yb], [xa,y], [xa,ya], [x,ya], [xb,ya], [xb,y],\
    		[xb-ard, yb-ard], [x,yb-ard], [xa+ard, yb-ard], [xa+ard,y],\
    		[xa+ard,ya+ard], [x, ya+ard], [xb-ard,ya+ard], [xb-ard,y],\
                [xb-2*ard,yb-2*ard], [x,yb-2*ard], [xa+2*ard,yb-2*ard], [xa+2*ard,y],\
                [xa+2*ard,ya+2*ard],[x,ya+2*ard],[xb-2*ard,ya+2*ard],[xb-2*ard,y]]

    if PEOPLE_NUM == 2:
        # 1st : my chip : 3 consicutive -> 4개
        for i in range(4):
            if CONT_CHIP[i] in MINE:#2연속
                if CONT_CHIP[i+4] in MINE:#3연속
                    if CONT_CHIP[i+12] in ALL_VALID_POS:#4연속
                        return CONT_CHIP[i+12]
                    elif CONT_CHIP[i+8] in ALL_VALID_POS:#4연속
                        return CONT_CHIP[i+8]
                elif CONT_CHIP[i+12] in MINE:
                    if CONT_CHIP[i+4] in ALL_VALID_POS:
                        return CONT_CHIP[i+4]
                elif CONT_CHIP[i+8] in MINE:
                    if CONT_CHIP[i+16] in ALL_VALID_POS:#3-4연속
                        return CONT_CHIP[i+16]
                    elif CONT_CHIP[i+4] in ALL_VALID_POS:
                        return CONT_CHIP[i+4]
                elif CONT_CHIP[i+16] in MINE:
                    if CONT_CHIP[i+8] in ALL_VALID_POS:#3-4연속
                        return CONT_CHIP[i+8]
        for i in range(4,8):
            if CONT_CHIP[i] in MINE:
                if CONT_CHIP[i+8] in MINE:
                    if CONT_CHIP[i+16] in ALL_VALID_POS:
                        return CONT_CHIP[i+16]
                    elif CONT_CHIP[i-4] in ALL_VALID_POS:
                        return CONT_CHIP[i-4]
                elif CONT_CHIP[i+16] in MINE:
                    if CONT_CHIP[i+8] in ALL_VALID_POS:
                        return CONT_CHIP[i+8]
        # 2nd : opponent's chip : 3 consicutive -> defense
        for i in range(4):
            if CONT_CHIP[i] in LCT_CHIP:#2연속
                if CONT_CHIP[i+4] in LCT_CHIP:#3연속
                    if CONT_CHIP[i+12] in ALL_VALID_POS:#4연속
                        return CONT_CHIP[i+12]
                    elif CONT_CHIP[i+8] in ALL_VALID_POS:#4연속
                        return CONT_CHIP[i+8]
                elif CONT_CHIP[i+12] in LCT_CHIP:
                    if CONT_CHIP[i+4] in ALL_VALID_POS:
                        return CONT_CHIP[i+4]
                elif CONT_CHIP[i+8] in LCT_CHIP:
                    if CONT_CHIP[i+16] in ALL_VALID_POS:#3-4연속
                        return CONT_CHIP[i+16]
                    elif CONT_CHIP[i+4] in ALL_VALID_POS:
                        return CONT_CHIP[i+4]
                elif CONT_CHIP[i+16] in LCT_CHIP:
                    if CONT_CHIP[i+8] in ALL_VALID_POS:#3-4연속
                        return CONT_CHIP[i+8]
        for i in range(4,8):
            if CONT_CHIP[i] in LCT_CHIP:
                if CONT_CHIP[i+8] in LCT_CHIP:
                    if CONT_CHIP[i+16] in ALL_VALID_POS:
                        return CONT_CHIP[i+16]
                    elif CONT_CHIP[i-4] in ALL_VALID_POS:
                        return CONT_CHIP[i-4]
                elif CONT_CHIP[i+16] in LCT_CHIP:
                    if CONT_CHIP[i+8] in ALL_VALID_POS:
                        return CONT_CHIP[i+8]
        # 3rd : opponent's chip : 2 consicutive -> defense
        for i in range(4):
            if CONT_CHIP[i] in LCT_CHIP:#2연속
                if CONT_CHIP[i+4] in ALL_VALID_POS:#def
                    return CONT_CHIP[i+4]
                elif CONT_CHIP[i+8] in ALL_VALID_POS:#def
                        return CONT_CHIP[i+8]
        for i in range(4,8):
            if CONT_CHIP[i] in LCT_CHIP:#2연속
                if CONT_CHIP[i+8] in ALL_VALID_POS:#def
                    return CONT_CHIP[i+8]
                elif CONT_CHIP[i-4] in ALL_VALID_POS:
                    return CONT_CHIP[i-4]
        # 4th : my chip : 2 consicutive
        for i in range(4):
            if CONT_CHIP[i] in MINE:#2연속
                if CONT_CHIP[i+4] in ALL_VALID_POS:#3연속
                    return CONT_CHIP[i+4]
                elif CONT_CHIP[i+8] in ALL_VALID_POS:#3연속
                        return CONT_CHIP[i+8]
        for i in range(4,8):
            if CONT_CHIP[i] in MINE:#2연속
                if CONT_CHIP[i+8] in ALL_VALID_POS:#3연속
                    return CONT_CHIP[i+8]
                elif CONT_CHIP[i-4] in ALL_VALID_POS:
                    return CONT_CHIP[i-4]
        # 5th : around chip
        for i in range(8):
            if CONT_CHIP[i] in ALL_VALID_POS:
                return CONT_CHIP[i]
        # 6th : Anywhere possible.
        for i in range(len(ALL_VALID_POS)):
            if isValidMove_C(ALL_VALID_POS[i][0], ALL_VALID_POS[i][1]) == True:
                return [ALL_VALID_POS[i][0], ALL_VALID_POS[i][1]]

        return False

def Computer_AI_Hard():
    global SAVE_MOVE, PEOPLE_NUM, ALL_POS_POS, GOOD_LIST, OPPO_1, MINE

    ALL_VALID_POS = []      # 현 칩 + 중 비어있는 모든 좌표 get
    GOOD_LIST = []          # 모든 위치에 대해 자료수집 ; [우선순위, x, y]

    OPPO_1 = []             # 상대 팀(player 1)의 모든 좌표를 get
    MINE = []               # 나(AI : player 2)의 모든 좌표를 get

    for i in range(len(SAVE_MOVE)):
        if SAVE_MOVE[i][0] == 0:
            OPPO_1.append(list(SAVE_MOVE[i][1:]))

    for i in range(len(SAVE_MOVE)):
        if SAVE_MOVE[i][0] == 1:
            MINE.append(list(SAVE_MOVE[i][1:]))

    for i in range(len(ALL_POS_POS)):
        if isValidMove_C(ALL_POS_POS[i][0], ALL_POS_POS[i][1]) == True:
            ALL_VALID_POS.append([ALL_POS_POS[i][0], ALL_POS_POS[i][1]])

    ard = SQUARE_LEN	# around.
    x = SAVE_MOVE[-1][1]
    xb = x-ard
    xa = x+ard

    y = SAVE_MOVE[-1][2]
    yb = y-ard
    ya = y+ard

    CONT_CHIP = [[xb,yb], [x,yb], [xa,yb], [xa,y], [xa,ya], [x,ya], [xb,ya], [xb,y],\
    		[xb-ard, yb-ard], [x,yb-ard], [xa+ard, yb-ard], [xa+ard,y],\
    		[xa+ard,ya+ard], [x, ya+ard], [xb-ard,ya+ard], [xb-ard,y],\
            [xb-2*ard,yb-2*ard], [x,yb-2*ard], [xa+2*ard,yb-2*ard], [xa+2*ard,y],\
            [xa+2*ard,ya+2*ard],[x,ya+2*ard],[xb-2*ard,ya+2*ard],[xb-2*ard,y]]

    for i in SAVE_MOVE:
        # 1,4순위
        if i[0] == 1:
            Conti_Check(1, i[1:])
        # 2,3순위
        elif i[0] == 0:
            Conti_Check(0, i[1:])
    # 1st
    for j in GOOD_LIST:
        if j[0] == 1 and j[1] in ALL_VALID_POS:
            return j[1]
    # 2nd - 1
    # 상대가 3개 연속인 게 다른 위치에 있는 데 그게 내 경로 상에 없는 경우
    # 그 경로를 피하게 만든다.
    for j in GOOD_LIST:
        if j[0] == 2 and not( j[1] in ALL_VALID_POS ):
            for k in ALL_VALID_POS:
                if k[0] == j[1][0]:
                    ALL_VALID_POS.remove(k)
                elif k[1] == j[1][1]:
                    ALL_VALID_POS.remove(k)
    # 2nd - 2
    # 상대가 3개 연속인 데 내 경로 상에 있는 경우
    # 그 좌표에 둔다.
    for j in GOOD_LIST:
        if j[0] == 2 and j[1] in ALL_VALID_POS:
            return j[1]
    # 3rd
    for j in GOOD_LIST:
        if j[0] == 3 and j[1] in ALL_VALID_POS:
            return j[1]
    # 4th
    for j in GOOD_LIST:
        if j[0] == 4 and j[1] in ALL_VALID_POS:
            return j[1]
    # 5th : around chip
    for i in range(8):
        if CONT_CHIP[i] in ALL_VALID_POS:
            return CONT_CHIP[i]
    # 6th : Anywhere possible.
    for i in ALL_VALID_POS:
        if isValidMove_C(i[0],i[1]):
            return i
    return False

def Conti_Check(turn_num, current_check):
    global GOOD_LIST, OPPO_1, MINE
    #current_check : 현재 체크하려는 칩의 좌표
    #array : 같은 색 칩 좌표 리스트
    ard = SQUARE_LEN	# around.
    x = current_check[0]
    xb = x-ard
    xa = x+ard

    y = current_check[1]
    yb = y-ard
    ya = y+ard

    cont_chip = [[xb,yb], [x,yb], [xa,yb], [xa,y], [xa,ya], [x,ya], [xb,ya], [xb,y],\
    		[xb-ard, yb-ard], [x,yb-ard], [xa+ard, yb-ard], [xa+ard,y],\
    		[xa+ard,ya+ard], [x, ya+ard], [xb-ard,ya+ard], [xb-ard,y],\
            [xb-2*ard,yb-2*ard], [x,yb-2*ard], [xa+2*ard,yb-2*ard], [xa+2*ard,y],\
            [xa+2*ard,ya+2*ard],[x,ya+2*ard],[xb-2*ard,ya+2*ard],[xb-2*ard,y]]

    array = []
    #1,4순위
    if turn_num == 1:
        array = MINE
        for i in range(4):
            if cont_chip[i] in array:#2연속
                if cont_chip[i+4] in array:#3연속
                    if isValidMove_C(cont_chip[i+12][0],cont_chip[i+12][1]):#4연속
                        GOOD_LIST.append([1,cont_chip[i+12]])
                    if isValidMove_C(cont_chip[i+8][0],cont_chip[i+8][1]):#4연속
                        GOOD_LIST.append([1, cont_chip[i+8]])
                if cont_chip[i+12] in array:
                    if isValidMove_C(cont_chip[i+4][0],cont_chip[i+4][1]):
                        GOOD_LIST.append([1, cont_chip[i+4]])
                if cont_chip[i+8] in array:
                    if isValidMove_C(cont_chip[i+16][0],cont_chip[i+16][1]):#3-4연속
                        GOOD_LIST.append([1, cont_chip[i+16]])
                    if isValidMove_C(cont_chip[i+4][0],cont_chip[i+4][1]):
                        GOOD_LIST.append([1, cont_chip[i+4]])
                if cont_chip[i+16] in array:
                    if isValidMove_C(cont_chip[i+8][0],cont_chip[i+8][1]):#3-4연속
                        GOOD_LIST.append([1, cont_chip[i+8]])
        for i in range(4,8):
            if cont_chip[i] in array:#2연속
                if cont_chip[i+8] in array:#3연속
                    if isValidMove_C(cont_chip[i+16][0],cont_chip[i+16][1]):#4연속
                        GOOD_LIST.append([1, cont_chip[i+16]])
                    if isValidMove_C(cont_chip[i-4][0],cont_chip[i-4][1]):#4연속
                        GOOD_LIST.append([1, cont_chip[i-4]])
                if cont_chip[i+16] in array:#3연속
                    if isValidMove_C(cont_chip[i+8][0],cont_chip[i+8][1]):#4연속
                        GOOD_LIST.append([1, cont_chip[i+8]])
        for i in range(4):
            if cont_chip[i] in array:#2연속
                if isValidMove_C( cont_chip[i+4][0],cont_chip[i+4][1]):#3연속
                    GOOD_LIST.append([4, cont_chip[i+4]])
                if isValidMove_C( cont_chip[i+8][0],cont_chip[i+8][1]):#3연속
                    GOOD_LIST.append([4, cont_chip[i+8]])
        for i in range(4,8):
            if cont_chip[i] in array:#2연속
                if isValidMove_C( cont_chip[i+8][0],cont_chip[i+8][1]):#3연속
                    GOOD_LIST.append([4, cont_chip[i+8]])
                if isValidMove_C( cont_chip[i-4][0],cont_chip[i-4][1]):
                    GOOD_LIST.append([4, cont_chip[i-4]])
    #2,3순위
    elif turn_num == 0:
        array = OPPO_1
        for i in range(4):
            if cont_chip[i] in array:#2연속
                if cont_chip[i+4] in array:#3연속
                    if isValidMove_C(cont_chip[i+12][0],cont_chip[i+12][1]):#4연속
                        GOOD_LIST.append([2,cont_chip[i+12]])
                    if isValidMove_C(cont_chip[i+8][0],cont_chip[i+8][1]):#4연속
                        GOOD_LIST.append([2, cont_chip[i+8]])
                if cont_chip[i+12] in array:
                    if isValidMove_C(cont_chip[i+4][0],cont_chip[i+4][1]):
                        GOOD_LIST.append([2, cont_chip[i+4]])
                if cont_chip[i+8] in array:
                    if isValidMove_C(cont_chip[i+16][0],cont_chip[i+16][1]):#3-4연속
                        GOOD_LIST.append([2, cont_chip[i+16]])
                    if isValidMove_C(cont_chip[i+4][0],cont_chip[i+4][1]):
                        GOOD_LIST.append([2, cont_chip[i+4]])
                if cont_chip[i+16] in array:
                    if isValidMove_C(cont_chip[i+8][0],cont_chip[i+8][1]):#3-4연속
                        GOOD_LIST.append([2, cont_chip[i+8]])
        for i in range(4,8):
            if cont_chip[i] in array:#2연속
                if cont_chip[i+8] in array:#3연속
                    if isValidMove_C(cont_chip[i+16][0],cont_chip[i+16][1]):#4연속
                        GOOD_LIST.append([2, cont_chip[i+16]])
                    if isValidMove_C(cont_chip[i-4][0],cont_chip[i-4][1]):#4연속
                        GOOD_LIST.append([2, cont_chip[i-4]])
                if cont_chip[i+16] in array:#3연속
                    if isValidMove_C(cont_chip[i+8][0],cont_chip[i+8][1]):#4연속
                        GOOD_LIST.append([2, cont_chip[i+8]])
        for i in range(4):
            if cont_chip[i] in array:#2연속
                if isValidMove_C( cont_chip[i+4][0],cont_chip[i+4][1]):#3연속
                    GOOD_LIST.append([3, cont_chip[i+4]])
                if isValidMove_C( cont_chip[i+8][0],cont_chip[i+8][1]):#3연속
                    GOOD_LIST.append([3, cont_chip[i+8]])
        for i in range(4,8):
            if cont_chip[i] in array:#2연속
                if isValidMove_C( cont_chip[i+8][0],cont_chip[i+8][1]):#3연속
                    GOOD_LIST.append([3, cont_chip[i+8]])
                if isValidMove_C( cont_chip[i-4][0],cont_chip[i-4][1]):
                    GOOD_LIST.append([3, cont_chip[i-4]])

def TurnMoving():               # 키 설정 ; 슬라이더 움직임, 방향 바꿈, 턴 바꿈, 칩 둠.
    global TURN_NUM, SLIDER_X, SLIDER_Y, SLIDER_BEFX, SLIDER_BEFY, SLIDER_CHANGE,\
     PEOPLE_NUM, SAVE_MOVE

    for event in pygame.event.get():
        if event.type == QUIT:                           # QUIT은 pygame.locals의 모듈
            return False
        if event.type == pygame.KEYDOWN:
            if SLIDER_CHANGE == 'hor':
                if event.key == pygame.K_RIGHT:
                    if isValidMove_S(K_RIGHT):
                        SLIDER_X += SQUARE_LEN
                elif event.key == pygame.K_LEFT:
                    if isValidMove_S(K_LEFT):
                        SLIDER_X += - SQUARE_LEN
                elif event.key == pygame.K_SPACE:
                    SLIDER_CHANGE = 'ver'
                    SLIDER_X = SLIDER_BEFX
                elif event.key == pygame.K_c: # 턴 바꾸기 조건 --> 키 바꿀 때 반드시 텍스트 내용도 바꾸기
                    if isValidMove_C(SLIDER_X, SLIDER_Y) == True:
                        SLIDER_BEFX = SLIDER_X
                        SLIDER_BEFY = SLIDER_Y
                        SLIDER_CHANGE = 'hor'
                        # put a chip
                        SAVE_MOVE.append((TURN_NUM, SLIDER_X, SLIDER_Y))
                        TURN_NUM += 1
                        if TURN_NUM == PEOPLE_NUM :
                            TURN_NUM = 0
                        return 'C'
            elif SLIDER_CHANGE == 'ver':
                if event.key == pygame.K_DOWN:
                    if isValidMove_S(K_DOWN):
                        SLIDER_Y += SQUARE_LEN
                elif event.key == pygame.K_UP:
                    if isValidMove_S(K_UP):
                        SLIDER_Y += -SQUARE_LEN
                elif event.key == pygame.K_SPACE:
                    SLIDER_CHANGE = 'hor'
                    SLIDER_Y = SLIDER_BEFY
                elif event.key == pygame.K_c: # 턴 바꾸기 조건 --> 키 바꿀 때 반드시 텍스트 내용도 바꾸기
                    if isValidMove_C(SLIDER_X, SLIDER_Y) == True:
                        SLIDER_BEFX = SLIDER_X
                        SLIDER_BEFY = SLIDER_Y
                        SLIDER_CHANGE = 'hor'
                        # put a chip
                        SAVE_MOVE.append((TURN_NUM, SLIDER_X, SLIDER_Y))
                        TURN_NUM += 1
                        if TURN_NUM == PEOPLE_NUM :
                            TURN_NUM = 0
                        return 'C'

def CheckForQuit():             # QUIT 이벤트가 발생했는 지 검사하고 종료.
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit(4)
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit(4)
        pygame.event.post(event)

def drawBoard():                # 처음 게임 보드를 그린다.
    # rect, line, Button blit.
    global SCREEN
    pygame.draw.rect(SCREEN,BLACK,BOARD_SIZE)  #BOARD_SIZE = (왼쪽, 위, 너비, 높이) 순

def drawBoardLine():
    global SCREEN
    for i in range(9):
        pygame.draw.line(SCREEN,WHITE,(X_MARGIN + SQUARE_LEN*i, Y_MARGIN),\
            (X_MARGIN + SQUARE_LEN*i, Y_MARGIN + BOARD_LEN),3)
        pygame.draw.line(SCREEN,WHITE,(X_MARGIN, Y_MARGIN + SQUARE_LEN*i),\
            (X_MARGIN + BOARD_LEN, Y_MARGIN + SQUARE_LEN*i),3)

def drawButton(change_state):   # 슬라이더 상태를 표시해주는 버튼을 그린다.
    global SCREEN
    if change_state == 'hor':
        Button = pygame.draw.polygon(SCREEN,DARK_BLUE,[(X_MARGIN, Y_MARGIN),\
             (X_MARGIN+SQUARE_LEN, Y_MARGIN), (X_MARGIN+SQUARE_LEN,Y_MARGIN+SQUARE_LEN)])
        drawText_Center('Horizon',(X_MARGIN+SQUARE_LEN/2,Y_MARGIN+SQUARE_LEN/2),WHITE)
    elif change_state == 'ver':
        Button = pygame.draw.polygon(SCREEN,DARK_BLUE,[(X_MARGIN, Y_MARGIN),\
             (X_MARGIN, Y_MARGIN+SQUARE_LEN), (X_MARGIN+SQUARE_LEN,Y_MARGIN+SQUARE_LEN)])
        drawText_Center('Vertical',(X_MARGIN+SQUARE_LEN/2,Y_MARGIN+SQUARE_LEN/2),WHITE)

def drawBackground():           # 배경화면을 그린다.
    global SCREEN, BACKGROUND,TURN_NUM, SAVE_MOVE,turn_str, turn_color
    SCREEN.blit(BACKGROUND, (0,0))
    drawText('Press the \'c\' = Place a chip', (10,10),WHITE)
    drawText('Press the \'Space bar\' = Change a direction of the slider', (10,30),WHITE)
    drawText('Press the \'esc\' = Quit the game', (10,50),WHITE)
    turn_str = str(TURN_NUM+1)
    turn_color = 0
    if TURN_NUM == 0:
        turn_color = 'RED'
    elif TURN_NUM == 1:
        turn_color = 'YELLOW'
    elif TURN_NUM == 2:
        turn_color = 'BLUE'
    else:
        turn_color = 'PURPLE'

    # .blit() : 한 객체 상의 내용(BACKGROUND)을
    # 다른 개체 상(SCREEN)의 특정한 위치((0,0))에 옮겨 그린다.

def drawSliderHor(slider_hor_x):           # 가로 줄 슬라이더를 그린다.
    global SCREEN, SLIDER_HOR
    SLIDER_HOR_Y = Y_MARGIN - SLIDER_WIDTH
    SCREEN.blit(SLIDER_HOR, (slider_hor_x, SLIDER_HOR_Y))

def drawSliderVer(slider_ver_y):           # 세로 줄 슬라이더를 그린다.
    global SCREEN, SLIDER_VER
    SLIDER_VER_X = X_MARGIN - SLIDER_WIDTH
    SCREEN.blit(SLIDER_VER, (SLIDER_VER_X, slider_ver_y))

def drawSliderMark(state = True):          # 슬라이더가 가르키는 좌표를 표시한다.
    global SCREEN, SLIDER_X, SLIDER_Y
    Mark_X = SLIDER_X -(SQUARE_LEN - SLIDER_HEIGHT)/2
    Mark_Y = SLIDER_Y - (SQUARE_LEN - SLIDER_HEIGHT)/2
    if state == True:
        Mark = pygame.draw.rect(SCREEN, LIGHT_BLUE, (Mark_X,\
               Mark_Y,SQUARE_LEN,SQUARE_LEN))
    else:
        Mark = pygame.draw.rect(SCREEN, RED, (Mark_X,\
               Mark_Y,SQUARE_LEN,SQUARE_LEN))

def drawHowToPlay():
    global HOW_TO_PLAY, HOW_TO_EXIT

    HTP_WIDTH = 600
    HTP_HEIGHT = 500
    HOW_TO_EXIT_SURF = HOW_TO_EXIT.get_rect()
    HOW_TO_EXIT_SURF.center = ((SCREEN_WIDTH + HTP_WIDTH)/2 - 50, (SCREEN_HEIGHT - HTP_HEIGHT)/2 + 50)
    HOW_TO_PLAY_SURF = HOW_TO_PLAY.get_rect()
    HOW_TO_PLAY_SURF.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    SCREEN.blit(HOW_TO_PLAY, HOW_TO_PLAY_SURF)
    SCREEN.blit(HOW_TO_EXIT, HOW_TO_EXIT_SURF)
    clock.tick(TARGET_FPS)
    pygame.display.update()
    while True:
        CheckForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if HOW_TO_EXIT_SURF.collidepoint((mousex,mousey)):
                    return 0

def isValidMove_S(direction):              # 슬라이더가 이동 가능한 범위인지 확인해준다.
    global SLIDER_X, SLIDER_Y
    if direction == K_RIGHT:
        if SLIDER_X > X_MARGIN and \
           SLIDER_X < (X_MARGIN + BOARD_LEN - SQUARE_LEN):
            return True
    elif direction == K_LEFT:
        if SLIDER_X > X_MARGIN + SQUARE_LEN and \
            SLIDER_X < X_MARGIN + BOARD_LEN:
            return True
    elif direction == K_DOWN:
        if SLIDER_Y > Y_MARGIN and\
            SLIDER_Y <(Y_MARGIN + BOARD_LEN - SQUARE_LEN):
            return True
    elif direction == K_UP:
        if SLIDER_Y > Y_MARGIN + SQUARE_LEN and\
            SLIDER_Y <(Y_MARGIN + BOARD_LEN):
            return True
    return False

def isValidMove_C(SLIDER_X, SLIDER_Y):                       # 칩을 둘 수 있는 자리인지 확인해준다. & ANOTHER_MOVE : DecisionDraw 전용
	global SAVE_MOVE, SLIDER_DX, SLIDER_DY

	# 모서리 자리 불가능
	if (SLIDER_X == (SLIDER_DX - 3 * SQUARE_LEN) and SLIDER_Y == (SLIDER_DY - 3 * SQUARE_LEN)) or\
		(SLIDER_X == (SLIDER_DX + 4 * SQUARE_LEN) and SLIDER_Y == (SLIDER_DY - 3 * SQUARE_LEN)) or\
		(SLIDER_X == (SLIDER_DX - 3 * SQUARE_LEN) and SLIDER_Y == (SLIDER_DY + 4 * SQUARE_LEN)) or\
		(SLIDER_X == (SLIDER_DX + 4 * SQUARE_LEN) and SLIDER_Y == (SLIDER_DY + 4 * SQUARE_LEN)):
		return False

	# 이미 둔 자리 불가능
	for i in range(len(SAVE_MOVE)):
		if SLIDER_X == SAVE_MOVE[i][1] and SLIDER_Y == SAVE_MOVE[i][2]:
			return False

	return True

def deterChipColor(turn_num,x,y):          # 차례에 따른 칩 색상과 위치를 정한다.
    global SCREEN, CHIP_1, CHIP_2, CHIP_3, CHIP_4

    if turn_num == 0:
        SCREEN.blit(CHIP_1, (x-4, y-4))
    elif turn_num == 1:
        SCREEN.blit(CHIP_2, (x-4, y-4))
    elif turn_num == 2:
        SCREEN.blit(CHIP_3, (x-4, y-4))
    elif turn_num == 3:
        SCREEN.blit(CHIP_4, (x-4, y-4))

def drawText(text, position, color):    # 텍스트를 적는다.
    global SCREEN, BASIC_FONT
    text_Surface_obj = BASIC_FONT.render(text, True, color)
    text_Rect_obj = text_Surface_obj.get_rect()
    (text_Rect_obj.x, text_Rect_obj.y) = position
    SCREEN.blit(text_Surface_obj, text_Rect_obj)

def drawText_Center(text, position, color):          # 텍스트의 중앙이 중심이 된다.
    global SCREEN, BASIC_FONT
    text_Surface_obj = BASIC_FONT.render(text, True, color)
    text_Rect_obj = text_Surface_obj.get_rect()
    text_Rect_obj.center = position
    SCREEN.blit(text_Surface_obj, text_Rect_obj)

if __name__ == '__main__':
    main()

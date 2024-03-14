from pygame import * 
import random
import math
init()
size = width, height = 1000, 700
screen = display.set_mode(size)

#define colours

BLACK = (0,0,0)
PASTELGREEN = (189, 210, 182)
GREEN = (109, 139, 116)
DARKGREEN = (121, 135, 119)
BEIGE = (233, 229, 214)
DARKBEIGE = (200, 195, 174)

# define fonts
menuFont = font.Font("Caviar-Dreams/CaviarDreams.ttf",40)
titleFont = font.Font("Caviar-Dreams/CaviarDreams.ttf", 120)
subtitleFont = font.Font("Caviar-Dreams/CaviarDreams.ttf", 60)
basicFont = font.Font("Caviar-Dreams/CaviarDreams.ttf",30)

# Load images
imgList = []
for i in range(1,31):
  imgList.append(("images/img" + str(i) + ".png"))

backArrow = image.load("images/backArrow.png")
backArrow = transform.scale(backArrow, (50,50))

InstrPic = image.load("images/InstrImg.png")
InstrPic = transform.scale(InstrPic, (400, 250))

# define states
STATEMENU = 0
STATEPLAY = 1
STATEDIFFICULTY = 2
STATEINSTR = 3
STATESTAT = 4
STATEGAMEDONE = 5
STATEQUIT = 6


# Unflipped = 0
# Flipped = 1
# Matched = -1
flippedList = [0] * 60 

# defining lists and variables needed in the functions (mostly for statistics screen)
difficultyWord = ""
statListDifficulty = []
statListTime = []
statEasy = []
statMedium = []
statHard = []
statExtreme = []

# puts info from file into list to save it across runs
statFile = open("stat.txt", "r")
while True:
  text = statFile.readline()
  text = text.rstrip("\n")
  if text == "":
    break
  space = text.find(" ")
  statListDifficulty.append(text[:space])
  statListTime.append(text[space+1:])
  


# function for printing in the center of a rect
def centerTextPrint(font, text, x, y, l, w, colour):
  size = font.size(text)
  rectangle = (x, y, l, w)
  # finds the middle values of x and y 
  startX = (rectangle[2] - size[0])//2 + rectangle[0] 
  startY = (rectangle[3] - size[1])//2 + rectangle[1]
  x, y, l, w = startX, startY, size[0], size[1]
  textRender = font.render(text, 1, colour)
  screen.blit(textRender, (x, y, l, w))

# figures out the number of rows and columsn the cards should be in
def getLayout(numberOfCards):
  root = math.sqrt(numberOfCards) # square roots the total number of cards
  for i in range(10): # finds the closest divisors from the middle to give the most even grid
    divisor = math.floor(root) + i
    if (numberOfCards / divisor).is_integer():
      divisor2 = numberOfCards / divisor
      break
  return divisor, int(divisor2)

# figures out what state the code is in
def getState(mx, my, currentState):
  if currentState == STATEMENU: # buttons on the menu
    if mx > 150 and mx < 450 and my > 350 and my < 425:
      currentState = STATEDIFFICULTY
    elif mx > 550 and mx < 850 and my > 350 and my < 425:
      currentState = STATEINSTR
    elif mx > 150 and mx < 450 and my > 500 and my < 575:
      currentState = STATESTAT
    elif mx > 550 and mx < 850 and my > 500 and my < 575:
      currentState = STATEQUIT
      
  elif mx > 0 and mx < 50 and my > 0 and my < 50 and currentState == STATEPLAY: # goes back from play screen to difficulty screen instead of menu
    currentState = STATEDIFFICULTY
    
  elif currentState == STATEGAMEDONE: # game done buttons
    if mx > 180 and mx < 480 and my > 450 and my < 525:
      currentState = STATEMENU
    elif mx > 520 and mx < 820 and my > 450 and my < 525:
      currentState = STATEDIFFICULTY
      
  elif mx > 0 and mx < 50 and my > 0 and my < 50: # catch all for other back buttons
    currentState = STATEMENU
    
  return currentState

# turns the number difficulty into a word (Easy, Medium, etc..)
def getDifficulty(difficulty):
  if difficulty == 1:
    difficulty = "Easy"
  elif difficulty == 3:
    difficulty = "Medium"
  elif difficulty == 7:
    difficulty = "Hard"
  elif difficulty == 10:
    difficulty = "Extreme"
  return difficulty

# draws the cards based on the flip list
def drawCards(cards, flip, imgs, cardWidth, cardHeight, difficulty):
  for card in cards:
    x, y, l, w = card # seperates the rect values
    if flip[cards.index(card)] == -1: # when card is already matched
      draw.rect(screen, BEIGE, card)
      
    elif flip[cards.index(card)] == 1: # when card is flipped
      draw.rect(screen, BEIGE, card)
      cardPic = image.load(imgs[cards.index(card)])
      if difficulty == 7: # cards are slightly elongated, compensates to make picture look better
        cardPic = transform.scale(cardPic, (cardWidth//2.2, cardHeight//1.5))
        cardx = x + ((cardWidth - cardWidth//2.2) / 2)
        cardy = y + ((cardHeight - cardHeight//1.5) / 2)        
      else: # scales the pictures to the card size
        cardPic = transform.scale(cardPic, (cardWidth//1.7, cardHeight//1.5))
        cardx = x + ((cardWidth - cardWidth//1.7) / 2)
        cardy = y + ((cardHeight - cardHeight//1.5) / 2)
      screen.blit(cardPic, (cardx, cardy, l, w))
      draw.rect(screen, DARKBEIGE, card, 3, 10)
      
    else: # when card is unflipped (backside)
      draw.rect(screen, PASTELGREEN, card, 0, 10)
      draw.rect(screen, GREEN, card, 3, 10)      
    
# checks if the two flipped cards match or not
def cardMatch(imgList, flipList):
  firstCard = -1
  for i in range(len(flipList)):
    if flipList[i] == 1 and firstCard == -1: # finds the first flipped card and saves it
      firstCard = i
    elif flipList[i] == 1: # finds the second flipped card and compares images
      if imgList[firstCard] == imgList[i]:
        flipList[i], flipList[firstCard] = -1, -1 # if same, match the cards
      else:
        flipList[i], flipList[firstCard] = 0, 0 # if not, flip them back over
  return flipList

# draws the menu screen
def drawMenu(mx, my):
  rect = [Rect(150, 350, 300, 75), Rect(550, 350, 300, 75), Rect(150, 500, 300, 75), Rect(550, 500, 300, 75)] # list of buttons
  
  screen.fill(BEIGE) # drawing menu
  centerTextPrint(titleFont, "Nature", 0, 0, 1000, 150, GREEN)
  centerTextPrint(titleFont, "Match", 0, 100, 1000, 200, GREEN) 
  
  for rectangle in rect:
    draw.rect(screen, PASTELGREEN, rectangle)

  centerTextPrint(menuFont, "play", 150, 350, 300, 75, BLACK)
  centerTextPrint(menuFont, "instructions", 550, 350, 300, 75, BLACK)
  centerTextPrint(menuFont, "statistics", 150, 500, 300, 75, BLACK)
  centerTextPrint(menuFont, "quit", 550, 500, 300, 75, BLACK)
  
  for i in rect: # checks if mouse is over button
    if i.collidepoint(mx, my) == True:
      draw.rect(screen, BLACK, i, 2)

# draws the difficulty selection screen
def drawDifficultyMenu(mx, my):
  difficulty = -1
  
  screen.fill(BEIGE) # base screen
  draw.rect(screen, PASTELGREEN, (0,0,50,50))
  screen.blit(backArrow, (0,0,50,50))

  # buttons and title
  centerTextPrint(subtitleFont, "Select a difficulty:", 0, 0, 1000, 150, GREEN)
  rect = [Rect(250, 200, 500, 75), Rect(250, 300, 500, 75), Rect(250, 400, 500, 75), Rect(250, 500, 500, 75)]
  for rectangle in rect:
    draw.rect(screen, PASTELGREEN, rectangle)
  centerTextPrint(menuFont, "Easy", 250, 200, 500, 75, BLACK)
  centerTextPrint(menuFont, "Medium", 250, 300, 500, 75, BLACK)
  centerTextPrint(menuFont, "Hard", 250, 400, 500, 75, BLACK)
  centerTextPrint(menuFont, "Extreme", 250, 500, 500, 75, BLACK)  
  
  for i in rect: # checks if mouse is over button to highlight it
    if i.collidepoint(mx, my) == True:
      draw.rect(screen, BLACK, i, 2)  

# draws the screen for when the game is finished
def gameDone(timeTook, difficulty, mx, my):
  screen.fill(BEIGE)
  draw.rect(screen, PASTELGREEN, (150, 100, 700, 500))
  draw.rect(screen, DARKGREEN, (150, 100, 700, 500), 10)
  centerTextPrint(subtitleFont,"Well Done!", 200, 100, 600, 150, BLACK)
  text1Render = menuFont.render("difficulty:", 1, BLACK)
  text2Render = menuFont.render("time taken:", 1, BLACK)
  minutes = str(timeTook // 60)
  if timeTook-(timeTook//60) < 10:
    seconds = "0" + str(timeTook-((timeTook//60)*60))
  else:
    seconds = str(timeTook-((timeTook//60)*60))
  text3Render = menuFont.render(minutes + ":" + seconds, 1, BLACK)
  text4Render = menuFont.render(str(getDifficulty(difficulty)), 1, BLACK)
  screen.blit(text1Render, (250, 250, 300, 150))
  screen.blit(text2Render, (250, 300, 300, 150))
  screen.blit(text3Render, (500, 300, 300, 150))
  screen.blit(text4Render, (500, 250, 300, 150))
  
  optionsList = [Rect(180, 450, 300, 75), Rect(520, 450, 300, 75)]
  
  
  for rectangle in optionsList:
    draw.rect(screen, GREEN, rectangle)
  centerTextPrint(menuFont, "return to home", 180, 450, 300, 75, BLACK)
  centerTextPrint(menuFont, "play again", 520, 450, 300, 75, BLACK)
  
  for i in optionsList:
    if i.collidepoint(mx, my) == True:
      draw.rect(screen, BLACK, i, 2)    

# draws the play screen
def drawPlay(mx, my, difficulty, imgs, flipList):
  # base screen w/ back arrow
  screen.fill(BEIGE)
  draw.rect(screen, PASTELGREEN, (0,0,50,50))
  screen.blit(backArrow, (0,0,50,50))
  # prints difficulty at the top of the screen
  difficultyWord = getDifficulty(difficulty)
  centerTextPrint(menuFont, "Difficulty: " + difficultyWord, 0, 0, 1000, 100, GREEN)
  # finds the number of cards and how large each one should be
  cards = (difficulty*4)+8
  rows, columns = getLayout(cards)
  width = 1000 / columns
  height = 600 / rows
  h = 100
  
  # prints card
  cardsList = []
  for i in range(rows):
    for j in range(columns):
        cardsList.append(Rect(j*width, h, width, height))
    h += height
    
  # flips card once clicked
  for card in cardsList:
    if e.type == MOUSEBUTTONDOWN and card.collidepoint(mx, my) == True and flippedList[cardsList.index(card)] != -1:
      if flipList.count(1) == 2: # if two cards are flipped, checks if they match
        flipList = cardMatch(cardImg, flipList)
      if flippedList[cardsList.index(card)] != -1: # in case you re-click a matched card
        flipList[cardsList.index(card)] = 1

  drawCards(cardsList, flipList, imgs, width, height, difficulty)

  return flipList

# draws the instruction screen
def drawInstr():
  screen.fill(BEIGE) # base screen
  draw.rect(screen, PASTELGREEN, (0,0,50,50))  
  screen.blit(backArrow, (0,0,50,50))
  
  # prints text and image instructions
  centerTextPrint(subtitleFont, "How to Play", 0, 0, 1000, 150, GREEN)  
  text1Render = basicFont.render("The goal of the game is to match all the pairs", 1, GREEN)
  text2Render = basicFont.render("of cards under the time limit", 1, GREEN)
  text3Render = basicFont.render("Click the card to see what the symbol is underneath", 1, GREEN)
  text4Render = basicFont.render("Match all the cards as fast", 1, GREEN)
  text5Render = basicFont.render("as you can!", 1, GREEN)
  
  screen.blit(text1Render, (90, 140, 300, 150))
  screen.blit(text2Render, (90, 170, 300, 150))
  screen.blit(text3Render, (90, 220, 300, 150))
  screen.blit(text4Render, (520, 320, 300, 150))
  screen.blit(text5Render, (520, 350, 300, 150))
  
  screen.blit(InstrPic, (90, 300, 600, 400))

# draws the statistic screen
def drawStat():
  screen.fill(BEIGE) # base screen
  draw.rect(screen, PASTELGREEN, (0,0,50,50))  
  screen.blit(backArrow, (0,0,50,50))
  
  # text and boxes for each dificulty
  centerTextPrint(subtitleFont, "Statistics", 0, 0, 1000, 100, GREEN)
  draw.rect(screen, PASTELGREEN, (525, 125, 400, 250))
  draw.rect(screen, PASTELGREEN, (75, 425, 400, 250))
  draw.rect(screen, PASTELGREEN, (75, 125, 400, 250))
  draw.rect(screen, PASTELGREEN, (525, 425, 400, 250))
      
  draw.rect(screen, DARKGREEN, (525, 125, 400, 250), 5)
  draw.rect(screen, DARKGREEN, (75, 425, 400, 250), 5)
  draw.rect(screen, DARKGREEN, (75, 125, 400, 250), 5)
  draw.rect(screen, DARKGREEN, (525, 425, 400, 250), 5)

  centerTextPrint(menuFont, "Easy", 75, 125, 400, 50, BLACK)
  centerTextPrint(menuFont, "Medium", 525, 125, 400, 50, BLACK)
  centerTextPrint(menuFont, "Hard", 75, 425, 400, 50, BLACK)
  centerTextPrint(menuFont, "Extreme", 525, 425, 400, 50, BLACK)

  # empties lists for each difficulty and time
  statEasy = []
  statMedium = []
  statHard = []
  statExtreme = []

  # reads from file and sorts each game into lists of respective difficulties
  statFile = open("stat.txt", "r")
  while True:
    text = statFile.readline()
    text = text.rstrip("\n")
    if text == "":
      break
    if text.count("Easy") == 1:
      statEasy.append(text)
    elif text.count("Medium") == 1:
      statMedium.append(text)
    elif text.count("Hard") == 1:
      statHard.append(text)
    elif text.count("Extreme") == 1:
      statExtreme.append(text)
  
  statFile.close()

  # for each difficulty, displays the top 5 times
  statEasy.sort()
  place = 1
  y = 170
  for i in statEasy:
    space = i.find(" ")
    number = basicFont.render(str(place) + ".", 1, BLACK)
    timeText = basicFont.render(i[space+1:], 1, BLACK)
    screen.blit(number, (100, y, 100, 50))
    screen.blit(timeText, (150, y, 100, 50))
    place += 1
    y += 40
    if place >= 6:
      break
    
  statMedium.sort()
  place = 1
  y = 170
  for i in statMedium:
    space = i.find(" ")
    number = basicFont.render(str(place) + ".", 1, BLACK)
    timeText = basicFont.render(i[space+1:], 1, BLACK)
    screen.blit(number, (550, y, 100, 50))
    screen.blit(timeText, (600, y, 100, 50))
    place += 1
    y += 40
    if place >= 6:
      break
    
  statHard.sort()
  place = 1
  y = 470
  for i in statHard:
    space = i.find(" ")
    number = basicFont.render(str(place) + ".", 1, BLACK)
    timeText = basicFont.render(i[space+1:], 1, BLACK)
    screen.blit(number, (100, y, 100, 50))
    screen.blit(timeText, (150, y, 100, 50))
    place += 1
    y += 40
    if place >= 6:
      break
    
  statExtreme.sort()
  place = 1
  y = 470
  for i in statExtreme:
    space = i.find(" ")
    number = basicFont.render(str(place) + ".", 1, BLACK)
    timeText = basicFont.render(i[space+1:], 1, BLACK)
    screen.blit(number, (550, y, 100, 50))
    screen.blit(timeText, (600, y, 100, 50))
    place += 1
    y += 40
    if place >= 6:
      break
    
#menu screen (play, instructions, quit, statistics)
state = STATEMENU
prevState = 0
myClock = time.Clock()
mx, my, = 0, 0
flipTimer = time.get_ticks()
difficulty = -1
# Game Loop
while state != STATEQUIT:

  for e in event.get():  # checks all events that happen
    
    if e.type == QUIT:
      state = STATEQUIT
      
    if e.type == MOUSEBUTTONDOWN:
      mx, my = e.pos
      button = e.button
      state = getState(mx, my, state)
      
    elif e.type == MOUSEMOTION and state == STATEMENU: # checks mouse position every time it moves to highlight the current option on menu
      mx, my = e.pos
      drawMenu(mx, my)
      
    if state == STATEDIFFICULTY and (prevState == STATEMENU or prevState == STATEPLAY or prevState == STATEGAMEDONE): # for the first time difficulty menu is entered, won't accidentally click an option
      mx, my = 100, 0
      drawDifficultyMenu(mx, my)

    if state == STATEDIFFICULTY and prevState == STATEDIFFICULTY:
      if e.type == MOUSEMOTION:
        mx, my = e.pos
        drawDifficultyMenu(mx, my)
      if e.type == MOUSEBUTTONDOWN: # options for difficulty
        mx, my = e.pos
        
        if mx > 250 and mx < 750 and my > 200 and my < 275:
          difficulty = 1
          state = STATEPLAY
        elif mx > 250 and mx < 750 and my > 300 and my < 375:
          difficulty = 3
          state = STATEPLAY
        elif mx > 250 and mx < 750 and my > 400 and my < 475:
          difficulty = 7
          state = STATEPLAY
        elif mx > 250 and mx < 750 and my > 500 and my < 575:
          difficulty = 10        
          state = STATEPLAY
          
      prevState = STATEDIFFICULTY

    if e.type == MOUSEBUTTONDOWN and state == STATEPLAY: # starting set up
      if prevState == STATEDIFFICULTY:
        
        cards = ((difficulty*4)+8)/2
        cardImg = random.sample(imgList, int(cards))
        cardImg = cardImg + cardImg
        random.shuffle(cardImg)
        mx, my = 100, 0
        flippedList = [0] * 60
        gameTimer = time.get_ticks()
        centerTextPrint(basicFont, "60", 900, 0, 100, 100, BLACK)
      flippedList = drawPlay(mx, my, difficulty, cardImg, flippedList)
      
      # notes down the time from when two cards are flipped
      if flippedList.count(1) == 2:
        flipTimer = time.get_ticks()
        
  # cards automatically flip back over after 700ms of two cards being flipped (or matches them)
  if flippedList.count(1) > 1 and time.get_ticks() - flipTimer >= 700:
    flippedList = cardMatch(cardImg, flippedList)
    flippedList = drawPlay(mx, my, difficulty, cardImg, flippedList)

  # in-game timer that counts up from 0
  if state == STATEPLAY:
    gameTime = (time.get_ticks() - gameTimer) / 1000
    gameTime = math.floor(gameTime)
    draw.rect(screen, BEIGE, (900, 0, 100, 100))
    centerTextPrint(basicFont, str(gameTime), 900, 0, 100, 100, BLACK)
    display.update()

  # when game finishes
  if state == STATEPLAY and flippedList.count(-1) == len(cardImg):
    state = STATEGAMEDONE
    mx, my = 0, 0
    gameDone(int(gameTime), difficulty, mx, my)
    statListDifficulty.append(str(getDifficulty(difficulty)))
    
    # makes the time into the format 0:00
    if (gameTime-(gameTime//60)) < 10:
      seconds = "0" + str(gameTime-((gameTime//60)*60))
    else:
      seconds = str(gameTime-((gameTime//60)*60))
      
    statListTime.append(str(gameTime // 60) + ":" + seconds)

    # writes the game into a file in the format  difficulty 0:00
    statFile = open("stat.txt", "w")
    for i in range(len(statListDifficulty)):
      statFile.write(statListDifficulty[i] + " " + statListTime[i] + "\n")
    statFile.close()

  # continues feeding mouse position to game done state for button highlights
  if state == STATEGAMEDONE and e.type == MOUSEMOTION:
    mx, my = e.pos
    gameDone(int(gameTime), difficulty, mx, my)
    getState(mx, my, state)
  
  if state != prevState:
    if state == STATEMENU:              
      drawMenu(mx, my)

    elif state == STATEINSTR:
      drawInstr()

    elif state == STATESTAT:
      drawStat()

    prevState = state

  display.update()
  myClock.tick(60)
    # waits long enough to have 60 fps

quit()


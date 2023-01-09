import math
import os
import pygame
import random

SCREENWIDTH  = 612
SCREENHEIGHT = 512
FPS = 144

IMAGES, HITMASKS, SPRITES = {}, {}, {}

SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.init()

IMAGES['dot'] = pygame.image.load('assets/dot.png').convert_alpha()
IMAGES['target'] = pygame.image.load('assets/target.png').convert_alpha()
IMAGES['rock'] = pygame.image.load('assets/obstructions/rock.png').convert_alpha()
IMAGES['sniper'] = pygame.image.load('assets/sniper.png').convert_alpha()

def getHitmask(image):
    #  returns a hitmask using an image's alpha
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

#  Hitmasks for graph dot and target
HITMASKS['dot'] = (
  getHitmask(IMAGES['dot'])
)

HITMASKS['target'] = (
  getHitmask(IMAGES['target'])
)

HITMASKS['rock'] = (
  getHitmask(IMAGES['rock'])
)

#  Creates the level. Make the locations for the target and obstructions
def GenerateLevel(difficultyFactor):
  tPosX = random.randint(500, 560)
  tPosY = random.randint(100, 400)
  SCREEN.fill((255,255,255))
  obstructionList = []

  num = 0

  #  Loads boulders on the top. Also checks distance between each boulder so they aren't too close.
  while num < difficultyFactor/2:
    while True:
      dist = 60
      randomPos = (random.randint(150, 420), random.randint(-10, 300))
      if not len(obstructionList) == 0:
        for obstruction in obstructionList:
          obstructionDist = math.hypot(obstruction[1][0] - randomPos[0], obstruction[1][1] - randomPos[1])
          if obstructionDist < dist:
            dist = obstructionDist
      else:
        break
      if dist >= 60:
        break

        
    obstructionList.append([IMAGES['rock'], randomPos])
    num += 1

  
  while num < difficultyFactor:
    while True:
      dist = 60
      randomPos = (random.randint(150, 420), random.randint(300, 550))
      if not len(obstructionList) == 0:
        for obstruction in obstructionList:
          obstructionDist = math.hypot(obstruction[1][0] - randomPos[0], obstruction[1][1] - randomPos[1])
          if obstructionDist < dist:
            dist = obstructionDist
      else:
        break

      if dist >= 60:
        break
        
    obstructionList.append([IMAGES['rock'], randomPos])
    num += 1
  
  return tPosX, tPosY, obstructionList

#  Sets up the level by placing the target, obstructions, etc.
def SetupLevel(posX, posY, obstructions):
  #  Place target
  SCREEN.blit(IMAGES['target'], (posX, posY))

  #  Place sniper
  SCREEN.blit(IMAGES['sniper'], (-40, 230))
  
  #  Place obstructions
  for obstruction in obstructions:
    SCREEN.blit(obstruction[0], obstruction[1])
  
  pygame.display.update()


#  Purpose is to find subfunctions within the equation (ex. find sin, cos, log, etc.)
def FindFunction(functionName, equation):

  startingVal = 0
  while True:
    try:
      FunctionLocation = equation.find(functionName, startingVal)
      if FunctionLocation >= 0 and FunctionLocation < len(equation):
        numberLocation = FunctionLocation + len(functionName)

        #  Counts the amount of brackets within the function. If it drops below 0, then that means the function has ended
        BracketCounter = 0
        numberLocationEnd = FunctionLocation
        for letter in range(len(equation)):
          if letter >= FunctionLocation:
            if equation[letter] == "(":
              BracketCounter += 1
            elif equation[letter] == ")":
              BracketCounter -= 1
              if BracketCounter == 0:
                numberLocationEnd = letter
                break
            
        functionEquation = (equation[FunctionLocation:(numberLocationEnd + 1)])
        innerEquation = (equation[numberLocation:numberLocationEnd])
        
        #  Clean up/calculate equations and functions within the function (ex. sin(sin(pi/6)) would simplify to sin(0.5) instead)
        #  Basically just recalling the same function to calculate the subfunction/equation
        innerEquationValue = eval(CleanupEquation(innerEquation))

        if functionName == "sin(":
          innerEquationValue = math.sin(innerEquationValue)
        elif functionName == "cos(":
          innerEquationValue = math.cos(innerEquationValue)
        elif functionName == "ln(":
          innerEquationValue = math.log(innerEquationValue, math.e)
        elif functionName == "sqrt(":
          innerEquationValue = math.sqrt(innerEquationValue)

        equation = equation.replace(functionEquation, str(innerEquationValue))
      else:
        break
      startingVal = numberLocationEnd
    except:
      break
  return equation
  
#  Since eval has different syntax for operations, we have to make the expression compatible
#  Turns x^2 to x**2, and 3(x)2  to 3*x*2 etc.
def CleanupEquation(equation):
  #  Change ^ to **
  if equation.find("^") >= 0:
    equation = equation.replace("^", "**")

  #  Change e to the actual value
  if equation.find("e") >= 0:
    equation = equation.replace("e", str(math.e))

  # Change pi to to the actual value
  if equation.find("pi") >= 0:
    equation = equation.replace("pi", str(math.pi))

  # Change log to natural log automatically
  if equation.find("log") >= 0:
    equation = equation.replace("log", "ln")

  # Look for sin, cos, ln, and sqrt function
  equation = FindFunction("sin(", equation)
  equation = FindFunction("cos(", equation)
  equation = FindFunction("ln(", equation)
  equation = FindFunction("sqrt(", equation)
  
  # Look for multiplications via opening brackets
  # Basically loops through all the brackets and sees if its directly next to a real number
  startingVal = 1
  while True:
    openingBracketLocation = equation.find("(", startingVal)
    if openingBracketLocation >= 0 and openingBracketLocation < len(equation):
      numberLocation = openingBracketLocation - 1
      #  If the number next to bracket is not a closing bracket or a number, then don't worry about it
      try:
        if equation[numberLocation] != ")":
          float(equation[numberLocation])
        equation = ''.join((equation[:openingBracketLocation],'*', equation[openingBracketLocation:]))
        openingBracketLocation += 1
      except:
        openingBracketLocation = openingBracketLocation
    else:
      break
    startingVal = openingBracketLocation + 1

  # Look for multiplications via closing brackets
  # Basically same code as above but with closing brackets
  startingVal = 1
  
  while True:
    closingBracketLocation = equation.find(")", startingVal)
    if closingBracketLocation >= 1 and closingBracketLocation < len(equation):
      numberLocation = closingBracketLocation + 1
      try:
        if equation[numberLocation] != "(":
          float(equation[numberLocation])
        equation = ''.join((equation[:numberLocation],'*', equation[numberLocation:]))
        closingBracketLocation += 1
      except:
        closingBracketLocation = closingBracketLocation
    else:
      break
    startingVal = closingBracketLocation + 1
  return equation
    

def CalculateEquation(equation, tPosX, tPosY, obstructions):
  os.system('clear')
  x = 0
  yShift = 0
  errornum = 0
  coordinatesTable = []
  dotTable = []
  while x <= 28.5:
    try:
      newEquation = equation.replace("x", "({})".format(str(x)))
      newEquation = CleanupEquation(newEquation)
      if x == 0:
        yShift = -(eval(newEquation))
      #print("f({})".format(str(x)), "=", (newEquation), "=", eval(newEquation))
      coords = [x, eval(newEquation) + yShift]
      coordinatesTable.append(coords)
      PlotGraph(coords, dotTable, tPosX, tPosY, obstructions)
      crashChecker = checkCrash({'x': tPosX, 'y': tPosY}, dotTable, obstructions)
      if crashChecker[0]:
        if crashChecker[1]:
          print("Nice!")
          return "Hit"
        else:
          print("Miss!")
          return "Miss"
    except:
      #  Might be an asymptote or undefined (x/0)
      errornum += 1
      coordinatesTable.append((x, "None"))
      print("Unknown Value", errornum)
      #  If error happens more than 15 times then theres a problem
      if errornum > 20:
        return "Error"
    x += 0.1
    pygame.time.Clock().tick(FPS)
  return "Miss"
#  Place brackets between all x to easily work with the equation
#equation = CleanupEquation(equation.replace("x", "(x)"))
  

def PlotGraph(coords, dotTable, tPosX, tPosY, obstructions):
  #  Used to alternate positions between dots to reduce lag
  SCREEN.fill((255,255,255))
  if coords[1] != 'None':
    pos = (125 + coords[0]*20, 200 - coords[1]*20 + 120)
    dotTable.append([IMAGES['dot'], pos])
    if len(dotTable) > 30:
      dotTable.pop(0)
  for dot in dotTable:
    SCREEN.blit(dot[0], dot[1])
  SetupLevel(tPosX, tPosY, obstructions)
  pygame.display.update()

def checkCrash(target, dots, obstructions):
   #  Returns True if a dot collides with an object. Returns 2 trues if it also collides with the target
    target['w'] = IMAGES['target'].get_width()
    target['h'] = IMAGES['target'].get_height()

    rockWidth = IMAGES['rock'].get_width()
    rockHeight = IMAGES['rock'].get_height()
  
    targetRect = pygame.Rect(target['x'], target['y'], target['w'], target['h'])
    dotW = IMAGES['dot'].get_width()
    dotH = IMAGES['dot'].get_height()

    for dot in dots:
        #  All dot rects
        dotRect = pygame.Rect(dot[1][0], dot[1][1], dotW, dotH)

        #  target, dots and obstructions hitmasks
        targetHitMask = HITMASKS['target']
        dotHitmask = HITMASKS['dot']
        rockHitmask = HITMASKS['rock']

        # if dot collided with rock
        for obstruction in obstructions:
          rockRect = pygame.Rect(obstruction[1][0], obstruction[1][1], rockWidth, rockHeight)
          rockCollide = pixelCollision(rockRect, dotRect, rockHitmask, dotHitmask)
          if rockCollide:
            return [True, False]
          
        # if dot collided with target
        targetCollide = pixelCollision(targetRect, dotRect, targetHitMask, dotHitmask)

        if targetCollide:
            return [True, True]

    return [False, False]

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    #  Checks if two objects collide and not just their rects
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

difficultyFactor = 2
def main(difficultyFactor):
  tPosX, tPosY, obstructions = GenerateLevel(difficultyFactor)
  SetupLevel(tPosX, tPosY, obstructions)
  while True:
    equation = input("type equation: f(x) = ")
    coordinates = CalculateEquation(equation, tPosX, tPosY, obstructions)
    if coordinates == "Hit":
      print("next stage")
      difficultyFactor += 2
      main(difficultyFactor)
    elif coordinates == "Miss":
      print("loose 1 life")

main(difficultyFactor)
import math
import os
import pygame
import random
from pygame.locals import *

SCREENWIDTH  = 612
SCREENHEIGHT = 512

IMAGES, BACKGROUNDS, SPRITES = {}, {}, {}

SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.init()

#Alternates between dots to reduce lag
tableOfDots = []
IMAGES['dot'] = pygame.image.load('assets/dot.png').convert_alpha()
IMAGES['target'] = pygame.image.load('assets/target.png').convert_alpha()

#  Sets up the level by placing the target, obstructions, etc.
def SetupLevel(posX, posY):
  #  Place target
  SCREEN.blit(IMAGES['target'], (posX, posY))
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
  os.system('clear')
  return equation
    

def CalculateEquation(equation, dotTable, tPosX, tPosY):
  x = 0
  errornum = 0
  coordinatesTable = []
  while x <= 28.5:
    try:
      newEquation = equation.replace("x", "({})".format(str(x)))
      newEquation = CleanupEquation(newEquation)
      #print("f({})".format(str(x)), "=", (newEquation), "=", eval(newEquation))
      coords = [x, eval(newEquation)]
      coordinatesTable.append(coords)
      PlotGraph(coords, dotTable, tPosX, tPosY)
    except:
      #  Might be an asymptote or undefined (x/0)
      errornum += 1
      coordinatesTable.append((x, "None"))
      print("Unknown Value", errornum)
      #  If error happens more than 15 times then theres a problem
      if errornum > 20:
        return "Error"
    x += 0.1
  return coordinatesTable
#  Place brackets between all x to easily work with the equation
#equation = CleanupEquation(equation.replace("x", "(x)"))
  

def PlotGraph(coords, dotTable, tPosX, tPosY):
  #Used to alternate positions between dots to reduce lag
  SCREEN.fill((255,255,255))
  if coords[1] != 'None':
    pos = (100 + coords[0]*20, 200 - coords[1]*20)
    dotTable.append([IMAGES['dot'], pos])
    if len(dotTable) > 30:
      dotTable.pop(0)
  for dot in dotTable:
    SCREEN.blit(dot[0], dot[1])
  SetupLevel(tPosX, tPosY)
  pygame.display.update()

tPosX = random.randint(500, 560)
tPosY = random.randint(200, 400)
SCREEN.fill((255,255,255))
SetupLevel(tPosX, tPosY)
equation = input("type equation: f(x) = ")

coordinates = CalculateEquation(equation, tableOfDots, tPosX, tPosY)
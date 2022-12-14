import math

equation = input("type equation: f(x) = ")

#  Since eval has different syntax for operations, we have to make the expression compatible
#  Turns x^2 to x**2, and 3(x)2  to 3*x*2 etc.
def CleanupEquation(equation):
  #  Change ^ to **
  if equation.find("^") > 0:
    equation = equation.replace("^", "**")

  #  Change e to the actual value
  if equation.find("e") > 0:
    equation = equation.replace("e", str(math.e))

  # Change pi to to the actual value
  if equation.find("pi") > 0:
    equation = equation.replace("pi", str(math.pi))

    
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
        print(" ")
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
        print(" ")
    else:
      break
    startingVal = closingBracketLocation + 1

  # Look for sin function
  startingVal = 0
  while True:
    #try:
      sinFunctionLocation = equation.find("sin(", startingVal)
      if sinFunctionLocation >= 0 and sinFunctionLocation < len(equation):
        numberLocation = sinFunctionLocation + 5
        numberLocationEnd = equation.find(")", sinFunctionLocation)
        #  Clean up the equation within the sin function (ex. sin(2(2)) would simplify to sin(4) instead)
        innerEquation = (equation[numberLocation:numberLocationEnd])
        print(equation, innerEquation)
        innerEquationValue = eval(CleanupEquation(innerEquation))
        innerEquationValue = math.sin(innerEquationValue)
        equation.replace(str(innerEquation), str(innerEquationValue))
        print(equation)
      else:
        break
      startingVal = numberLocationEnd
   # except:
     # break
            
          
  return equation
    

def CalculateEquation(equation):
  num = 0
  while num < 10:
      newEquation = equation.replace("x", "({})".format(str(num)))
      newEquation = CleanupEquation(newEquation)
      print((newEquation), "=")
      num += 0.1

#  Place brackets between all x to easily work with the equation
#equation = CleanupEquation(equation.replace("x", "(x)"))
CalculateEquation(equation)
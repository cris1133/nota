#! /home/cristopher/Enthought/Canopy_64bit/User/bin/python
from decimal import *

## This executes simple "list" expressions
## These need to be pre-parsed into lists
## Prefix notation

def initalize():
	operations = ['+','-','*','^','/']
	variables = {}
	global operations
	global variables
initalize()

# The most basic expressions are executed here after being parsed
def expressionSimple(expression):
	operation = expression[0]
	n1 = expression[1]
	n2 = expression[2]
	if operation == '+':
		return str(Decimal(n1) + Decimal(n2))	
	elif operation == '-':
		return str(Decimal(n1) - Decimal(n2))
	elif operation == '*':
		return str(Decimal(n1) * Decimal(n2))
	elif operation == '^':
		return str(Decimal(n1) ** Decimal(n2))
	elif operation == '/':
		return str(Decimal(n1) / Decimal(n2))

# Workings
# First every operation is pushed onto the stack
# The operations are popped from the expression
# Each operation works on the first two numbers of the list, a new list is created to be passed to expressionSimple
# The two numbers are popped, passed to expressionSimple and the result is pushed to the list
# This is repeated until there's one result
def breakDown(expression):
	operationStack = []
	if not expression[0] in operations:
		if not expression[0].isdigit():
			return "Error: Invalid Operation"
		else:
			return expression[0]
	if len(expression) == 3:
		return expressionSimple(expression)
	if len(expression) >= 5:
		# Get the operations into the stack, pop them from the expression
		for symbol in expression:
			if symbol in operations:
				operationStack.insert(0, symbol)
				expression = expression[1:]
		while len(expression) > 1:
			#print expression
			#print operationStack
			# Execute the first expression
			result = 0
			result = expressionSimple([operationStack[0], expression[0], expression[1]])
			# Pop the appropriate symbols
			expression = expression[2:]
			operationStack = operationStack[1:]
			# Add in the result
			expression.insert(0, result)
		return expression[0]

# Our data cleaning is done here
# Parens are removed
# Extra spaces are cleaned out
# Variables are plugged in
def parseExpression(expression):
	if expression.startswith(" "):
		expression = expression[1:]
	if expression[0] != '(':
		return "Error: Malformed Expression"
	if expression[-1] != ')':
		return "Error: Malformed Expression"
	if len(expression) < 5:
		return "Error: Malformed Expression"
	# Strip out the parens and extra space in front
	expression = expression.replace('(', "")
	expression = expression.replace(')', "")
	# Convert the string to a list
	expression = expression.split(" ")
	# Clean out extra spaces
	expressionClean = []
	for symbol in range(len(expression)):
		if not expression[symbol] == '':
			expressionClean.append(expression[symbol])
	# Plug in variables
	for symbol in range(len(expressionClean)):
		if expressionClean[symbol].replace('.', '').isdigit() or expressionClean[symbol] in operations:
			continue
		elif expressionClean[symbol] in variables.keys():
			if expressionClean[symbol] != None:
				expressionClean[symbol] = variables[expressionClean[symbol]]
		else:
			expressionClean[symbol] = "0"

	# Break it down 
	return breakDown(expressionClean)



## This function classifies expressions and variable assignments
## It also requires that a number is supplied in the field
## Variables: Splits via a colon
def classify(string):
	string_ = string.replace('\t', '')
	string_ = string_.replace(' ', '')
	if string_.startswith('(') and string_.endswith(')'):
		return [1, parseExpression(string.replace('\t', ''))]
	elif ':' in string:
		string_ = string_.split(':')
		# These two are for checking if it's an expression on the right
		string = string.replace('\t', '')
		string = string.split(':')
		# Check if the assigment is an expression
		if classify(string[1])[0] == 1:
			variables[string_[0]] = parseExpression(string[1])
		else:
			variables[string_[0]] = string_[1]
		return [2, "Variable Assigment"]
	else:
		return [0, "Error"]
			

	


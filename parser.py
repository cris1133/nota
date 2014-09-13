#! /home/cristopher/Enthought/Canopy_64bit/User/bin/python
def parseExpression(expression):
	tokens = []
	for character in range(len(expression)):
		if expression[1] != '(':
			break
		if expression[-1] != ')':
			break
		if 

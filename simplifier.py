#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tree import Node
import math
import re
#  from LaTEX import parseLaTEX

def main():
    simplify('\\frac{x+y}{t}', {"x":2, "t":4, "y":4})

def parseLaTEX(expression:str) -> Node:
    # Normalize expression before handling it
    expression = expression.strip()
    expression = expression.replace(" ", "")

    regexes = {
            "functions" : {
                "logarithm" :   re.compile(r'\\log(?:_(.+))?\((.+)\)'),
                "ln" :          re.compile(r'\\ln\((.+)\)'),
                "sine" :        re.compile(r'\\sin\((.+)\)'),
                "cosine" :      re.compile(r'\\cos\((.+)\)'),
                "tangent" :     re.compile(r'\\tan\((.+)\)'),
                "cosecant" :    re.compile(r'\\csc\((.+)\)'),
                "secant" :      re.compile(r'\\sec\((.+)\)'),
                "cotangent" :   re.compile(r'\\cot\((.+)\)'),
                "arcsine" :     re.compile(r'\\arcsin\((.+)\)'),
                "arccosine" :   re.compile(r'\\arccos\((.+)\)'),
                "arctangent" :  re.compile(r'\\arctan\((.+)\)')
                },
            "fraction" :        re.compile(r'\\d?frac{(.+)}{(.+)}'),
            "parenthesis" :     re.compile(r'(?:\\left)?\((.+)(?:\\right)?\)'),
            "exponent" :        re.compile(r'.+\^.+'),
            "root" :            re.compile(r'\\sqrt(?:(.+))\{(.+)\}'),
            # Multiplication of coefficients still in progress
            "multiplication" :  re.compile(r'(?:\\times|\d+\(.+|.+\)\d+)'),
            "division" :        re.compile(r'.+\/.+'),
            "addition" :        re.compile(r'\+'),
            "substraction" :    re.compile(r'\-'),
            "variables" : {
                "alpha" :       re.compile(r'\\alpha'),
                "beta" :        re.compile(r'\\beta'),
                "Gamma" :       re.compile(r'\\Gamma'),
                "Delta" :       re.compile(r'\\Delta'),
                "Theta" :       re.compile(r'\\Theta'),
                "Pi" :          re.compile(r'\\Pi'),
                "Sigma" :       re.compile(r'\\Sigma'),
                "gamma" :       re.compile(r'\\gamma'),
                "delta" :       re.compile(r'\\delta'),
                "theta" :       re.compile(r'\\theta'),
                "pi" :          re.compile(r'\\pi'),
                "sigma" :       re.compile(r'\\sigma'),
                "alphabetic" :  re.compile(r'([A-Za-z](?:_[A-Za-z])?)'),
                "number" :      re.compile(r'(\d+)')
                }
            }
    matches = {}
    temp = expression[:]

    # Search for matches inside expression 
    for regex in regexes:
        # If item inside regexes is another dictionary
        if isinstance(regexes[regex], dict):
            for item in regexes[regex]:
                iterator = regexes[regex][item].finditer(temp)
                if bool(iterator):
                    for match in iterator:
                        groups = match.groups()

                        if groups and item in ["alphabetic", "number"]:
                            return groups[0]

                        output = [parseLaTEX(group) for group in groups]
                        
                        return Node(regex, output)

        else:
            # Look for all matches with current regex
            iterator = regexes[regex].finditer(temp)
            # Match found?
            if bool(iterator):
                for match in iterator:
                    # Does it not have groups, like addition and substraction?
                    if not match.groups():
                        fragments = list(regexes[regex].split(temp))
                        output = [parseLaTEX(fragment) for fragment in fragments]
                        
                        return Node(regex, output)
                    # Does it have matches, like fractions and functions?
                    else:
                        groups = match.groups()
                        output = [parseLaTEX(group) for group in groups]
                        
                        return Node(regex, output)


def recomposeLaTEX(expression:Node) -> str:
    if expression.value == "fraction":
        a, b = expression.children
        return "\\frac{{{}}}{{{}}}".format(a,b)
    if expression.value == "addition":
        output = ""
        for child in expression.children:
            output += child + ' + '
        output = output[:-1]
        return output


def simplify(expression, variables):

    print(expression)

    # Interpret the LaTEX and
    expression = parseLaTEX(expression)

    print(expression.getDict())


if __name__ == "__main__":
    main()

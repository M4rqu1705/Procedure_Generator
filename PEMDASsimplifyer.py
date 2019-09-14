#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
#  from time import sleep

debug_mode = False
procedure = None

def simplify(expression, variables):
    global procedure

    # Initially parse expression to work with a standarized input
    expression = str(expression).strip()            # Remove surrounding whitespace
    expression = ''.join(expression.split(' '))     # Remove internal spaces

    if procedure == None:
        procedure = [expression]


    # Identify which operations are to be done
    regexes = {
            "substitution" : re.compile(r'[A-Za-z]'),
            "parenthesis" : re.compile(r'(?:\(([^\[\]\{\}\(\)]+)\)|\[([^\[\]\{\}\(\)]+)\]|\{([^\[\]\{\}\(\)]+)\})'),
            "exponent" : re.compile(r'(\w+)(?:\^)(\w+)'),
            "product" : re.compile(r'(?<=[^\*])\*(?=[^\*])|\/'),
            "coefficient" : re.compile(r'(\d+)([A-Za-z](?:(?:\^|\*\*)([A-Za-z])?(?(3)[A-Za-z]+|\d+))?)'),
            "addition" : re.compile(r'\+|\-')

            }

    operations = {
            "substitution" : bool(regexes["substitution"].search(expression)),
            "parenthesis" : bool(regexes["parenthesis"].search(expression)),
            "exponent" : bool(regexes["exponent"].search(expression)),
            "product" : bool(regexes["product"].search(expression)),
            "coefficient": bool(regexes["coefficient"].search(expression)),
            "addition" : bool(regexes["addition"].search(expression))
            }

    #  print("Expression: {}".format(expression))
    #  print(operations)

    # Substitute variable letters for their actual values inside parens
    if operations["substitution"]:
        if debug_mode:
            print("Began substituting variables in {}".format(expression))

        i, expression_length = 0, len(expression)
        while i < expression_length-1:
            character = str(expression[i])
            # If character is valid letter and is in keys
            if regexes["substitution"].match(character) and character in variables.keys():
                value = str(variables[character])
                # Insert value with surrounding parenthesis
                expression = expression[:i] + "({})".format(value) + expression[i+1:]
                # Increase working index and final index
                expression_length += 1 + len(value); i += 2 + len(value)
            else:
                i+=1

        procedure.append(expression)

        return simplify(expression, variables)

    # Work with parenthesis first. The're the most important
    elif operations["parenthesis"]:
        if debug_mode:
            print("Began evaluating parenthesis in {}".format(expression))
        # Identify every parenthesis inside expression
        matches = regexes["parenthesis"].finditer(expression)
        #  matches = [y for x in matches for y in x]   # Flatten 2d list
        matches = list(filter(None, matches))       # Remove Nones from list

        replacements = 0
        # Substitute matches with simplified matches
        for i in range(len(matches)):
            start, end = matches[i].span()
            start-=replacements*2
            end-=replacements*2
            match = list(filter(None, [x for x in matches[i].groups()]))
            temp = str(simplify(match[0], variables))
            expression = expression[:start] + temp + expression[end:]
            replacements += 1
        procedure.append(expression)


        return simplify(expression, variables)

    # Decompose and process expression into polynomial terms
    elif operations["addition"]:
        if debug_mode:
            print("Began adding/subtracting {}".format(expression))
        # Divide expression into list of terms
        terms = regexes["addition"].sub(',', expression).split(',')
        # Get operators of matches
        operators = regexes["addition"].findall(expression)

        # Recompose expression
        output = ""
        for i in range(len(operators)):
            output += str(simplify(terms[i], variables)) + str(operators[i])
        output += str(simplify(terms[-1], variables))

        procedure.append(output)

        # Return evaluated form
        return eval(output)

    # Decompose and process expression into mutiplications and divisions, if possible
    elif operations["product"]:
        if debug_mode:
            print("Began multiplying/dividing {}".format(expression))
        # Divide expression into multiplication and division factors
        factors = regexes["product"].sub(',', expression).split(',')
        # Get operators of matches
        operators = regexes["product"].findall(expression)

        # Recompose expression
        output = ""
        for i in range(len(operators)):
            output += str(simplify(factors[i], variables)) + str(operators[i])
        output += str(simplify(factors[-1], variables))

        # Return for further simplification
        return eval(output)

    # Decompose and process terms into multiplications of coefficients and variables
    elif operations["coefficient"]:
        if debug_mode:
            print("Began finding coefficients for {}".format(expression))
        # Get operators of matches
        instances = regexes["coefficient"].findall(expression)
        instances = [y for x in matches for y in x]   # Flatten 2d list
        instances = list(filter(None, matches))       # Remove Nones from list

        simplified_instances = [str(simplify(instance, variables)) for instance in instances]

        # Recompose expression in terms of multiplications        
        output = ""
        for i in range(len(simplified_instances)-1):
            output += simplified_instances[i] + "*"
        output += simplified_instances[-1]

        return eval(output)

    # Simplify exponents
    elif operations["exponent"]:
        if debug_mode:
            print("Began exponentiating {}".format(expression))
        # Evaluate base and exponent based on regex captures
        base, exponent = regexes["exponent"].findall(expression)[0]

        # Return simplified exponent
        output = "{}**{}".format(base, exponent)

        return eval(output)

    # If no operations left to do, simply return the number
    else:
        if debug_mode:
            print(procedure)
        return expression

if __name__ == "__main__":
    temp = str(simplify("2*x^3 + 10*x^2 + 3*x - 1", {"x":1}))
    procedure.append(temp)
    procedure = " = ".join(procedure)
    print(procedure)
    procedure = procedure.replace('*', '')
    procedure = procedure.replace('(', ' \\left( ')
    procedure = procedure.replace(')', ' \\right) ')
    procedure = "\\begin{center}\n" + procedure + "\n\\end{center}"
    print(procedure)

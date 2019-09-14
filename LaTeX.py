#  http://tug.ctan.org/info/symbols/comprehensive/symbols-a4.pdf

def math(expression):
    return"$$ %s $$" % (str(expression))

def fraction(numerator, denominator):
    return "\\frac{ %s }{ %s }" % (str(numerator), str(denominator))

def abs(content):
    return "\\left| %s \\right|" % (str(content))

def sqrt(power, contents):
    return "\\sqrt[%s]{ %s }" % (str(power), str(contents))

def root(root, contents):
    return "\\sqrt[ %s ]{ %s }" % (str(root), str(contents))

def power(contents,exponent):
    return "%s^{ %s }" % (str(contents), str(exponent))

def multipleOperation(operator, *args):
    output = ""
    for c in range(len(args)-1):
        output += "%s %s " % (str(args[c]), str(operator))
    output += "%s" % (str(args[-1]))

    return output

def multiply(*args):
    return multipleOperation("\\times", *args)

def divide(*args):
    return multipleOperation("\\div", *args)

def add(*args):
    return multipleOperation("+", *args)

def substract(*args):
    return multipleOperation("-", *args)

def equals(*args):
    return multipleOperation("=", *args)

if __name__ == "__main__":
    output = add(
            fraction(1,2),
            sqrt("3","jasdfkl as"),
            power("Hello", "World"),
            4)
    output = math(output)
    print(output)


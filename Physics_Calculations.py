import LaTeX

PI = 3.1415926535897932384626433833

def formula1(length,gravity):
    procedure = [
            (LaTeX.multiply("2\\pi", LaTeX.sqrt(LaTeX.fraction("l", "g")))),
            (LaTeX.multiply("2\\pi", LaTeX.sqrt(LaTeX.fraction("%0.2fm" % length, "%0.2f^m/_{s^2}" % gravity)))),
            (LaTeX.multiply("2\\pi", LaTeX.sqrt("%0.5fs^{2}" % float(length/gravity)))),
            (LaTeX.multiply("2\\pi", "%0.5fs" % float((length/gravity) ** 0.5))),
            (LaTeX.multiply( "%0.5fs" % (2 * PI * float(length/gravity) ** 0.5)))
            ]

    return(LaTeX.math(LaTeX.equals(*procedure)))

def porcientoError(teórico, experimental, unidad):
    procedure = [
            LaTeX.multiply(LaTeX.abs(LaTeX.fraction(LaTeX.substract("%s%s" % (teórico, unidad), "%s$s" % (experimental, unidad)), "%s%s" % (teórico, unidad) ) ),"100%"),
            LaTeX.multiply(LaTeX.abs(LaTeX.fraction("%s%s" % ((teórico - experimental),unidad), "%s%s" % (teórico, unidad) ) ),"100%"),
            LaTeX.multiply(LaTeX.abs( "%s%s" (((teórico - experimental)/teórico), unidad) ,"100%")),
            ("%s" % (abs(((teórico - experimental) / teórico) * 100)))
            
            ]

    return(LaTeX.math(LaTeX.equals(*procedure)))



formulas = [formula1, porcientoError]

data = [
        [
            [1.0, 9.8],
            [0.8, 9.8],
            [0.6, 9.8],
            [0.4, 9.8],
            ],
        [
            [2.00709,2.00, "s"],
            [1.79520,1.79, "s"],
            [1.55469,1.58, "s"],
            [1.26940,1.27, "s"]

            ]

        ]


for c in range(len(formulas)):
    for values in data[c]:
        print(formulas[c](*values))

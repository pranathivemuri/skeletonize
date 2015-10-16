import numpy as np

from pyeda.inter import exprvar
from Thin3dtemplates import firstSubIter, secondSubIter, thirdSubIter, fourthSubIter, fifthSubIter, sixthSubIter, seventhSubIter, eighthSubIter, ninthSubIter, tenthSubIter, eleventhSubIter, twelvethSubIter

"""
   To avoid pyeda overhead and evaluating the
   expressions each time,get a boolean
   expression in advance and evaluate it
"""

a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z = map(exprvar, 'abcdefghijklmnopqrstuvwxyz')
origin = exprvar('origin')
validateMatrix = np.array([[[a, b, c], [d, e, f], [g, h, i]], [[j, k, l], [m, origin, n], [o, p, q]], [[r, s, t], [u, v, w], [x, y, z]]])
usDeletiondirection, str1 = firstSubIter(validateMatrix)
neDeletiondirection, str2 = secondSubIter(validateMatrix)
wdDeletiondirection, str3 = thirdSubIter(validateMatrix)
esDeletiondirection, str4 = fourthSubIter(validateMatrix)
uwDeletiondirection, str5 = fifthSubIter(validateMatrix)
ndDeletiondirection, str6 = sixthSubIter(validateMatrix)
swDeletiondirection, str7 = seventhSubIter(validateMatrix)
unDeletiondirection, str8 = eighthSubIter(validateMatrix)
edDeletiondirection, str9 = ninthSubIter(validateMatrix)
nwDeletiondirection, str10 = tenthSubIter(validateMatrix)
ueDeletiondirection, str11 = eleventhSubIter(validateMatrix)
sdDeletiondirection, str12 = twelvethSubIter(validateMatrix)


def emitCodeFromEqtn(eqtn, eqName):
    simplified = eqtn.simplify()
    uniqueIDtoSymbol = {symbol.uniqid: symbol for symbol in eqtn.inputs}

    # args = ", ".join(["uint8 %s" % symbol.name for symbol in eqtn.inputs])

    # Emit the c function header
    # print("uint8 %s(%s) {" % (eqName, args))
    statement = recursiveEmitter(simplified.to_ast(), uniqueIDtoSymbol)
    # print("\treturn %s;" % statement)
    # print("}")
    return statement


def recursiveEmitter(ast, symbolTable):
    # Input ast format is (operator, expr, expr, expr, expr. . .)
    op = ast[0]
    exprs = ast[1:]

    if op == "and":
        subExprs = [recursiveEmitter(exp, symbolTable) for exp in exprs]
        return "(" + " & ".join(subExprs) + ")"

    elif op == "or":
        subExprs = [recursiveEmitter(exp, symbolTable) for exp in exprs]
        return "(" + " | ".join(subExprs) + ")"

    elif op == "not":
        subExprs = [recursiveEmitter(exp, symbolTable) for exp in exprs]
        return "(" + " not ".join(subExprs) + ")"

    elif op == "lit":
        # Lit can have only one operator
        symbol = exprs[0]

        if symbol < 0:
            symbol *= -1
            return "(not %s)" % symbolTable[symbol].name
        else:
            return symbolTable[symbol].name
    raise RuntimeError("No way to resolve operation named '%s' with %i arguments" % (op, len(exprs)))

us = emitCodeFromEqtn(usDeletiondirection, usDeletiondirection)
ne = emitCodeFromEqtn(neDeletiondirection, neDeletiondirection)
wd = emitCodeFromEqtn(wdDeletiondirection, wdDeletiondirection)
es = emitCodeFromEqtn(esDeletiondirection, esDeletiondirection)
uw = emitCodeFromEqtn(uwDeletiondirection, uwDeletiondirection)
nd = emitCodeFromEqtn(ndDeletiondirection, ndDeletiondirection)
sw = emitCodeFromEqtn(swDeletiondirection, swDeletiondirection)
un = emitCodeFromEqtn(unDeletiondirection, unDeletiondirection)
ed = emitCodeFromEqtn(edDeletiondirection, edDeletiondirection)
nw = emitCodeFromEqtn(nwDeletiondirection, nwDeletiondirection)
ue = emitCodeFromEqtn(ueDeletiondirection, ueDeletiondirection)
sd = emitCodeFromEqtn(sdDeletiondirection, sdDeletiondirection)

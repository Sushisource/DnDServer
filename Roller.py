import random
import numpy as np
import re
__author__ = 'Spencer Judge'

def subDice(diestr):
    (numdice, sides) = diestr.group(0).split('d')
    numdice = int(numdice)
    sides = int(sides)
    rolls = np.arange(numdice)
    for i in range(numdice):
        rolls[i]=random.randint(1,sides)
    print rolls
    summ = np.sum(rolls)
    print "Total: ", summ
    print "StdD: ", np.std(rolls)
    print "Var: ", np.var(rolls)
    return str(summ)

def rollDice(dieReq):
    print dieReq
    result = "err"
    try:
        result = eval(re.sub('(\d+d\d+)', subDice, dieReq))
    except Exception:
        pass
    return result

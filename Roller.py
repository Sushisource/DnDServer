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
    summ = np.sum(rolls)
    return str(summ)

def rollDice(dieReq):
    result = "err"
    try:
        result = eval(re.sub('(\d+d\d+)', subDice, dieReq))
    except Exception:
        pass
    return "%s for %s" % (dieReq, result)

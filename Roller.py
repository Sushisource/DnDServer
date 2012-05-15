import random
import re
__author__ = 'Spencer Judge'

def doRolls(numdice, sides):
    numdice = int(numdice)
    sides = int(sides)
    rolls = []
    for i in range(numdice):
        rolls.append(random.randint(1,sides))
    return rolls

def rollDice(dieReq):
    result = "err"
    additional = [""]

    def diceSub(diestr):
        (numdice, sides) = diestr.group(0).split('d')
        rolls = doRolls(numdice, sides)
        summ = sum(rolls)
        if 3<int(numdice)<200:
            rolls = ','.join(map(str, rolls)) #Make rolls into comma list
            additional[0] += "<img src='dicehisto?list=%s&width=10&" \
            "height=50&limits=0,%s&upper=%s'>" \
        % (rolls,sides,sides)
        return str(summ)
    try:
        result = str(eval(re.sub('(\d+d\d+)', diceSub, dieReq)))
    except Exception as e:
        print e
    return "<h4>" + result + "</h4>" + additional[0]

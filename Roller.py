import uuid
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
    result = False
    graphs = list()
    single = {'draw': False}

    def diceSub(diestr):
        (numdice, sides) = diestr.group(0).split('d')
        rolls = doRolls(numdice, sides)
        aggrolls = [0 for x in range(1,int(sides) + 1)]
        for roll in rolls:
            aggrolls[roll-1] += 1
        summ = sum(rolls)
        if 3<int(numdice)<200:
            graphs.append({'max': sides,
                           'id': uuid.uuid4(),
                           'rolls': aggrolls})
        if int(numdice) == 1:
            single['draw'] = True
            single['sides'] = sides
        return str(summ)
    try:
        result = int(eval(re.sub('(\d+d\d+)', diceSub, dieReq)))
    except Exception as e:
        print e
    return result, graphs, single

import re


def linStringToPBN(linstring):
    linList = linstring.split('||')

    # Extract Players SWNE
    players=linList[0].split('|')[1].split(',')
    print(players)

    # Extract hands
    deal = linList[1].split('|')[1].split(',')
    hands = [list(map(lambda x: x[::-1],re.split('S|H|D|C',d))) for d in deal]
    [dealer,_,_,_]=[x.pop(0) for x in hands]
    if len(hands[3])==0:
        rank='AKQJT98765432'   
        hands[3]=4*['']
        for i in range(4):
            for j in range(13):
                if all([rank[j] not in hands[k][i] for k in range(3)]):
                    hands[3][i]=hands[3][i]+rank[j]
    print(hands)

    # Extract auction
    auction = linList[2].split('|')[1::2]
    boardNumber = auction[0].split(' ')[1]
    vulnerability = auction[1]
    bids = auction[2::]
    print(bids)

    # Extract play
    play = linList[3::]
    play = [p.split('|')[1::2] for p in play]
    if play[-1] == []:
        claim = 0
    else:
        claim = play[-1][-1]
    print(play)

f=open('test.lin','r')
linStringToPBN(f.read())

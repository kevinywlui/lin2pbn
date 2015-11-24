import re

def linStringToPBNString(linstring):
    linList = linstring.split('||')

    # Extract Players SWNE
    [south,west,north,east] = linList[0].split('|')[1].split(',')

    # Extract hands
    dd = linList[1].split('|')[1].split(',')
    hands = [list(map(lambda x: x[::-1],re.split('S|H|D|C',d))) for d in dd]
    [dealer,_,_,_]=[x.pop(0) for x in hands]
    if len(hands[3])==0:
        rank='AKQJT98765432'   
        hands[3]=4*['']
        for i in range(4):
            for j in range(13):
                if all([rank[j] not in hands[k][i] for k in range(3)]):
                    hands[3][i]=hands[3][i]+rank[j]
    deal = ['S','W','N','E'][int(dealer)-1]+":"+" ".join([".".join(x) for x in hands])


    # Extract auction
    auction = linList[2].split('|')[1::2]
    board = auction[0].split(' ')[1]
    if auction[1]=='o':
        vulnerable='None'
    elif auction[1]=='e':
        vulnerable='ES'
    elif auction[1]=='n':
        vulnerable='NS'
    else:
        vulnerable='All'

    bids = auction[2::]

    # Extract play
    play = linList[3::]
    play = [p.split('|')[1::2] for p in play]
    if play[-1] == []:
        claim = 0
    else:
        claim = play[-1][-1]
    
    PBNString = ''
    PBNString = PBNString + '[Event \"\"]\n'
    PBNString = PBNString + '[Site \"\"]\n'
    PBNString = PBNString + '[Date \"\"]\n'
    PBNString = PBNString + '[Board \"{}\"]\n'.format(board)
    PBNString = PBNString + '[West \"{}\"]\n'.format(west)
    PBNString = PBNString + '[North \"{}\"]\n'.format(north)
    PBNString = PBNString + '[East \"{}\"]\n'.format(east)
    PBNString = PBNString + '[South \"{}\"]\n'.format(south)
    PBNString = PBNString + '[Dealer \"{}\"]\n'.format(dealer)
    PBNString = PBNString + '[Vulnerable \"{}\"]\n'.format(vulnerable)
    PBNString = PBNString + '[Deal \"{}\"]\n'.format(deal)
    PBNString = PBNString + '[Scoring \"\"]\n'
    PBNString = PBNString + '[Declarer \"{}\"]\n'#.format(declarer)
    PBNString = PBNString + '[Contract \"{}\"]\n'#.format(contract)
    PBNString = PBNString + '[Result \"\"]\n'
    PBNString = PBNString + '[Auction \"{}\"]\n{}\n'#.format(dealer,auction)
    PBNString = PBNString + '[Play \"{}\"]\n{}\n'#.format(play[0],play[1])
    print(PBNString)

f=open('test.lin','r')
linStringToPBNString(f.read())

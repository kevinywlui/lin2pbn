import re
import sys

def numToDirection(n):
    return ['S', 'W', 'N', 'E'][n%4]
def linStringToPBNString(linstring):
    linList = linstring.split('||')

    # Extract Players SWNE
    [south, west, north, east] = linList[0].split('|')[1].split(',')

    # Extract hands
    dd = linList[1].split('|')[1].split(',')
    hands = [list(map(lambda x: x[::-1], re.split('S|H|D|C', d))) for d in dd]
    [dealerIndex, _, _, _] = [x.pop(0) for x in hands]
    dealerIndex = int(dealerIndex)
    dealer = numToDirection(dealerIndex -1)
    if len(hands[3]) == 0:
        rank = 'AKQJT98765432'
        hands[3] = 4 * ['']
        for i in range(4):
            for j in range(13):
                if all([rank[j] not in hands[k][i] for k in range(3)]):
                    hands[3][i] = hands[3][i] + rank[j]
    deal = dealer + ":" + " ".join([".".join(x) for x in hands])

    # Extract auction
    aa = linList[2].split('|')[1::2]
    board = aa[0].split(' ')[1]
    if aa[1] == 'o':
        vulnerable = 'None'
    elif aa[1] == 'e':
        vulnerable = 'ES'
    elif aa[1] == 'n':
        vulnerable = 'NS'
    else:
        vulnerable = 'All'

    bids = aa[2::]
    bids = ['Pass' if x == 'p' else x for x in bids]
    auction = ''
    for i in range(len(bids) // 4):
        t = ['', '', '', '']
        for j in range(4):
            if 4 * i + j < len(bids):
                t[j] = bids[4 * i + j]
        auction = auction + '{0[0]:<7}{0[1]:<7}{0[2]:<7}{0[3]:<7}\n'.format(t)

    stake = ''
    for x in bids[::-1]:
        if x == 'XX':
            stake = 'XX'
            continue
        if x == 'X' and stake != 'XX':
            stake = 'X'
            continue
        if x[1] in ['S', 'H', 'C', 'D', 'N']:
            contract = x + stake
            strain = x[1:]
            break

    for x in bids:
        if x[1:] == strain:
            declarerIndex = bids.index(x)
            break
    declarer = ['S', 'W', 'N', 'E'][(declarerIndex+dealerIndex - 1) % 4]

    # Extract play
    pp = linList[3::]
    pp = [p.split('|')[1::2] for p in pp]
    if pp[-1] == []:
        claim = 0
    else:
        claim = pp[-1][-1] 
    
    play = ''
    for x in pp:
        if x == []:
            continue
        t = ['', '', '', '']
        for j in range(len(x)):
            t[j] = x[j]
        play = play + '{0[0]:<4}{0[1]:<4}{0[2]:<4}{0[3]:<4}\n'.format(t)
    play = [numToDirection(declarerIndex+1),play]

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
    PBNString = PBNString + '[Declarer \"{}\"]\n'.format(declarer)
    PBNString = PBNString + '[Contract \"{}\"]\n'.format(contract)
    PBNString = PBNString + '[Result \"\"]\n'
    PBNString = PBNString + '[Auction \"{}\"]\n{}'.format(dealer, auction)
    PBNString = PBNString + '[Play \"{0[0]}\"]\n{0[1]}'.format(play)
    return PBNString

linString=input()
print(linStringToPBNString(linString))

from random import shuffle
import sys


class SpadesGame:
    def __init__(self):
        self.num_players = 4
        self.cards_in_hand = 13
        self.hands = self.deal_hands()

    def deal_hands(self):
        deck = range(52)
        for i in range(7): shuffle( deck )

        hands = [ deck[player*self.cards_in_hand:(player+1)*self.cards_in_hand] \
                for player in range(self.num_players)]

        return hands


#if len(sys.argv)==1:
#    exit('Give the order of magnitude of the number of runs as an argument')
try:
    runs = 10**int(sys.argv[1])
except:
    sys.exit('Give the order of magnitude of the number of runs as an argument')
    

#except 

club_wins = [0]*13
club_losses = [0]*13

for iters in range(runs):

    # Deal out the cards
    game = SpadesGame()

    # Get the lowest card from each player's hand
    low_cards = [min(hand) for hand in game.hands]

    #Keep only clubs. (For our purposes clubs are integers 0--12.)
    low_clubs = filter(lambda card: card<13, low_cards)

    #The highest club is the winner
    winner = max(low_clubs)
    #The rest are losers
    low_clubs.remove(winner)

    #Store the values of winner and losers
    club_wins[winner] += 1
    for card in low_clubs:
        club_losses[ card ] += 1

    #iters += 1

print "We ran {} hands. Low club stats are:".format(runs)
card_names = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
for i in range(13):
    print '{} won {} times and lost {} times'.format(card_names[i],club_wins[i],club_losses[i])

    if club_wins[i] != 0 or club_losses[i] != 0:
        print "Percent won: {0:.3f}".format(100.0*float(club_wins[i])/float(club_wins[i]+club_losses[i])) 


import cards
import sys
import argparse


class SpadesGame:
	def __init__(self):
		self.num_players = 4
		self.cards_per_hand = 13

		deck = cards.Deck()
		self.hands = deck.deal(self.num_players,self.cards_per_hand)


parser = argparse.ArgumentParser(description='Runs a bunch of spades hands and keeps statistics on wins/losses of low clubs.')

parser.add_argument('n', type=int, help='Order of magnitude of runs. Will run 10**n hands.')
parser.add_argument('--name', type=str, default='results.csv', \
					help='Write to the specified file (if -f is set). If no filename is specified, writes to "results.csv".')

args = parser.parse_args(sys.argv[1:])

runs = 10**args.n
filename = args.name
#write = args.f

##########
# Initialize the arrays to hold wins and losses for each card
club_wins = [0]*13
club_losses = [0]*13

for iters in range(runs):

	# Deal out the cards
	game = SpadesGame()

	# Get the lowest card from each player's hand
	low_cards = [min(hand) for hand in game.hands]

	#Keep only clubs. (For our purposes clubs are integers 0--12.)
	low_clubs = [card for card in low_cards if card<13]

	#The highest club is the winner
	winner = max(low_clubs)
	#The rest are losers
	low_clubs.remove(winner)

	#Store the values of winner and losers
	club_wins[winner] += 1
	for card in low_clubs:
		club_losses[ card ] += 1

# Format the results
column_titles = ['low club','wins','losses','win v loss %\n']
card_names = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
win_pct = [0]*13
for i in range(13):
	if club_wins[i] != 0 or club_losses[i] != 0:
		win_pct[i] = 100.0*float(club_wins[i])/float(club_wins[i]+club_losses[i])
	else:
		win_pct[i] = float('nan')
data_lines = list(zip(card_names,club_wins,club_losses,win_pct))

# Write results to a file
if write:
	with open(filename,'a') as f:
		f.write('10^{},,,\n'.format(args.n))
		f.write(','.join(column_titles))
		for line in data_lines:
			f.write('{0},{1},{2},{3:.3f}\n'.format(*list(line)))


# Print results to screen
print("We ran {} hands. Low club stats are:".format(runs))

for line in data_lines:
	print('{3:.2f}%\t{0} won {1} times and lost {2} times.'.format(*list(line)))
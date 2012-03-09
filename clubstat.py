import cards
from sys import argv
import argparse
import csv


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

args = parser.parse_args(argv[1:])

runs = 10**args.n
total_runs = runs
filename = args.name
#write = args.f

##########
# Initialize the arrays to hold wins and losses for each card
club_wins = [0]*13
club_losses = [0]*13

##########
# Before we run any games, we see if games have been run before. If so, we read in that data. No use letting our old data go to waste.
try:
	print('Reading old data')
	f = open(filename,'r')
except:
	print('Tried reading old data but it failed')
else:
		reader = csv.reader(f)
		line_list = list(reader)
		##########
		# First Row: Get runs 
		row = line_list[0]
		runs_old = int(row[0])
		total_runs += runs_old

		##########
		# Second line is card titles. Skip to third line.
		next_index = 2
		row = line_list[next_index]

		##########
		# Wins
		# This row has one title space then all the 'club_wins' data.
		for i in range(13):
			club_wins[i] += int(row[i+1])

		##########
		# Losses
		# This row has one title space then all the 'club_losses' data.
		next_index += 1
		row = line_list[next_index]
		for i in range(13):
			club_losses[i] += int(row[i+1])
		
		f.close()


line_out = '{},Hands'.format(total_runs) \
			+'\nlow club,2,3,4,5,6,7,8,9,10,J,Q,K,A'
print('Starting games...')
every_ten = 10
for this_game in range(runs):
	if (this_game+1) % every_ten == 0:
		print('Played {} games'.format(this_game+1))
		if every_ten < runs/10:
			every_ten *= 10

	# Deal out the cards
	game = SpadesGame()

	# Get the lowest card from each player's hand
	low_cards = [min(hand) for hand in game.hands]

	#Keep only clubs.
	low_clubs = [card for card in low_cards if card.suit==0]

	#The highest club is the winner
	winner = max(low_clubs)
	#The rest are losers
	low_clubs.remove(winner)

	#Store the values of winner and losers
	club_wins[winner] += 1
	for card in low_clubs:
		club_losses[ card ] += 1


win_pct = [0]*13
for i in range(13):
	if club_wins[i] != 0 or club_losses[i] != 0:
		win_pct[i] = 100.0*float(club_wins[i])/float(club_wins[i]+club_losses[i])
	else:
		win_pct[i] = float('nan')

line_out += '\nwins,'+','.join(club_wins)+'\nlosses,'+','.join(club_losses) \
			+'\nwin %'+','.join(win_pct)

# Write results to a file
print('Writing results to file')
with open(filename,'w') as f:
	f.write(line_out)

print('Results written to file '+filename)

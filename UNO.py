import os # to clear terminal after every turn
from random import shuffle # to shuffle the deck
import easygui
import time 
def create_deck():
    '''
        This function generates the deck and shuffles it.
         : return: the deck as a list of cards (dictionaries)
    '''
    colors = ['Red', 'Yellow', 'Green', 'Blue'] 
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'Skip', 'Draw Two', 'Reverse']
    deck = []
    for color in colors:
        for value in values:
            if value == '0':
                #there is only one 0 for each color
                deck.append({'color': color, 'value': value})
            else:
                #there are 2 of each card in each color
                for i in range(2):
                    deck.append({'color': color, 'value': value})
    for i in range(2):
        deck.append({'color': '', 'value': 'Wild'})
        deck.append({'color': '', 'value': 'Wild Draw'})
    
    shuffle(deck)
    return deck

def draw_card(deck):
    '''
        This function draws a card from the deck and shows which card is taken from the deck
         : param deck: list of remaining cards in the deck
         : type deck: list (of cards which are dictionaries)
         : return: card (dictionary with 2 keys: 'color' and 'value')
    '''
    if deck: # to check if there are any cards left in the deck
        return deck.pop(0)
    else:
        print("The deck is empty! No card to draw.")

def valid_move(card, top_card):
    '''
        Checks if move player intends to play is valid or not
         : param card: the card player chooses to play
         : type card: dictionary
         : param top_card: the previous card played (top card in the discard pile)
         : type top_card: dictionary
         : return: boolean (True or False)
    '''
    if 'Wild' in str(card['value']) or card['color'] == top_card['color'] or card['value'] == top_card['value']:
        return True
    return False

def play_turn(player_hand, deck, discard_pile):
    '''
        This function manages action for each turn, if necessary drawing cards from the deck
         : param player_hand: list of player's cards (dictionaries)
         : param deck: list of left cards (dictionaries)
         : param discard_pile: list of played cards (dictionaries)
         : return: None
    '''

    global turn, players_cards, direction
    move = '-'

    while move == '-':
        print("The top card is:", end= ' ')
        print_card(discard_pile[0])
        print(f"Player {turn}, your cards are:")
        for i in range(len(player_hand)):
            if player_hand[i] != None:
                print(i + 1, end= '. ')
                print_card(player_hand[i])

        move = input(f"Input your card's number or if you don't have suitable card write -: ")
        
        try:
            move = int(move)
            if 0 < move <= len(player_hand) and valid_move(player_hand[move - 1], discard_pile[0]):
                discard_pile.insert(0, player_hand.pop(move - 1))
                next_turn = (turn + direction - 1) % len(players_cards) + 1 # for draw or skip cards, we need to know the next player

                if discard_pile[0]['value'] == 'Reverse':
                    direction *= -1         # Reverse direction

                elif discard_pile[0]['value'] == 'Skip':
                    turn = (turn + direction - 1) % len(players_cards) + 1 # skip the next player

                elif discard_pile[0]['value'] == "Draw Two":
                    for i in range(2):
                        players_cards[f"Player{next_turn}"].append(draw_card(deck))

                elif "Wild" in str(discard_pile[0]['value']):
                    while discard_pile[0]['color'] == "":
                        color = easygui.buttonbox("Choose a color:","Wild Card Color", choices=["Red", "Yellow", "Green", "Blue"])
                        discard_pile[0]['color'] = color
                        
                        # color = input("Choose a color (r, y, g, b): ").strip().casefold()

                        # if color in "rygb":
                        #     if color == 'r': discard_pile[0]['color'] = "Red"
                        #     elif color == 'y': discard_pile[0]['color'] = "Yellow"
                        #     elif color == 'g': discard_pile[0]['color'] = "Green"
                        #     else: discard_pile[0]['color'] = "Blue"
                        # else:
                        #     print("Invalid color. Please choose again.")

                    if discard_pile[0]['value'] == 'Wild Draw':
                        for i in range(4):
                            players_cards[f"Player{next_turn}"].append(draw_card(deck))

                break  # Exit loop after a valid move

            else:
                print("\nInvalid move. Try again or draw a card with '-'.\n")
        
        except ValueError:
            if move == '-':
                if deck:
                    player_hand.append(draw_card(deck)) # Draw a card
                else:    #if there are not any card in the deck this player
                    easygui.msgbox("There's no card left, your turn skips :(",title=':(')
                    time.sleep(2)
                    break
                    
            else:
                print("Invalid input. Enter a card number or '-' to draw a card.")
        
        move = '-'

def check_winner(player_hand):
    '''
        Checks if there is any player with no cards left to determine the winner
        : param player_hand: cards of the player to be checked
        : type player_hand: list of cards (dictionaries)
        : return: boolean (True or False)
    '''
    return len(player_hand) == 0

def print_card(card):
    '''
        Prints the given card as a string and in its respective color.
         : param card: dictionary
         : return: None (this is not a function, but a procedure)
    '''
    # Define ANSI color codes for terminal output
    color_codes = { 'Red': '\033[91m','Yellow': '\033[93m', 'Green': '\033[92m', 'Blue': '\033[94m', '': '\033[95m'}
    reset_code = '\033[0m'    # to reset color

    color = card['color']
    print(f"{color_codes[color]}{color + ' ' + str(card['value'])}{reset_code}")

easygui.msgbox('''Game Rules for UNO:
1. Each player must play a card that matches the previous card in either color or value.
2. If a player cannot make a move, they must draw cards from the deck until they can play a matching card.
3. There is one '0' card per color and two of each number (1-9) per color. Special cards include:
    - Reverse: Reverses the direction of play.
    - Draw Two: The next player must draw two cards from the deck.
    - Skip: Skips the next player's turn.
    — Wild: Changes the color of play.
    — Wild Draw: The next player must draw 4 cards, also changes color
4. When a player has only one card left, they must shout "UNO!"
5. The first player to get rid of all their cards wins.
''',title="UNO")

number_of_players = int(input("Enter the number of players: "))
while not 2 <= number_of_players <= 10:
    print('\033[91mThere must be 2 to 12 players.\033[0m')
    number_of_players = int(input("Enter the number of players: "))

deck = create_deck()
discard_pile = []
players_cards = {}
direction = 1
turn = 0

# we randomly give 5 cards to each player from shuffled deck
for i in range(number_of_players):
    turn = turn + 1
    hand = []
    for j in range(5):
        hand.append(draw_card(deck))
    players_cards["Player" + str(turn)] = hand

# in order not to have the first card as a special card we create a loop
for i in range(len(deck)):
    if isinstance(deck[i]['value'], int):
        top_card = deck.pop(i)
        break
discard_pile.insert(0, top_card)

# we create a loop so game continues until 1 person finishes cards
while True:
    turn = (turn + direction - 1) % number_of_players + 1
    play_turn(players_cards["Player" + str(turn)], deck, discard_pile)
    
    os.system('cls' if os.name == 'nt' else 'clear') # clear terminal before every player's turn to prevent cheating
    
    if check_winner(players_cards["Player" + str(turn)]):
        easygui.msgbox(f"\U0001F389 Congratulations! The winner is Player{turn}! \U0001F389", 
                       title="\U0001F3C6 WINNER \U0001F3C6")
        break

    elif len(players_cards["Player" + str(turn)]) == 1:
        easygui.msgbox(f"Player {turn} said UNO!",title="UNO")

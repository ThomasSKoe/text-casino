import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def get_value(self):
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 11  # We'll handle ace logic in the hand calculation
        else:
            return int(self.rank)

class Deck:
    def __init__(self):
        self.cards = []
        self.reset_deck()
    
    def reset_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.cards)
    
    def deal_card(self):
        if len(self.cards) < 10:  # Reshuffle if deck is running low
            print("Reshuffling deck...")
            self.reset_deck()
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        self.cards.append(card)
    
    def get_value(self):
        value = 0
        aces = 0
        
        for card in self.cards:
            if card.rank == 'Ace':
                aces += 1
                value += 11
            else:
                value += card.get_value()
        
        # Adjust for aces
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        return value
    
    def is_blackjack(self):
        return len(self.cards) == 2 and self.get_value() == 21
    
    def is_bust(self):
        return self.get_value() > 21
    
    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.game_over = False
    
    def start_new_game(self):
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.game_over = False
        
        # Deal initial cards
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
    
    def display_hands(self, hide_dealer_card=True):
        print("\n" + "="*50)
        print("CURRENT HANDS:")
        print("="*50)
        
        # Player hand
        print(f"Player Hand: {self.player_hand}")
        print(f"Player Value: {self.player_hand.get_value()}")
        
        # Dealer hand
        if hide_dealer_card and not self.game_over:
            print(f"Dealer Hand: {self.dealer_hand.cards[0]}, [Hidden Card]")
            print(f"Dealer Showing: {self.dealer_hand.cards[0].get_value()}")
        else:
            print(f"Dealer Hand: {self.dealer_hand}")
            print(f"Dealer Value: {self.dealer_hand.get_value()}")
        
        print("="*50)
    
    def player_turn(self):
        while not self.game_over:
            self.display_hands()
            
            # Check for blackjack
            if self.player_hand.is_blackjack():
                print("🎉 BLACKJACK! You got 21!")
                self.game_over = True
                return
            
            # Check for bust
            if self.player_hand.is_bust():
                print("💥 BUST! You went over 21!")
                self.game_over = True
                return
            
            # Get player action
            while True:
                action = input("Do you want to (h)it or (s)tand? ").lower().strip()
                if action in ['h', 'hit']:
                    self.player_hand.add_card(self.deck.deal_card())
                    print(f"You drew: {self.player_hand.cards[-1]}")
                    break
                elif action in ['s', 'stand']:
                    print("You chose to stand.")
                    self.game_over = True
                    return
                else:
                    print("Invalid input. Please enter 'h' for hit or 's' for stand.")
    
    def dealer_turn(self):
        print("\nDealer's turn...")
        self.display_hands(hide_dealer_card=False)
        
        while self.dealer_hand.get_value() < 17:
            card = self.deck.deal_card()
            self.dealer_hand.add_card(card)
            print(f"Dealer draws: {card}")
            print(f"Dealer value: {self.dealer_hand.get_value()}")
        
        if self.dealer_hand.is_bust():
            print("💥 Dealer busts!")
        else:
            print(f"Dealer stands with {self.dealer_hand.get_value()}")
    
    def determine_winner(self):
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        print("\n" + "="*50)
        print("FINAL RESULTS:")
        print("="*50)
        
        self.display_hands(hide_dealer_card=False)
        
        # Check for player bust
        if self.player_hand.is_bust():
            print("🔴 You busted! Dealer wins!")
            return
        
        # Check for dealer bust
        if self.dealer_hand.is_bust():
            print("🟢 Dealer busted! You win!")
            return
        
        # Check for blackjacks
        if self.player_hand.is_blackjack() and not self.dealer_hand.is_blackjack():
            print("🎉 BLACKJACK! You win!")
            return
        elif self.dealer_hand.is_blackjack() and not self.player_hand.is_blackjack():
            print("🔴 Dealer has blackjack! Dealer wins!")
            return
        elif self.player_hand.is_blackjack() and self.dealer_hand.is_blackjack():
            print("🟡 Both have blackjack! It's a push!")
            return
        
        # Compare values
        if player_value > dealer_value:
            print("🟢 You win!")
        elif dealer_value > player_value:
            print("🔴 Dealer wins!")
        else:
            print("🟡 It's a push (tie)!")
    
    def play(self):
        print("🎰 Welcome to Blackjack! 🎰")
        print("Goal: Get as close to 21 as possible without going over!")
        print("Face cards are worth 10, Aces are 11 or 1 (whichever is better)")
        
        while True:
            print("\n" + "🃏" * 20)
            print("Starting new game...")
            
            self.start_new_game()
            self.player_turn()
            
            if not self.player_hand.is_bust():
                self.dealer_turn()
            
            self.determine_winner()
            
            # Ask to play again
            while True:
                play_again = input("\nDo you want to play again? (y/n): ").lower().strip()
                if play_again in ['y', 'yes']:
                    break
                elif play_again in ['n', 'no']:
                    print("Thanks for playing Blackjack! 🎰")
                    return
                else:
                    print("Please enter 'y' for yes or 'n' for no.")

# Run the game
if __name__ == "__main__":
    game = BlackjackGame()
    game.play()
import random
import time
import os
import sys

##Overarching casino class
class Casino:

    def __init__(self, startingMoney):
        self.balance = startingMoney

    def mainMenu(self):

        clearScreen()
        print("@~~~~~~~~~~~~~~~~~~~~~~@\nWelcome to the Casino")
        print(f"Balance: ${self.balance}\n@~~~~~~~~~~~~~~~~~~~~~~@")
        print("\nSelect an option:\n" \
        "1 : Blackjack\n" \
        "2 : Slots\n" \
        "3 : Roullette\n" \
        "4 : Check balance / stats\n" \
        "5 : Cash out \n")

        while True : 
            userInput = input("> ")

            if(userInput == "1") :
                game = Blackjack(self)
                game.welcome()
            elif(userInput == "2") :
                print("Not implemented yet")
            elif(userInput == "3") :
                print("Not implemented yet")
            elif(userInput == "4") :
                print("Not implemented yet")
                print(f"TOTAL BALANCE :{self.balance}")
            elif(userInput =="5") :
                print(f"TOTAL BALANCE :{self.balance}")
                return
            else :
                print("Invalid selection (1 - 5)")
    
    def removeBalance(self, amount) :
        self.balance = self.balance - amount
    
    def addBalance(self, amount) :
        self.balance = self.balance + amount


class Card:
        
    def __init__(self, suit, rank) :
        self.suit = suit
        self.rank = rank
        self.id = id
    
    def __str__(self) :
        return f"{self.suit} | {self.rank}"
    
    def getRank(self) :
        return self.rank

    def getSuit(self) :
        return self.suit

class Deck :
    Suits = ["♣", "♦", "♥", "♠"]
    Ranks = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

    def __init__(self):
        self.cards = []

        ##creates a list of cards with all suits and ranks
        for suit in range(4) :
            for rank in range(13) :
                self.cards.append(Card(self.Suits[suit],self.Ranks[rank]))

    #returns a random card
    def drawCard(self) :
        output = self.cards[random.randint(0, len(self.cards)-1)]
        self.cards.remove(output)
        return output
    
    #shuffles the deck
    def shuffle(self) :
        random.shuffle(self.cards)
    
    #resets the deck
    def reset(self) :
        newDeck = []
        for suit in range(4) :
            for rank in range(13) :
                newDeck.append(Card(self.Suits[suit],self.Ranks[rank]))
        self.cards = newDeck
    
    #prints all cards in the deck - for testing purposes
    def printDeck(self) :
        for card in self.cards :
            print(card)


class Blackjack :
    bet = 1

    def __init__(self, casinoObject) :
        self.casino = casinoObject
        self.balance = casinoObject.balance

    def welcome(self) :

        clearScreen()
        print(">>====================<<\nWelcome to Blackjack")
        print(f"Balance: \033[1m${self.balance}\n\033[0mCurrent bet: \033[1m${self.bet}")
        print(f"\033[0m>>====================<<\nSelect an option:\n\n" \
        "1 : Place bet\n" \
        "2 : Draw hand\n" \
        "3 : Return to main menu\n")
        
        while True :
            userInput = input("> ")
            if(userInput == "1") :
                self.placeBet()
                return
            elif(userInput == "2") :
                self.playHand()
                return                
            elif(userInput == "3") :
                self.casino.mainMenu()
                return
            else :
                print("Not a valid selection (1 - 3)")

    def placeBet(self) :
        while True :
            i = input(f"Bet amount ($1 - ${self.balance}) > ")
            ##makes it an int
            val = int(float(i))
            if(val >= 1 and val <= self.balance) :
                self.bet = val
                self.welcome()
            else :
                print(f"Please enter a valid number between 1 and {self.balance}")
                    
    def playHand(self) :

        deck = Deck()

        dealerScore = 0
        playerScore = 0

        dealerHand = [deck.drawCard()]
        playerHand = [deck.drawCard(), deck.drawCard(),]

        dealerScore = self.calculateScore(dealerHand)
        playerScore = self.calculateScore(playerHand)

        clearScreen()
        print("🃏>====================<🃏\n\033[1mBlackjack \033[0m")
        print(f"Balance: \033[1m${self.balance}\n\033[0mCurrent bet: \033[1m${self.bet}\033[0m")
        print(f">>====================<<")
        
        
        print(f"Dealer hand: (Score: {dealerScore})")
        self.printHand(dealerHand)
        print(f"Your hand: (Score: {playerScore})")
        self.printHand(playerHand)
        

        while True :
            i = input("Would you like to (h)it or (s)tand? > ")
            
            if(i == "h" or i == "hit") :
                playerHand.append(deck.drawCard());
                playerScore = self.calculateScore(playerHand)

                clearScreen()
                print("🃏>====================<🃏\n\033[1mBlackjack \033[0m")
                print(f"Balance: \033[1m${self.balance}\n\033[0mCurrent bet: \033[1m${self.bet}\033[0m")
                print(f">>====================<<")

                print(f"Dealer hand: (Score: {dealerScore})")
                self.printHand(dealerHand)
                print(f"Your hand: (Score: {playerScore})")
                self.printHand(playerHand)

                #if player busts
                if(playerScore > 21) :
                    self.looseBalance()
                    print(f"Bust. You loose ${self.bet}.")

                    l = input("Would you like to play again(y/n)? > ")
                    if(l == "y" or l == "yes") :
                        ##if the bet is higher than the balance
                        if(self.balance < self.bet) :
                            self.placeBet()
                        self.playHand()
                    else :
                        casino.mainMenu()



            elif (i == "s" or i == "stand") :
                while(dealerScore < 17) :
                    dealerHand.append(deck.drawCard())
                    dealerScore = self.calculateScore(dealerHand)

                clearScreen()
                print("🃏>====================<🃏\n\033[1mBlackjack \033[0m")
                print(f"Balance: \033[1m${self.balance}\n\033[0mCurrent bet: \033[1m${self.bet}\033[0m")
                print(f">>====================<<")

                print(f"Dealer hand: (Score: {dealerScore})")
                self.printHand(dealerHand)
                print(f"Your hand: (Score: {playerScore})")
                self.printHand(playerHand)

                if(dealerScore > 21) :
                    self.winBalance()
                    print(f"Dealer busts! You win ${self.bet}.")

                elif(dealerScore == playerScore) :
                    print("Push. Bet is returned.")
                
                elif(dealerScore > playerScore) :
                    self.looseBalance()
                    print(f"Dealer wins. You loose ${self.bet}.")
                
                elif(dealerScore < playerScore) :
                    self.winBalance()
                    print(f"You win! You win ${self.bet}")
                
                l = input("Would you like to play again(y/n)? > ")
                if(l == "y" or l == "yes") :
                    ##if the bet is higher than the balance
                    if(self.balance < self.bet) :
                        self.placeBet()
                    self.playHand()
                else :
                    casino.mainMenu()
                        


            else :
                print("Please hit or stand (h,hit / s,stand)")
    

    def printHand(self, hand) :
        for card in hand :
            print(f"{card.getRank()} of {card.getSuit()}")
        print("----------")

    ##calculates the score of the hand that is passed in
    def calculateScore(self, hand) :
        numAce = 0
        output = 0

        for card in hand :
            if(card.getRank() == "J" or card.getRank() == "Q" or card.getRank() == "K") :
                output += 10
            elif(card.getRank() == "A") :
                output += 11 
                numAce += 1
            else :
                output += int(card.getRank())

        ##handles ace logic
        while(numAce > 0 and output > 21) :
            output -= 10
            numAce -=1

        return output

    def looseBalance(self) :
        self.casino.removeBalance(self.bet)
        self.balance -= self.bet

    def winBalance(self) :
        self.casino.addBalance(self.bet)
        self.balance += self.bet


def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main() :
    casino = Casino(500)
    casino.mainMenu()

if __name__ == "__main__":
   ##main()
   casino = Casino(500)
   game = Blackjack(casino)
   game.playHand()
   

   
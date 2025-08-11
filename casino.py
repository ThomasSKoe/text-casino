import random
import time
import os
import sys

##Overarching casino class
class Casino:

    def __init__(self, startingMoney):
        self.balance = startingMoney
        self.stats = {
            "highestBalance": startingMoney,
            "biggestWin": 0,
            "biggestLoss": 0,
            "blackjackWins": 0,
            "blackjackLoses": 0,
            "blackjacks": 0
        }

    def mainMenu(self):


        while True : 
            clearScreen()
            print("\n".join([
                ">>==============================================<<",
                "📈 Welcome to the Casino 📉".center(50),
                f"Balance: ${self.balance}".center(50),
                ">>==============================================<<",
                "Select an option:",
                "",
                "1 : Blackjack",
                "2 : Roulette",
                "3 : Slots",
                "4 : Stats",
                "5 : Cash out (quit)"
            ]))

        
            userInput = input("> ")

            if(userInput == "1") :
                game = Blackjack(self)
                game.welcome()
            elif(userInput == "2") :
                print("Not implemented yet")
            elif(userInput == "3") :
                print("Not implemented yet")
            elif(userInput == "4") :
                self.showStats()
                input("Press (enter) to return")

            elif(userInput =="5") :
                r = input("Are you sure you would like to quit? (y/n) > ")
                if(r == "y" or r == "yes") :
                    self.cashOut()
                    return
            else :
                print("Invalid selection (1 - 5)")
                input("(enter) to continue")  

    def showStats(self) :
        clearScreen()
        s = self.stats
        print("===  Stats ===\n")

        print(f"Final balance:      | {self.balance}\n")
        print(f"Highest balance:    | {s['highestBalance']}")
        print(f"Biggest win:        | {s['biggestWin']}")
        print(f"Biggest loss:       | {s['biggestLoss']}\n")
        print(f"Blackjack wins:     | {s['blackjackWins']}")
        print(f"Blackjack Loses:    | {s['blackjackLoses']}\n")
        print(f"Natural Blackjacks: | {s['blackjacks']}\n")

    def cashOut(self) :
        self.showStats()
  
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
    bet = 0

    def __init__(self, casinoObject) :
        self.casino = casinoObject

    def welcome(self) :

        while True :
            clearScreen()
            print("\n".join([
                ">>==============================================<<",
                "🃏 Welcome to Blackjack 🃏".center(48),
                f"Balance: ${self.casino.balance} | Bet: ${self.bet}".center(50),
                ">>==============================================<<",
                "Select an option:",
                "",
                "1 : Place bet",
                "2 : Draw hand",
                "3 : Return to main menu"
            ]))

            
            
            userInput = input("> ").strip().lower()
            if(userInput == "1") :
                self.bet = self.placeBet()

            elif(userInput == "2") :
                if (self.bet > self.casino.balance) :
                    self.bet = self.placeBet()
                
                while True :
                    self.playHand()

                    if self.casino.balance <= 0 :
                        print("You are out of money.")
                        self.bet = 0
                        input("(enter)")
                        break   

                    i = input("Play again with same bet (y/n)? > ").strip().lower()
                    if i not in ("y","yes"):
                        break
                    
                    if self.bet > self.casino.balance:
                        print("Bet exceeds balance. Place a new bet.")
                        self.bet = self.placeBet()
                             
            elif(userInput == "3") :
                return
            else :
                print("Not a valid selection (1 - 3)")

    def placeBet(self) :
        while True :
            i = input(f"Bet amount ($1 - ${self.casino.balance}) > ").strip()
            try:
                val = int(float(i))
            except ValueError :
                print("Please enter a number.")
                continue
            if(val >= 1 and val <= self.casino.balance) :
                return val
            else :
                print(f"Please enter a valid number between 1 and {self.casino.balance}")
                    
    def playHand(self) :

        deck = Deck()

        dealerScore = 0
        playerScore = 0

        dealerHand = [deck.drawCard(), deck.drawCard()]
        playerHand = [deck.drawCard(), deck.drawCard()]

        dealerUpScore = self.calculateScore([dealerHand[0]])
        dealerScore = self.calculateScore(dealerHand)
        playerScore = self.calculateScore(playerHand)

        clearScreen()
        print("\n".join([
                ">>==============================================<<",
                "🃏 Blackjack 🃏".center(48),
                f"Balance: ${self.casino.balance} | Bet: ${self.bet}".center(50),
                ">>==============================================<<"
            ]))
        
        
        print(f"Dealer hand: (Score: {dealerUpScore})")
        print(f"{dealerHand[0].getRank()} of {dealerHand[0].getSuit()}")
        print("[hole card hidden]")
        print("----------")

        print(f"Your hand: (Score: {playerScore})")
        self.printHand(playerHand)
        
        playerNatural = (playerScore == 21 and len(playerHand) == 2)
        dealerNatural = (dealerScore == 21 and len(dealerHand) == 2)

        if (dealerNatural or playerNatural) :
            clearScreen()
            print("\n".join([
                ">>==============================================<<",
                "🃏 Blackjack 🃏".center(48),
                f"Balance: ${self.casino.balance} | Bet: ${self.bet}".center(50),
                ">>==============================================<<"
            ]))
            print(f"Dealer hand: (Score: {dealerScore})")
            self.printHand(dealerHand)
            print(f"Your hand: (Score: {playerScore})")
            self.printHand(playerHand)

            if dealerNatural and playerNatural:
                print("Both have natural blackjack! Wow! Push. Bet is returned.")
                return
            elif playerNatural:
                win = self.bet + (self.bet // 2)       
                self.winBalance(win)
                self.casino.stats["blackjackWins"] += 1
                self.casino.stats["blackjacks"] += 1
                print(f"Natural Blackjack! You win ${win}.")
                return
            else:
                self.loseBalance(self.bet)
                self.casino.stats["blackjackLoses"] += 1
                print(f"Dealer has natural blackjack. You lose ${self.bet}.")
                return

        while True :
            i = input("Would you like to (h)it or (s)tand? > ")
            
            if(i == "h" or i == "hit") :
                playerHand.append(deck.drawCard());
                playerScore = self.calculateScore(playerHand)

                clearScreen()
                print("\n".join([
                    ">>==============================================<<",
                    "🃏 Blackjack 🃏".center(48),
                    f"Balance: ${self.casino.balance} | Bet: ${self.bet}".center(50),
                    ">>==============================================<<"
                ]))
                
                print(f"Dealer hand: (Score: {dealerUpScore})")
                print(f"{dealerHand[0].getRank()} of {dealerHand[0].getSuit()}")
                print("[hole card hidden]")
                print("----------")
                print(f"Your hand: (Score: {playerScore})")
                self.printHand(playerHand)

                #if player busts
                if(playerScore > 21) :
                    self.loseBalance(self.bet)
                    self.casino.stats["blackjackLoses"] += 1
                    print(f"Bust. You lose ${self.bet}.")
                    return



            elif (i == "s" or i == "stand") :
                while(dealerScore < 17) :
                    dealerHand.append(deck.drawCard())
                    dealerScore = self.calculateScore(dealerHand)

                clearScreen()
                print("\n".join([
                    ">>==============================================<<",
                    "🃏 Blackjack 🃏".center(48),
                    f"Balance: ${self.casino.balance} | Bet: ${self.bet}".center(50),
                    ">>==============================================<<"
                ]))

                print(f"Dealer hand: (Score: {dealerScore})")
                self.printHand(dealerHand)
                print(f"Your hand: (Score: {playerScore})")
                self.printHand(playerHand)

                if(dealerScore > 21) :
                    self.winBalance(self.bet)
                    self.casino.stats["blackjackWins"] += 1
                    print(f"Dealer busts! You win ${self.bet}.")

                elif(dealerScore == playerScore) :
                    print("Push. Bet is returned.")
                
                elif(dealerScore > playerScore) :
                    self.loseBalance(self.bet)
                    self.casino.stats["blackjackLoses"] += 1
                    print(f"Dealer wins. You lose ${self.bet}.")
                
                elif(dealerScore < playerScore) :
                    self.winBalance(self.bet)
                    self.casino.stats["blackjackWins"] += 1
                    print(f"You win! You win ${self.bet}")
                return  
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

    def loseBalance(self,amount) :
        self.casino.removeBalance(amount)
        
        if(amount > self.casino.stats["biggestLoss"]) :
            self.casino.stats["biggestLoss"] = amount

    def winBalance(self,amount) :
        self.casino.addBalance(amount)

        if(amount > self.casino.stats["biggestWin"]) :
            self.casino.stats["biggestWin"] = amount
        
        if(self.casino.balance > self.casino.stats["highestBalance"]) :
            self.casino.stats["highestBalance"] = self.casino.balance

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main() :
    casino = Casino(500)
    casino.mainMenu()

if __name__ == "__main__":
   main()
   

   
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

        userInput = input("> ")

        if(userInput == "1") :
            game = Blackjack(self)
            game.play()
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
       

class Blackjack :

    def __init__(self, casinoObject) :
        self.casino = casinoObject
        self.balance = casinoObject.balance
    
    def play(self) :

        clearScreen()
        print("@~~~~~~~~~~~~~~~~~~~~~~@\nWelcome to Blackjack")
        print(f"Balance: ${self.balance}\n@~~~~~~~~~~~~~~~~~~~~~~@")
        print("\nSelect an option:\n" \
        "1 : Place bet\n" \
        "2 : Draw hand\n" \
        "3 : Return to main menu")
        
    
        while True :
            userInput = input("> ")
            if(userInput == "3") :
                self.casino.mainMenu()
                return
            else :
                print("Not a valid selection (1 - 3)")
            



def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main() :
    casino = Casino(500)
    casino.mainMenu()


if __name__ == "__main__":
    main()
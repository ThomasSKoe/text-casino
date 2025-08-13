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
            "blackjacks": 0,
            "rouletteSpins": 0,
            "rouletteHits":0,
            "rouletteLosses": 0
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

        
            userInput = input("> ").strip()

            if(userInput == "1") :
                game = Blackjack(self)
                game.welcome()
            elif(userInput == "2") :
                game = Roulette(self)
                game.welcome()
            elif(userInput == "3") :
                print("Not implemented yet")
            elif(userInput == "4") :
                self.showStats()
                input("\nPress (enter) to return")

            elif(userInput =="5") :
                r = input("Are you sure you would like to quit? (y/n) > ")
                if(r == "y" or r == "yes") :
                    self.cashOut()
                    return
            else :
                print("Invalid selection (1 - 5)")
                input("  <enter> to return")   

    def showStats(self) :
        clearScreen()
        s = self.stats
        print("===  Stats ===\n")

        print(f"Final balance:      | {self.balance}\n")
        print(f"Highest balance:    | {s['highestBalance']}")
        print(f"Biggest win:        | {s['biggestWin']}")
        print(f"Biggest loss:       | {s['biggestLoss']}\n")
        print(f"Blackjack wins:     | {s['blackjackWins']}")
        print(f"Blackjack losses:   | {s['blackjackLoses']}")
        print(f"Natural blackjacks: | {s['blackjacks']}\n")
        print(f"Roulette wins:      | {s['rouletteHits']}")
        print(f"Roulette losses:    | {s['rouletteLosses']}")

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

            userInput = input("> ").strip()
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
                print("Invalid selection (1 - 3)")
                input("  <enter> to return")   

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

class Roulette :

    WHEEL = [
        "0","28","9","26","30","11","7","20","32","17","5","22","34","15","3","24",
        "36","13","1","00","27","10","25","29","12","8","19","31","18","6","21",
        "33","16","4","23","35","14","2"]
    VALID_NUMBERS = {str(n) for n in range(1, 37)} | {"0", "00"}
    RED = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
    
    VALID_TYPES = {
        "straight", 
        "split",
        "street", 
        "corner", 
        "line", 
        "five", 
        "column", 
        "dozen",
        "red",
        "black",
        "odd", 
        "even", 
        "low", 
        "high"}
    

    PAYOUT = {
        "straight": 35,
        "split": 17,
        "street": 11,
        "corner": 8,
        "line": 5,
        "five": 6,
        "column": 2,
        "dozen": 2,
        "red": 1,
        "black": 1,
        "odd": 1,
        "even": 1,
        "low": 1,
        "high": 1,

    }

    def __init__(self, casinoObject) :
        self.casino = casinoObject
        self.bets = []
        self.totalBet = 0
    
    def welcome(self) :
        while True :

            clearScreen()
            print("\n".join([
                ">>==============================================<<",
                "🔴 Welcome to Roulette ⚫".center(48),
                f"Balance: ${self.casino.balance} | Total bet: ${self.totalBet}".center(50),
                ">>==============================================<<",
                "Select an option:",
                "",
                "1 : Place bets",
                "2 : List bets",
                "3 : Roulette rules",
                "4 : Roll",
                "5 : Return to main menu"
            ]))

            userInput = input("> ")
            if(userInput == "1") :
                self.bets = self.placeBets()
            elif(userInput == "2") :
                self.listBets()
            elif(userInput == "3") :
                clearScreen()
                self.printRouletteLayout()
                input("Press enter to return > ")
            elif(userInput == "4") :
                self.roll()
                input("\nPress enter to return > ")
                self.bets = []
                self.totalBet = 0

            elif(userInput == "5") :
                return
            else :
                print("Invalid selection (1 - 4)")
                input("  <enter> to return")  

    def listBets(self) :
        clearScreen()
        print("\n".join([
            ">>==============================================<<",
            "🔴 Welcome to Roulette ⚫".center(48),
            f"Balance: ${self.casino.balance} | Total bet: ${self.totalBet}".center(50),
            ">>==============================================<<",
            "List of bets:\n",
        ]))

        for bet in self.bets :
            print(bet["message"])
        input("\nPress enter to return > ")

    def placeBets(self) :
        betList = []

        clearScreen()

        print("\n".join([
            ">>==============================================<<",
            "🔴 Welcome to Roulette ⚫".center(48),
            f"Balance: ${self.casino.balance} | Total bet: ${self.totalBet}".center(50),
            ">>==============================================<<",
            "Type 'rules' for list of bets. Type 'done' to finalize bets.",
            "Place bets:\n"
        ]))
        
        while True :

            i = input("> ").strip().lower()
            if(i == 'done') :
                return betList
            elif(i == 'rules') :
                self.printRouletteLayout()
            else :
                if not i:
                    continue
                
                parts = i.split()

                if len(parts) == 1 :
                    print("Please enter a bet type and a bet. Examples:")
                    print("  red 10")
                    print("  straight 17 5")
                    print("  split 17 20 5")
                    continue
                    
                else :
                    try: 
                        amount = int(parts[-1])
                        if amount <= 0:
                            print("Bet amount must be a positive whole number.")
                            continue
                    
                    except ValueError:
                        print("The last value must be your bet amount (a number). Examples:")
                        print("  red 10")
                        print("  split 17 20 5")
                        continue

                    
                    betType = parts[0]
                    
                    ##numbers bet on
                    numbers = parts[1:-1] if len(parts) > 2 else []
                
                    ifValid, errorMessage = self.isValidBet(betType, numbers, amount) 
                    if not ifValid :
                        print( "Invalid bet:", errorMessage)
                        continue

                    betList.append({"type": betType, "nums": numbers, "bet": amount, "message": i})
                    self.casino.balance -= amount
                    self.totalBet += amount
                    print(f"Bet placed. Balance left: {self.casino.balance}")

    def printRouletteLayout(self):
        ##turns int red into string red list
        RED_STRINGS = {str(n).rjust(2) for n in self.RED}
        REDC = "\033[31m"
        RESET = "\033[0m"

        layout = f"""
================ AMERICAN ROULETTE ===============
|00| 0| 3| 6| 9|12|15|18|21|24|27|30|33|36|2-to-1|
      | 2| 5| 8|11|14|17|20|23|26|29|32|35|2-to-1|
      | 1| 4| 7|10|13|16|19|22|25|28|31|34|2-to-1|
      |==1st  12==|==2nd  12==|==3rd  12==|
      |1-18|EVEN | RED | BLACK | ODD|19-36| """

        #replace any red number with colored version
        for num in RED_STRINGS:
            layout = layout.replace(num, f"{REDC}{num}{RESET}")

        print(layout)
        print("""
    Inside Bets:
    36x |straight <#>                 <amt> - One number 
    18x |split    <#1> <#2>           <amt> - Two adjacent numbers
    12x |street   <lowest#>           <amt> - Three numbers in a row (3 nums)
    9x  |corner   <#1> <#2> <#3> <#4> <amt> - Four touching numbers
    6x  |line     <lowest#>           <amt> - Two adjacent rows (6 nums)
    7x  |five                         <amt> - Covers 0, 00, 1, 2 and 3 

    Outside Bets:
    3x |column    <1-3> <amt> - One of the 3 vertical columns
    3x |dozen     <1-3> <amt> - 1st (1-12), 2nd (13-24), 3rd (25-36)
    2x |red/black       <amt> - Any red/black number
    2x |odd/even        <amt> - Any even number
    2x |low/high        <amt> - 1-18 or 19-36 
    """)
        
    def isValidBet(self, betType, nums, amount) :
        
        if betType not in self.VALID_TYPES :
            return False, "Invalid bet type."
        
        if amount <= 0 :
            return False, "Bet must be positive."
        
        if amount > self.casino.balance :
            return False, f"Not enough money in balance ({self.casino.balance})."
        
        specialSplits = {
            ("0","00"), ("00","0"),
            ("0","1"),  ("1","0"),
            ("0","2"),  ("2","0"),
            ("00","2"), ("2","00"),
            ("00","3"), ("3","00")
        }

        
        validNums = set(self.VALID_NUMBERS)
        green= {"0","00"}

        pos = {}
        ##builds the roullete table in pos
        for r in range(1, 13):
            a, b, c = 3*r - 2, 3*r - 1, 3*r
            pos[str(a)] = (r, 1)
            pos[str(b)] = (r, 2)
            pos[str(c)] = (r, 3)

        streetStarts = {str(x) for x in range(1, 35, 3)}  
        lineStarts = {str(x) for x in range(1, 32, 3)}

        def is_adjacent(a,b) :
            if(a,b) in specialSplits :
                return True
            if a in {"0","00"} or b in {"0","00"}:
                return False
            if a not in pos or b not in pos:
                return False
            ra, ca = pos[a]
            rb, cb = pos[b]
            return (ra == rb and abs(ca - cb) == 1) or (ca == cb and abs(ra - rb) == 1)

        def is_corner(quad):
            if any(q in green for q in quad):
                return False
            if any(q not in pos for q in quad):
                return False
            rows = sorted({pos[q][0] for q in quad})
            cols = sorted({pos[q][1] for q in quad})
            if len(rows) != 2 or len(cols) != 2:
                return False
            expected = {
                (rows[0], cols[0]), (rows[0], cols[1]),
                (rows[1], cols[0]), (rows[1], cols[1])
            }
            return {pos[q] for q in quad} == expected
        
        def is_street(triple):
            if len(triple) != 3 or any(t in green or t not in pos for t in triple):
                return False
            rowset = {pos[t][0] for t in triple}
            if len(rowset) != 1:
                return False
            return sorted(pos[t][1] for t in triple) == [1, 2, 3]
        
        def is_line(six):
            if len(six) != 6 or any(t in green or t not in pos for t in six):
                return False
            rows = sorted({pos[t][0] for t in six})
            cols = sorted({pos[t][1] for t in six})
            return len(rows) == 2 and rows[1] == rows[0] + 1 and cols == [1, 2, 3]
        


        if betType == "straight" :
            if len(nums) != 1 or nums[0] not in validNums:
                return False, "Straight must have exactly one valid number."
            return True, ""


        elif betType == "split" :
            if len(nums) != 2 or any(n not in validNums for n in nums):
                return False, "Split needs exactly two valid numbers."
            if not is_adjacent(nums[0], nums[1]):
                return False, "Split numbers must be adjacent on the grid."
            return True, ""
        
        if betType == "street":
            if len(nums) == 1 and nums[0] in streetStarts:
                return True, ""
            if len(nums) == 3 and is_street(nums):
                return True, ""
            return False, "Street must be row start (1,4,...,34) or exactly a 3-number row."

        if betType == "corner":
            if len(nums) != 4 or any(n not in validNums for n in nums):
                return False, "Corner must list exactly four valid numbers."
            if not is_corner(nums):
                return False, "Corner numbers must form a 2x2 block on the grid."
            return True, ""
            
        if betType == "line":
            if len(nums) == 1 and nums[0] in lineStarts:
                return True, ""
            if len(nums) == 6 and is_line(nums):
                return True, ""
            return False, "Line must be a valid start (1,4,...,31) or exactly a 6-number double street."
        
        if betType == "column":
            if len(nums) != 1 or nums[0] not in {"1","2","3"}:
                return False, "Column requires a selector: 1, 2, or 3."
            return True, ""

        if betType == "dozen":
            if len(nums) != 1 or nums[0] not in {"1","2","3"}:
                return False, "Dozen requires a selector: 1 (1-12), 2 (13-24), or 3 (25-36)."
            return True, ""

        elif betType in {"five", "red", "black", "odd", "even", "low", "high"} :
            if nums :
                return False, f"{betType} should not have any numbers."
            return True, ""


        #if passes all test =valid bet
        return False, "Unknown bet"

    def betWins(self, betType, nums, winningNumber) :

        winner = str(winningNumber).strip()

        redStrings = {str(n) for n in self.RED}
        allNums = {str(n) for n in range(1, 37)}
        blackStrings = allNums - redStrings

        #columns
        col = {1: set(), 2: set(), 3: set()}
        for n in range(1, 37):
            c = ((n - 1) % 3) + 1
            col[c].add(str(n))
        
        #doezens
        dozen = {
            "1": {str(n) for n in range(1, 13)},
            "2": {str(n) for n in range(13, 25)},
            "3": {str(n) for n in range(25, 37)},
        }

        def streetFromStart(s):
            n = int(s)
            return {str(n), str(n+1), str(n+2)}

        def lineFromStart(s):
            n = int(s)
            return {str(n+i) for i in range(6)}
        

        if betType == "straight":
            return winner in {nums[0]}
        
        if betType == "split" :
            return winner in set(nums)

        if betType == "street":
            if len(nums) == 1:
                return winner in streetFromStart(nums[0])
            return winner in set(nums)
        
        if betType == "corner":
            return winner in set(nums)
        
        if betType == "dozen": 
            return winner in dozen[nums[0]]
        
        if betType == "red" :
            return winner in redStrings
        
        if betType == "black" :
            return winner in blackStrings
        if betType == "odd":
            return winner.isdigit() and int(winner) % 2 == 1
        if betType == "even":
            return winner.isdigit() and int(winner) % 2 == 0
        if betType == "low":
            return winner.isdigit() and 1 <= int(winner) <= 18
        if betType == "high":
            return winner.isdigit() and 19 <= int(winner) <= 36

        return False

    def roll(self) :
        clearScreen()
        print("\n".join([
            ">>==============================================<<",
            "🔴 Welcome to Roulette ⚫".center(48),
            f"Balance: ${self.casino.balance} | Total bet: ${self.totalBet}".center(50),
            ">>==============================================<<\n",
        ]))

        winning = self.spin_animation(5, 9)
        
        winBets = []
        lossBets = [] 

        totalWon = 0
        totalLost = 0

        #calculates winners
        for bet in self.bets:
            if self.betWins(bet["type"], bet["nums"], winning):
                winBets.append(bet)
                totalWon += bet["bet"] * (self.PAYOUT[bet["type"]] + 1)
            else:
                lossBets.append(bet)
                totalLost += bet["bet"] 
        
        print(f"Winning bets: (${totalWon})") 
        print("=============")
        for bet in winBets:
            payout = bet["bet"] * (self.PAYOUT[bet["type"]] + 1)
            self.casino.balance += payout
            print(f"    {bet['message']} -> Wins ${payout}")
            self.casino.stats["rouletteHits"] += 1

        
        if(totalWon > self.casino.stats["biggestWin"]) :
            self.casino.stats["biggestWin"] = totalWon
            

        print(f"Losing bets: (${totalLost})") 
        print("=============")
        for bet in lossBets :
            print(f"    {bet['message']} -> Lost ${bet["bet"]}")
            self.casino.stats["rouletteLosses"] += 1

        
        if(totalLost > self.casino.stats["biggestLoss"]) :
            self.casino.stats["biggestLoss"] = totalLost
        
        if(self.casino.balance == 0) :
            print("/nBankrupt. You loose.")


    def isRed(self, s) :
        return s.isdigit() and int(s) in self.RED

    def spin_animation(self, duration, window):


        n = len(self.WHEEL)
        start = random.randrange(n)  
        landing = random.randrange(n)  
        cycles = random.randint(2, 5)  

        steps = cycles * n + (landing - start) % n

        ##slowdown 
        t = [i / max(1, steps - 1) for i in range(steps)]
        base = 0.002
        raw = [base + (1 - base) * (x ** 2) for x in t]
        scale = duration / sum(raw)
        delays = [d * scale for d in raw]

        cur = start
        half = window // 2



        for d in delays:
            indexes = [(cur - half + k) % n for k in range(window)]
            cells = []
            for j in indexes:
                raw = self.WHEEL[j]
                if raw in ("0", "00"):
                    #green
                    color = "\033[92m"
                elif raw.isdigit() and int(raw) in self.RED:
                    #red
                    color = "\033[31m" 
                else:
                    color = "\033[97m" 

                #right align in 2 spaces so 00 and 9 line up
                disp = f"{raw:>2}"
                tok = f"{color}{disp}\033[0m"
                cells.append(f"[{tok}]" if j == cur else f" {tok} ")
            sys.stdout.write("\033[6;H")
            sys.stdout.write(" ".join(cells) + "\n\n")
            sys.stdout.flush()
            time.sleep(d)
            cur = (cur + 1) % n

        winningIndex = (cur - 1) % n
        winningVal = self.WHEEL[winningIndex]
        sys.stdout.flush()

        return winningVal


def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main() :
    casino = Casino(500)
    casino.mainMenu()

if __name__ == "__main__":
   main()
#    c = Casino(500)
#    game = Roulette(c)
#    game.print_roulette_layout()

   
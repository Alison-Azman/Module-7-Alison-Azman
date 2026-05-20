

import random



class Card:

    def __init__(self, suit:str, rank:str, value:int):
        self.suit=suit
        self.rank=rank
        self.value=value

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    



class Deck:

    def __init__(self):
        self.cards: list[Card] = []
        self.build_deck()
        self.shuffle()

    def build_deck(self):
        suits=["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
            "7": 7, "8": 8, "9": 9, "10": 10,
            "Jack": 10, "Queen": 10, "King": 10,
            "Ace": 11
            }
        for suit in suits:
            for rank, value in ranks.items():
                self.cards.append(Card(suit, rank, value))

                

    def shuffle(self):
        random.shuffle(self.cards)
        

    
    def deal_card(self):
        dealt=random.choice(self.cards)
        self.cards.remove(dealt)
        return dealt

    def cards_remaining(self):
        return len(self.cards)


class Hand:
    
    def __init__(self):
        self.cards: list[Card] = []


    def add_card(self, card:Card):
        self.cards.append(card)

    def get_total(self):
        total=0
        for card in self.cards:
            total+=card.value

        aces=0
        for card in self.cards:
            if card.rank=="Ace":
                aces+=1

        while total>21 and aces>0:
            total-=10
            aces-=1

        return total

    def show_hand(self):
        result=""
        for card in self.cards:
            result+= str(card) + ","

        return result
        
    def __str__(self):
        return self.show_hand()


class Participant:

    def __init__(self, name:str):
        self.name= name
        self.hand=Hand()


    def take_card(self, card:Card):
        self.hand.add_card(card)

    def show_hand(self):
        return self.hand.show_hand()

    def get_total(self):
        return self.hand.get_total()

    def is_busted(self):
        return self.get_total()>21

    def take_turn(self, deck:Deck):
        pass


class Player(Participant):
    def __init__(self, name: str):
        super().__init__(name)

    def take_turn(self, deck:Deck):
        
        while not self.is_busted():
            choice = input("Hit or Stand? ").strip().lower()
 
            if choice == "hit":
                card = deck.deal_card()
                self.take_card(card)
                print(f"You drew: {card}")
                print(f"Your new total: {self.get_total()}")
 
                if self.is_busted():
                    print(f"Bust! Your total is {self.get_total()}. You lost")
                    break
                
            elif choice == "stand":
                print(f"You stand with {self.get_total()}.")
                break
            else:
                print("***Invalid Input*** \nPlease enter 'hit' or 'stand'")
                
class Dealer(Participant):
    def __init__(self):
        super().__init__("Dealer")
    

    def show_first_card(self):
        if len(self.hand.cards)==0:
            return "There are no cards yet"

        else:
            return self.hand.cards[0]


    def take_turn(self, deck:Deck):
        print(f"Dealer revelas hidden card: {self.hand.cards[1]}")
        print(f"Dealer total: {self.get_total()}")

        while self.get_total()<17:
            card= deck.deal_card()
            self.take_card(card)
            print(f"Dealer draws: {card}")
            print(f"Dealer total: {self.get_total()}")

        if self.is_busted():
            print(f"Dealer busts with a total of {self.get_total()}")

class BlackjackGame:

    def __init__(self, player_name:str):
        self.player=Player(player_name)
        self.deck=Deck()

        self.dealer=Dealer()


    def initial_deal(self):
        for i in range(2):
            self.player.take_card(self.deck.deal_card())
            self.dealer.take_card(self.deck.deal_card())

    

    def show_game_state(self):
        print("********************************************************")
        print("Starting Game....")
        print("********************************************************")

        print(f"Dealer shows: {self.dealer.show_first_card()}")
        print("Dealer has: [Hidden Card]")
        print()
        print("********************************************************")
        print()
        print(f"Your hand: {self.player.show_hand()}")
        print(f"Your total: {self.player.get_total()}")

    def determine_winner(self):
        player_total= self.player.get_total()
        dealer_total= self.dealer.get_total()


        if self.player.is_busted():
            return "Dealer wins! Player busted"

        if self.dealer.is_busted():
            return f"{self.player.name} wins! Dealer busted"

        if player_total> dealer_total:
            return f"{self.player.name} wins!"
        elif dealer_total>player_total:
            return "Dealer wins!"
        else:
            return "It's a tie!"


    def play(self):
        print("Welcome to Blackjack")

        self.initial_deal()
        self.show_game_state()


        self.player.take_turn(self.deck)

        if self.player.is_busted()== False:
            self.dealer.take_turn(self.deck)

        print("Final Hand")
        print()
        print(f"Dealer hand: {self.dealer.show_hand()}")
        print(f"Dealer total: {self.dealer.get_total()}")

        print("***********************************************************")
        print()
 
        print(f"Your hand: {self.player.show_hand()}")
        print(f"Your total: {self.player.get_total()}")
        
        result=self.determine_winner()
        print(result)
    
if __name__ == "__main__":
    name = input("Enter your name: ").strip() or "Player"
    game = BlackjackGame(name)
    game.play()

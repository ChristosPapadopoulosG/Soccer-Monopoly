# -*- coding: latin-1 -*-
import random


a1=0;a2=0;a3=0;a4=0;a5=0;a6=0;a7=0;a8=0;
purchase=[0,60,0,60,0,200,100,0,100,120,0,140,150,140,160,200,180,0,180,200,00,220,0,220,240,200,260,260,150,280,0,300,300,0,320,200,0,350,100,400]
rent=[0,2,0,4,0,25,6,0,6,8,0,
      10,4,10,14,25,18,0,18,20,0,
      22,0,24,26,25,28,28,4,30,0,
      32,32,0,34,25,0,35,0,50]
mortgage_value=[x / 2 for x in purchase]

blocks=["To Go","Aik Stochkolm","Community Chest1","Malmo","Income Tax","San Mames",
        "Olympiakos","Chance1","Panathinaikos","PAOK","Jail",
        "Braga","Uefa Europa League","Benfica","Sporting Lisbon","Santiago Bernabeu",
        "Olympic Marseille","Community Chest2","Monaco","Pari Saint Germain","Free Parking",
        "Inter","Chance2","Milan","Juventus","Camp Nou",
        "Bayer Leverkousen","Dortmund","Uefa Champions League","Bayern Munich","Go to Jail!",
        "Atletico Madrid","Barchelona","Comunity Chest3","Real Madrid","Maracana",
        "Chance3","Arsenal","Luxury Tax","Manchester City"]
houses = [0]*40



ownership=[-1 for _ in range(40)]
non_purchasable_blocks = [0, 2, 4, 7, 10, 17, 20, 22, 30, 33, 36, 38]
for p in non_purchasable_blocks:
    ownership[p] = -2


class Player:
    def __init__(self,name,bank,own,pos,prison,turn_in_prison,doubledice,turn,n_own,build,get_out_of_jail_free,houses_owned,hotels_owned,style,active,mortgage,bankrupt):
        self.name=name
        self.bank =bank
        self.own=own
        self.pos=pos
        self.prison=prison
        self.turn_in_prison=turn_in_prison
        self.doubledice=doubledice
        self.turn=turn
        self.n_own=n_own
        self.build=build
        self.get_out_of_jail_free=get_out_of_jail_free
        self.houses_owned=houses_owned
        self.hotels_owned=hotels_owned
        self.style=style
        self.active=active
        self.mortgage=mortgage
        self.bankrupt=bankrupt


num_players = int(input("How many players want to play? "))
num_turns = int(input("How many turns want to play? "))
players=[]  

for i in range(num_players):
    player_name = input(f"Enter the name of player {i + 1}: ")
    player_style = int(input(f"Enter the style of player {player_name}-> 1.Agrresive, 2.Balanced, 3.Risk-Averse, 4.High Roller: "))
    pl = Player(player_name,1500,ownership,0,0,0,0,0,0,[0]*40,0,0,0,player_style,True,False,"")
    players.append(pl)
    
    #Aggressive buys in 95%
    #Balanced buys in 70%
    #Risk-Averse buys cheap properties with 90% and expensive with 10 (based on pos)%
    #High Roller buys expensive properties with 90% and expensive with 10 (based on pos)%

def game_is_on(players):
    # Check how many players have a positive bank balance
    positive_balance_players = [player for player in players if player.bank > 0]
    return len(positive_balance_players) > 1  # Game continues if more than one player is still in the game

def winner(players):
    for player in players:
        if player.bank > 0:
            print(f"{player.name} is the winner with {player.bank} EURO remaining!")

community_chest_cards = [
    "Advance to Manchester City",
    "Advance to Go (Collect 200 EURO)",
    "Advance to Juventus. If you pass Go, collect 200 EURO",
    "Advance to Braga. If you pass Go, collect 200 EURO",
    "Advance to the nearest Stadium.",
    "Advance to the nearest Stadium.",
    "Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total ten times amount thrown",
    "Bank pays you dividend of 50 EURO",
    "Get Out of Jail Free",
    "Go Back 3 Spaces",
    "Go to Jail. Go directly to Jail, do not pass Go, do not collect 200 EURO",
    "Make general repairs on all your property. For each house pay 25 EURO. For each hotel pay 100 EURO",
    "Speeding fine 15 EURO",
    "Take a trip to San Mames. If you pass Go, collect 200 EURO",
    "You have been elected Chairman of the Board. Pay each player 50 EURO",
    "Your building loan matures. Collect 150 EURO"
]

chance_cards = [
    "Advance to Go (Collect 200 EURO)",
    "Bank error in your favor. Collect 200 EURO",
    "Doctor’s fee. Pay 50 EURO",
    "From sale of stock you get 50 EURO",
    "Get Out of Jail Free",
    "Go to Jail. Go directly to jail, do not pass Go, do not collect 200 EURO",
    "Holiday fund matures. Receive 100 EURO",
    "Income tax refund. Collect 20 EURO",
    "It is your birthday. Collect 10 EURO from every player",
    "Life insurance matures. Collect 100 EURO",
    "Pay hospital fees of 100 EURO",
    "Pay school fees of 50 EURO",
    "Receive 25 EURO consultancy fee",
    "You are assessed for street repair. 40 EURO per house. 115 EURO per hotel",
    "You have won second prize in a beauty contest. Collect 10 EURO",
    "You inherit 100 EURO"
]
random.shuffle(chance_cards)
random.shuffle(community_chest_cards)

#Draw Chance cards
def draw_chance(player,players):
    card1 = chance_cards.pop(0)  # Draw the top card
    chance_cards.append(card1)  # Move the drawn card to the bottom of the deck
    print(f"Chance Card: {card1}")
    if card1 == "Advance to Go (Collect 200 EURO)":
        player.pos = 0  
        player.bank += 200  
        print(f"{player.name} advances to Go and collects 200 EURO!")
    elif card1 == "Bank error in your favor. Collect 200 EURO":
        player.bank += 200
        print(f"Bank error in favor of {player.name}. They collect 200 EURO!")
    elif card1 == "Doctor’s fee. Pay 50 EURO":
        player.bank -= 50
        print(f"{player.name} pays a doctor's fee of 50 EURO.")
        if player.bank<0:
                player.bankrupt="BANK"
    elif card1 == "From sale of stock you get 50 EURO":
        player.bank += 50
        print(f"{player.name} receives 50 EURO from the sale of stock.")
    elif card1 == "Get Out of Jail Free":
        player.get_out_of_jail_free +=1
        print(f"{player.name} gets a 'Get Out of Jail Free' card.")
    elif card1 == "Go to Jail. Go directly to jail, do not pass Go, do not collect 200 EURO":
        player.pos = 10  
        player.prison = 1
        print(f"{player.name} goes directly to jail!")
    elif card1 == "Holiday fund matures. Receive 100 EURO":
        player.bank += 100
        print(f"{player.name}'s holiday fund matures. They collect 100 EURO.")
    elif card1 == "Income tax refund. Collect 20 EURO":
        player.bank += 20
        print(f"{player.name} receives an income tax refund of 20 EURO.")
    elif card1 == "It is your birthday. Collect 10 EURO from every player":
        for j in range(num_players):
            if j != i:  # Every other player pays 10 EURO
                players[j].bank -= 10
                players[i].bank += 10
        print(f"{player.name}'s birthday! They collect 10 EURO from every player.")
    elif card1 == "Life insurance matures. Collect 100 EURO":
        player.bank += 100
        print(f"{player.name}'s life insurance matures. They collect 100 EURO.")
    elif card1 == "Pay hospital fees of 100 EURO":
        player.bank -= 100
        print(f"{player.name} pays 100 EURO in hospital fees.")
        if player.bank<0:
                player.bankrupt="BANK"
    elif card1 == "Pay school fees of 50 EURO":
        player.bank -= 50
        print(f"{player.name} pays 50 EURO in school fees.")
        if player.bank<0:
                player.bankrupt="BANK"
    elif card1 == "Receive 25 EURO consultancy fee":
        player.bank += 25
        print(f"{player.name} receives 25 EURO as a consultancy fee.")
    elif card1 == "You are assessed for street repair. 40 EURO per house. 115 EURO per hotel":
        total_fee = (player.houses_owned * 40) + (player.hotels_owned * 115)
        player.bank -= total_fee
        print(f"{player.name} pays {total_fee} EURO for street repairs.")
        if player.bank<0:
                player.bankrupt="BANK"
    elif card1 == "You have won second prize in a beauty contest. Collect 10 EURO":
        player.bank += 10
        print(f"{player.name} wins second prize in a beauty contest and collects 10 EURO.")
    elif card1 == "You inherit 100 EURO":
        player.bank += 100
        print(f"{player.name} inherits 100 EURO.")
    return card1

#Draw Comunity Chest cards
def draw_community(player,players):  
    card2 = community_chest_cards.pop(0)  # Draw the top card
    community_chest_cards.append(card2)  # Move the drawn card to the bottom of the deck
    print(f"Community Chest Card: {card2}")
    if card2 == "Advance to Manchester City":
        player.pos = 39  
        print(f"{player.name} advances to Manchester City!")
        mainturn(player)
    elif card2 == "Advance to Go (Collect 200 EURO)":
        player.pos = 0
        player.bank += 200
        print(f"{player.name} advances to Go and collects 200 EURO!")
    elif card2 == "Advance to Juventus. If you pass Go, collect 200 EURO":
        if player.pos > 24:  
            player.bank += 200  
        player.pos = 24
        print(f"{player.name} advances to Juventus and collects 200 EURO!")
        mainturn(player)
    elif card2 == "Advance to Braga. If you pass Go, collect 200 EURO":
        if player.pos > 11:  
            player.bank += 200  
        player.pos = 11
        print(f"{player.name} advances to Braga and collects 200 EURO!")
        mainturn(player)
    elif card2 == "Advance to the nearest Stadium.":
        if player.pos < 5 or player.pos > 35:
            player.pos = 5  
            print(f"{player.name} advances to the nearest stadium San Mames and collects 200 EURO!")
            mainturn(player)
        elif player.pos < 15:
            player.pos = 15  
            print(f"{player.name} advances to the nearest stadium Santiago Bernabeu and collects 200 EURO!")
            mainturn(player)
        elif player.pos < 25:
            player.pos = 25  
            print(f"{player.name} advances to the nearest stadium Camp Nou and collects 200 EURO!")
            mainturn(player)
        elif player.pos < 35:
            player.pos = 35  
            print(f"{player.name} advances to the nearest stadium Maracana and collects 200 EURO!")
            mainturn(player)
    elif card2 == "Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total ten times amount thrown":
        if player.pos < 12 or players[i].pos > 28:
            player.pos = 12  # mainturn
            print(f"{player.name} advances to the nearest Utility UEFA Europa League!")
            mainturn(player)
        else:
            player.pos = 28  # mainturn
            print(f"{player.name} advances to the nearest Utility UEFA Champions League!")
            mainturn(player)
    elif card2 == "Bank pays you dividend of 50 EURO":
        player.bank += 50
        print(f"Bank pays {player.name} a dividend of 50 EURO.")
    elif card2 == "Get Out of Jail Free":
        player.get_out_of_jail_free +=1  # 
        print(f"{player.name} receives a 'Get Out of Jail Free' card.")
    elif card2 == "Go Back 3 Spaces":
        player.pos -= 3
        print(f"{player.name} goes back 3 spaces.")
        mainturn(player)
    elif card2 == "Go to Jail. Go directly to Jail, do not pass Go, do not collect 200 EURO":
        player.pos = 10
        player.prison = 1
        print(f"{player.name} goes directly to jail!")
    elif card2 == "Make general repairs on all your property. For each house pay 25 EURO. For each hotel pay 100 EURO":
        total_fee = (player.houses_owned * 25) + (player.hotels_owned * 100)
        player.bank -= total_fee
        print(f"{player.name} pays {total_fee} EURO for general repairs on all properties.")
    elif card2 == "Speeding fine 15 EURO":
        player.bank -= 15
        print(f"{player.name} pays a speeding fine of 15 EURO.")
        if player.bank<0:
                player.bankrupt="BANK"
    elif card2 == "Take a trip to San Mames. If you pass Go, collect 200 EURO":
        if player.pos > 15:  
            player.bank += 200  
        player.pos = 15
        print(f"{player.name} takes a trip to San Mames and collects 200 EURO!")
        mainturn(player)
    elif card2 == "You have been elected Chairman of the Board. Pay each player 50 EURO":
        for j in range(num_players):
            if j != i:  # Each player receives 50 EURO, except the current player   ÓÕÍÈÇÊÇ ÃÉÁ ×ÑÅÏÊÏÐÉÁ ÁÍÔÉÐÁËÏÕ ÐÁÉÊÔÇ
                players[i].bank -= 50
                players[j].bank += 50
                if players[i].bank<0:
                    players[i].bankrupt="BANK"
        print(f"{players[i].name} has been elected Chairman of the Board and pays 50 EURO to each player.")
    elif card2 == "Your building loan matures. Collect 150 EURO":
        player.bank += 150
        print(f"{player.name}'s building loan matures, collecting 150 EURO.")

#Mortgage of a Property
def mortgage_property(player, pos):
    if player.own[pos] == 1 and player.mortgage[pos] == False:
        player.bank += mortgage_value[pos]  # Player receives half the property's value
        player.mortgage[pos] = True  
        print(f"{player.name} has mortgaged {blocks[pos]} and received {mortgage_value[pos]} EURO.")
    else:
        print(f"{blocks[pos]} cannot be mortgaged.")

#Unmortgage of a Property
def unmortgage_property(player, pos):
    if player.mortgage[pos] == True:
        unmortgage_cost = int((purchase[pos] // 2) * 1.1)  # Mortgage amount + 10% 
        if player.bank >= unmortgage_cost:
            player.bank -= unmortgage_cost
            player.mortgage[pos] = False 
            print(f"{player.name} has unmortgaged {blocks[pos]} by paying {unmortgage_cost} EURO.")
        else:
            print(f"{player.name} does not have enough money to unmortgage {blocks[pos]}.")


#Build phase
def buildR(player):
    
    if player.build[1]+player.build[3] == 2:
        #build with probability
        global a1
        if a1==0:   
            rent[1]*=2
            rent[3]*=2
            a1+=1
        print(f" {player.name} has complete the brown area. The rent now is doubled.")
        if player.bank>50:
            if houses[1]<4:
                player.bank-=50
                houses[1]+=1
                rent[1]+=houses[1]*20
            if houses[1]==4:
                player.bank-=50
                player.hotels_owned=1
                rent[1]+=5*20
            print(f" {player.name} has build {houses[1]} house(s), and {player.hotels_owned} hotel in {blocks[1]}")
            if houses[3]<4:
                player.bank-=50
                houses[3]+=1
                rent[3]+=houses[3]*20
            if houses[3]==4:
                player.bank-=50
                player.hotels_owned=1
                rent[3]+=5*20
            print(f" {player.name} has build {houses[3]} house(s), and {player.hotels_owned} hotel in {blocks[3]}")          
    elif player.build[6]+player.build[8]+player.build[9]==3:
        #build  with probability
        global a2
        if a2==0:   
                rent[6]*=2
                rent[8]*=2
                rent[9]*=2
                a2+=1
        print(f" {player.name} has complete the blue area. The rent now is doubled")
        if player.bank>50:
            if houses[6]<4:
                player.bank-=50
                houses[6]+=1
                rent[6]+=houses[6]*20
            if houses[6]==4:
                player.bank-=50
                player.hotels_owned=1
                rent[6]+=5*20
            print(f" {player.name} has build {houses[6]} house(s), and {player.hotels_owned} hotel in {blocks[6]}")
            if houses[8]<4:
                player.bank-=50
                houses[8]+=1
                rent[8]+=houses[8]*20
            if houses[8]==4:
                player.bank-=50
                player.hotels_owned=1
                rent[8]+=5*20
            print(f" {player.name} has build {houses[8]} house(s), and {player.hotels_owned} hotel in {blocks[8]}")
            if houses[9]<4:
                player.bank-=50
                houses[9]+=1
                rent[9]+=houses[9]*20
            if houses[9]==4:
                player.bank-=50
                player.hotels_owned=1
                rent[9]+=5*20
            print(f" {player.name} has build {houses[9]} house(s), and {player.hotels_owned} hotel in {blocks[9]}")
    elif player.build[11]+player.build[13]+player.build[14]==3:
        #build  with probability
        global a3
        if a3==0:   
            rent[11]*=2
            rent[13]*=2
            rent[14]*=2
            a3+=1  
        print(f" {player.name} has complete the Pink area. The rent now is doubled")
        if player.bank>100:
            if houses[11]<4:
                player.bank-=100
                houses[11]+=1
                rent[11]+=houses[11]*30
            if houses[11]==4:
                player.bank-=100
                player.hotels_owned=1
                rent[11]+=5*30
            print(f" {player.name} has build {houses[11]} house(s), and {player.hotels_owned} hotel in {blocks[11]}")
            if houses[13]<4:
                player.bank-=100
                houses[13]+=1
                rent[13]+=houses[13]*30
            if houses[13]==4:
               player.bank-=100
               player.hotels_owned=1
               rent[13]+=5*30
            print(f" {player.name} has build {houses[13]} house(s), and {player.hotels_owned} hotel in {blocks[13]}")
            if houses[14]<4:
                player.bank-=100
                houses[14]+=1
                rent[14]+=houses[14]*30
            if houses[14]==4:
                player.bank-=100
                player.hotels_owned=1
                rent[14]+=5*30
            print(f" {player.name} has build {houses[14]} house(s), and {player.hotels_owned} hotel in {blocks[14]}")
    elif player.build[16]+player.build[18]+player.build[19]==3:
        #build  with probability
        global a4
        if a4==0:   
            rent[16]*=2
            rent[18]*=2
            rent[19]*=2
            a4+=1  
        print(f" {player.name} has complete the Orange area. The rent now is doubled")
        if player.bank>100:
            if houses[16]<4:
                player.bank-=100
                houses[16]+=1
                rent[16]+=houses[16]*30
            if houses[16]==4:
                player.bank-=100
                player.hotels_owned=1
                rent[16]+=5*30
            print(f" {player.name} has build {houses[16]} house(s), and {player.hotels_owned} hotel in {blocks[16]}")
            if houses[18]<4:
                player.bank-=100
                houses[18]+=1
                rent[18]+=houses[18]*30
            if houses[18]==4:
                player.bank-=100
                player.hotels_owned=1
                rent[18]+=5*30
            print(f" {player.name} has build {houses[18]} house(s), and {player.hotels_owned} hotel in {blocks[18]}")
            if houses[19]<4:
                player.bank-=100
                houses[19]+=1
                rent[19]+=houses[19]*30
            if houses[19]==4:
                player.bank-=100
                player.hotels_owned=1
                rent[19]+=5*30
            print(f" {player.name} has build {houses[19]} house(s), and {player.hotels_owned} hotel in {blocks[19]}")
    elif player.build[21]+player.build[23]+player.build[24]==3:
        #build  with probability
        global a5
        if a5==0:   
            rent[21]*=2
            rent[23]*=2
            rent[24]*=2
            a5+=1  
        print(f" {player.name} has complete the Red area. The rent now is doubled")
        if player.bank>150:
            if houses[21]<4:
                player.bank-=150
                houses[21]+=1
                rent[21]+=houses[21]*40
            if houses[21]==4:
                player.bank-=150
                player.hotels_owned=1
                rent[21]+=5*40
            print(f" {player.name} has build {houses[21]} house(s), and {player.hotels_owned} hotel in {blocks[21]}")            
            if houses[23]<4:
                player.bank-=150
                houses[23]+=1
                rent[23]+=houses[23]*40
            if houses[23]==4:
                player.bank-=150
                player.hotels_owned=1
                rent[23]+=5*40
            print(f" {player.name} has build {houses[23]} house(s), and {player.hotels_owned} hotel in {blocks[23]}")
            if houses[24]<4:
                player.bank-=150
                houses[24]+=1
                rent[24]+=houses[24]*40
            if houses[24]==4:
                player.bank-=150
                player.hotels_owned=1
                rent[24]+=5*40
            print(f" {player.name} has build {houses[24]} house(s), and {player.hotels_owned} hotel in {blocks[24]}")
    elif player.build[26]+player.build[27]+player.build[29]==3:
        #build  with probability
        global a6
        if a6==0:   
            rent[26]*=2
            rent[27]*=2
            rent[29]*=2
            a6+=1  
        print(f" {player.name} has complete the Yellow area. The rent now is doubled")
        if player.bank>150:
            if houses[26]<4:
                player.bank-=150
                houses[26]+=1
                rent[26]+=houses[26]*40
            if houses[26]==4:
                player.bank-=150
                player.hotels_owned=1
                rent[26]+=5*40
            print(f" {player.name} has build {houses[26]} house(s), and {player.hotels_owned} hotel in {blocks[26]}")
            if houses[27]<4:
                player.bank-=150
                houses[27]+=1
                rent[27]+=houses[27]*40
            if houses[27]==4:
                player.bank-=150
                player.hotels_owned=1
                rent[27]+=5*40
            print(f" {player.name} has build {houses[27]} house(s), and {player.hotels_owned} hotel in {blocks[27]}")
            if houses[29]<4:
                player.bank-=150
                houses[29]+=1
                rent[29]+=houses[29]*40
            if houses[29]==4:
                player.bank-=150
                player.hotels_owned=1
                rent[29]+=5*40
            print(f" {player.name} has build {houses[29]} house(s), and {player.hotels_owned} hotel in {blocks[29]}")
    elif player.build[31]+player.build[32]+player.build[34]==3:
        #build  with probability
        global a7
        if a7==0:   
            rent[31]*=2
            rent[32]*=2
            rent[34]*=2
            a7+=1  
        print(f" {player.name} has complete the Green area. The rent now is doubled")
        if player.bank>200:
            if houses[31]<4:
                player.bank-=200
                houses[31]+=1
                rent[31]+=houses[31]*50
            if houses[31]==4:
                player.bank-=200
                player.hotels_owned=1
                rent[31]+=5*50
            print(f" {player.name} has build {houses[31]} house(s), and {player.hotels_owned} hotel in {blocks[31]}")
            if houses[32]<4:
                player.bank-=200
                houses[32]+=1
                rent[32]+=houses[32]*50
            if houses[32]==4:
                player.bank-=200
                player.hotels_owned=1
                rent[32]+=5*50
            print(f" {player.name} has build {houses[32]} house(s), and {player.hotels_owned} hotel in {blocks[32]}")
            if houses[34]<4:
                player.bank-=200
                houses[34]+=1
                rent[34]+=houses[34]*50
            if houses[34]==4:
                player.bank-=200
                player.hotels_owned=1
                rent[34]+=5*50
            print(f" {player.name} has build {houses[34]} house(s), and {player.hotels_owned} hotel in {blocks[34]}")
    elif player.build[37]+player.build[39]==2:
        #build  with probability
        global a8
        if a8==0:   
            rent[37]*=2
            rent[39]*=2
            a8+=1 
        
        print(f" {player.name} has complete the Black area. The rent now is doubled")
        if player.bank>200:
            if houses[37]<4:
                player.bank-=200
                houses[37]+=1
                rent[37]+=houses[37]*50
            if houses[37]==4:
                player.bank-=200
                player.hotels_owned=1
                rent[37]+=5*50
            print(f" {player.name} has build {houses[37]} house(s), and {player.hotels_owned} hotel in {blocks[37]}")
            if houses[39]<4:
                player.bank-=200
                houses[39]+=1
                rent[39]+=houses[39]*50
            if houses[39]==4:
                player.bank-=200
                player.hotels_owned=1
                rent[39]+=5*50
            print(f" {player.name} has build {houses[39]} house(s), and {player.hotels_owned} hotel in {blocks[39]}")
    elif 1<player.build[5]+player.build[15]+player.build[25]+player.build[35]<5:   
        for i in range(1,5):
            index = 5 + 10 * (i - 1)
            if player.build[index] == 1:
                st=player.build[5] + player.build[15] + player.build[25] + player.build[35]
                rent[index] = 25 * (2**(st-1))
                print(f" {player.name} owns {st} stadium(s) and rent now is {rent[index]} for {blocks[index]}") 
    elif player.build[12]+player.build[28]<3:
        if player.build[12]+player.build[28]==2:
            rent[12]=(d1+d2)*10
            rent[28]=(d1+d2)*10
            print(f" {player.name} owns both of utilities {blocks[12]} and {blocks[28]} and rent now is 10 times the dice, that is {rent[12]} EURO")
        if player.build[12]+player.build[28]==1:
            if player.build[12]==1:
                rent[12]=(d1+d2)*4
                print(f" {player.name} owns utility {blocks[12]} and rent now is 4 times the dice, that is {rent[12]} EURO")
            if player.build[28]==1:
                rent[28]=(d1+d2)*4
                print(f" {player.name} owns utility {blocks[28]} and rent now is 4 times the dice, that is {rent[28]} EURO")
op=-1
#Main turn (buy, rent, etc)
def mainturn(player):
    pos = player.pos
    if player.own[pos] == -1: 
        print(f"{player.name} stepped on {blocks[pos]} (block {pos}).The property is free")
        if player.bank > purchase[pos]:
            if pos<10:
                if player.style==1:
                    r = random.randint(1, 100)
                    if r<95:
                        player.own[pos] = 1                                                        
                        player.bank -= purchase[pos]  
                        print(f"{player.name} has just bought {blocks[pos]}.The rent for this property is {rent[pos]} EURO")
                        player.n_own+=1
                        player.build[pos]=1
                        buildR(player)
                    else:
                        print(f"{player.name} prefers not to buy {blocks[pos]}.")
                elif player.style==2:
                    r = random.randint(1, 100)
                    if r<75:
                        player.own[pos] = 1                                                         
                        player.bank -= purchase[pos]  
                        print(f"{player.name} has just bought {blocks[pos]}.The rent for this property is {rent[pos]} EURO")
                        player.n_own+=1
                        player.build[pos]=1
                        buildR(player)
                    else:
                        print(f"{player.name} prefers not to buy {blocks[pos]}.")
                elif player.style==3:
                    r = random.randint(1, 100)
                    if r<95:
                        player.own[pos] = 1                                                         
                        player.bank -= purchase[pos]  
                        print(f"{player.name} has just bought {blocks[pos]}.The rent for this property is {rent[pos]} EURO")
                        player.n_own+=1
                        player.build[pos]=1
                        buildR(player)
                    else:
                        print(f"{player.name} prefers not to buy {blocks[pos]}.")
                elif player.style==4:
                    r = random.randint(1, 100)
                    if r<25:
                        player.own[pos] = 1                                                         
                        player.bank -= purchase[pos]  
                        print(f"{player.name} has just bought {blocks[pos]}.The rent for this property is {rent[pos]} EURO")
                        player.n_own+=1
                        player.build[pos]=1
                        buildR(player)
                    else:
                        print(f"{player.name} prefers not to buy {blocks[pos]}.")
            elif 10<pos<20:
                if player.style==1:
                    r = random.randint(1, 100)
                    if r<95:
                        player.own[pos] = 1                                                        
                        player.bank -= purchase[pos]  
                        print(f"{player.name} has just bought {blocks[pos]}.The rent for this property is {rent[pos]} EURO")
                        player.n_own+=1
                        player.build[pos]=1
                        buildR(player)
                    else:
                        print(f"{player.name} prefers not to buy {blocks[pos]}.")
                elif player.style==2:
                    r = random.randint(1, 100)
                    if r<75:
                        player.own[pos] = 1                                                         
                        player.bank -= purchase[pos]  
                        print(f"{player.name} has just bought {blocks[pos]}.The rent for this property is {rent[pos]} EURO")
                        player.n_own+=1
                        player.build[pos]=1
                        buildR(player)
                    else:
                        print(f"{player.name} prefers not to buy {blocks[pos]}.")
                elif player.style==3:
                    r = random.randint(1, 100)
                    if r<75:
                        player.own[pos] = 1                                                         
                        player.bank -= purchase[pos]  
                        print(f"{player.name} has just bought {blocks[pos]}.The rent for this property is {rent[pos]} EURO")
                        player.n_own+=1
                        player.build[pos]=1
                        buildR(player)
                    else:
                        print(f"{player.name} prefers not to buy {blocks[pos]}.")
                elif player.style==4:
                    r = random.randint(1, 100)
                    if r<50:
                        player.own[pos] = 1                                                         
                        player.bank -= purchase[pos]  
                        print(f"{player.name} has just bought {blocks[pos]}.The rent for this property is {rent[pos]} EURO")
                        player.n_own+=1
                        player.build[pos]=1
                        buildR(player)
                    else:
                        print(f"{player.name} prefers not to buy {blocks[pos]}.")
            elif 20<pos<30:
                if player.style==1:
                    r = random.randint(1, 100)
                    if r<95:
                        player.own[pos] = 1                                                        
                        player.bank -= purchase[pos]  
                        print(f"{player.name} has just bought {blocks[pos]}.The rent for this property is {rent[pos]} EURO")
                        player.n_own+=1
                        player.build[pos]=1
                        buildR(player)
                    else:
                        print(f"{player.name} prefers not to buy {blocks[pos]}.")
                elif player.style==2:
                    r = random.randint(1, 100)
                    if r<75:
                        player.own[pos] = 1                                                         
                        player.bank -= purchase[pos]  
                        print(f"{player.name} has just bought {blocks[pos]}.The rent for this property is {rent[pos]} EURO")
                        player.n_own+=1
                        player.build[pos]=1
                        buildR(player)
                    else:
                        print(f"{player.name} prefers not to buy {blocks[pos]}.")
                elif player.style==3:
                    r = random.randint(1, 100)
                    if r<50:
                        player.own[pos] = 1                                                         
                        player.bank -= purchase[pos]  
                        print(f"{player.name} has just bought {blocks[pos]}.The rent for this property is {rent[pos]} EURO")
                        player.n_own+=1
                        player.build[pos]=1
                        buildR(player)
                    else:
                        print(f"{player.name} prefers not to buy {blocks[pos]}.")
                elif player.style==4:
                    r = random.randint(1, 100)
                    if r<75:
                        player.own[pos] = 1                                                         
                        player.bank -= purchase[pos]  
                        print(f"{player.name} has just bought {blocks[pos]}.The rent for this property is {rent[pos]} EURO")
                        player.n_own+=1
                        player.build[pos]=1
                        buildR(player)
                    else:
                        print(f"{player.name} prefers not to buy {blocks[pos]}.")
            elif 30<pos<40:
                if player.style==1:
                    r = random.randint(1, 100)
                    if r<95:
                        player.own[pos] = 1                                                        
                        player.bank -= purchase[pos]  
                        print(f"{player.name} has just bought {blocks[pos]}.The rent for this property is {rent[pos]} EURO")
                        player.n_own+=1
                        player.build[pos]=1
                        buildR(player)
                    else:
                        print(f"{player.name} prefers not to buy {blocks[pos]}.")
                elif player.style==2:
                    r = random.randint(1, 100)
                    if r<75:
                        player.own[pos] = 1                                                         
                        player.bank -= purchase[pos]  
                        print(f"{player.name} has just bought {blocks[pos]}.The rent for this property is {rent[pos]} EURO")
                        player.n_own+=1
                        player.build[pos]=1
                        buildR(player)
                    else:
                        print(f"{player.name} prefers not to buy {blocks[pos]}.")
                elif player.style==3:
                    r = random.randint(1, 100)
                    if r<25:
                        player.own[pos] = 1                                                         
                        player.bank -= purchase[pos]  
                        print(f"{player.name} has just bought {blocks[pos]}.The rent for this property is {rent[pos]} EURO")
                        player.n_own+=1
                        player.build[pos]=1
                        buildR(player)
                    else:
                        print(f"{player.name} prefers not to buy {blocks[pos]}.")
                elif player.style==4:
                    r = random.randint(1, 100)
                    if r<95:
                        player.own[pos] = 1                                                         
                        player.bank -= purchase[pos]  
                        print(f"{player.name} has just bought {blocks[pos]}.The rent for this property is {rent[pos]} EURO")
                        player.n_own+=1
                        player.build[pos]=1
                        buildR(player)
                    else:
                        print(f"{player.name} prefers not to buy {blocks[pos]}.")
        else:
            print(f"{player.name} does not have enough money to purchase {blocks[pos]}.")
    elif player.own[pos] == -2: 
        if player.pos == 30:
            print(f"{player.name} must go to jail right now!")
            player.prison = 1
            player.pos = 10
            print(f"{player.name} is in jail")
        elif player.pos == 0:
            print(f"{player.name} stepped on To Go!")
        elif player.pos == 4:
            print(f"{player.name} must pay tax 200  EURO!")
            player.bank -= 200
            if player.bank<0:
                player.bankrupt="BANK"
        elif player.pos == 38:
            print(f"{player.name} must pay tax 100  EURO!")
            player.bank -= 100
            if player.bank<0:
                player.bankrupt="BANK"
        elif player.pos == 10:
            print(f"{player.name} visits the jail!")
        elif player.pos == 20:
            print(f"{player.name} is relaxing on free parking!")
        elif player.pos in [2, 17, 33]:
            print(f"{player.name} stepped on Community Chest.")
            draw_community(player,players)
        elif player.pos in [7, 22, 36]:
            print(f"{player.name} stepped on Chance.")
            draw_chance(player,players)
    elif player.own[pos] ==1: 
        print(f"The property {blocks[pos]} is owned by current player {player.name}. End turn")
    else: 
        u = player.own[pos]  
        owner = players[u].name
        if player[u].active==True:
            print(f"The property belongs to {owner}. You must pay rent.")
            if player.bank >= 0:  
                player.bank -= rent[pos] 
                players[u].bank += rent[pos]  
                print(f"{player.name} paid {rent[pos]} to {owner}.")
                if player.bank<0:
                    player.bankrupt="OPPONENT"
                    op=u
            else:
                print(f"{player.name} cannot pay {owner}. Consider mortgaging or losing the property!")
                # Handle mortgage or property loss, sthing here
        else:
             print(f"The property belongs to {owner} but he has lost. You must NOT pay anything!")

import random
def die1():
    d1 = random.randint(1, 6)
    return d1
def die2():
    d2 = random.randint(1, 6)
    return d2

def game_is_on(players):
    active_players = [player for player in players if player.bank > 0]
    return len(active_players) > 1

def winner(players):
    active_players = [player for player in players if player.bank > 0]
    if len(active_players) == 1:
        print(f"Congratulations, {active_players[0].name} is the winner with {active_players[0].bank}  EURO!")
    else:
        print("No winner yet.")
k=0
while game_is_on(players) and all(player.turn < num_turns for player in players):
    while i < num_players :
        if players[i].bank > 0:  
            players[i].turn+=1
            print(f"{players[i].name} is the active player!")
            d1=die1()
            d2=die2()
            k=0
            print(f" The dice of {players[i].name} are {d1} and {d2}.")
            if d1==d2:
                players[i].doubledice=+1
                print(f"{players[i].name} will play again due to double dice!")
                k=1
            else:
                players[i].doubledice=0

            if players[i].doubledice==3:
                players[i].doubledice=0
                players[i].prison = 1
                players[i].pos = 10
                print(f"{players.name} rolled 3 doubles in a row. Go to jail!")

            if players[i].prison == 0:
                print(f"He must move {d1+d2} blocks!")
                players[i].pos += d1 + d2
                if players[i].pos > 39:
                    players[i].pos -=39
                    players[i].bank +=200
                    print(f"{players[i].name} passed from starting point. He gained 200 EURO")
                    mainturn(players[i])
                else:
                    mainturn(players[i])
                buildR(players[i])
            elif players[i].prison == 1:
                print(f"{players[i].name} is in jail!")
                if d1 == d2:
                    if k==1:
                        players[i].pos += d1 + d2
                        players[i].prison = 0
                        print(f"{players[i].name} got out of jail due to rolling a double ({d1},{d2})!")
                        mainturn(players[i])
                else:
                    if players[i].get_out_of_jail_free>=1:
                        players[i].get_out_of_jail_free-=1
                        print(f" {players[i].name} used 'Get out of jail Free' card and he got out of jail!")
                    else:
                        print(f" The dice of {players[i].name} are {d1} and {d2}.He can't go out of jail!")
                        players[i].turn_in_prison += 1
                        players[i].doubledice = 0
                    if players[i].turn_in_prison == 3:
                        print(f"{players[i].name} was in jail for 3 turns and must pay 50  EURO to get out.The dice are {d1} and {d2}.")
                        players[i].bank -= 50
                        players[i].prison = 0
                        players[i].turn_in_prison = 0
                        players[i].doubledice = 0
                        mainturn(players[i])
       
        if players[i].bankrupt=="BANK":
            print(f"{players[i].name} has bankrupted and returned the following properties to the bank:")
            for j in range(1, 40): 
                if players[i].own[j]==1:
                    players[i].own[j]=-1
                    houses[j]=0
                    players[i].hotels_owned[j]=0
                    print({blocks[j]})
        elif players[i].bankrupt=="OPPONENT":
            print(f"{players[i].name} has bankrupted and transferred the following properties to {players[op].name}:")
            for j in range(1, 40): 
                if players[i].own[j]==1:
                    players[op].own[j]=-1
                    houses[j]=0
                    players[i].hotels_owned[j]=0
                    print({blocks[j]})

        print(f"In turn No{players[i].turn}, {players[i].name} has {players[i].bank} EURO and holds {players[i].n_own} ownerships! He stepped on block {blocks[players[i].pos]}")
        
        if k == 0:
            i += 1  # Move to the next player
        else:
            print(f"{players[i].name} gets another turn due to rolling doubles!")
            k=0
        print("_______________________________________________________________")
        
    if i==num_players:
        i=0

winner(players)






import classes
import levels
import time
from classes import lnAndDelay
from classes import Player

gameState = True

print("Welcome to the Game!")
print("What is your name?")
name = input("Input Name: ")
Player.name = name

print("Game Started")
while gameState:
    print("What do you want to do? (Note: type help for more information)")
    responce = input()
    responce = responce.lower()
    
    if responce == "help":
        inHelpPage = True
        print("Welcome to Help (help)")
        print("Type a number to bring up that page of commands")
        print("10 items on a page")

        while inHelpPage:
            responce = input("Input Page Number or type exit ")
            responce.lower()
    
    
            if responce == "1":
                print("Help Page 1 (help/page1)")
                print("stats - Displays your current stats (ex. Coins, Gems, Health, etc.)")
                print("map - displays map; you can start missions from here")
                print("store - enter the store and get items")
                print("gemStore - enter a store for using just gems")
                print("inventory - shows current items in inventory")
                print("quit - exits the game (no save files implemented yet)")
    
    
            elif responce == "exit":
                print("Leaving Help (help/exit)")
                inHelpPage = False
    
    
            else:
                print("Something Went Wrong")
                print("Please Try Again")
    
    
    
    elif responce == "stats":
        print("Stats (stats)")
        print("{} (Level {} XP: {}/{})".format(name, Player.level, Player.experience, Player.level * 1000))
        print("Coins: {}".format(Player.coins))
        print("Gems: {}".format(Player.gems))
        print("Current Health: {}/{}".format(Player.health, Player.maxHealth))

    
    
    elif responce == "map":
        print("There is currently one world on the map. Type 1 to open that world (map)")
        inMap = True
        while inMap:
            responce = input("Please Type World Number or other command ")
    
    
            if responce == "1":
                print("World 1 (map/world1)")
                print()
                print("World 1-1")
                print("World 1-2")
                print("World 1-3")
                print()
                responce = input("Type the second number to select that level ")
    
                if responce == "1":
                    print("World 1-1 (map/world1/level1)")
                    levels.world1lev1()
    
                elif responce == "2":
                    print("World 1-2 (map/world1/level2)")
                    levels.world1lev2()
    
                elif responce == "3":
                    print("World 1-3 (map/world1/level3)")
                    levels.world1lev3()
    
    
            elif responce == "exit":
                inMap = False
                print("Leaving Map (map/exit)")
    
    
            else:
                print("Something went wrong")
                print("Please try again")
    
    
    
    elif responce == "inventory":
        Player.editInventory()
    

    elif responce == "store":
        print("Welcome to the store! (store)")
        print("buy - Buy Items; sell - Sell Items from inventory")
        

        inStore = True
        while inStore:
            print()
            responce = str(input("What do you want to do? ")).lower()
            print()

            if responce == "buy":
                buying = True
                while buying:
                    print("Type the selection number to buy the item.")
                    print("ID: 1    5 EXP Points    1 Gold Coin")
                    print("ID: 2    Lesser Healing Poition (5 HP) 10 Gold Coins")
                    print("ID: 3    Healing Potion (15 HP) 30 Gold Coins")
                    print("ID: 4    Stone Sword (7 damage)  25 Gold Coins")
                    print("ID: 5    Leather Tunic (3 Defence)   25 Gold Coins")

                    print()
                    responce = str(input("What do you want to buy (type exit to leave)? ")).lower()
                    print()

                    if responce == "1":
                        responce = int(input("How many? "))
                        print()
                        coinsNeeded = 1 * responce
                        if Player.coins >= coinsNeeded:
                            Player.coins -= coinsNeeded
                            Player.addExperience(coinsNeeded * 5)
                            print("Bought {} EXP Points".format(coinsNeeded * 5))
                        else:
                            print("You don't have enough coins.")
                    
                    elif responce == "2":
                        responce = int(input("How many? "))
                        print()
                        coinsNeeded = 10 * responce
                        if Player.coins >= coinsNeeded:
                            Player.coins -= coinsNeeded
                            for i in range(0, responce):
                                Player.addToInventory(classes.HealthConsumable("Lesser Healing Poition", 1, 10, 2, 5))
                            print("Bought {} Lesser Healing Poition(s).".format(responce))
                        else:
                            print("You don't have enough coins.")
                    
                    elif responce == "3":
                        responce = int(input("How many? "))
                        print()
                        coinsNeeded = 30 * responce
                        if Player.coins  >= coinsNeeded:
                            Player.coins -= coinsNeeded
                            for i in range (0, responce):
                                Player.addToInventory(classes.HealthConsumable("Healing Poition", 1, 30, 7, 15))
                            print("Bought {} Healing Poition(s).".format(responce))
                        else:
                            print("You don't have enough coins.")

                    elif responce == "4":
                        if Player.coins >= 25:
                            Player.coins -= 25
                            Player.addToInventory(classes.Weapon("Stone Sword", 1, 25, 5, 7))
                            print("Bought a stone sword.")
                        else:
                            print("You don't have enough coins.")
                    
                    elif responce == "5":
                        if Player.coins >= 25:
                            Player.coins -= 25
                            Player.addToInventory(classes.Armor("Leather Tunic", 1, 25, 7, 3))
                            print("Bought a Leather Tunic.")
                        else:
                            print("You don't have enough coins.")

                    elif responce == "exit":
                        buying = False

                    else:
                        print("What did you say?")

            elif responce == "sell":
                selling = True
                while selling:
                    print("Inventory")
                    Player.printInventory()
                    responce = input("Type an item id to sell it. (Or Type Exit to Leave) ")
                    if responce == "exit":
                        selling = False
                    else:
                        try:
                            responce = int(responce)
                            Player.sellFromInventory(responce)
                        except TypeError:
                            print("Not Valid Input.")
                        except ValueError:
                            print("Not Valid Input.")

            elif responce == "exit":
                inStore = False
                    
    

    elif responce == "quit":
        print("Thanks for playing")
        input()
        gameState = False
    
    
    
    else:
        print("Something went wrong")
        print("Please Try Again")
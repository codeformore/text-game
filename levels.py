from classes import lnAndDelay
import classes
from classes import Player

def world1lev1():
    lnAndDelay("INTO THE TEXT", 3)
    lnAndDelay("By: Caden Fischer", 3)
    print()
    lnAndDelay("A New Adventure awaits, {}!".format(Player.name), 4)
    lnAndDelay("You awake from a deep sleep.", 1.5)
    lnAndDelay("You find yourself in your tent.", 2.5)
    lnAndDelay("You get out of your tent and find yourself in the middle of a forest.", 5)
    lnAndDelay("There is one path to the north", 1.5)
    print()
    print("Basic Controls")
    print("Type a command when prompted.")
    print("n - north; e - east; s - south; w - west")
    print("inv - opens up your inventory")
    print()

    awaitCommand = True
    theInput = ""
    while awaitCommand:
        print()
        theInput = str(input("What do you want to do? ")).lower()
        print()

        if theInput == "n":
            lnAndDelay("You follow the path to the north.", 2.5)
            lnAndDelay("You notice it's getting darker and darker.", 3.5)
            lnAndDelay("You see a bag on the ground.", 1.5)
            lnAndDelay("You can continue on the path to the north.", 2.5)

            aAwaitCommand = True
            searchedBag = True
            while aAwaitCommand:
                print()
                theInput = str(input("What do you want to do? ")).lower()
                print()

                if theInput == "n":
                    lnAndDelay("You exit the forest and enter a vast, open field", 3)
                    lnAndDelay("You continue to walk north as it gets darker and darker", 4)
                    lnAndDelay("As the last bit of light slips away, you see something glisten in the corner of your eye.", 6)
                    theInput = input("Search the glistening object? (y or n) ")
                    bAwaitCommand = True
                    while bAwaitCommand:
                        if theInput == "y":
                            lnAndDelay("You search for the glistening object ...", 3)
                            lnAndDelay("You try to make out the object ...", 3)
                            print("You find a 'Lesser Healing Potion'!")
                            Player.addToInventory(classes.HealthConsumable("Lesser Healing Potion", 1, 10, 2, 5))
                            bAwaitCommand = False
                        elif theInput == "n":
                            lnAndDelay("You decide to continue on the path", 3)
                            bAwaitCommand = False
                        else:
                            print("That's not a yes (y) or a no (n)!")
                    
                    lnAndDelay("You look over a small hill and find a cave to stay in for the night.", 5)
                    lnAndDelay("You try to find a good spot to sleep.", 3)
                    lnAndDelay("You don't, but you sleep anyways.", 2)
                    print()
                    lnAndDelay("This is the end of World 1-1", 2)
                    lnAndDelay("You earned 150 exp!", 2)
                    Player.addExperience(150)
                    print()
                    return

                elif theInput == "e" or theInput == "w":
                    print("Still a lot of trees.")
                elif theInput == "s":
                    print("You decide not to head back to your tent.")
                elif theInput == "search bag" and searchedBag:
                    lnAndDelay("You decide to search the bag ...", 5)
                    lnAndDelay("You find 2 Gold Coins!", 2)
                    Player.coins += 2
                    searchedBag = False
                elif theInput == "inv":
                    Player.editInventory()
                else:
                    print("{} doesn't want to do that".format(Player.name))

        elif theInput == "e" or theInput == "s" or theInput == "w":
            print("Just a bunch of trees")
        elif theInput == "inv":
            Player.editInventory()
        else:
            print("{} doesn't want to do that".format(Player.name))

def world1lev2():
    print()
    lnAndDelay("You wake up from a deep sleep in your cave.", 3)
    lnAndDelay("You walk outside and get blinded by the sunlight", 4)
    lnAndDelay("Your eyes adjust to the light.", 3)
    wolf = classes.enemy("Wolf", 2, 0, 10, classes.LootTable({0: classes.Item("Coins", 1, 3,10), 1: classes.Item("Wolf Tooth", 1, 0, 15), 2: classes.Item("exp", 1, 100, 300)}, [100, 35, 100]))
    lnAndDelay("You are attacked by a Wolf!", 3)
    if classes.battle(Player, wolf):
        del wolf
        lnAndDelay("You beat the wolf to death.", 3)
    else:
        lnAndDelay("You quickly run away from the wolf.", 3)
    lnAndDelay("You continue north.", 2)
    lnAndDelay("You see a small village.", 2)
    lnAndDelay("You head to the village.", 2)
    lnAndDelay("You enter the town, but ...", 5)
    lnAndDelay("No one is here.", 3)
    print()
    lnAndDelay("This is the end of World 1-2", 3.5)
    lnAndDelay("You earned 200 xp!", 1.5)
    Player.addExperience(200)
    print()

def world1lev3():
    print()
    lnAndDelay("You walk into the town", 3)
    lnAndDelay("You see 3 houses. One to the north, east, and south.", 5)
    lnAndDelay("You see a point of interest to the west.", 3)
    inTown = True
    while inTown:
        print()
        responce = str(input("What do you do? ")).lower()
        print()

        if responce == "n":
            lnAndDelay("You search the house to the north.", 3)
            lnAndDelay("It's an older building bulit with clay bricks.", 4)
            lnAndDelay("You the room you enter is dark.", 3)
            if Player.checkInventoryByName("Candle"):
                print("Lit party!!!")
                #Make House Inside (Battle?)
            else:
                lnAndDelay("Maybe if you had a light source you could see the room. ", 5)
        
        elif responce == "e":
            lnAndDelay("You approach an old house.", 2)
            lnAndDelay("You see through the window, a candle that has been lit.", 4)
            lnAndDelay("You enter the house and see it is completly empty.", 3)
            lnAndDelay("The only thing left is a table with a lit candle on it.", 4)
            lnAndDelay("You also see stairs going up to the south.", 3)
            lnAndDelay("The exit is to the west.", 2.5)
            inHouse = True
            candleTaken = False
            gemTaken = False
            while inHouse:
                print()
                responce = str(input("What do you want to do? ")).lower()
                print()

                if responce == "take candle" and not candleTaken:
                    Player.addToInventory(classes.Item("Candle", 1, 8, 3))
                    lnAndDelay("You Took the candle off the table.", 3)
                    candleTaken = True
                
                elif responce == "n" or responce == "e":
                    lnAndDelay("It's a wall.", 3)
                
                elif responce == "w":
                    inHouse = False
                    lnAndDelay("You decide to leave the house.", 2)
                
                elif responce == "s" and not gemTaken:
                    lnAndDelay("You walk up the stairs.", 2)
                    lnAndDelay("You find a shinny object in the corner of the room.", 5)
                    lnAndDelay("You found a gem!", 2)
                    Player.gems += 1
                    lnAndDelay("You head back down stairs.", 3)
                    gemTaken = True

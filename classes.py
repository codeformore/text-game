import time
import random
import math
import sys

class Item():

    def __init__(self, name, ident, bValue, sValue):
        self.name = name
        self.ident = ident
        self.bValue = bValue
        self.sValue = sValue

class Weapon(Item):

    def __init__(self, name, ident, bValue, sValue, attackDamage):
        self.name = name
        self.ident = ident
        self.bValue = bValue
        self.sValue = sValue
        self.attackDamage = attackDamage

class Armor(Item):

    def __init__(self, name, ident, bValue, sValue, defPoints):
        self.name = name
        self.ident = ident
        self.bValue = bValue
        self.sValue = sValue
        self.defPoints = defPoints

class HealthConsumable(Item):

    def __init__(self, name, ident, bValue, sValue, healthPointsRestored):
        self.name = name
        self.ident = ident
        self.bValue = bValue
        self.sValue = sValue
        self.healthPointsRestored = healthPointsRestored

class LootTable(object):
    
    #The loot must match the same index as the chance object (use id system)
    def __init__(self, loot, chance):
        self.loot = loot
        self.chance = chance
    
    def giveLootToPlayer(self, playerToAdd):
        for ID in self.loot:
            lootToGive = self.loot[ID]
            chance = random.randint(0, 100)
            if lootToGive.name.lower() == "coins":
                #bValue is lowest amount; sValue is highest amount; of coins collected
                playerToAdd.coins += random.randint(lootToGive.bValue, lootToGive.sValue)
            elif lootToGive.name.lower() == "gems":
                playerToAdd.gems += random.randint(lootToGive.bValue, lootToGive.sValue)
            elif lootToGive.name.lower() == "exp":
                playerToAdd.addExperience(random.randint(lootToGive.bValue, lootToGive.sValue))
            else:
                if chance <= self.chance[ID]:
                    playerToAdd.addToInventory(lootToGive)

class Player():

    uniq = 0
    coins = 25
    gems = 0
    experience = 0
    maxHealth = 15
    inventory = {}
    name = ""
    health = maxHealth
    level = 1
    weaponSlot = Weapon("Fists", 0, 0, 0, 2)
    armorSlot = None

    @staticmethod
    def dealDamage(target):
        target.takeDamage()
    
    @staticmethod
    def takeDamageRaw(damageTaken):
        Player.health -= damageTaken
        if Player.health <= 0:
            print("You take your last breaths")
            print("You think about your adventrue and how far you come.")
            print("You did this all to be struck down, never to come back up")
            print("Good Night, forever ...")
            input("Press Enter to take final breath. ")
            sys.exit()

    @staticmethod
    def takeDamage(damageTaken):
        trueDamageTaken = random.randint(damageTaken - damageTaken//2, damageTaken + damageTaken//2)
        if Player.armorSlot == None:
            
            Player.health -= trueDamageTaken
        else:
            finalDamage = trueDamageTaken - Player.armorSlot.defPoints
            if finalDamage <= 0:
                Player.health -= finalDamage
        
        if Player.health <= 0:
            print("You take your last breaths")
            print("You think about your adventrue and how far you come.")
            print("You did this all to be struck down, never to come back up")
            print("Good Night, forever ...")
            input("Press Enter to take final breath. ")
            sys.exit()

    @staticmethod
    def editInventory():
        editingInv = True
        while editingInv:
            print()
            print("Inventory")
            print()
            Player.printInventory()
            print()
            print("List of commands:")
            print("equip")
            print("trash")
            print("use")
            print("exit")
            print()
            responce = str(input("Command: ")).lower()
            print()

            if responce == "equip":
                try:
                    responce = int(input("What do you want to equip? "))
                    Player.equipItem(responce)
                except:
                    print("Command Failed")
            elif responce == "trash":
                try:
                    responce = int(input("What do you want to trash? "))
                    Player.trashItem(responce)
                except:
                    print("Trash Failed")
            elif responce == "use":
                try:
                    responce = int(input("What do you want to use? "))
                    Player.useItem(responce)
                except:
                    print("Didn't use item.")
            elif responce == "exit":
                editingInv = False
            else:
                print("Not Valid Command")
    
    @staticmethod
    def checkInventoryByName(itemNameToCheck):
        for item in Player.inventory:
            if Player.inventory[item].name == itemNameToCheck:
                return True
        return False
    
    @staticmethod
    def getItemIDByName(itemNameToCheck: str):
        for item in Player.inventory:
            if Player.inventory[item].name == itemNameToCheck:
                return item
        print("{} Not Found".format(itemNameToCheck))

    @staticmethod
    def equipItem(itemId):
        try:
            itemToEquip = Player.inventory[itemId]
            itemToEquipType = type(itemToEquip)
            if itemToEquipType == Armor:
                if Player.armorSlot != None:
                    Player.inventory[Player.armorSlot.ident] = Player.armorSlot
                Player.armorSlot = itemToEquip
                del Player.inventory[itemId]
            elif itemToEquipType == Weapon:
                if Player.weaponSlot.name != "Fists":
                    Player.inventory[Player.weaponSlot.ident] = Player.weaponSlot
                Player.weaponSlot = itemToEquip
                del Player.inventory[itemId]
            else:
                print("Not an Item to equip")
        except:
            print("Not an Item to equip")

    @staticmethod
    def useItem(itemId):
        try:
            itemToUse = Player.inventory[itemId]
            itemType = type(itemToUse)

            if itemType == HealthConsumable:
                Player.health += itemToUse.healthPointsRestored
                if Player.health > Player.maxHealth:
                    Player.health = Player.maxHealth
                print("Your Health is now {}/{}".format(Player.health, Player.maxHealth))
                del Player.inventory[itemId]
        except:
            print("Failed To Use Item")
    
    @staticmethod
    def trashItem(itemId):
        try:
            itemToTrash = Player.inventory[itemId]
            print("Trashed {}".format(itemToTrash.name))
            del Player.inventory[itemId]
        except:
            print("Failed to Trash")

    @staticmethod
    def addToInventory(itemToAdd):
        Player.uniq += 1
        itemToAdd.ident = Player.uniq
        Player.inventory[itemToAdd.ident] = itemToAdd
    
    @staticmethod
    def sellFromInventory(itemSell):
        try:
            itemToSell = Player.inventory[itemSell]
            Player.coins += itemToSell.sValue
            print("Sold {} for {} coins.".format(itemToSell.name, itemToSell.sValue))
            del Player.inventory[itemSell]
        except KeyError:
            print("Not Valid ID")
    
    @staticmethod
    def printInventory():
        for i in Player.inventory:
            itemToPrint = Player.inventory[i]
            whatIsIt = type(itemToPrint)

            if whatIsIt == Item:
                print("id: {}   {}   Buy Price: {}   Sell Price: {}".format(itemToPrint.ident, itemToPrint.name, itemToPrint.bValue, itemToPrint.sValue))
            elif whatIsIt == Weapon:
                print("id: {}   {}   Buy Price: {}   Sell Price: {}  Attack Damage: {}".format(itemToPrint.ident, itemToPrint.name, itemToPrint.bValue, itemToPrint.sValue, itemToPrint.attackDamage))
            elif whatIsIt == Armor:
                print("id: {}   {}   Buy Price: {}   Sell Price: {}  Defence Points: {}".format(itemToPrint.ident, itemToPrint.name, itemToPrint.bValue, itemToPrint.sValue, itemToPrint.defPoints))
            elif whatIsIt == HealthConsumable:
                print("id: {}   {}   Buy Price: {}   Sell Price: {}  Restores {} HP".format(itemToPrint.ident, itemToPrint.name, itemToPrint.bValue, itemToPrint.sValue, itemToPrint.healthPointsRestored))

    @staticmethod
    def addExperience(exp):
        Player.experience += exp
        pastLevel = Player.level
        Player.level = math.floor(Player.experience/1000) + 1
        if Player.level == 0:
            Player.level = 1
        if pastLevel != Player.level:
            print("Level Up!")
            print("You are now level {}!".format(Player.level))
            print("Plus 5 max health!")
            Player.maxHealth += 5
            Player.health = Player.maxHealth
        else:
            print("Level: {} XP: {}/{}".format(Player.level, Player.experience, Player.level * 1000))

class enemy(object):

    def __init__(self, name, damage, defence, health, loot):
        Player.name = name
        Player.damage = damage
        Player.defence = defence
        Player.health = health
        Player.loot = loot
    
    def attack(self, playerToAttack):
        playerToAttack.takeDamage(Player.damage)
    
    def takeDamage(self, damageTaken):
        trueDamageTaken = random.randint(damageTaken - damageTaken//2, damageTaken + damageTaken//2)
        finalDamage = trueDamageTaken - Player.defence
        if finalDamage >= 0:
            Player.health -= finalDamage

#Future Add Support For Multiple Enemies
def battle(playerFight, enemyToFight):
    print()
    print("BATTLE START!")
    print()
    didYouWin = False
    inBattle = True
    while inBattle:
        print("{} has {} HP".format(enemyToFight.name, enemyToFight.health))
        print("You have {}/{} HP".format(playerFight.health, playerFight.maxHealth))
        responce = str(input("f - fight; i - inv; r - run away; incorrect input - skip turn ")).lower()
        print()

        if responce == "f":
            enemyToFight.takeDamage(playerFight.weaponSlot.attackDamage)
        elif responce == "i":
            playerFight.editInventory()
        elif responce == "r":
            print("You decide to run away.")
            runDamage = 4 * (playerFight.health // 5)
            coinsLost = playerFight.coins/4 + enemyToFight.health/4, -1
            print("You lost {} health and {} coins".format(runDamage ,coinsLost))
            playerFight.takeDamageRaw(runDamage)
            playerFight.coins -= coinsLost
            inBattle = False
        
        if inBattle:
            if enemyToFight.health <= 0:
                print("You Won!")
                enemyToFight.loot.giveLootToPlayer(playerFight)
                del enemyToFight
                didYouWin = True
                inBattle = False
            else:
                enemyToFight.attack(playerFight)
    return didYouWin

def lnAndDelay(words, delayTime):
    print(words)
    time.sleep(delayTime)
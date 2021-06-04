import classes
import json
import abc
from classes import Player

#Requirement base class
class Requirement(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def CheckRequirement(self) -> bool:
        pass

#Types of requirements
class checkForItem(Requirement):

    def __init__(self, itemToCheck: str):
        self.itemToCheck = itemToCheck

    def CheckRequirement(self) -> bool:
        itemFound = False
        if Player.getItemIDByName(self.itemToCheck) is not None:
            itemFound = True
        return itemFound

#Sub Action base class
class SubAction(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def RunSubAction(self):
        pass

#Types of sub actions (more to be implemented)
#GiveItem gives the player the item dictated by the itemType and itemToGive
class GiveItem(SubAction):

    def __init__(self, itemToGive: dict):
        itemType = itemToGive["type"]
        #If-else each item class to find one that matches itemType and assign accordingly
        if itemType == "item":
            try:
                self.ItemToGive = classes.Item(itemToGive["name"], 1, itemToGive["bValue"], itemToGive["sValue"])
            except:
                print("The following item failed to import. {}".format(itemToGive))
        elif itemType == "weapon":
            try:
                self.ItemToGive = classes.Weapon(itemToGive["name"], 1, itemToGive["bValue"], itemToGive["sValue"], itemToGive["attackDamage"])
            except:
                print("The following weapon failed to import. {}".format(itemToGive))
        elif itemType == "armor":
            try:
                self.ItemToGive = classes.Armor(itemToGive["name"], 1, itemToGive["bValue"], itemToGive["sValue"], itemToGive["defPoints"])
            except:
                print("The following armor failed to import. {}".format(itemToGive))
        elif itemType == "health-consumable":
            try:
                self.ItemToGive = classes.HealthConsumable(itemToGive["name"], 1, itemToGive["bValue"], itemToGive["sValue"], itemToGive["healthPointsRestored"])
            except:
                print("The following health consumable failed to import. {}".format(itemToGive))
        else:
            print("Failed to import the following object: {}".format(itemToGive))
    
    def RunSubAction(self):
        Player.addToInventory(self.ItemToGive)

#RemoveItem removes an item, specified by the name string, from the player's inventory
class RemoveItem(SubAction):

    def __init__(self, itemToRemove: str):
        self.itemToRemove = itemToRemove
    
    def RunSubAction(self):
        Player.trashItem(Player.getItemIDByName(self.itemToRemove))

#DisplayText displays text to the screen
class DisplayText(SubAction):

    def __init__(self, textToDisplay: str):
        self.textToDisplay = textToDisplay
    
    def RunSubAction(self):
        print(self.textToDisplay)

#Action class
class Action():

    def __init__(self, actionName: str, hiddenAction: bool, subActions: list[SubAction]):
        self.actionName = actionName
        self.hiddenAction = hiddenAction
        self.subActions = subActions

    def CallAction(self):
        for subAction in self.subActions:
            subAction.RunSubAction()

class Condition():

    def __init__(self, conditionName: str, trueStateActions: list[Action], falseStateActions: list[Action], requirements=[], conditionState=False):
        self.conditionName = conditionName
        self.conditionState = conditionState
        self.changedState = False
        self.trueStateActions = trueStateActions
        self.falseStateActions = falseStateActions
        self.requirements = requirements
    
    def RunActions(self):
        if self.conditionState == False:
            for action in self.falseStateActions:
                action.CallAction()
        elif self.conditionState == True:
            for action in self.trueStateActions:
                action.CallAction()

    def SetConditionTrue(self):
        requirementsPass = True
        for requirement in self.requirements:
            if not requirement.CheckRequirement():
                requirementsPass = False
        
        if requirementsPass == True:
            self.conditionState = True

        if self.changedState == False:
            self.RunActions()
            self.changedState = True
        

    def ToggleStateMan(self):
        self.conditionState = not self.conditionState
    
    def SetStateMan(self, state: bool):
        self.conditionState = state

#Door class
class Door():

    def __init__(self, doorName: str, doorRoom: tuple, doorInfo: dict, conditionList: dict):
        self.doorName = doorName
        if doorInfo["condition"] in conditionList:
            self.doorCondition = conditionList[doorInfo["condition"]]
        else:
            self.doorCondition = None
        self.connectedRoom = tuple(doorInfo["connectedRoom"])
        self.doorRoom = doorRoom
        print("imported door")
    
    def UseDoor(self):
        if self.doorCondition is not None:
            self.doorCondition.SetConditionTrue()
        
        if self.doorCondition == None or self.doorCondition.conditionState == True:
            return self.connectedRoom
        else:
            return None

#Room class
class Room():

    def __init__(self, roomData: dict, conditionList: dict):
        self.position = tuple(roomData["position"])
        self.description = roomData["description"]
        self.doorList={}
        for door in roomData["doors"]:
            self.doorList[door] = Door(door, self.position, roomData["doors"][door], conditionList)

        self.visibleActions = {}
        if "visible-actions" in roomData:
            for action in roomData["visible-actions"]:
                newSubActionList=[]
                for subAction in range(0, len(roomData["visible-actions"][action])):
                    newSubActionList.append(CreateSubActionByType(roomData["visible-actions"][action][subAction]))
                self.visibleActions[action] = Action(action, False, newSubActionList)
        

#Methods to create subactions and requirements
def CreateRequirementByType(requirementData: dict):
    requirementType = requirementData["type"]
    if requirementType == "checkForItem":
        return checkForItem(requirementData["item"]["name"])
    
def CreateSubActionByType(subActionData: dict):
    subActionType = subActionData["type"]
    if subActionType == "giveItem":
        return GiveItem(subActionData["item"])
    elif subActionType == "removeItem":
        return RemoveItem(subActionData["itemName"])
    elif subActionType == "displayText":
        return DisplayText(subActionData["text"])

class levelInfo():

    def __init__(self, levelData: dict):
        
        #Second Create a Dictionary of hidden actions with the name as the key
        self.hiddenActionList={}
        for action in levelData["hidden-actions"]:
            newSubActionList=[]
            for subAction in range(0, len(levelData["hidden-actions"][action])):
                print(type(levelData["hidden-actions"][action][subAction]))
                newSubActionList.append(CreateSubActionByType(levelData["hidden-actions"][action][subAction]))
            self.hiddenActionList[action] = Action(action, True, newSubActionList)
        #print(self.hiddenActionList)

        #Third Create a Dictionary of visible actions with the name as the key
        # self.visibleActionList={}
        # for room in self.roomList:
        #     try:
        #         for action in self.roomList[room]["visible-actions"]:
        #             newSubActionList=[]
        #             for subAction in range(0, len(self.roomList[room]["visible-actions"][action])):
        #                 newSubActionList.append(CreateSubActionByType(self.roomList[room]["visible-actions"][action][subAction]))
        #             self.visibleActionList[action] = Action(action, False, newSubActionList)
        #     except:
        #         print("Room {} does not have visible actions.".format(self.roomList[room]["position"]))

        #Fourth Create a Dictionary of conditions with the condition name as the key
        self.conditionList={}
        for conditionName in levelData["conditions"]:
            requirementList=[]
            if "requirements" in levelData["conditions"][conditionName]:
                for requirement in range(0, len(levelData["conditions"][conditionName]["requirements"])):
                    requirementList.append(CreateRequirementByType(levelData["conditions"][conditionName]["requirements"][requirement]))
            
            trueStateActions=[]
            for actionNum in range(0, len(levelData["conditions"][conditionName]["active"])):
                trueStateActions.append(self.hiddenActionList[levelData["conditions"][conditionName]["active"][actionNum]])
            
            falseStateActions=[]
            for actionNum in range(0, len(levelData["conditions"][conditionName]["notActive"])):
                falseStateActions.append(self.hiddenActionList[levelData["conditions"][conditionName]["notActive"][actionNum]])
            
            self.conditionList[conditionName] = Condition(conditionName, trueStateActions, falseStateActions, requirementList, levelData["conditions"][conditionName]["initialState"])
        
        #Make Room List
        self.roomList={}
        for x in range(0, len(levelData["rooms"])):    
            newRoom = Room(levelData["rooms"][x], self.conditionList)
            self.roomList[newRoom.position] = newRoom
        
        self.introText = levelData["levelIntroText"]
        self.currentRoom = (0,0)
        
        print("Level Import Complete")
        #Debug Log of Everything Imported
        """ print()
        print()
        print("Rooms: ")
        for item in self.roomList:
            print("Room {} imported with following info {}".format(item, self.roomList[item]))
        print()
        print("Hidden Actions:")
        for item in self.hiddenActionList:
            print("{} was imported with the following Sub Actions {}".format(item, self.hiddenActionList[item].subActions))
        print()
        print("Conditions: ")
        for item in self.conditionList:
            print("{} was imported with the following info {}".format(item, self.conditionList[item].conditionName))
        print() """

    def RunPlayerCommand(self, responce: str):
        #Check if the responce is a written command else try doors and visible actions
        if responce == "inventory":
            Player.editInventory()
            return True
        
        for door in self.roomList[self.currentRoom].doorList:
            if responce == "move {}".format(door) or responce == door:
                doorResult = self.roomList[self.currentRoom].doorList[door].UseDoor()
                if doorResult is not None:
                    self.currentRoom = doorResult
                    return True
        
        for action in self.roomList[self.currentRoom].visibleActions:
            if responce == action:
                self.roomList[self.currentRoom].visibleActions[action].CallAction()
        



def LaunchLevel(world, levelNum):
    #Open json file based on level and load the json
    levelFile = open("Levels/level{}-{}.json".format(world, levelNum), "r")
    levelData = json.load(levelFile)
    level = levelInfo(levelData)
    
    #Initalize Parameters
    gameState = True
    
    #Start Adventure
    print(level.introText)
    Player.name = "codeformore"
    while gameState:

        print(level.roomList[level.currentRoom].description)
        responce = input("What do you do, {}? ".format(Player.name))
        level.RunPlayerCommand(responce)

LaunchLevel(1,1)
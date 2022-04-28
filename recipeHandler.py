import json
from gameSettings import craftingIDs

class RecipeHandler():
    def __init__(self):
        self.file = open("recipes.json")
        self.data = json.load(self.file)
        self.recipe = {}

    # return a dictionary with all the details of the recipe
    def getRecipeInfo(self, itemID):
        craftID = 0
        for c, resource in enumerate(self.data):
            if(resource["itemID"] == itemID):
                craftID = c
        return self.data[craftID]

    # returns a dictionary of the resources needed to make the recipe in the form: {itemID : number of blocks needed}
    def getRecipe(self, itemID):
        for recipe in self.data:
            if(recipe["itemID"] == itemID):
                tempDict = dict()
                for itemNeeded in recipe["recipe"]:
                    tempDict[itemNeeded["itemID"]] = itemNeeded["numBlocks"]
                return tempDict
        
    # returns the crafting amount of the new recipe we are crafting
    def getCraftingAmount(self, itemID):
        craftID = 0
        for c, resource in enumerate(self.data):
            if(resource["itemID"] == itemID):
                craftID = c
        return self.data[craftID]['craftingAmount']

    def getAllItemIDs(self):
        nameArr = []
        for id in craftingIDs:
            nameArr.append(self.data[id]['itemID'])
        return nameArr

    def getCraftingShape(self, itemID):
        craftID = 0
        for c, resource in enumerate(self.data):
            if(resource["itemID"] == itemID):
                craftID = c
        return self.data[craftID]['shape']
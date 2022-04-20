import json


class recipeHandler:
    def __init__(self, file):
        self.file = open(file)
        self.data = json.load(self.file)
        self.recipe = {}

    # return a dictionary with all the details of the recipe
    def getRecipeInfo(self, craftingID):
        return self.data[craftingID]

    # returns a dictionary of the resources needed to make the recipe in the form: {itemID : number of blocks needed}
    def getRecipe(self, craftingID):
        for resource in self.data[craftingID]['recipe']:
            self.recipe[resource['itemID']] = resource['numBlocks']
        return self.recipe

    # returns the crafting amount of the new recipe we are crafting
    def getCraftingAmount(self, craftingID):
        return self.data[craftingID]['craftingAmount']
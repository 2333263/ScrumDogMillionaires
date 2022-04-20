#Item class to make implementation of inventory system easier
#Allows inventory to work with items that may not be Block objects
class Item:
    def __init__(self, itemName, itemID):
        self.itemName = itemName
        self.itemID = itemID
        self.amount = 0

    def increase(self):
        self.amount += 1

    def decrease(self):
        self.amount -= 1
    
    def getCount(self):
        return self.amount
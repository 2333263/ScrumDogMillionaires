#Item class to make implementation of inventory system easier
#Allows inventory to work with items that may not be Block objects
class Item:
    def __init__(self, item_name, item_id):
        self.item_name = item_name
        self.item_id = item_id
        self.amount = 0

    def increase(self):
        self.amount += 1

    def decrease(self):
        self.amount -= 1
    
    def getCount(self):
        return self.amount
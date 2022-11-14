""""
comments":
    "These are comment tags that do not define any item and are essentially garbage data, you'd have to try very hard to somehow grab this data x)"

    "                                       HARDNESS OVERHAUL                                       "
    "@Ben you should have enough with these properties to scale breaking speed and time with any tool permutations how you see fit"
    "The hardness property has been separated into five parts: 'breakTime', 'blockHardness', 'itemHardness', 'reqToolType' and 'toolType' "

        "The first 'breakTime' is now explicitly defined as an integer greater than 0 and gives the block the time given to break if the correct tool or above is provided"
        "Measured in milliseconds"

            "0: The block will break instantly if the correct tool hardness (defined later) is provided"
            "100: Example: will take 0.1 seconds to break this block."
            "1000: Example 2: will take 1 seconds to break. etc,"

        "The second hardness variable will now be blockHardness, an integer ranging from 0-5 (subject to change), defined below is what each integer indicates"
        "This is the effective hardness of an item when it is __PLACED AS A BLOCK__ in the world"


            "0: No tool level, anything can break this block"
            "1: Wooden tool level or higher required to break this block"
            "2: Stone tool level or higher required to break this block"
            "3: Iron tool level or higher required to break this block"
            "4: Diamond tool level (maybe higher level implemented later)"
            "5: THIS IS RESERVED FOR UNBREAKABLE BLOCKS ONLY!"

        "The third variable will be itemHardness, an integer ranging from 0-5 (subject to change), defined below is what each integer indicates"
        "This is the effective hardness of an item when it is __USED AS AN ITEM TO BREAK A BLOCK__ in the world"

            "0: No tool level, this will break only blocks with blockHardness 0"
            "1: Wooden tool level, this will break only blocks with blockHardness 1 and below"
            "2: Stone tool level, this will break only blocks with blockHardness 2 and below"
            "3: Iron tool level, this will break only blocks with blockHardness 3 and below"
            "4: Diamond tool level, this will break only blocks with blockHardness 4 and below"
            "5: UNATTAINABLE TOOL, could be used to debug later? Not sure, leaving it for consistency’s sake."

        "The fourth variable will be reqToolType, as implied, this will be the required type of tool needed to break a given block."
        "This is a fix for the otherwise unavoidable issue of breaking given level blocks with any equal given level tool/item"
        "Example: Breaking a stone block with a wooden shovel as opposed to a wooden pickaxe."

            "none: This will be used on blocks that don't require a specific tool to be harvested"
            "axe"
            "pickaxe"
            "shovel"
            "hoe"
            "sword"

        "The fifth and final variable will be toolType, as implied, this will be the type of tool a given item is specified as, used to compare with reqToolType"
        "Ignore the / in front of /axe, /pickaxe, /shovel, /hoe and /sword, just was tired of json error saying there were duplicates"

            "null: reserved for the null item, do not use this."
            "none: reserved for items that are not explicitly tools."
            "axe"
            "pickaxe"
            "shovel"
            "hoe"
            "sword"

"""

class Item:

    #New item logic, much better than the overloaded evilevil evil evileiev evile evil veil evil spirits we had in the original Item file
    def __init__(self, itemID, itemDisplayName, breakTime, blockHardness, itemHardness, reqToolType, toolType, texture, isPlaceable, drops):
        self.itemID = itemID
        self.itemDisplayName = itemDisplayName
        self.breakTime = breakTime
        self.blockHardness = blockHardness
        self.itemHardness = itemHardness
        self.reqToolType = reqToolType
        self.toolType = toolType
        self.texture = texture
        self.isPlaceable = isPlaceable
        self.drops = drops

        self.amount = 0

    #Logic used in break place handler to append and remove from inventory count of a given item
    def increase(self):
        self.amount += 1

    def decrease(self):
        self.amount -= 1

    def getCount(self):
        return self.amount

    #Item properties logic regardless of tool or block. See comments for better understanding
    def getItemId(self):
        return self.itemID
    
    def getItemName(self):
        return self.itemDisplayName
    
    def getBreakTime(self):
        return self.breakTime

    def getBlockHardness(self):
        return self.blockHardness

    def getItemHardness(self):
        return self.itemHardness
    
    def getReqToolType(self):
        return self.reqToolType
    
    def getToolType(self):
        return self.toolType

    def getTexture(self):
        return self.texture
    
    def getIsPlaceable(self):
        return self.isPlaceable

    def getDrop(self):
        return self.drops

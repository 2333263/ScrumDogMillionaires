from item import Item
from game_settings import itemIDs

#Init inv with item objects
hotbar_arr = []

for item in itemIDs:
    hotbar_arr.append(Item(itemIDs[item], item))

global selected;
selected = 0;

def add_block(block):
    #Updates based on ItemID - need to ensure hotbar arr has all items added first
    hotbar_arr[block.itemID].increase()


def decrease():
    #decreases currently selected item
    hotbar_arr[selected].decrease()


def decreaseSpec(i):
    # decreases a specific item based on id
    hotbar_arr[i].decrease()

def get_selected():
    #Returns the selected item
    return hotbar_arr[selected]


def set_selected(i):
    selected = i

def select_next():
    #Changes the selected item to the next element in hotbar_arr
    #Loops around if too big
    global selected
    if (selected + 1 <= len(hotbar_arr)-1):
        selected += 1
    else:
        selected = 0


def select_previous():
    #Changes the selected item to the previous element in hotbar_arr
    #Loops around if too small
    global selected
    if (selected == 0):
        selected =len(hotbar_arr)-1
    else:
        selected-=1

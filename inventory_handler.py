from item import Item

#Init inv with item objects
hotbar_arr = []
hotbar_arr.append(Item('Grass', 0))
hotbar_arr.append(Item('Dirt', 1))
hotbar_arr.append(Item('Stone', 2))
hotbar_arr.append(Item('Cloud', 3))
global selected;
selected = 0;


def add_block(block):
    #func will need to change when we move away from colours

    if(block.itemID == 0):
        #Grass
        hotbar_arr[0].increase()
        
    elif(block.itemID == 1):
        #Dirt
        hotbar_arr[1].increase()

    elif (block.itemID == 2):
        #Stone
        hotbar_arr[2].increase()

    elif (block.itemID == 3):
        #Cloud
        hotbar_arr[3].increase()

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

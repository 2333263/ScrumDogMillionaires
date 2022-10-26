In order to add new items and crafting recipies into the game you will need to navigate to where you installed main game package.

## Add new items
* Go to ```install_location\Scrum-Dog-Millionaires\MainGame\Items\items.json```
* Add an entry in the following format:

```json
"itemname:" {
        "itemID": integer representng item ID,
        "itemDisplayName": "string representing the in game name of the item",
        "breakTime": integer representing time in miliseconds needed to break the block, please set to 99999 if the you're adding an item,
        "blockHardness": integer representing what level of tool is neede to break the block, please set to 0 if you're adding an item,
        "itemHardness": inteer representing the level of the tool, please set to 0 if you're adding a block.
        "reqToolType": "string representing what type of tool is needed to break the block if youre adding an item set it to "none"",
        "toolType":"string representing what type of tool the item is, if you are adding a item set it to "none"",
        "texture": "string that is a file path to a png of the texure, please note there is a texture file if you want to put the image there",
        "isPlaceable": boolean representing if the new item is placeable: false for items; true for blocks,
        "drops": integer representing item id you want this block to drop when broken: set it to itself if you want it to drop itself; -1 if you dont want to drop anything at all; or any other item id in the game
} 
```
* Please note that if you want the block to spawn in the game naturally you will have to edit the chunk generator code in the chunks file.

## Add new crafting recipe
* Go to ```install_location\Scrum-Dog-Millionaires\MainGame\Recipes\recipes.json ```
* Add an entry in the following format
```json
{
    "craftingID": integer representing its ID in the crafting table,
    "toolName": "string representing the name of the item being crafted",
    "itemID": integer representing the item ID of the item being crafted,
    "craftingAmount": integer representing the number of items placed in the players inventory when crafted (ie 1 plank becomes 4 logs),
    "recipe": list of items needed for the recipe in the following format
        [
            {
                "itemID": integer representing the item ID of the material,
                "numBlocks": integer reprsendting the amount of this material needed in the recipie
            }
            to have more than one item in the crafting recipie add a comma and another item to the list in the same format
        ],
    "shape": list of item ids, in the position they are in the table in the format as follows
            [-1,-1,-1
            -1,-1,-1,
            -1,-1,-1]
            -1 represents a blank position in the crafting table, swap these -1s for the item id of the material that goes in that position


}
```

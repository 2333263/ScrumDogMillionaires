from MainGame.Settings import gameSettings as gs
from MainGame.Chunks.ChunkGenerator import generateChunk
#this function updates which chunks ids should be loaded into the world
def updateChunkPositions(playerChunk):
    gs.visibleChunks[0] = playerChunk - 1
    gs.visibleChunks[1] = playerChunk
    gs.visibleChunks[2] = playerChunk + 1
def checkChunkUpdates(player, worldBlocks):
    #get the new chunk number the player is in
    newPlayerChunk = (player.rect.x//gs.blockSize)//gs.CHUNK_SIZE[0]
    #if the new chunk isnt the same as the center chunk
    if(newPlayerChunk != gs.visibleChunks[1]):  
        #if it is to the right of the current player  
        if(newPlayerChunk < gs.visibleChunks[1]):
            #unload the left most chunk from the world
            worldBlocks.remove(gs.generatedChunks[gs.visibleChunks[2]])
            #update the player chunks
            updateChunkPositions(newPlayerChunk)
            #if there isnt a a chunk with that id already
            if(gs.visibleChunks[0] not in gs.generatedChunks):
                #generate a new one
                gs.generatedChunks[gs.visibleChunks[0]] = generateChunk(gs.CHUNK_SIZE[0] * gs.visibleChunks[0], worldBlocks)
            else:
                #else load it in
                worldBlocks.add(gs.generatedChunks[gs.visibleChunks[0]])
        else:
            #same as above but fot the other direction
            if(newPlayerChunk > gs.visibleChunks[1]):
                worldBlocks.remove(gs.generatedChunks[gs.visibleChunks[0]])
                updateChunkPositions(newPlayerChunk)
            if(gs.visibleChunks[2] not in gs.generatedChunks):
                gs.generatedChunks[gs.visibleChunks[2]] = generateChunk(gs.CHUNK_SIZE[0]* gs.visibleChunks[2], worldBlocks)
            else:
                worldBlocks.add(gs.generatedChunks[gs.visibleChunks[2]])
 
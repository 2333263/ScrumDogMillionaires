from MainGame.Settings import gameSettings as gs
from MainGame.Chunks.ChunkGenerator import generateChunk

def updateChunkPositions(playerChunk):
    gs.visibleChunks[0] = playerChunk - 1
    gs.visibleChunks[1] = playerChunk
    gs.visibleChunks[2] = playerChunk + 1
def checkChunkUpdates(player, worldBlocks):

    newPlayerChunk = (player.rect.x//gs.blockSize)//gs.CHUNK_SIZE[0]

    if(newPlayerChunk != gs.visibleChunks[1]):    
        if(newPlayerChunk < gs.visibleChunks[1]):
            worldBlocks.remove(gs.generatedChunks[gs.visibleChunks[2]])
            updateChunkPositions(newPlayerChunk)
            if(gs.visibleChunks[0] not in gs.generatedChunks):
                gs.generatedChunks[gs.visibleChunks[0]] = generateChunk(gs.CHUNK_SIZE[0] * gs.visibleChunks[0], worldBlocks)
            else:
                worldBlocks.add(gs.generatedChunks[gs.visibleChunks[0]])
        else:
            if(newPlayerChunk > gs.visibleChunks[1]):
                worldBlocks.remove(gs.generatedChunks[gs.visibleChunks[0]])
                updateChunkPositions(newPlayerChunk)
            if(gs.visibleChunks[2] not in gs.generatedChunks):
                gs.generatedChunks[gs.visibleChunks[2]] = generateChunk(gs.CHUNK_SIZE[0]* gs.visibleChunks[2], worldBlocks)
            else:
                worldBlocks.add(gs.generatedChunks[gs.visibleChunks[2]])
 
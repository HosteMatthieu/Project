# Custom class that handles the late inclusion of nodes on a network

class BlockBuffer:
    
    def __init__(self):
        self.__blockSet = set()  # Du
        
    # This function tries to add a pending block, and returns false if we already have it. It allows us to not broadcast a block we already broadcasted before.
    def try_add_block(self, block):
        if block in self.__blockSet:
            return False
        self.__blockSet.add(block)
        return True
        
    # This function returns all blocks in a row that continue the blockchain starting index latestBlockIndex+1, and that we have in our buffer. For each block we return, we remove it from the buffer since it will be added in the blockchain.
    def get_next_blocks(self, latestBlockIndex):
        nextIndex = latestBlockIndex
        output = []
        while nextIndex == latestBlockIndex:
            nextIndex += 1
            for block in list(self.__blockSet):
                if block.indexInBlockchain == nextIndex:
                    output.append(block)
                    latestBlockIndex = nextIndex
                    self.__blockSet.remove(block)
        return output
    
    # This function returns all indices that lie between latestBlockIndex and the minimum of all indices in our buffer.
    def get_missing_indices(self, latestBlockIndex):
        smallestIndexInBuffer = None
        for block in self.__blockSet:
            if (smallestIndexInBuffer is None) or (smallestIndexInBuffer > block.indexInBlockchain):
                smallestIndexInBuffer = block.indexInBlockchain
        return list(range(latestBlockIndex + 1, smallestIndexInBuffer))
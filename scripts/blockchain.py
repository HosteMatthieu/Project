from helpers import cryptography
from block import Block

class Blockchain:
    
    @staticmethod                # Static function
    def build_genesis_block():   # Here we build the genesis block and return it
        blackHolePublicKey = cryptography.get_black_hole_public_key()  # The black hole is the issuer
        defaultHash = cryptography.get_default_hash()                  # No parent
        genesisBlock = Block(blackHolePublicKey, 0, defaultHash, [])   # No certificate
        genesisBlock.timestamp = 0                                     # It exists since dawn of times
        return genesisBlock
    
    def __init__(self):
        genesisBlock = Blockchain.build_genesis_block()   # Any empty blockchain contains at least the genesis block
        self.blockList = [genesisBlock]
    
    def get_latest_block(self):
        return self.blockList[-1]  # In Python, list[-X] gives the Xth element from the end (thanks Python)
    
    def is_legit(self): 
        genesisBlock = self.blockList[0]
        if not genesisBlock.equals(Blockchain.build_genesis_block()): # We need to check that genesis block hasn't been tampered with
            return False
        for i in range(1, len(self.blockList)):      # Next, starting index 1, we need to verify each block
            checkingBlock = self.blockList[i]        # Index i
            parentBlock = self.blockList[i - 1]      # Needs verification with index i-1
            if checkingBlock.indexInBlockchain != parentBlock.indexInBlockchain + 1: # If one or both indices are wrongly ordered, it is corrupted
                return False
            if checkingBlock.parentBlockHash != parentBlock.hash(): # If parent hash does not target parent block, it is corrupted
                return False
            if not checkingBlock.is_legit(): # If current block is not legit, it is corrupted
                return False
        return True
        
    def display(self):   # Just display all blocks
        blocks = []
        for block in self.blockList:
            blocks.append(block.display())
        return { 'type': 'Blockchain', 'blocks': blocks }
    
    def contains_certificate(self, certificate):
        for block in self.blockList:         # For each block inside the blockchain...
            for c in block.certificateList:      # For each certificate inside the block...
                if c.equals(certificate):            # If it is the same as the one passed as argument, we return True
                    return True
        return False
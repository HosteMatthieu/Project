
class ProofOfWork:
    
    def __init__(self, difficulty):
        self.difficulty = difficulty   # Puzzle difficulty (K number of zeros starting the hash)

    def solve_puzzle(self, block):
        prefix = '0' * self.difficulty   # Expected hash prefix to solve the puzzle (K zeros)
        while block.hash()[:self.difficulty] != prefix:   # As long as we do not have a hash which starts by K zeros...
            block.nonce += 1                              # We increase the block nonce by one to calculate a new hash
            
    # Deterministic function : we don't need the blockchain for this task, only the next block
    def is_next_block_forger_legit(self, blockList, nextBlock):
        # Verifying the block owner is the legit owner is equivalent to checking for K zeros at the beginning of the block hash
        return nextBlock.hash()[:self.difficulty] == '0' * self.difficulty
    
    def is_blockchain_legit(self, blockchain):
        # Simply check for each block in the blockchain (except genesis block) that the block's hash starts with K zeros
        for block in blockchain.blockList[1:]:
            if not self.is_next_block_forger_legit([], block):
                return False
        return True
from stake import StakingOperation
from ticket import RaffleTicket

class ProofOfStake:
    
    def __init__(self, defaultForgerPublicKey):
        self.defaultForgerPublicKey = defaultForgerPublicKey  # Default forger if no token has been staked yet
        
    def hash_distance(self, hash1, hash2):
        intHash1 = int(hash1, 16)             # Convert hexadecimal hash into integer number
        intHash2 = int(hash2, 16)             # Same
        return abs(intHash1 - intHash2)       # Take the absolute value of the difference as distance
    
    def get_next_forger_public_key(self, blockList):
        stakingAccounts = StakingOperation.build_staking_accounts(blockList) # First we need to know how many tickets to distribute to all stakers
        raffleHash = blockList[-1].hash()  # The raffle hash is the hash of blockchain's last block
        raffleTickets = []                 # We will now generate all raffle tickets
        for staker in stakingAccounts:     # For each staker...
            ticketCount = int(stakingAccounts[staker])   # We count how many tickets to generate for him/her (= amount of staked tokens, rounded down)
            for i in range(ticketCount):                 # For each staked token...
                ticket = RaffleTicket(staker, i, raffleHash)    # We generate a numbered ticket
                raffleTickets.append(ticket)
        if len(raffleTickets) == 0:        # If no token has been staked yet...
            return self.defaultForgerPublicKey   # The raffle winner is the default forger
        winnerTicket = None
        bestDistanceYet = None
        for ticket in raffleTickets:       # For each generated ticket...
            distanceToWin = self.hash_distance(ticket.hash(), raffleHash)  # We calculate the distance to raffle hash
            if (bestDistanceYet is None) or (distanceToWin < bestDistanceYet):  # If this ticket is the closest until now...
                bestDistanceYet = distanceToWin
                winnerTicket = ticket      # We keep it as temporary winner
        return winnerTicket.ownerPublicKey  # We eventually return the owner of the closest of all tickets
    
    # Deterministic function
    def is_next_block_forger_legit(self, blockList, nextBlock):
        return self.get_next_forger_public_key(blockList) == nextBlock.issuerPublicKey  # Checking for forger legality is the same as replaying the raffle
    
    def is_blockchain_legit(self, blockchain):
        # Simply replay all raffles to see if any block as an invalid forger (except for genesis block)
        for i in range(1, len(blockchain.blockList)):
            previousBlocksAtThatTime = blockchain.blockList[:i]  # We need to replay the raffle in time, which means all blocks after block i-1 did not exist yet
            nextBlockAtThatTime = blockchain.blockList[i]  # We are analyzing block i
            if not self.is_next_block_forger_legit(previousBlocksAtThatTime, nextBlockAtThatTime):
                return False
        return True
from network import Node
from certificate import Certificate
from blockchain import Blockchain
from buffer import BlockBuffer
from block import Block

class BlockchainNode(Node):
    
    # A node contains ...
    def __init__(self, wallet, consensusAlgorithm):
        super().__init__(wallet.publicKey)            # ... the properties of a network node ...
        self.wallet = wallet                          # ... a wallet (its identity) ...
        self.consensusAlgorithm = consensusAlgorithm  # ... a consensus algorithm ...
        self.blockchain = Blockchain()                # ... his copy of the blockchain ...
        self.__certificateBox = set()                 # ... his certificate box ...
        self.__blockBuffer = BlockBuffer()            # (Bonus) ... and his block buffer.
        
    # When I receive an object from another node ...
    def receive_object_from_node(self, obj, nodeIdentifier):
        if isinstance(obj, Block):          # ... if it's a block, I try to add it to the blockchain ...
            self.new_block(obj)
        elif isinstance(obj, Certificate):  # ... if it's a certificate, I keep it warm until it is time to forge ...
            self.new_certificate(obj)
        elif isinstance(obj, int):          # (Bonus) ... and if it's an integer, I send the corrsponding block back.
            indexRequested = int(obj)
            if indexRequested >= len(self.blockchain.blockList):
                return
            for block in self.blockchain.blockList:
                if block.indexInBlockchain == indexRequested:
                    self.send_object_to_node(block, nodeIdentifier)
                    return
        
    # This function tries to forge next block, only if we are into the right state, which means...
    def try_forge_next_block(self):
        if len(self.__certificateBox) < 5:  # ... I indeed have 5 certificates or more ...
            return False
        latestBlock = self.blockchain.get_latest_block()
        newBlockIssuerPublicKey = self.wallet.publicKey
        newBlockIndexInBlockchain = latestBlock.indexInBlockchain + 1
        newBlockParentBlockHash = latestBlock.hash()
        newBlockCertificateList = list(self.__certificateBox)
        newBlock = Block(newBlockIssuerPublicKey, newBlockIndexInBlockchain, newBlockParentBlockHash, newBlockCertificateList)
        if not self.consensusAlgorithm.is_next_block_forger_legit(self.blockchain.blockList, newBlock):  # ... and I am next forger.
            return False
        self.__certificateBox = set()
        self.wallet.sign(newBlock)      # Do not forget to sign the block
        self.new_block(newBlock)        # Adding the block to the blockchain
        self.broadcast_object(newBlock) # And broadcasting it to everyone
        return True
        
    # I accept and keep a new certificate if ...
    def new_certificate(self, certificate):
        if not certificate.is_legit():  # ... it is legit ...
            return
        if certificate in self.__certificateBox:  # .. I don't already have it in my box ...
            return
        if self.blockchain.contains_certificate(certificate):  # ... nor in my blockchain.
            return
        self.__certificateBox.add(certificate)
        if not self.try_forge_next_block():  # If I can't forge yet, I broadcast this new certificate to other nodes
            self.broadcast_object(certificate)
            
    # I need to accept a new block if ...
    def new_block(self, block):
        if not block.is_legit():  # ... it is legit ...
            return
        if len(block.certificateList) < 5:  # ... it contains 5 certificates or more ...
            return
        latestBlock = self.blockchain.get_latest_block()
        if latestBlock.indexInBlockchain > block.indexInBlockchain - 1:  # ... its index is right ...
            return
        elif latestBlock.indexInBlockchain < block.indexInBlockchain - 1:  # (Bonus) (if I'm late I send requests to get blocks in-between, keeping the current block for later)
            if self.__blockBuffer.try_add_block(block):
                self.broadcast_object(block)
                missingIndices = self.__blockBuffer.get_missing_indices(latestBlock.indexInBlockchain)
                for missingIndice in missingIndices:
                    self.broadcast_object(missingIndice)
            return
        if latestBlock.hash() != block.parentBlockHash:  # ... its parent has the right hash ...
            return
        if not self.consensusAlgorithm.is_next_block_forger_legit(self.blockchain.blockList, block):  # ... its forger is legit ...
            return
        for certificate in block.certificateList:  # ... and it contains new certificates only.
            if self.blockchain.contains_certificate(certificate):
                return
        # If all conditions are met, I add it to my blockchain and broadcast it to every other node ...
        self.blockchain.blockList.append(block)
        for certificate in block.certificateList:
            if certificate in self.__certificateBox:
                self.__certificateBox.remove(certificate)  # ... without forgetting to remove its certificates from my certificate box.
        self.broadcast_object(block)
        for b in self.__blockBuffer.get_next_blocks(block.indexInBlockchain):  # (Bonus) With this new block, maybe I can add some other blockcs I have in my buffer
            self.new_block(b)
        self.try_forge_next_block()  # If I can forge next block, I do.
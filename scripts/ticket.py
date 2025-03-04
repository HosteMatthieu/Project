from json import dumps
from helpers import cryptography

class RaffleTicket:
    
    def __init__(self, ownerPublicKey, number, raffleHash):
        self.ownerPublicKey = ownerPublicKey                 # Ticket owner
        self.number = number                                 # Ticket number
        self.raffleHash = raffleHash                         # Raffle hash for which this ticket is due (= hash of the last block in the blockchain)
        
    def build_payload(self):                                 # We hash tickets the same way we hash certificates, using a payload
        payload = {}
        payload['ownerPublicKey'] = self.ownerPublicKey
        payload['number'] = self.number
        payload['raffleHash'] = self.raffleHash
        return payload
        
    def hash(self):                                          # Same as certificate
        payload = self.build_payload()
        payloadString = dumps(payload, sort_keys=True)
        return cryptography.hash_string(payloadString)
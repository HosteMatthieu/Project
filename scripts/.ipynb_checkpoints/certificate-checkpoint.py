from helpers import timestamp, cryptography
from json import dumps

class Certificate:
    
    def __init__(self, issuerPublicKey):
        self.issuerPublicKey = issuerPublicKey
        self.timestamp = timestamp.now()        # Date of creation
        self.signature = ''                     # As long as no signature was applied, it is empty
        
    def build_payload(self):
        payload = {}
        payload['issuerPublicKey'] = self.issuerPublicKey  # In the payload we must include the issuer...
        payload['timestamp'] = self.timestamp              # ...but also the creation date
        return payload                                     # Because those values must remain immutable
    
    def hash(self):
        payload = self.build_payload()                     # We want to hash the whole payload
        payloadString = dumps(payload, sort_keys=True)     # Here I use dumps to transform a dictionary into a string, also sort_keys to ensure all keys will be in the same order
        return cryptography.hash_string(payloadString)     # The "cryptography" module does the rest
    
    def equals(self, otherCertificate):
        myHash = self.hash()                   # My hash
        otherHash = otherCertificate.hash()    # The other's hash
        return myHash == otherHash             # If both have the same hash, they are identical
    
    def is_legit(self):                     # A valid certificate...
        publicKey = self.issuerPublicKey    # ...ensures the issuer...
        signature = self.signature          # ...has signed...
        hash = self.hash()                  # ...the certificate's hash
        return cryptography.has_public_key_signed_this_hash(publicKey, signature, hash) # The "cryptography" does the rest
    
    def display(self):
        # Only display a piece of our keys and hashes for readibility (16 characters are enough)
        return { 'type': self.__class__.__name__, 'issuer': f'...{self.issuerPublicKey[256:272]}...', 'timestamp': self.timestamp, 'hash': f'{self.hash()[:16]}...', 'signature': f'{self.signature[:16]}...' }

    def __eq__(self, other):
        return self.equals(other)
    
    def __hash__(self):
        return int(self.hash(), 16)  # Converting hexadecimal hash to integer hash
from helpers import cryptography
from json import dumps, loads

class Wallet:
    
    def __init__(self):
        self.__privateKey = cryptography.generate_random_private_key()    # Random private key
        self.publicKey = cryptography.get_public_key_from_private_key(self.__privateKey)  # Public key is generated using private key
        
    def sign(self, certificate):
        certificateHash = certificate.hash()   # We are signing the hash so we need to generate it
        privateKey = self.__privateKey         # Our private key signs
        certificate.signature = cryptography.sign_hash_with_private_key(certificateHash, privateKey) # We apply the signature to the certificate
        
    def display(self):
        return { 'type': 'Wallet', 'publicKey': f'...{self.publicKey[256:272]}...' } # Only display a piece of our public key for readibility (16 characters are enough)
        # NO PRIVATE KEY !!!

# Defines the base for a cryptography library that will be used in blockchain
# Any cryptography library for the blockchain should use this exact layout, and should treat input and out as strings

class CryptographyBase:
    
    """
    Cryptography library to help with blockchain security.
    
    ALL METHOD INPUTS AND OUTPUTS ARE OF TYPE 'str'
    """
    
    # Generating private/public keys for the wallets and identities

    def generate_random_private_key(self):
        """
        Generates a random private key (str).
        """
        raise NotImplementedError

    def get_public_key_from_private_key(self, privateKey):
        """
        Derives the public key from a given private key.
        """
        raise NotImplementedError
        
    # Multi-purpose hashing

    def hash_string(self, string):
        """
        Transforms any string into another string, such that the tiniest difference between two input strings results in two hashes that are completely different.
        """
        raise NotImplementedError
        
    # Signature handling

    def sign_hash_with_private_key(self, hash, privateKey):
        """
        Generates a signature from the input hash using a private key.
        """
        raise NotImplementedError

    def has_public_key_signed_this_hash(self, publicKey, signature, hash):
        """
        Tells whether the input public key has indeed signed the input hash.
        """
        raise NotImplementedError
        
    # Some constants

    def get_black_hole_public_key(self):
        """
        Returns a public key that represents a wallet noone will ever own.
        """
        raise NotImplementedError

    def get_default_hash(self):
        """
        Returns an arbitrary hash.
        """
        raise NotImplementedError
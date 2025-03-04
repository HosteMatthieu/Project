from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

from .cryptography_base import CryptographyBase

# Defines a cryptography library based on the RSA cryptosystem

class RSACryptography(CryptographyBase):
    
    def __init__(self, rsaStrength):
        self.__rsaStrength = rsaStrength
        self.__dummyPrivateKey = self.generate_random_private_key()
        self.__dummyPublicKey = self.get_public_key_from_private_key(self.__dummyPrivateKey)
        self.__blackHolePublicKey = '0' * len(self.__dummyPublicKey)
        self.__dummyHash = self.hash_string('JUNIA')
        self.__defaultHash = '0' * len(self.__dummyHash)

    def generate_random_private_key(self):
        randomPrivateKeyRSA = RSA.generate(self.__rsaStrength)
        randomPrivateKeyBytes = randomPrivateKeyRSA.exportKey('DER')
        return randomPrivateKeyBytes.hex()

    def get_public_key_from_private_key(self, privateKey):
        privateKeyBytes = bytes.fromhex(privateKey)
        privateKeyRSA = RSA.importKey(privateKeyBytes)
        publicKeyRSA = privateKeyRSA.publickey()
        publicKeyBytes = publicKeyRSA.exportKey('DER')
        return publicKeyBytes.hex()
    
    def __sha256(self, string):
        stringBytes = string.encode()
        return SHA256.new(stringBytes)

    def hash_string(self, string):
        stringHashSHA256 = self.__sha256(string)
        return stringHashSHA256.hexdigest()

    def sign_hash_with_private_key(self, hash, privateKey):
        hashSHA256 = self.__sha256(hash)
        privateKeyBytes = bytes.fromhex(privateKey)
        privateKeyRSA = RSA.importKey(privateKeyBytes)
        signatory = PKCS1_v1_5.new(privateKeyRSA)
        signatureBytes = signatory.sign(hashSHA256)
        return signatureBytes.hex()

    def has_public_key_signed_this_hash(self, publicKey, signature, hash):
        publicKeyBytes = bytes.fromhex(publicKey)
        publicKeyRSA = RSA.importKey(publicKeyBytes)
        hashSHA256 = self.__sha256(hash)
        validator = PKCS1_v1_5.new(publicKeyRSA)
        signatureBytes = bytes.fromhex(signature)
        return validator.verify(hashSHA256, signatureBytes)

    def get_black_hole_public_key(self):
        return self.__blackHolePublicKey

    def get_default_hash(self):
        return self.__defaultHash
from certificate import Certificate

class Block(Certificate):     # A block is also a certificate since it must be signed and protected
    
    def __init__(self, issuerPublicKey, indexInBlockchain, parentBlockHash, certificateList):
        super().__init__(issuerPublicKey)           # Don't forget to call Certificate's constructor
        self.indexInBlockchain = indexInBlockchain
        self.parentBlockHash = parentBlockHash
        self.certificateList = certificateList
        self.nonce = 0                              # For Proof-of-Work
        
    def build_payload(self):
        payload = super().build_payload()           # Don't forget to include Certificate's payload as well since we always need to include issuer and date.
        payload['indexInBlockchain'] = self.indexInBlockchain   # We also need the block index
        payload['parentBlockHash'] = self.parentBlockHash       # And the parent hash
        payloadCertificateList = []
        for certificate in self.certificateList:
            payloadCertificateList.append(certificate.build_payload())  # It is very important to include the data (payload) for all certificate inside the block, as to ensure none can be modified afterwards
        payload['certificateList'] = payloadCertificateList
        payload['nonce'] = self.nonce                                   # For Proof-of-Work
        return payload
    
    def is_legit(self):
        if not super().is_legit():                  # A legit block is a legit certificate
            return False
        for certificate in self.certificateList:    # We then need to check for all certificates inside
            if not certificate.is_legit():
                return False
        # No need to verify that the block index and parent are okay since a block alone doesn't care
        return True
        
    def display(self):    
        output = super().display()                  # Let's use Certificate's display function
        output['index'] = self.indexInBlockchain
        output['parent'] = f'{self.parentBlockHash[:16]}...'   # No need to display the whole hash, 16 characters is enough
        certificates = []
        for certificate in self.certificateList:
            certificates.append(certificate.display())
        output['certificates'] = certificates
        output['nonce'] = self.nonce                           # For Proof-of-Work
        return output
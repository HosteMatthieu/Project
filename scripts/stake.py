from certificate import Certificate

class StakingOperation(Certificate):                    # A staking operation is a certificate
    
    def __init__(self, issuerPublicKey, tokenAmount):
        super().__init__(issuerPublicKey)
        self.tokenAmount = tokenAmount                  # token amount to stake
        
    def build_payload(self):
        payload = super().build_payload()               # Include issuer public key and timestamp
        payload['tokenAmount'] = self.tokenAmount       # Include also the amount of token to stake
        return payload
    
    def display(self):
        output = super().display()                      # Overriding the display function
        output['tokenAmount'] = self.tokenAmount
        return output
    
    @staticmethod
    def build_staking_accounts(blockList):
        output = {}                                     # Output dictionary
        for block in blockList:                         # For each block in ascending order...
            for certificate in block.certificateList:           # For each certificate inside the block...
                if isinstance(certificate, StakingOperation):           # If the certificate is a staking operation...
                    issuerPublicKey = certificate.issuerPublicKey           # We extract the issuer
                    tokenAmount = certificate.tokenAmount                   # And the token amount
                    if issuerPublicKey in output:                           # If the issuer is already known...
                        output[issuerPublicKey] += tokenAmount                  # We add the token amount to his account
                    else:                                                   # Otherwise...
                        output[issuerPublicKey] = tokenAmount                   # We open an account for this issuer
        return output                                   # Returning all accounts
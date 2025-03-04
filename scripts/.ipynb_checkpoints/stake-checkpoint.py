from certificate import Certificate

class StakingOperation(Certificate):                    # Une opération de jalonnement est un certificat
    
    def __init__(self, issuerPublicKey, tokenAmount):
        super().__init__(issuerPublicKey)
        self.tokenAmount = tokenAmount                  # Quantité de jeton à jalonner
        
    def build_payload(self):
        payload = super().build_payload()               # Il est important de considérer aussi la charge utile de l'opération de jalonnement en tant que certificat. On collecte alors son émetteur et sa date de création.
        payload['tokenAmount'] = self.tokenAmount       # On ajoute aussi la quantité de jeton à jalonner
        return payload
    
    def display(self):
        output = super().display()                      # Servons nous de la fonction "display" de Certificate
        output['tokenAmount'] = self.tokenAmount
        return output
    
    @staticmethod
    def build_staking_accounts(blockList):
        output = {}                                     # Dictionnaire à renvoyer
        for block in blockList:                         # Pour chaque bloc dans l'ordre...
            for certificate in block.certificateList:           # Pour chaque certificat dans le bloc...
                if isinstance(certificate, StakingOperation):           # Si le certificat est une opération de jalonnement...
                    issuerPublicKey = certificate.issuerPublicKey           # On prend son émetteur
                    tokenAmount = certificate.tokenAmount                   # Et son nombre de jeton
                    if issuerPublicKey in output:                           # Si l'émetteur est déjà connu...
                        output[issuerPublicKey] += tokenAmount                  # On ajoute le nombre de jeton à son compte
                    else:                                                   # Sinon...
                        output[issuerPublicKey] = tokenAmount                   # On démarre un compte pour cet émetteur
        return output                                   # On renvoie le tout
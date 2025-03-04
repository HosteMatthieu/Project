from certificate import Certificate
from helpers import timestamp

class SmartContractDefinition(Certificate) :

    def __init__(self, issuerPublicKey, sourceCode, Ntoken):
        super().__init__(issuerPublicKey)
        self.sourceCode = sourceCode
        self.Ntoken=Ntoken #Nombre de token qu'on autorise
        self.owners = {} #dictionnaire qui va contenir les NFT et leur propriétaire
        self.mintingStart = None # Date de début de la période de frappe
        self.mintingDuration = None # Durée de la période de frappe (en ms)

    def build_payload(self):
        payload = super().build_payload()
        payload['sourceCode'] = self.sourceCode
        payload['Ntoken']=self.Ntoken
        payload['owners']=self.owners
        return payload
    
    # Frappe le NFT
    def mint(self, ownerPublicKey, nftId):
        if self.is_minting_open() == False:
            raise ValueError("La période de minage est fermée.")
        
        if len(self.owners) < self.Ntoken: #si on a pas atteint la limite
            if nftId not in self.owners: #si l'id n'existe pas
                self.owners[nftId] = ownerPublicKey #on ajoute le NFT
                print("NFT {} minée par {}".format(nftId, ownerPublicKey))
            else:
                raise ValueError("NFT déjà existant")
        else:
            raise ValueError("Nombre de token maximal atteint")
    
    # Ouvre la période de frappe
    def open_minting(self, issuerPublicKey, duration):
        # On vérifie que c'est bien le propriétaire du smart contract qui essaye d'ouvrir la période de frappe
        if issuerPublicKey != self.issuerPublicKey:
            raise ValueError("Seul le propriétaire du smart contract peut ouvrir la période de minage")
        
        self.mintingStart = timestamp.now() # On stocke la date de début
        self.mintingDuration = duration * 1000 # On stocke la durée en ms
        print("Période de minage ouverte pendant {} secondes".format(duration))

    # Verifie si la période de frappe est ouverte
    def is_minting_open(self):
        if self.mintingStart is None or self.mintingDuration is None: #si la date de début ou la durée n'est pas définie
            return False
        return timestamp.now() <= self.mintingStart + self.mintingDuration
    

    def transfer(self, senderPublicKey, receiverPublicKey, nftId):
        if nftId in self.owners: #si le NFT existe
            if self.owners[nftId] == senderPublicKey: #si les propriétaire du NFT correspond bien à l'envoyeur
                self.owners[nftId] = receiverPublicKey #alors on change le propriétaire
                print("NFT {} transférée de {} à {}".format(nftId, senderPublicKey, receiverPublicKey))
            else:
                raise ValueError("NFT n'appartient pas à l'expéditeur")
        else:
            raise ValueError("NFT inexistant")
    

    # generates a Python object from the contract's source code
    def instantiate_contract(self):
        dico = {} #dictionnaire qui va contenir les varirables générées
        exec(self.sourceCode, {}, dico) #on execute le code source et on stocke les variables dans dico
        contract_instance=None

        for obj in dico.values(): #On parcourt les valeurs de dico
            if  isinstance(obj, type): #Quand on trouve une classe on la stocke et on arrete de parcourir
                contract_instance = obj
                break

        if contract_instance is None: #si on a pas trouvé de classe : erreur
            raise ValueError("Pas de classe trouvée")

        return contract_instance(self.issuerPublicKey)

    @staticmethod
    def get_smart_contract_at_current_state(blockchain, targetSmartContractHash):

        smartContract = None
        for certificate in blockchain:
            if isinstance(certificate, SmartContractDefinition) and certificate.hash() == targetSmartContractHash: # on cherche le smart contract dans la blockchain
                smartContract = certificate
                break
        
        smartContract_instance = smartContract.instantiate_contract() #on l'instancie

        all_operations = []
        for certificate in blockchain:
            if isinstance(certificate, SmartContractWritingOperation) and certificate.targetSmartContractHash == targetSmartContractHash: # on recupere les operations
                all_operations.append(certificate)

        sorted_operations = sorted(all_operations, key=lambda x: x.timestamp) # on les trie par timestamp

        for operation in sorted_operations:
            operation.apply_on_contract(smartContract_instance) # On applique les operations sur le smart contract dans l'ordre

        return smartContract_instance


class SmartContractWritingOperation(Certificate) :

    def __init__(self, issuerPublicKey, targetSmartContractHash, targetFunctionName, functionArgumentList):
        super().__init__(issuerPublicKey)
        self.targetSmartContractHash = targetSmartContractHash
        self.targetFunctionName = targetFunctionName
        self.functionArgumentList = functionArgumentList

    def build_payload(self):
        payload = super().build_payload()
        payload['targetSmartContractHash'] = self.targetSmartContractHash
        payload['targetFunctionName'] = self.targetFunctionName
        payload['functionArgumentList'] = self.functionArgumentList
        return payload

    def apply_on_contract(self, contractPythonObject):
        functionToDo = getattr(contractPythonObject, self.targetFunctionName)
        newList = [self.issuerPublicKey] + self.functionArgumentList #on ajoute l'issuerPublicKey à fonctionArgumentList pour qu'il nous manque aucun argument
        return functionToDo(*newList)
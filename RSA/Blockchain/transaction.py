from rsa_public_key import *

class transaction:
    def __init__(self, message, RSAkey):
        """
        genera una transacci´o signant "message" amb la clau "RSAkey"
        """
        self.public_key = rsa_public_key(RSAkey)
        self.message = message
        self.signature = RSAkey.sign(message)

        print("message: " + str(message))
        print("signature: " + str(self.signature))
        print("test: " + str(self.public_key.verify(self.message, self.signature)))

    def verify(self):
        """
        retorna el boole`a True si "signature" es correspon amb una
        signatura de "message" feta amb la clau p´ublica "public_key".
        En qualsevol altre cas retorma el boole`a False
        """
        return self.public_key.verify(self.message, self.signature)
class rsa_public_key:
    def __init__(self, rsa_key):
        """
        genera la clau p´ublica RSA asociada a la clau RSA "rsa_key"
        """
        self.publicExponent = rsa_key.publicExponent
        self.modulus = rsa_key.modulus

    def verify(self, message, signature):
        """
        retorna el boole`a True si "signature" es correspon amb una
        signatura de "message" feta amb la clau RSA associada a la clau
        p´ublica RSA.
        En qualsevol altre cas retorma el boole`a False
        """
        return pow(signature, self.publicExponent, self.modulus) == message

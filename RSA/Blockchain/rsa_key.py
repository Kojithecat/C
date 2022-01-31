from sympy import *
from timeit import default_timer
from transaction import *


class rsa_key:
    def __init__(self, bits_modulo=2048, e=2 ** 16 + 1):
        """
        genera una clau RSA (de 2048 bits i amb exponent p´ublic 2**16+1 per defecte)
        """
        self.publicExponent = e
        self.primeP = randprime(2 ** (bits_modulo-1) + 1, 2 ** bits_modulo - 1)
        self.primeQ = randprime(2 ** (bits_modulo-1) + 1, 2 ** bits_modulo - 1)
        self.modulus = self.primeP * self.primeQ

        self.privateExponent = mod_inverse(self.publicExponent, (self.primeP-1) * (self.primeQ-1))

        self.privateExponentModulusPhiP = self.privateExponent % (self.primeP - 1)
        self.privateExponentModulusPhiQ = self.privateExponent % (self.primeQ - 1)
        self.inverseQModulusP = mod_inverse(self.primeQ, self.primeP)


    def sign(self, message):
        """
        retorma un enter que ´es la signatura de "message" feta amb la clau RSA fent servir el TXR
        """
        a = pow(message, self.privateExponentModulusPhiP, self.primeP)
        b = pow(message, self.privateExponentModulusPhiQ, self.primeQ)

        inversePModulusQ = mod_inverse(self.primeP, self.primeQ)

        res = (a * self.primeQ * self.inverseQModulusP + b * self.primeP * inversePModulusQ) % self.modulus
        return res

    def sign_slow(self, message):
        """
        retorma un enter que ´es la signatura de "message" feta amb la clau RSA sense fer servir el TXR
        """
        return pow(message, self.privateExponent, self.modulus)


if __name__ == "__main__":
    bits_testing = [512, 1024, 2048, 4096]
    messages = [i for i in range(100)] # Missatges de 0 fins a 99

    for bits in bits_testing:
        print(f"TESTING {bits} bits:\n")

        rsa = rsa_key(bits_modulo=bits)

        """TAULA COMPARATIVA ENTRE LA FIRMA LENTA I LA FIRMA RÀPIDA(TXR)"""
        iniTime = default_timer()
        for message in messages:
            rsa.sign(message)
        finTime = default_timer()
        print(f"Temps FIRMA RÀPIDA(TXR) de {bits} bits: {finTime - iniTime}")

        iniTime = default_timer()
        for message in messages:
            rsa.sign_slow(message)
        finTime = default_timer()
        print(f"Temps FIRMA LENTA de {bits} bits: {finTime - iniTime}\n\n")
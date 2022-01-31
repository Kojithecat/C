from hashlib import sha256
from random import randint


def block_hash_generator(block, blockError):
    if not block.transaction.verify():
        print("transaction not valid")
    else:
        while 1:
            block.seed = randint(0, 2 ** 256)  ## Buscar un seed fins que compleixi la condicio
            entrada = str(block.previous_block_hash)
            entrada += str(block.transaction.public_key.publicExponent)
            entrada += str(block.transaction.public_key.modulus)
            entrada += str(block.transaction.message)
            entrada += str(block.transaction.signature)
            entrada += str(block.seed)
            entrada = int(sha256(entrada.encode()).hexdigest(), 16)
            if blockError:
                if entrada >= 2 ** (256 - 16):
                    break
            else:
                if entrada < 2 ** (256 - 16):
                    break
        block.block_hash = entrada


class block:

    def __init__(self):
        """
        crea un bloc (no neces`ariamnet v`alid)
        """
        self.block_hash = None
        self.previous_block_hash = None
        self.transaction = None
        self.seed = None

    def genesis(self, transaction, blockError):
        """
        genera el primer bloc d’una cadena amb la transacci´o "transaction" que es caracteritza per:
        - previous_block_hash=0
        - ser v`alid
        """
        self.previous_block_hash = 0
        self.transaction = transaction
        block_hash_generator(self, blockError)

    def next_block(self, transaction, blockError):
        """
        genera el seg¨uent block v`alid amb la transacci´o "transaction"
        """
        B = block()
        B.previous_block_hash = self.block_hash
        B.transaction = transaction
        block_hash_generator(B, blockError)
        return B

    def verify_block(self):
        """
        Verifica si un bloc ´es v`alid:
        -Comprova que el hash del bloc anterior cumpleix las condicions exigides
        -Comprova la transacci´o del bloc ´es v`alida
        -Comprova que el hash del bloc cumpleix las condicions exigides
        Si totes les comprovacions s´on correctes retorna el boole`a True.
        En qualsevol altre cas retorma el boole`a False
        """
        print("message: " + str(self.transaction.message))
        print("signature: " + str(self.transaction.signature))
        print("test: " + str(self.transaction.verify()))
        print("blockHash:" + str(self.block_hash < 2 ** (
                256 - 16)))
        print("previousBlockHash:" + str(self.previous_block_hash < 2 ** (256 - 16)))
        return self.previous_block_hash < 2 ** (256 - 16) and self.transaction.verify() and self.block_hash < 2 ** (
                    256 - 16)

import pickle
from block import *
from rsa_key import *
import pandas as pd
import os

def block_chain_generator():
    rsa = rsa_key()
    messages = map(lambda i: transaction(i, rsa), range(100))

    res = block_chain(next(messages), False)

    for _ in range(1, 100):
        res.add_block(next(messages), False)

    with open("blocks_valids.pickle", 'wb') as file:
        pickle.dump(res, file)


def block_chain_seed_wrong_generator(B, name):
    rsa = rsa_key()
    messages = map(lambda i: transaction(i, rsa), range(100))

    if B == 1:
        res = block_chain(next(messages), True)
    else:
        res = block_chain(next(messages), False)

    for i in range(1, B):
        res.add_block(next(messages), False)

    for i in range(B, 100):
        res.add_block(next(messages), True)

    fileName = './100_blocks_' + name + '.pickle'
    with open(fileName, 'wb') as file:
        pickle.dump(res, file)


def block_chain_check(formato, name=None):
    if name is None:
        object = pd.read_pickle(r'./100_blocks_valids.pickle')
    else:
        object = pd.read_pickle(r'./100_blocks_' + name + '.pickle')

    print(object.verify())


class block_chain:
    def __init__(self, transaction, blockError):
        """
        genera una cadena de blocs que ´es una llista de blocs,
        el primer bloc ´es un bloc "genesis" generat amb la transacci´o "transaction"
        """
        first_block = block()
        first_block.genesis(transaction, blockError)
        self.list_of_blocks = [first_block]

    def add_block(self, transaction, blockError):
        """
        afegeix a la llista de blocs un nou bloc v`alid generat amb la transacci´o "transaction"
        """
        last_block = self.list_of_blocks[len(self.list_of_blocks) - 1]
        self.list_of_blocks.append(last_block.next_block(transaction, blockError))

    def verify(self):
        """
        - Comprova que tots el blocs s´on v`alids
        - Comprova que el primer bloc ´es un bloc "genesis"
        - Comprova que per cada bloc de la cadena el seg¨uent ´es el correcte
        Si totes les comprovacions s´on correctes retorna el boole`a True.
        En qualsevol altre cas retorma el boole`a False i fins a quin bloc la cadena ´es v´alida
        """

        for i in range(len(self.list_of_blocks)):

            currentB = self.list_of_blocks[i]
            previousB = self.list_of_blocks[i-1]

            if not currentB.verify_block():
                print("El bloque " + str(i) + " no es valido")
                return False
            elif i == 0 and currentB.previous_block_hash != 0:
                print("El bloque " + str(i) + " no es genesis ")
                return False
            elif i != 0 and previousB.block_hash != currentB.previous_block_hash:
                print("El bloque " + str(i) + " no es valido")
                return False

        return True


if __name__ == "__main__":

    
    """CREACIÓ DELS BLOCS VÀLIDS FINS AL BLOC XX"""
    dniRaul = 10
    block_chain_seed_wrong_generator(dniRaul, 'RaulLumbreras')
    block_chain_check("pickle", 'RaulLumbreras')
    
    """CREACIÓ DELS 100 BLOCS VÀLIDS"""
    
    block_chain_generator()
    #block_chain_check("pickle")

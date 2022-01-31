import hashlib, filetype, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

##no tiran MODE_CFB 
##          MODE_CBC
##raul => MODE_OFB
##nico => MODE_OFB


def AES_Decrypt_Long(enc, K):
    IV = enc[:16]
    cipher = AES.new(K, AES.MODE_CFB, IV)
    return unpad(cipher.decrypt(enc[16:]), AES.block_size)

def AES_Decrypt_Raul(enc, K, IV):
    cipher = AES.new(K, AES.MODE_OFB, IV)
    return unpad(cipher.decrypt(enc), AES.block_size)

def AES_Decrypt_Nico(enc, K, IV):
    cipher = AES.new(K, AES.MODE_OFB, IV)
    return unpad(cipher.decrypt(enc), AES.block_size)

def AES_Decrypt_ex_2(enc, K, IV):
    cipher = AES.new(K, AES.MODE_CBC, IV)
    return unpad(cipher.decrypt(enc), AES.block_size)

if __name__ == "__main__":
    
    """PRIMERA PARTE"""
    My_key = open("2021_09_30_10_54_12_raulumbreras.key", 'rb')
    My_key = My_key.read()

    M_enc = open("2021_09_30_10_54_12_raulumbreras.enc", 'rb')
    M_enc = M_enc.read()

    decrypted = AES_Decrypt_Raul(M_enc[16:], My_key, M_enc[:16])

    M_decrypted = open("result", 'wb')
    M_decrypted.write(decrypted)
    M_decrypted.close()
    
    """SEGUNDA PARTE"""
    M_enc = open("2021_09_30_10_54_12_raulumbreras.puerta_trasera.enc", 'rb')
    M_enc = M_enc.read()

    n = 0
    prog = 0

    ascii_table = [chr(i) for i in range(128)]
    for i in ascii_table:
        print(str(prog)+"%")
        prog += 100/128
        for j in ascii_table:
            key = f"{i * 8}{j * 8}"
            try:
                H = hashlib.sha256(key.encode()).digest()  # La funcion next() sirve para iterar los valores devueltos por la funciÃ³n generate_key
                decrypted = AES_Decrypt_ex_2(M_enc, H[:16], H[16:])  # La H tiene 32 bytes, por lo tanto, su primera mitad (16 bytes = 128 bits) corresponde a la clave secreta K
                                                                  # y su segunda mitad a los bits del vector inicial IV
            except ValueError: # Un error posible durante la cerca
                pass
            else: # Padd is okay
                path = "n_" + str(n) + "_2021_09_30_10_54_12_raulumbreraspuerta_trasera"
                M_decrypted = open(path, 'wb')
                M_decrypted.write(decrypted)
                M_decrypted.close()
                res = filetype.guess("./"+path)
                if filetype.guess("./"+path) == None :
                    os.remove("./"+path)
                else :
                    print("WICTORIA")
                n += 1
    print("END")

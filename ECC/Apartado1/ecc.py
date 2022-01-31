import sympy as sp
import hashlib as hl
from ecpy.curves     import Curve,Point

#a)

E = Curve.get_curve('secp256r1')
orden = E.order
print('✅El nº. de puntos de la curva (orden) es primo.') if(sp.isprime(orden)) else print('❌El nº. de puntos de la curva (orden) NO es primo.')

#b)

P_x = 0xe8502cd0d24ea2b192aab6730fcfa0b457e5c2c07cae6e55914aa69467faa5f8
P_y = 0xb03f46ac2352b4483b6464fbeacde9e4fb8f10a7f4e823ba95296eefca72bb83
P = Point(P_x, P_y, E, False)

print('✅La clave pública P de www.wikipedia.org está en la curva.') if(P.is_on_curve) else print('❌La clave pública P de www.wikipedia.org NO está en la curva.')

#c)

#El orden del punto es el mismo que el de la curva porque este es primo y por lo tanto como el orden de P divide el orden de la curva, el orden de P es 1 o el orden de la curva y si fuese 1 seria el punto al infinito (que no el caso). Por lo tanto el orden de P es el orden de la curva.
print(orden)

#d)

Qx = 0xe8502cd0d24ea2b192aab6730fcfa0b457e5c2c07cae6e55914aa69467faa5f8
Qy = 0xb03f46ac2352b4483b6464fbeacde9e4fb8f10a7f4e823ba95296eefca72bb83

f1 = 0x00335ec42e241ec13a00207379a32b3a1a8697efd9a464b36a708793f502fecd06
f2 = 0x00fd91f189fec1b38407a151209c18f9a7c61ae03a20394e68ef2fd815142fc6bb

Px = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
Py = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5


m = 0x74a79d2830048cc2f7de3cba11f8588d2113e84c8f3118e91df278a0647e02ae

n = orden
f = open("./mensaje.bin", "rb") #Leemos el mensaje
mess = f.read()

mess384 = hl.sha384(mess).hexdigest()

preambulo = "20202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020544c5320312e332c2073657276657220436572746966696361746556657269667900"

final = preambulo + mess384

r = hl.sha256(bytes(bytearray.fromhex(final))).hexdigest()
r = int(r,16)

f2inv = sp.mod_inverse(f2,n)

w1 = r*f2inv

w2 = f1 *f2inv

Q = Point(Qx, Qy, E, False)
P = Point(Px, Py, E, False)

R = w1*P + w2*Q
v = R.x % n
print("✅La firma es correcta") if (v==f1) else print("❌La firma es incorrecta")



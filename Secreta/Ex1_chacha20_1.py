#! /usr/bin/python3
# by pts@fazekas.hu at Thu May 24 18:44:15 CEST 2018

"""Pure Python 3 implementation of the ChaCha20 stream cipher.
It works with Python 3.5 (and probably also earler Python 3.x).
Based on https://gist.github.com/cathalgarvey/0ce7dbae2aa9e3984adc
Based on Numpy implementation: https://gist.github.com/chiiph/6855750
Based on http://cr.yp.to/chacha.html
More info about ChaCha20: https://en.wikipedia.org/wiki/Salsa20
"""

import struct
import matplotlib.pyplot as plt

def yield_chacha20_xor_stream(key, iv, position):

  def rotate(v, c):
    return ((v << c) & 0xffffffff) | v >> (32 - c)

  def quarter_round(x, a, b, c, d):
    x[a] = (x[a] + x[b]) & 0xffffffff
    x[d] = rotate(x[d] ^ x[a], 16)
    x[c] = (x[c] + x[d]) & 0xffffffff
    x[b] = rotate(x[b] ^ x[c], 12)
    x[a] = (x[a] + x[b]) & 0xffffffff
    x[d] = rotate(x[d] ^ x[a], 8)
    x[c] = (x[c] + x[d]) & 0xffffffff
    x[b] = rotate(x[b] ^ x[c], 7)

  ctx = [0] * 16
  ctx[:4] = (1634760805, 857760878, 2036477234, 1797285236)
  ctx[4 : 12] = key
  ctx[12] = position
  ctx[13 : 16] = iv
  x = list(ctx)
  for i in range(10):
    quarter_round(x, 0, 4,  8, 12)
    quarter_round(x, 1, 5,  9, 13)
    quarter_round(x, 2, 6, 10, 14)
    quarter_round(x, 3, 7, 11, 15)
    quarter_round(x, 0, 5, 10, 15)
    quarter_round(x, 1, 6, 11, 12)
    quarter_round(x, 2, 7,  8, 13)
    quarter_round(x, 3, 4,  9, 14)
  ctx[12] = (ctx[12] + 1) & 0xffffffff
  return x

if __name__ == "__main__":
  key = (0, 0, 0, 0, 0, 0, 0, 0)
  iv = (0, 0, 0)
  initial_x = yield_chacha20_xor_stream(key,iv,1)
  frequencia = [0] * (4096)
  sumas = [0] * (4096)
  get_bin = lambda x, n: format(x, 'b').zfill(n)
  for i in range(2,4096):
    if ( i%100 == 0) : print(i)
    x_i = yield_chacha20_xor_stream(key,iv,i)
    res = [ a ^ b for (a,b) in zip(initial_x, x_i) ]
    frec_res = []
    for j in range(16) :
      frec_res += [int(x) for x in str(get_bin(res[j],32))]
    frequencia = [sum(x) for x in zip(frec_res, frequencia)]
    sumas[i] = sum(res)
  print(frequencia)
  print(sumas)
  plt.plot(frequencia)
  plt.show()
  plt.plot(sumas)
  plt.show()
  

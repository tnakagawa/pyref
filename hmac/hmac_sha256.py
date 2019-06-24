import hashlib


def hmac_sha256(key, data):
    ipad = bytearray([0] * 64)
    opad = bytearray([0] * 64)
    k = bytearray([0] * 32)
    if len(key) <= len(k):
        for i in range(len(key)):
            k[i] = key[i]
    else:
        k = hashlib.sha256(key).digest()
    for i in range(32):
        ipad[i] = k[i]
        opad[i] = k[i]
    for i in range(64):
        ipad[i] ^= 0x36
        opad[i] ^= 0x5c
    # H(K XOR opad, H(K XOR ipad, text))
    digest = hashlib.sha256(ipad + data).digest()
    digest = hashlib.sha256(opad + digest).digest()
    return digest

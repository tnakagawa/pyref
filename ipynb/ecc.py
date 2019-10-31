import copy


class FiniteField:
    def __init__(self, num, prime):
        self.prime = prime
        self.num = num % prime

    def __add__(self, other):  # a + b
        if self.prime != other.prime:
            raise TypeError('No match prime.')
        num = (self.num + other.num) % self.prime
        return self.__class__(num, self.prime)

    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError('No match prime.')
        num = (self.num - other.num) % self.prime
        return self.__class__(num, self.prime)

    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError('No match prime.')
        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)

    def __rmul__(self, coefficient):
        num = (self.num * coefficient) % self.prime
        return self.__class__(num, self.prime)

    def __pow__(self, exponent):
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError('No match prime.')
        num = (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
        return self.__class__(num, self.prime)

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        return 'prime:{} , num:{}'.format(self.prime, self.num)


class ECCPoint:
    def __init__(self, a, b, x, y):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        if self.x is None and self.y is None:
            return
        if self.y**2 != self.x**3 + self.a * self.x + self.b:
            raise ValueError(
                'The x and y are not on curve.{} {}'.format(x.num, y.num))

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise TypeError('They are not the same curve.')
        if self.x == None:
            return other.__class__(other.a, other.b, other.x, other.y)
        if other.x == None:
            return self.__class__(self.a, self.b, self.x, self.y)
        if self.x == other.x and self.y != other.y:
            return self.__class__(self.a, self.b, None, None)
        if self.x != other.x:
            s = (self.y - other.y) / (self.x - other.x)
            x = s**2 - self.x - other.x
            y = s * (self.x - x) - self.y
            return self.__class__(self.a, self.b, x, y)
        if self == other and self.y == 0 * self.x:
            return self.__class__(self.a, self.b, None, None)
        if self == other:
            s = (3 * self.x**2 + self.a) / (2 * self.y)
            x = s**2 - 2 * self.x
            y = s * (self.x - x) - self.y
            return self.__class__(self.a, self.b, x, y)

    def __rmul__(self, coefficient):
        if self.x is None:
            return self.__class__(self.a, self.b, None, None)
        coef = coefficient
        current = self.__class__(self.a, self.b, self.x, self.y)
        result = self.__class__(self.a, self.b, None, None)
        while coef:
            if coef & 1:
                result += current
            current += current
            coef >>= 1
        return result


class sha256:
    H0 = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
          0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

    K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
         0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
         0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
         0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
         0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
         0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
         0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
         0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

    def ROTR(self, x, n):
        return ((x >> n) | (x << (32 - n))) & 0xffffffff

    def SHR(self, x, n):
        return x >> n

    def Ch(self, x, y, z):
        return (x & y) ^ ((~x) & z)

    def Maj(self, x, y, z):
        return (x & y) ^ (x & z) ^ (y & z)

    def SIGMA0(self, x):
        return self.ROTR(x, 2) ^ self.ROTR(x, 13) ^ self.ROTR(x, 22)

    def SIGMA1(self, x):
        return self.ROTR(x, 6) ^ self.ROTR(x, 11) ^ self.ROTR(x, 25)

    def sigma0(self, x):
        return self.ROTR(x, 7) ^ self.ROTR(x, 18) ^ self.SHR(x, 3)

    def sigma1(self, x):
        return self.ROTR(x, 17) ^ self.ROTR(x, 19) ^ self.SHR(x, 10)

    def padding(self, msg):
        l = len(msg)
        bs = bytes(msg) + b'\x80'
        if l % 64 < 56:
            bs += b'\x00'*(55 - (l % 64))
        else:
            bs += b'\x00'*(64 + 55 - (l % 64))
        l *= 8
        bs += l.to_bytes(8, 'big')
        return bs

    def compute(self, msg):
        N = int(len(msg) / 64)
        W = [0]*64
        H = copy.deepcopy(self.H0)
        for i in range(N):
            for t in range(64):
                if t < 16:
                    p = i*64 + t*4
                    W[t] = int.from_bytes(msg[p: p+4], 'big')
                else:
                    W[t] = (self.sigma1(W[t-2]) + W[t-7] +
                            self.sigma0(W[t-15]) + W[t-16]) & 0xffffffff
            a, b, c, d, e, f, g, h = H[0], H[1], H[2], H[3], H[4], H[5], H[6], H[7]
            for t in range(64):
                T1 = h + self.SIGMA1(e) + self.Ch(e, f, g) + self.K[t] + W[t]
                T2 = self.SIGMA0(a) + self.Maj(a, b, c)
                h, g, f, e = g, f, e, (d + T1) & 0xffffffff
                d, c, b, a = c, b, a, (T1 + T2) & 0xffffffff
            H[0] = (a + H[0]) & 0xffffffff
            H[1] = (b + H[1]) & 0xffffffff
            H[2] = (c + H[2]) & 0xffffffff
            H[3] = (d + H[3]) & 0xffffffff
            H[4] = (e + H[4]) & 0xffffffff
            H[5] = (f + H[5]) & 0xffffffff
            H[6] = (g + H[6]) & 0xffffffff
            H[7] = (h + H[7]) & 0xffffffff
        hash = bytes()
        for i in range(8):
            hash += H[i].to_bytes(4, 'big')
        return hash

    def Digest(self, msg):
        return self.compute(self.padding(msg))


class ripemd160:
    r1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
          7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8,
          3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12,
          1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2,
          4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13, ]

    r2 = [	5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
           6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
           15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13,
           8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
           12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11, ]

    s1 = [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8,
          7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
          11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5,
          11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
          9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6, ]

    s2 = [8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
          9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
          9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
          15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
          8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11, ]

    def f(self, j, x, y, z):
        if 0 <= j and j <= 15:
            return x ^ y ^ z
        if 16 <= j and j <= 31:
            return (x & y) | ((~x) & z)
        if 32 <= j and j <= 47:
            return (x | (~y)) ^ z
        if 48 <= j and j <= 63:
            return (x & z) | (y & (~z))
        if 64 <= j and j <= 79:
            return x ^ (y | (~z))
        return 0

    def K1(self, j):
        if 0 <= j and j <= 15:
            return 0x00000000
        if 16 <= j and j <= 31:
            return 0x5A827999
        if 32 <= j and j <= 47:
            return 0x6ED9EBA1
        if 48 <= j and j <= 63:
            return 0x8F1BBCDC
        if 64 <= j and j <= 79:
            return 0xA953FD4E
        return 0

    def K2(self, j):
        if 0 <= j and j <= 15:
            return 0x50A28BE6
        if 16 <= j and j <= 31:
            return 0x5C4DD124
        if 32 <= j and j <= 47:
            return 0x6D703EF3
        if 48 <= j and j <= 63:
            return 0x7A6D76E9
        if 64 <= j and j <= 79:
            return 0x00000000
        return 0

    def rol(self, s, x):
        return (x << s) | (x >> (32 - s))

    def padding(self, msg):
        l = len(msg)
        bs = bytes(msg) + b'\x80'
        if l % 64 < 56:
            bs += b'\x00'*(55 - (l % 64))
        else:
            bs += b'\x00'*(64 + 55 - (l % 64))
        l *= 8
        bs += l.to_bytes(8, 'little')
        return bs

    def ta(self, x, y):
        return (x + y) & 0xFFFFFFFF

    def compute(self, msg):
        t = int(len(msg) / 64)
        h0, h1, h2, h3, h4 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0
        for i in range(t):
            X = [0]*16
            for t in range(16):
                p = i*64 + t*4
                X[t] = int.from_bytes(msg[p: p+4], 'little')
            A1, B1, C1, D1, E1 = h0, h1, h2, h3, h4
            A2, B2, C2, D2, E2 = h0, h1, h2, h3, h4
            T = 0
            for j in range(80):
                T = self.ta(
                    self.rol(self.s1[j], self.ta(self.ta(self.ta(A1, self.f(j, B1, C1, D1)), X[self.r1[j]]), self.K1(j))), E1)
                A1, E1, D1, C1, B1 = E1, D1, self.rol(10, C1), B1, T
                T = self.ta(
                    self.rol(self.s2[j], self.ta(self.ta(self.ta(A2, self.f(79-j, B2, C2, D2)), X[self.r2[j]]), self.K2(j))), E2)
                A2, E2, D2, C2, B2 = E2, D2, self.rol(10, C2), B2, T
            T = self.ta(self.ta(h1, C1), D2)
            h1 = self.ta(self.ta(h2, D1), E2)
            h2 = self.ta(self.ta(h3, E1), A2)
            h3 = self.ta(self.ta(h4, A1), B2)
            h4 = self.ta(self.ta(h0, B1), C2)
            h0 = T
        hash = bytes()
        hash += h0.to_bytes(4, 'little')
        hash += h1.to_bytes(4, 'little')
        hash += h2.to_bytes(4, 'little')
        hash += h3.to_bytes(4, 'little')
        hash += h4.to_bytes(4, 'little')
        return hash

    def Digest(self, msg):
        return self.compute(self.padding(msg))

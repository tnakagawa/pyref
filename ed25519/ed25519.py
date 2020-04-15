import hashlib


class Ed25519P():
    p = 2**255 - 19
    L = 2**252 + 27742317777372353535851937790883648493
    d = (-121665 * pow(121666, p-2, p)) % p

    def __init__(self, x, y):
        if x is None or y is None:
            raise ValueError("x or y are None")
        self.x = x % self.p
        self.y = y % self.p
        # : −x^2 + y^2 = 1 + dx^2y^2
        if (-1 * pow(self.x, 2, self.p) + pow(self.y, 2, self.p)) % self.p != (1 + self.d * pow(self.x, 2, self.p) * pow(self.y, 2, self.p)) % self.p:
            raise ValueError("x and y are not on the curve")

    def __add__(self, other):
        x1 = self.x
        y1 = self.y
        x2 = other.x
        y2 = other.y
        #        x1y2 + x2y1
        # x3 = ---------------
        #       1 + dx1x2y1y2
        x3 = ((x1*y2 + x2*y1) * pow((1 + self.d*x1*x2*y1*y2) %
                                    self.p, self.p-2, self.p)) % self.p
        #        y1y2 + x1x2
        # y3 = ---------------
        #       1 − dx1x2y1y2
        y3 = ((y1*y2 + x1*x2) * pow((1 - self.d*x1*x2*y1*y2) %
                                    self.p, self.p-2, self.p)) % self.p
        return self.__class__(x3, y3)

    def __sub__(self, other):
        return self + other.__class__(self.p - self.x, self.y)

    def __rmul__(self, coefficient):
        coef = coefficient % self.L
        current = self.__class__(self.x, self.y)
        result = self.__class__(0, 1)
        while coef:
            if coef & 1:
                result += current
            current += current
            coef >>= 1
        return result

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __str__(self):
        return '({:064x},{:064x})'.format(self.x, self.y)

    def encode(self):
        return int.to_bytes(self.y | ((self.x & 1) << 255), 32, 'little')


def DecodePoint(encode_point):
    if len(encode_point) != 32:
        raise ValueError("invalid length of encode point")
    y = int.from_bytes(encode_point, 'little')
    sign = y >> 255
    y &= (1 << 255) - 1
    # x^2 = (y^2−1)/(dy^2+1)
    x2 = ((y*y-1)
          * pow(Ed25519P.d*y*y+1, Ed25519P.p-2, Ed25519P.p)) % Ed25519P.p
    if x2 == 0:
        if sign:
            raise ValueError("invalid sign of encode point")
    # x = ±√(y^2−1)/(dy^2+1)
    x = pow(x2, (Ed25519P.p+3) // 8, Ed25519P.p)
    if (x*x - x2) % Ed25519P.p != 0:
        x = (x * pow(2, (Ed25519P.p-1) // 4, Ed25519P.p)) % Ed25519P.p
        if (x*x - x2) % Ed25519P.p != 0:
            raise ValueError("invalid square of encode point")
    if (x & 1) != sign:
        x = Ed25519P.p - x
    return Ed25519P(x, y)


By = (4*pow(5, Ed25519P.p-2, Ed25519P.p)) % Ed25519P.p
B = DecodePoint(By.to_bytes(32, 'little'))


def Sign(secret, m):
    if len(secret) != 32:
        raise ValueError("invalid length of secret")
    h = hashlib.sha512(secret).digest()
    b = (h[0] & 0xf8).to_bytes(1, byteorder='little') + \
        h[1:31] + \
        ((h[31] & 0x7f) | 0x40).to_bytes(1, byteorder='little')
    s = int.from_bytes(b, 'little')
    A = s*B
    prefix = h[32:]
    r = int.from_bytes(hashlib.sha512(prefix + m).digest(), 'little')
    R = r*B
    k = int.from_bytes(hashlib.sha512(
        R.encode() + A.encode() + m).digest(), 'little')
    S = (r + k * s) % Ed25519P.L
    return R.encode() + S.to_bytes(32, 'little')


def Verify(A, signature, m):
    if len(signature) != 64:
        raise ValueError("invalid length of signature")
    R = DecodePoint(signature[:32])
    S = int.from_bytes(signature[32:], 'little')
    H = int.from_bytes(hashlib.sha512(
        R.encode() + A.encode() + m).digest(), 'little')
    return 8*S*B == 8*R + 8*H*A


Ed25519_TEST_VECTOR = [
    [
        'TEST 1',
        # SECRET KEY:
        '9d61b19deffd5a60ba844af492ec2cc4'
        + '4449c5697b326919703bac031cae7f60',
        # PUBLIC KEY:
        'd75a980182b10ab7d54bfed3c964073a'
        + '0ee172f3daa62325af021a68f707511a',
        # MESSAGE(length 0 bytes):
        '',
        # SIGNATURE:
        'e5564300c360ac729086e2cc806e828a'
        + '84877f1eb8e5d974d873e06522490155'
        + '5fb8821590a33bacc61e39701cf9b46b'
        + 'd25bf5f0595bbe24655141438e7a100b',
    ],
    [
        'TEST 2',
        # SECRET KEY:
        '4ccd089b28ff96da9db6c346ec114e0f'
        + '5b8a319f35aba624da8cf6ed4fb8a6fb',
        # PUBLIC KEY:
        '3d4017c3e843895a92b70aa74d1b7ebc'
        + '9c982ccf2ec4968cc0cd55f12af4660c',
        # MESSAGE(length 1 byte):
        '72',
        # SIGNATURE:
        '92a009a9f0d4cab8720e820b5f642540'
        + 'a2b27b5416503f8fb3762223ebdb69da'
        + '085ac1e43e15996e458f3613d0f11d8c'
        + '387b2eaeb4302aeeb00d291612bb0c00',
    ],
    [
        'TEST 3',
        # SECRET KEY:
        'c5aa8df43f9f837bedb7442f31dcb7b1'
        + '66d38535076f094b85ce3a2e0b4458f7',
        # PUBLIC KEY:
        'fc51cd8e6218a1a38da47ed00230f058'
        + '0816ed13ba3303ac5deb911548908025',
        # MESSAGE(length 2 bytes):
        'af82',
        # SIGNATURE:
        '6291d657deec24024827e69c3abe01a3'
        + '0ce548a284743a445e3680d7db5ac3ac'
        + '18ff9b538d16f290ae67f760984dc659'
        + '4a7c15e9716ed28dc027beceea1ec40a',
    ],
    [
        'TEST 1024',
        # SECRET KEY:
        'f5e5767cf153319517630f226876b86c'
        + '8160cc583bc013744c6bf255f5cc0ee5',
        # PUBLIC KEY:
        '278117fc144c72340f67d0f2316e8386'
        + 'ceffbf2b2428c9c51fef7c597f1d426e',
        # MESSAGE(length 1023 bytes):
        '08b8b2b733424243760fe426a4b54908'
        + '632110a66c2f6591eabd3345e3e4eb98'
        + 'fa6e264bf09efe12ee50f8f54e9f77b1'
        + 'e355f6c50544e23fb1433ddf73be84d8'
        + '79de7c0046dc4996d9e773f4bc9efe57'
        + '38829adb26c81b37c93a1b270b20329d'
        + '658675fc6ea534e0810a4432826bf58c'
        + '941efb65d57a338bbd2e26640f89ffbc'
        + '1a858efcb8550ee3a5e1998bd177e93a'
        + '7363c344fe6b199ee5d02e82d522c4fe'
        + 'ba15452f80288a821a579116ec6dad2b'
        + '3b310da903401aa62100ab5d1a36553e'
        + '06203b33890cc9b832f79ef80560ccb9'
        + 'a39ce767967ed628c6ad573cb116dbef'
        + 'efd75499da96bd68a8a97b928a8bbc10'
        + '3b6621fcde2beca1231d206be6cd9ec7'
        + 'aff6f6c94fcd7204ed3455c68c83f4a4'
        + '1da4af2b74ef5c53f1d8ac70bdcb7ed1'
        + '85ce81bd84359d44254d95629e9855a9'
        + '4a7c1958d1f8ada5d0532ed8a5aa3fb2'
        + 'd17ba70eb6248e594e1a2297acbbb39d'
        + '502f1a8c6eb6f1ce22b3de1a1f40cc24'
        + '554119a831a9aad6079cad88425de6bd'
        + 'e1a9187ebb6092cf67bf2b13fd65f270'
        + '88d78b7e883c8759d2c4f5c65adb7553'
        + '878ad575f9fad878e80a0c9ba63bcbcc'
        + '2732e69485bbc9c90bfbd62481d9089b'
        + 'eccf80cfe2df16a2cf65bd92dd597b07'
        + '07e0917af48bbb75fed413d238f5555a'
        + '7a569d80c3414a8d0859dc65a46128ba'
        + 'b27af87a71314f318c782b23ebfe808b'
        + '82b0ce26401d2e22f04d83d1255dc51a'
        + 'ddd3b75a2b1ae0784504df543af8969b'
        + 'e3ea7082ff7fc9888c144da2af58429e'
        + 'c96031dbcad3dad9af0dcbaaaf268cb8'
        + 'fcffead94f3c7ca495e056a9b47acdb7'
        + '51fb73e666c6c655ade8297297d07ad1'
        + 'ba5e43f1bca32301651339e22904cc8c'
        + '42f58c30c04aafdb038dda0847dd988d'
        + 'cda6f3bfd15c4b4c4525004aa06eeff8'
        + 'ca61783aacec57fb3d1f92b0fe2fd1a8'
        + '5f6724517b65e614ad6808d6f6ee34df'
        + 'f7310fdc82aebfd904b01e1dc54b2927'
        + '094b2db68d6f903b68401adebf5a7e08'
        + 'd78ff4ef5d63653a65040cf9bfd4aca7'
        + '984a74d37145986780fc0b16ac451649'
        + 'de6188a7dbdf191f64b5fc5e2ab47b57'
        + 'f7f7276cd419c17a3ca8e1b939ae49e4'
        + '88acba6b965610b5480109c8b17b80e1'
        + 'b7b750dfc7598d5d5011fd2dcc5600a3'
        + '2ef5b52a1ecc820e308aa342721aac09'
        + '43bf6686b64b2579376504ccc493d97e'
        + '6aed3fb0f9cd71a43dd497f01f17c0e2'
        + 'cb3797aa2a2f256656168e6c496afc5f'
        + 'b93246f6b1116398a346f1a641f3b041'
        + 'e989f7914f90cc2c7fff357876e506b5'
        + '0d334ba77c225bc307ba537152f3f161'
        + '0e4eafe595f6d9d90d11faa933a15ef1'
        + '369546868a7f3a45a96768d40fd9d034'
        + '12c091c6315cf4fde7cb68606937380d'
        + 'b2eaaa707b4c4185c32eddcdd306705e'
        + '4dc1ffc872eeee475a64dfac86aba41c'
        + '0618983f8741c5ef68d3a101e8a3b8ca'
        + 'c60c905c15fc910840b94c00a0b9d0',
        # SIGNATURE:
        '0aab4c900501b3e24d7cdf4663326a3a'
        + '87df5e4843b2cbdb67cbf6e460fec350'
        + 'aa5371b1508f9f4528ecea23c436d94b'
        + '5e8fcd4f681e30a6ac00a9704a188a03',
    ],
    [
        'TEST SHA(abc)',
        # SECRET KEY:
        '833fe62409237b9d62ec77587520911e'
        + '9a759cec1d19755b7da901b96dca3d42',
        # PUBLIC KEY:
        'ec172b93ad5e563bf4932c70e1245034'
        + 'c35467ef2efd4d64ebf819683467e2bf',
        # MESSAGE(length 64 bytes):
        'ddaf35a193617abacc417349ae204131'
        + '12e6fa4e89a97ea20a9eeee64b55d39a'
        + '2192992a274fc1a836ba3c23a3feebbd'
        + '454d4423643ce80e2a9ac94fa54ca49f',
        # SIGNATURE:
        'dc2a4459e7369633a52b1bf277839a00'
        + '201009a3efbf3ecb69bea2186c26b589'
        + '09351fc9ac90b3ecfdfbc7c66431e030'
        + '3dca179c138ac17ad9bef1177331a704',
    ]
]


for test in Ed25519_TEST_VECTOR:
    NAME = test[0]
    SECRET_KEY = test[1]
    PUBLIC_KEY = test[2]
    MESSAGE = test[3]
    SIGNATURE = test[4]
    A = DecodePoint(bytes.fromhex(PUBLIC_KEY))
    print('{:15}'.format(NAME),
          Sign(bytes.fromhex(SECRET_KEY),
               bytes.fromhex(MESSAGE)).hex() == SIGNATURE,
          A.encode().hex() == PUBLIC_KEY,
          Verify(A, bytes.fromhex(SIGNATURE),
                 bytes.fromhex(MESSAGE)))

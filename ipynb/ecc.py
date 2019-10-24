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
            return self.__class__(None, None, self.a, self.b)
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

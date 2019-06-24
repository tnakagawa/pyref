import unittest
from hmac.hmac_sha256 import hmac_sha256

testvectors = [
    {
        "key": bytes.fromhex('0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b' +
                             '0b0b0b0b'),
        "data": bytes.fromhex('4869205468657265'),
        "sha256": bytes.fromhex('b0344c61d8db38535ca8afceaf0bf12b' +
                                '881dc200c9833da726e9376c2e32cff7'),
    },
    {
        "key": bytes.fromhex('4a656665'),
        "data": bytes.fromhex('7768617420646f2079612077616e7420' +
                              '666f72206e6f7468696e673f'),
        "sha256": bytes.fromhex('5bdcc146bf60754e6a042426089575c7' +
                                '5a003f089d2739839dec58b964ec3843'),
    },
    {
        "key": bytes.fromhex('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
                             'aaaaaaaa'),
        "data": bytes.fromhex('dddddddddddddddddddddddddddddddd' +
                              'dddddddddddddddddddddddddddddddd' +
                              'dddddddddddddddddddddddddddddddd' +
                              'dddd'),
        "sha256": bytes.fromhex('773ea91e36800e46854db8ebd09181a7' +
                                '2959098b3ef8c122d9635514ced565fe'),
    },
    {
        "key": bytes.fromhex('0102030405060708090a0b0c0d0e0f10' +
                             '111213141516171819'),
        "data": bytes.fromhex('cdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcd' +
                              'cdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcd' +
                              'cdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcd' +
                              'cdcd'),
        "sha256": bytes.fromhex('82558a389a443c0ea4cc819899f2083a' +
                                '85f0faa3e578f8077a2e3ff46729665b'),
    },
    {
        "key": bytes.fromhex('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
                             'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
                             'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
                             'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
                             'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
                             'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
                             'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
                             'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
                             'aaaaaa'),
        "data": bytes.fromhex('54657374205573696e67204c61726765' +
                              '72205468616e20426c6f636b2d53697a' +
                              '65204b6579202d2048617368204b6579' +
                              '204669727374'),
        "sha256": bytes.fromhex('60e431591ee0b67f0d8a26aacbf5b77f' +
                                '8e0bc6213728c5140546040f0ee37f54'),
    },
    {
        "key": bytes.fromhex('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
                             'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
                             'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
                             'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
                             'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
                             'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
                             'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
                             'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
                             'aaaaaa'),
        "data": bytes.fromhex('54686973206973206120746573742075' +
                              '73696e672061206c6172676572207468' +
                              '616e20626c6f636b2d73697a65206b65' +
                              '7920616e642061206c61726765722074' +
                              '68616e20626c6f636b2d73697a652064' +
                              '6174612e20546865206b6579206e6565' +
                              '647320746f2062652068617368656420' +
                              '6265666f7265206265696e6720757365' +
                              '642062792074686520484d414320616c' +
                              '676f726974686d2e'),
        "sha256": bytes.fromhex('9b09ffa71b942fcb27635fbcd5b0e944' +
                                'bfdc63644f0713938a7f51535c3a35e2'),
    },
]


class TestHmacSha256(unittest.TestCase):
    def test_hmac_sha256(self):
        for test in testvectors:
            key = test['key']
            data = test['data']
            h = hmac_sha256(key, data)
            print(test['sha256'].hex())
            print(h.hex())
            self.assertEqual(h, test['sha256'])


if __name__ == '__main__':
    unittest.main()

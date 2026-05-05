import struct
import math

class MD5Core:
    T = [int((1 << 32) * abs(math.sin(i + 1))) for i in range(64)]

    S = (
        [7, 12, 17, 22] * 4 +
        [5, 9, 14, 20] * 4 +
        [4, 11, 16, 23] * 4 +
        [6, 10, 15, 21] * 4
    )

    @staticmethod
    def rotate(x, c):
        return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

    @staticmethod
    def hash_string(message: str) -> str:
        msg = bytearray(message.encode("utf-8"))
        orig_len_bits = (8 * len(msg)) & 0xFFFFFFFFFFFFFFFF

        # Крок 1: додавання доповнення
        msg.append(0x80)
        while ((len(msg) * 8) % 512) != 448:
            msg.append(0)

        # Крок 2: додавання значення довжини
        msg += struct.pack("<Q", orig_len_bits)

        # Крок 3: ініціалізація MD-буфера
        a0 = 0x67452301
        b0 = 0xEFCDAB89
        c0 = 0x98BADCFE
        d0 = 0x10325476

        # Крок 4: обробка блоками по 512 біт
        for offset in range(0, len(msg), 64):
            a, b, c, d = a0, b0, c0, d0
            chunk = msg[offset:offset+64]
            M = list(struct.unpack("<16I", chunk))

            for i in range(64):
                if 0 <= i <= 15:
                    f = (b & c) | (~b & d)
                    g = i
                elif 16 <= i <= 31:
                    f = (d & b) | (~d & c)
                    g = (5*i + 1) % 16
                elif 32 <= i <= 47:
                    f = b ^ c ^ d
                    g = (3*i + 5) % 16
                else:
                    f = c ^ (b | ~d)
                    g = (7*i) % 16

                f = (f + a + MD5Core.T[i] + M[g]) & 0xFFFFFFFF
                a, d, c, b = d, c, b, (b + MD5Core.rotate(f, MD5Core.S[i])) & 0xFFFFFFFF

            a0 = (a0 + a) & 0xFFFFFFFF
            b0 = (b0 + b) & 0xFFFFFFFF
            c0 = (c0 + c) & 0xFFFFFFFF
            d0 = (d0 + d) & 0xFFFFFFFF

        # Крок 5: вихід
        digest = struct.pack("<4I", a0, b0, c0, d0)
        return ''.join(f"{byte:02x}" for byte in digest).upper()

    @staticmethod
    def hash_file(filename: str) -> str:
        with open(filename, "rb") as f:
            data = f.read()
        return MD5Core.hash_string(data.decode("latin1"))

    @staticmethod
    def verify_file(filename: str, md5file: str) -> bool:
        calc = MD5Core.hash_file(filename)
        with open(md5file, "r", encoding="utf-8") as f:
            ref = f.read().strip().upper()
        return calc == ref

    @staticmethod
    def run_tests():
        tests = {
            "": "D41D8CD98F00B204E9800998ECF8427E",
            "a": "0CC175B9C0F1B6A831C399E269772661",
            "abc": "900150983CD24FB0D6963F7D28E17F72",
            "message digest": "F96B697D7CB7938D525A2F31AAF161D0",
            "abcdefghijklmnopqrstuvwxyz": "C3FCD3D76192E4007DFB496CCA67E13B",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789": "D174AB98D277D9F5A5611C2C9F419D9F",
            "12345678901234567890123456789012345678901234567890123456789012345678901234567890": "57EDF4A22BE3C955AC49DA2E2107B67A"
        }
        results = ["=== Протокол тестування MD5 ==="]
        for s, expected in tests.items():
            result = MD5Core.hash_string(s)
            status = "OK" if result == expected else "FAIL"
            results.append(f"H({s}) = {result} | Очікувано: {expected} | {status}")
        return "\n".join(results)

import time
from labs.lab1_lcg import LCGCore
from labs.lab2_md5 import MD5Core

class RC5Core:
    def __init__(self, key: bytes, w=64, r=8):
        self.w = w
        self.r = r
        self.b = len(key)
        self.u = w // 8    
        self.mask = (1 << w) - 1 

        self.c = max(1, (self.b + self.u - 1) // self.u)
        L = [0] * self.c
        for i in range(self.c):
            chunk = key[i * self.u : (i + 1) * self.u]
            L[i] = int.from_bytes(chunk.ljust(self.u, b'\x00'), 'little')

        P64 = 0xB7E151628AED2A6B
        Q64 = 0x9E3779B97F4A7C15
        
        self.S = [0] * (2 * r + 2)
        self.S[0] = P64
        for i in range(1, len(self.S)):
            self.S[i] = (self.S[i - 1] + Q64) & self.mask

        i = j = A = B = 0
        t = max(self.c, 2 * r + 2)
        for _ in range(3 * t):
            A = self.S[i] = self.rotl((self.S[i] + A + B) & self.mask, 3)
            B = L[j] = self.rotl((L[j] + A + B) & self.mask, A + B)
            i = (i + 1) % len(self.S)
            j = (j + 1) % self.c

    def rotl(self, val, shift):
        shift %= self.w
        return ((val << shift) & self.mask) | (val >> (self.w - shift))

    def rotr(self, val, shift):
        shift %= self.w
        return (val >> shift) | ((val << (self.w - shift)) & self.mask)

    def encrypt_block(self, data: bytes) -> bytes:
        A = int.from_bytes(data[:8], 'little')
        B = int.from_bytes(data[8:], 'little')

        A = (A + self.S[0]) & self.mask
        B = (B + self.S[1]) & self.mask

        for i in range(1, self.r + 1):
            A = (self.rotl(A ^ B, B) + self.S[2 * i]) & self.mask
            B = (self.rotl(B ^ A, A) + self.S[2 * i + 1]) & self.mask

        return A.to_bytes(8, 'little') + B.to_bytes(8, 'little')

    def decrypt_block(self, data: bytes) -> bytes:
        A = int.from_bytes(data[:8], 'little')
        B = int.from_bytes(data[8:], 'little')

        for i in range(self.r, 0, -1):
            B = self.rotr((B - self.S[2 * i + 1]) & self.mask, A) ^ A
            A = self.rotr((A - self.S[2 * i]) & self.mask, B) ^ B

        B = (B - self.S[1]) & self.mask
        A = (A - self.S[0]) & self.mask

        return A.to_bytes(8, 'little') + B.to_bytes(8, 'little')

class RC5Manager:
    BLOCK_SIZE = 16

    @staticmethod
    def derive_key(password: str, key_size_bits: int) -> bytes:
        h1 = bytes.fromhex(MD5Core.hash_string(password))
        if key_size_bits == 64:
            return h1[:8]
        if key_size_bits == 128:
            return h1
        if key_size_bits == 256:
            h2 = bytes.fromhex(MD5Core.hash_string(h1))
            return h2 + h1
        return h1

    @staticmethod
    def generate_iv() -> bytes:
        lcg = LCGCore()
        lcg.x0 = int(time.time() * 1000) % lcg.m 
        return bytes(x % 256 for x in lcg.lcg(RC5Manager.BLOCK_SIZE))

    @staticmethod
    def encrypt_file(in_f, out_f, password, key_size_bits=128):
        rc5 = RC5Core(RC5Manager.derive_key(password, key_size_bits), w=64, r=8)
        iv = RC5Manager.generate_iv()
        bs = RC5Manager.BLOCK_SIZE
        
        with open(in_f, 'rb') as f_in, open(out_f, 'wb') as f_out:
            f_out.write(rc5.encrypt_block(iv)) 
            prev = iv
            while True:
                chunk = f_in.read(bs)
                if len(chunk) == 0:
                    chunk = bytes([bs] * bs)
                    last = True
                elif len(chunk) < bs:
                    pad_len = bs - len(chunk)
                    chunk += bytes([pad_len] * pad_len)
                    last = True
                else:
                    last = False
                cipher = rc5.encrypt_block(bytes(x ^ y for x, y in zip(chunk, prev)))
                f_out.write(cipher)
                prev = cipher
                if last:
                    break

    @staticmethod
    def decrypt_file(in_f, out_f, password, key_size_bits=128):
        rc5 = RC5Core(RC5Manager.derive_key(password, key_size_bits), w=64, r=8)
        bs = RC5Manager.BLOCK_SIZE
        
        with open(in_f, 'rb') as f_in, open(out_f, 'wb') as f_out:
            enc_iv = f_in.read(bs)
            if not enc_iv: return
            
            prev_cipher = rc5.decrypt_block(enc_iv) 
            curr_chunk = f_in.read(bs)
            
            while curr_chunk:
                next_chunk = f_in.read(bs)
                dec = rc5.decrypt_block(curr_chunk)
                plain = bytes(x ^ y for x, y in zip(dec, prev_cipher))
                
                if not next_chunk: 
                    pad_len = plain[-1]
                    if 1 <= pad_len <= bs:
                        plain = plain[:-pad_len]
                    f_out.write(plain)
                else:
                    f_out.write(plain)
                
                prev_cipher = curr_chunk
                curr_chunk = next_chunk
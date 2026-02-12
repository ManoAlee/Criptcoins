import hashlib
import secrets
from typing import Tuple, Optional
import binascii

# Optional dependencies: ecdsa, base58
try:
    import ecdsa
    HAS_ECDSA = True
except Exception:
    ecdsa = None
    HAS_ECDSA = False

try:
    import base58
    HAS_BASE58 = True
except Exception:
    base58 = None
    HAS_BASE58 = False

class BitcoinCrypto:
    def __init__(self):
        if not HAS_ECDSA:
            print("[!] Biblioteca 'ecdsa' nao encontrada. Usando fallback inseguro.")
        self.curve = ecdsa.SECP256k1 if HAS_ECDSA else None
    
    def generate_private_key(self) -> str:
        private_key_bytes = secrets.token_bytes(32)
        return private_key_bytes.hex()
    
    def private_key_to_public_key(self, private_key_hex: str) -> str:
        private_key_bytes = bytes.fromhex(private_key_hex)
        if HAS_ECDSA:
            signing_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=self.curve)
            verifying_key = signing_key.get_verifying_key()
            public_key_bytes = verifying_key.to_string()
            x_coord = int.from_bytes(public_key_bytes[:32], 'big')
            y_coord = int.from_bytes(public_key_bytes[32:], 'big')
            prefix = b'\x02' if y_coord % 2 == 0 else b'\x03'
            compressed_public_key = prefix + x_coord.to_bytes(32, 'big')
            return compressed_public_key.hex()
        pseudo = hashlib.sha256(private_key_bytes).hexdigest()
        return ('02' + pseudo)[:66]
    
    def public_key_to_address(self, public_key_hex: str) -> str:
        public_key_bytes = bytes.fromhex(public_key_hex)
        sha256_hash = hashlib.sha256(public_key_bytes).digest()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_hash)
        ripemd160_hash = ripemd160.digest()
        network_byte = b'\x00'
        extended_hash = network_byte + ripemd160_hash
        checksum = hashlib.sha256(hashlib.sha256(extended_hash).digest()).digest()[:4]
        address_bytes = extended_hash + checksum
        if HAS_BASE58:
            return base58.b58encode(address_bytes).decode('utf-8')
        return address_bytes.hex()
    
    def create_wallet(self) -> Tuple[str, str, str]:
        private_key = self.generate_private_key()
        public_key = self.private_key_to_public_key(private_key)
        address = self.public_key_to_address(public_key)
        return private_key, public_key, address
    
    def sign_message(self, message: str, private_key_hex: str) -> str:
        private_key_bytes = bytes.fromhex(private_key_hex)
        if not HAS_ECDSA:
            raise RuntimeError("Biblioteca 'ecdsa' nao disponivel.")
        signing_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=self.curve)
        message_hash = hashlib.sha256(message.encode()).digest()
        signature = signing_key.sign_digest(message_hash, sigencode=ecdsa.util.sigencode_der)
        return signature.hex()
    
    def verify_signature(self, message: str, signature_hex: str, public_key_hex: str) -> bool:
        try:
            if not HAS_ECDSA: return False
            public_key_bytes = bytes.fromhex(public_key_hex)
            if len(public_key_bytes) == 33:
                public_key_bytes = self._decompress_public_key(public_key_bytes)
            verifying_key = ecdsa.VerifyingKey.from_string(public_key_bytes, curve=self.curve)
            message_hash = hashlib.sha256(message.encode()).digest()
            signature_bytes = bytes.fromhex(signature_hex)
            return verifying_key.verify_digest(signature_bytes, message_hash, sigdecode=ecdsa.util.sigdecode_der)
        except Exception: return False
    
    def _decompress_public_key(self, compressed_key: bytes) -> bytes:
        prefix = compressed_key[0]
        x = int.from_bytes(compressed_key[1:], 'big')
        p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        y_squared = (pow(x, 3, p) + 7) % p
        y = pow(y_squared, (p + 1) // 4, p)
        if (y % 2 == 0) != (prefix == 0x02):
            y = p - y
        return x.to_bytes(32, 'big') + y.to_bytes(32, 'big')

class BitcoinWallet:
    def __init__(self):
        self.crypto = BitcoinCrypto()
        self.private_key = None
        self.public_key = None
        self.address = None
    
    def create_new_wallet(self) -> None:
        self.private_key, self.public_key, self.address = self.crypto.create_wallet()
        print(f"[*] Nova carteira criada! Endereco: {self.address}")
    
    def import_from_private_key(self, private_key_hex: str) -> None:
        self.private_key = private_key_hex
        self.public_key = self.crypto.private_key_to_public_key(private_key_hex)
        self.address = self.crypto.public_key_to_address(self.public_key)
        print(f"[*] Carteira importada! Endereco: {self.address}")
    
    def sign_transaction(self, transaction_data: str) -> str:
        if not self.private_key: raise ValueError("Carteira nao inicializada")
        return self.crypto.sign_message(transaction_data, self.private_key)
    
    def export_wallet(self) -> dict:
        return {'address': self.address, 'public_key': self.public_key, 'private_key': self.private_key}

    def print_wallet_info(self, show_private: bool = False) -> None:
        print(f"[*] Endereco: {self.address}")
        if show_private: print(f"[*] Chave Privada: {self.private_key}")

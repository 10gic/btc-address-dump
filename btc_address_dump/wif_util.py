import hashlib
import base58
from typing import Union


def scrub_input(hex_str_or_bytes: Union[str, bytes]) -> bytes:
    if isinstance(hex_str_or_bytes, str):
        hex_str_or_bytes = bytes.fromhex(hex_str_or_bytes)
    return hex_str_or_bytes


# wallet import format key - base58 encoded format
# https://bitcoin.stackexchange.com/questions/9244/private-key-to-wif
def encode_wif(private_key: Union[str, bytes], version: bytes, compressed_wif: bool = False) -> bytes:
    """ Encode wif format private key """
    private_key = scrub_input(private_key)

    # prepended version byte to private key
    private_key_with_version = version + private_key
    if compressed_wif:
        private_key_with_version = version + private_key + b'\x01'
    # perform SHA-256 hash on the mainnet_private_key
    sha256 = hashlib.sha256()
    sha256.update(private_key_with_version)
    hash_bytes = sha256.digest()

    # perform SHA-256 on the previous SHA-256 hash
    sha256 = hashlib.sha256()
    sha256.update(hash_bytes)
    hash_bytes = sha256.digest()

    # create a checksum using the first 4 bytes of the previous SHA-256 hash
    # append the 4 checksum bytes to the mainnet_private_key
    checksum = hash_bytes[:4]

    # print('checksum', checksum.hex())
    hash_bytes = private_key_with_version + checksum
    # print('hash', hash_bytes.hex())

    # convert private_key_with_version + checksum into base58 encoded string
    return base58.b58encode(hash_bytes)


def decode_wif(wif: str) -> bytes:
    """ Decode wif format private key """
    compressed = False
    if wif.startswith('K') or wif.startswith('L'):
        compressed = True
    decoded = base58.b58decode(wif)
    if compressed:
        private_key = decoded[1:-5]  # [80 xxx 1 checksum]
    else:
        private_key = decoded[1:-4]  # [80 xxx checksum]
    return private_key

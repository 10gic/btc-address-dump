import hashlib
import groestlcoin_hash
import base58
import base58grs
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


def grs_encode_wif(private_key: Union[str, bytes], version: bytes, compressed_wif: bool = False) -> bytes:
    """ Encode wif format private key """
    private_key = scrub_input(private_key)

    # prepended version byte to private key
    private_key_with_version = version + private_key
    if compressed_wif:
        private_key_with_version = version + private_key + b'\x01'
    # perform DOUBLE GROESTL-512 hash on the mainnet_private_key
    hash_bytes = groestlcoin_hash.getHash(private_key_with_version, len(private_key_with_version))

    # create a checksum using the first 4 bytes of the GROESTL-512 hash
    # append the 4 checksum bytes to the mainnet_private_key
    checksum = hash_bytes[:4]

    # print('checksum', checksum.hex())
    hash_bytes = private_key_with_version + checksum
    # print('hash', hash_bytes.hex())

    # convert private_key_with_version + checksum into base58 encoded string
    return base58grs.b58encode(hash_bytes)


def decode_wif(wif: str, compressed_wif: bool = False) -> bytes:
    """ Decode wif format private key """
    decoded = base58.b58decode(wif)
    if len(decoded) == 38 or len(decoded) == 37:
        private_key = decoded[1:33]  # WIF-compressed: [0x80 xxxx 0x01 checksum] or WIF: [0x80 xxxx checksum]
    else:
        raise ValueError("invalid WIF")
    return private_key


def grs_decode_wif(wif: str, compressed_wif: bool = False) -> bytes:
    """ Decode wif format private key """
    decoded = base58grs.b58decode(wif)
    if len(decoded) == 38 or len(decoded) == 37:
        private_key = decoded[1:33]  # WIF-compressed: [0x80 xxxx 0x01 checksum] or WIF: [0x80 xxxx checksum]
    else:
        raise ValueError("invalid WIF")
    return private_key


def is_valid_wif(wif: str, chain: str) -> bool:
    """ Check if wif is valid"""
    try:
        if chain == "grs" or chain == "grs_testnet":
            result = base58grs.b58decode(wif)
            #print(result)
            result, check = result[:-4], result[-4:]
            # DOUBLE GROESTL-512 hash
            digest = groestlcoin_hash.getHash(result, len(result))
        else:
            result = base58.b58decode(wif)
            #print(result)
            result, check = result[:-4], result[-4:]
            # DOUBLE sha256 hash
            digest = hashlib.sha256(hashlib.sha256(result).digest()).digest()
        return check == digest[:4]
    except ValueError:
        return False

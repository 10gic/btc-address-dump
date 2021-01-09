# Adapted from:
# https://github.com/vergl4s/ethereum-mnemonic-utils/blob/master/mnemonic_utils.py
import hashlib
import hmac
import struct
import os
import sys

from ecdsa.curves import SECP256k1
from ecdsa.ellipticcurve import Point, PointJacobi

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(file_path))

import common_util

BIP39_PBKDF2_ROUNDS = 2048
BIP39_SALT_MODIFIER = "mnemonic"
BIP32_PRIVDEV = 0x80000000
BIP32_CURVE = SECP256k1
BIP32_SEED_MODIFIER = b'Bitcoin seed'  # https://en.bitcoin.it/wiki/BIP_0032

LEDGER_ETH_DERIVATION_PATH = "m/44'/0'/0'/0/0"
# bip44 define 5 levels in BIP32 path: m / purpose' / coin_type' / account' / change / address_index
# for bip44, purpose = 44
# for eth, coin_type = 60
# Registered coin types for BIP-0044, see https://github.com/satoshilabs/slips/blob/master/slip-0044.md


def mnemonic_to_bip39seed(mnemonic: str, passphrase: str = "") -> bytes:
    """ BIP39 seed from a mnemonic key.
        Logic adapted from https://github.com/trezor/python-mnemonic. """
    mnemonic = bytes(mnemonic, 'utf8')
    salt = bytes(BIP39_SALT_MODIFIER + passphrase, 'utf8')
    return hashlib.pbkdf2_hmac('sha512', mnemonic, salt, BIP39_PBKDF2_ROUNDS)


def bip39seed_to_bip32masternode(seed: bytes) -> tuple[bytes, bytes]:
    """ BIP32 master node derivation from a bip39 seed.
        Logic adapted from https://github.com/satoshilabs/slips/blob/master/slip-0010/testvectors.py. """
    h = hmac.new(BIP32_SEED_MODIFIER, seed, hashlib.sha512).digest()
    key, chain_code = h[:32], h[32:]
    return key, chain_code


def derive_bip32childkey(parent_key: bytes, parent_chain_code: bytes, index: int) -> tuple[bytes, bytes]:
    """ Derives a child key from an existing key, index is current derivation parameter.
        Support:
        1. parent private key -> child private key, in this case, parent_key must be 32 bytes
        2. parent public key -> child public key, in this case, parent_key must be 33 bytes, index must < 0x80000000
    """
    assert len(parent_key) == 32 or len(parent_key) == 33
    assert len(parent_chain_code) == 32

    parent_is_public_key = len(parent_key) == 33
    if parent_is_public_key:
        if (index & BIP32_PRIVDEV) != 0:  # index >= 0x80000000, hardened child
            raise Exception("hardened derivation is only defined for private key derivation, "
                            "not defined for public key derivation")
        else:  # normal public child
            msg = parent_key
    else:
        if (index & BIP32_PRIVDEV) != 0:  # index >= 0x80000000, hardened child
            msg = b'\x00' + parent_key
        else:  # normal private child
            msg = common_util.prikey_to_pubkey(parent_key)  # get compressed public key from a private key
    msg = msg + struct.pack('>L', index)  # `>` means big-endian, `L` means unsigned long
    # compute sha512
    h = hmac.new(parent_chain_code, msg, hashlib.sha512).digest()
    left32, chain_code = h[:32], h[32:]
    a = int.from_bytes(left32, byteorder='big')
    b = int.from_bytes(parent_key, byteorder='big')
    if parent_is_public_key:
        # build Point from compressed public key
        x, y = common_util.pubkey_from_bytes_to_point(parent_key)
        parent_public_key: Point = Point(BIP32_CURVE.curve, x, y)
        # child_public_key = left32 * G + parent_public_key
        child_public_key: PointJacobi = a * BIP32_CURVE.generator + PointJacobi.from_affine(parent_public_key)
        if a >= BIP32_CURVE.order:
            raise Exception("left32 greater than or equal to the order, please use another index")
        if child_public_key == 0:
            raise Exception("resulting public key is the point at infinity, please use another index")
        key = common_util.pubkey_from_point_to_bytes(child_public_key.x(), child_public_key.y())  # 33 bytes
    else:
        child_private_key = (a + b) % BIP32_CURVE.order
        # check validation of resulting key
        if a >= BIP32_CURVE.order:
            raise Exception("left32 greater than or equal to the order, please use another index")
        if child_private_key == 0:
            raise Exception("resulting private key is zero, please use another index")
        key = child_private_key.to_bytes(32, byteorder='big')  # 32 bytes
    return key, chain_code


def parse_derivation_path(str_derivation_path: str) -> list[int]:
    """ Parses a derivation path such as "m/44'/60/0'/0" and returns
        list of integers for each element in path. """
    path = []
    if str_derivation_path[0:2] != 'm/':
        raise ValueError("Can't recognize derivation path. It should look like \"m/44'/60/0'/0\".")

    for i in str_derivation_path.lstrip('m/').split('/'):
        if "'" in i:
            path.append(BIP32_PRIVDEV + int(i[:-1]))
        else:
            path.append(int(i))
    return path


def mnemonic_to_private_key(mnemonic: str, str_derivation_path: str = LEDGER_ETH_DERIVATION_PATH,
                            passphrase: str = "") -> bytes:
    """ Performs all convertions to get a private key from a mnemonic sentence, including:

            BIP39 mnemonic to seed
            BIP32 seed to master key
            BIP32 child derivation of a path provided

        Parameters:
            mnemonic -- seed wordlist, usually with 24 words, that is used for ledger wallet backup
            str_derivation_path -- string that directs BIP32 key derivation, defaults to path
                used by ledger ETH wallet

    """
    derivation_path = parse_derivation_path(str_derivation_path)
    bip39seed = mnemonic_to_bip39seed(mnemonic, passphrase)
    master_private_key, master_chain_code = bip39seed_to_bip32masternode(bip39seed)
    private_key, chain_code = master_private_key, master_chain_code
    for i in derivation_path:
        private_key, chain_code = derive_bip32childkey(private_key, chain_code, i)
    return private_key

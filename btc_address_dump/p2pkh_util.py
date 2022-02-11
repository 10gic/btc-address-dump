import base58
import base58grs
import os
import sys

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(file_path))

import common_util


def pubkey_to_hash160(pubkey: bytes) -> bytes:
    """ Computes ripemd160(sha256(pubkey)) """
    out1 = common_util.sha256(pubkey)
    out2 = common_util.ripemd160(out1)
    return out2


def hash160_to_p2pkh_addr(hash160: bytes, version: bytes) -> bytes:
    """ Derives legacy (p2pkh) address from hash160 of pubkey """
    # Base-58 encoding with a checksum
    checksum = common_util.base58_cksum(version + hash160)
    address = base58.b58encode(version + hash160 + checksum)
    return address


def pubkey_to_p2pkh_addr(pubkey: bytes, version: bytes) -> bytes:
    """ Derives legacy (p2pkh) address from pubkey """
    out1 = common_util.sha256(pubkey)
    out2 = common_util.ripemd160(out1)
    # Base-58 encoding with a checksum
    checksum = common_util.base58_cksum(version + out2)
    address = base58.b58encode(version + out2 + checksum)
    return address


def grs_hash160_to_p2pkh_addr(hash160: bytes, version: bytes) -> bytes:
    """ Derives legacy (p2pkh) address from hash160 of pubkey """
    # Base-58 encoding with a checksum
    checksum = common_util.grs_base58_cksum(version + hash160)
    address = base58grs.b58encode(version + hash160 + checksum)
    return address


def grs_pubkey_to_p2pkh_addr(pubkey: bytes, version: bytes) -> bytes:
    """ Derives legacy (p2pkh) address from pubkey """
    out1 = common_util.sha256(pubkey)
    out2 = common_util.ripemd160(out1)
    # Base-58 encoding with a checksum
    checksum = common_util.grs_base58_cksum(version + out2)
    address = base58grs.b58encode(version + out2 + checksum)
    return address

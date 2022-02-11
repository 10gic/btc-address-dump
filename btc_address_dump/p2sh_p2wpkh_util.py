import base58
import base58grs
import os
import sys

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(file_path))

import common_util


def hash160_to_p2sh_p2wpkh_addr(hash160: bytes, version: bytes) -> bytes:
    redeem_script = b'\x00\x14' + hash160  # 0x00: OP_0, 0x14: PushData
    redeem_hash = common_util.sha256(redeem_script)
    redeem_rip = common_util.ripemd160(redeem_hash)
    # Base-58 encoding with a checksum
    checksum = common_util.base58_cksum(version + redeem_rip)
    address = base58.b58encode(version + redeem_rip + checksum)
    return address


def pubkey_to_p2sh_p2wpkh_addr(pubkey_compressed: bytes, version: bytes) -> bytes:
    """ Derives p2sh-segwit (p2sh p2wpkh) address from pubkey """
    pubkey_hash = common_util.sha256(pubkey_compressed)
    rip = common_util.ripemd160(pubkey_hash)
    return hash160_to_p2sh_p2wpkh_addr(rip, version)


def grs_hash160_to_p2sh_p2wpkh_addr(hash160: bytes, version: bytes) -> bytes:
    redeem_script = b'\x00\x14' + hash160  # 0x00: OP_0, 0x14: PushData
    redeem_hash = common_util.sha256(redeem_script)
    redeem_rip = common_util.ripemd160(redeem_hash)
    # Base-58 encoding with a checksum
    checksum = common_util.grs_base58_cksum(version + redeem_rip)
    address = base58grs.b58encode(version + redeem_rip + checksum)
    return address


def grs_pubkey_to_p2sh_p2wpkh_addr(pubkey_compressed: bytes, version: bytes) -> bytes:
    """ Derives p2sh-segwit (p2sh p2wpkh) address from pubkey """
    pubkey_hash = common_util.sha256(pubkey_compressed)
    rip = common_util.ripemd160(pubkey_hash)
    return grs_hash160_to_p2sh_p2wpkh_addr(rip, version)

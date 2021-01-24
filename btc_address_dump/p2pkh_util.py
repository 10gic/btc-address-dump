import base58
import os
import sys

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(file_path))

import common_util


def pubkey_to_p2pkh_addr(pubkey: bytes, version: bytes) -> bytes:
    """ Derives legacy (p2pkh) address from pubkey """
    out1 = common_util.sha256(pubkey)
    out2 = common_util.ripemd160(out1)
    # Base-58 encoding with a checksum
    checksum = common_util.base58_cksum(version + out2)
    address = base58.b58encode(version + out2 + checksum)
    return address

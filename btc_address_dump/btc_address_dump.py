#!/usr/bin/env python3
import os
import sys
import re
import binascii
import ecdsa
from ecdsa.curves import SECP256k1

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(file_path))

import mnemonic_util
import wif_util
import p2pkh_util
import p2wpkh_util


def prikey_to_pubkey(private_key, compressed_pubkey=False):
    Q = int.from_bytes(private_key, byteorder='big') * ecdsa.curves.SECP256k1.generator
    xstr = Q.x().to_bytes(32, byteorder='big')
    ystr = Q.y().to_bytes(32, byteorder='big')
    if compressed_pubkey:
        parity = Q.y() & 1
        return (2 + parity).to_bytes(1, byteorder='big') + xstr
    else:
        return b'\04' + xstr + ystr


def pubkey_compressed_to_uncompressed(compressed_pubkey: bytes) -> bytes:
    # modulo p which is defined by secp256k1's spec
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    x = int.from_bytes(compressed_pubkey[1:33], byteorder='big')
    y_sq = (pow(x, 3, p) + 7) % p
    y = pow(y_sq, (p + 1) // 4, p)
    if compressed_pubkey[0] % 2 != y % 2:
        y = p - y
    y = y.to_bytes(32, byteorder='big')
    return compressed_pubkey[1:33] + y  # x + y


def pubkey_uncompressed_to_compressed(uncompressed_pubkey: bytes) -> bytes:
    # Compressed public key is:
    # 0x02 + x - coordinate if y is even
    # 0x03 + x - coordinate if y is odd
    x = int.from_bytes(uncompressed_pubkey[1:33], byteorder='big') # uncompressed_pubkey must start with b'\04'
    y = int.from_bytes(uncompressed_pubkey[32:65], byteorder='big')
    parity = y & 1
    compressed_public_key = (2 + parity).to_bytes(1, byteorder='big') + x.to_bytes(32, byteorder='big')
    return compressed_public_key


def main_entry(argv):
    mnemonic = ''
    private_key = ''
    private_key_wif = ''
    private_key_wif_compressed = ''
    public_key_uncompressed = ''
    public_key_compressed = ''
    addr_p2pkh_uncompressed = ''
    addr_p2pkh_compressed = ''
    addr_p2wpkh = ''
    if len(argv) == 1:
        sys.stderr.write("usage: {0} [mnemonic-words|private-key|public-key]\n".format(argv[0]))
        sys.exit(1)
    addresses = argv[1:]
    for address_input in addresses:
        if re.search("^([a-zA-Z]+\\s){11}([a-zA-Z]+).*$", address_input):
            # 12 mnemonic words
            # For example: olympic wine chicken argue unaware bundle tunnel grid spider slot spell need
            sys.stderr.write("you input mnemonic\n")
            mnemonic = address_input
            private_key = mnemonic_util.mnemonic_to_private_key(mnemonic)
            private_key_wif = wif_util.gen_wif_key(private_key)
            private_key_wif_compressed = wif_util.gen_wif_key(private_key, compressed_WIF=True)
            public_key_uncompressed = prikey_to_pubkey(private_key, compressed_pubkey=False)
            public_key_compressed = pubkey_uncompressed_to_compressed(public_key_uncompressed)
            addr_p2pkh_uncompressed = p2pkh_util.pubkey_to_addr(public_key_uncompressed)
            addr_p2pkh_compressed = p2pkh_util.pubkey_to_addr(public_key_compressed)
            addr_p2wpkh = p2wpkh_util.pubkey_to_segwit_addr(public_key_compressed)
        elif (len(address_input) == 66 and address_input.startswith("0x")) or len(address_input) == 64:
            sys.stderr.write("you input private key\n")
            # private key
            # For example: 0xc7ac679b56f50bfd54dd924fe45a8dca7a1c2dced254b03dac22afc03adb9127
            # For example: c7ac679b56f50bfd54dd924fe45a8dca7a1c2dced254b03dac22afc03adb9127
            private_key_hex = address_input.lower().replace('0x', '')
            private_key = binascii.unhexlify(private_key_hex)
            private_key_wif = wif_util.gen_wif_key(private_key)
            private_key_wif_compressed = wif_util.gen_wif_key(private_key, compressed_WIF=True)
            public_key_uncompressed = prikey_to_pubkey(private_key, compressed_pubkey=False)
            public_key_compressed = pubkey_uncompressed_to_compressed(public_key_uncompressed)
            addr_p2pkh_uncompressed = p2pkh_util.pubkey_to_addr(public_key_uncompressed)
            addr_p2pkh_compressed = p2pkh_util.pubkey_to_addr(public_key_compressed)
            addr_p2wpkh = p2wpkh_util.pubkey_to_segwit_addr(public_key_compressed)
        elif (len(address_input) == 130 and address_input.startswith("0x")) or len(address_input) == 128 \
                or (len(address_input) == 132 and address_input.startswith("0x04")) \
                or (len(address_input) == 130 and address_input.startswith("04")):
            sys.stderr.write("you input uncompressed public key\n")
            # public key
            # For example: 0x4cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
            # For example: 4cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
            # For example: 0x044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
            # For example: 044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
            public_key_hex = address_input[-128:]  # keep last 128 (remove leading 0x04, 0x, 04)
            public_key_uncompressed = b'\04' + binascii.unhexlify(public_key_hex)
            public_key_compressed = pubkey_uncompressed_to_compressed(public_key_uncompressed)
            addr_p2pkh_uncompressed = p2pkh_util.pubkey_to_addr(public_key_uncompressed)
            addr_p2pkh_compressed = p2pkh_util.pubkey_to_addr(public_key_compressed)
            addr_p2wpkh = p2wpkh_util.pubkey_to_segwit_addr(public_key_compressed)
        elif (len(address_input) == 68 and address_input.startswith("0x")) or len(address_input) == 66:
            sys.stderr.write("you input compressed public key\n")
            # compressed public key
            # For example: 0x024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
            # For example: 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
            public_key_compressed_hexstr = address_input.lower().replace('0x', '')
            public_key_compressed = binascii.unhexlify(public_key_compressed_hexstr)
            public_key_uncompressed = pubkey_compressed_to_uncompressed(public_key_compressed)
            addr_p2pkh_uncompressed = p2pkh_util.pubkey_to_addr(public_key_uncompressed)
            addr_p2pkh_compressed = p2pkh_util.pubkey_to_addr(public_key_compressed)
            addr_p2wpkh = p2wpkh_util.pubkey_to_segwit_addr(public_key_compressed)
        elif address_input.startswith("5") or address_input.startswith("K") or address_input.startswith("L"):
            private_key = wif_util.decode_wif(address_input)
            private_key_wif = wif_util.gen_wif_key(private_key)
            private_key_wif_compressed = wif_util.gen_wif_key(private_key, compressed_WIF=True)
            public_key_uncompressed = prikey_to_pubkey(private_key, compressed_pubkey=False)
            public_key_compressed = pubkey_uncompressed_to_compressed(public_key_uncompressed)
            addr_p2pkh_uncompressed = p2pkh_util.pubkey_to_addr(public_key_uncompressed)
            addr_p2pkh_compressed = p2pkh_util.pubkey_to_addr(public_key_compressed)
            addr_p2wpkh = p2wpkh_util.pubkey_to_segwit_addr(public_key_compressed)
        else:
            sys.stderr.write("invalid input: {0}\n".format(address_input))
            sys.exit(1)

        if mnemonic:
            print("mnemonic = {}".format(mnemonic))
        if private_key:
            print("private key (hex) = {}".format(str(binascii.hexlify(private_key), 'ascii')))
        if private_key_wif:
            print("private key (WIF) = {}".format(str(private_key_wif, 'ascii')))
        if private_key_wif_compressed:
            print("private key (WIF compressed) = {}".format(str(private_key_wif_compressed, 'ascii')))
        if public_key_uncompressed:
            print("public key (uncompressed) = {}".format(str(binascii.hexlify(public_key_uncompressed), 'ascii')))
        if public_key_compressed:
            print("public key (compressed) = {}".format(str(binascii.hexlify(public_key_compressed), 'ascii')))
        if addr_p2pkh_uncompressed:
            print("address (p2pkh uncompressed) = {}".format(str(addr_p2pkh_uncompressed, 'ascii')))
        if addr_p2pkh_compressed:
            print("address (p2pkh compressed) = {}".format(str(addr_p2pkh_compressed, 'ascii')))
        if addr_p2wpkh:
            print("address (p2wpkh) = {}".format(addr_p2wpkh))


if __name__ == '__main__':
    main_entry(sys.argv)

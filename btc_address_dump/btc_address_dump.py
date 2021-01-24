#!/usr/bin/env python3
import os
import sys
import re
import argparse

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(file_path))

import mnemonic_util
import wif_util
import p2pkh_util
import p2wpkh_util
import p2sh_p2wpkh_util
import common_util


def main_entry(argv):
    mnemonic = ''
    private_key = b''
    private_key_wif = b''
    private_key_wif_compressed = b''
    public_key_uncompressed = b''
    public_key_compressed = b''
    addr_p2pkh_uncompressed = b''
    addr_p2pkh_compressed = b''
    addr_p2sh_p2wpkh = b''
    addr_p2wpkh = ''

    parser = argparse.ArgumentParser(description='A utility for dump btc address')
    parser.add_argument(
        "-c",
        "--chain",
        help="specify btc chain, can be main or test",
        metavar='main|test',
        default="main",
        dest="chain",
        choices=["main", "test"])
    parser.add_argument("inputs", metavar="mnemonic-words|private-key|public-key")
    args = parser.parse_args(argv[1:])
    chain = args.chain
    inputs = args.inputs

    # See https://en.bitcoin.it/wiki/List_of_address_prefixes
    pubkey_version_bytes = b'\x00'  # 0x00 for mainnet, 0x6f for testnet
    script_version_bytes = b'\x05'  # 0x05 for mainnet, 0xc4 for testnet
    wif_version_bytes = b'\x80'  # 0x80 for mainnet, 0xef for testnet
    human_readable_part = "bc"  # "bc" for mainnet, and "tb" for testnet
    if chain == "test":
        pubkey_version_bytes = b'\x6f'
        script_version_bytes = b'\xc4'
        wif_version_bytes = b'\xef'
        human_readable_part = "tb"

    if re.search("^([a-zA-Z]+\\s){11}([a-zA-Z]+).*$", inputs):
        # 12 mnemonic words
        # For example: olympic wine chicken argue unaware bundle tunnel grid spider slot spell need
        # sys.stderr.write("you input mnemonic\n")
        mnemonic = inputs
        private_key = mnemonic_util.mnemonic_to_private_key(mnemonic)
        private_key_wif = wif_util.encode_wif(private_key, wif_version_bytes)
        private_key_wif_compressed = wif_util.encode_wif(private_key, wif_version_bytes, compressed_wif=True)
        public_key_uncompressed = common_util.prikey_to_pubkey(private_key, compressed=False)
        public_key_compressed = common_util.pubkey_uncompressed_to_compressed(public_key_uncompressed)
        addr_p2pkh_uncompressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_uncompressed, pubkey_version_bytes)
        addr_p2pkh_compressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_compressed, pubkey_version_bytes)
        addr_p2sh_p2wpkh = p2sh_p2wpkh_util.pubkey_to_p2sh_p2wpkh_addr(public_key_compressed, script_version_bytes)
        addr_p2wpkh = p2wpkh_util.pubkey_to_segwit_addr(human_readable_part, public_key_compressed)
    elif (len(inputs) == 66 and inputs.startswith("0x")) or len(inputs) == 64:
        # sys.stderr.write("you input private key\n")
        # private key
        # For example: 0xc7ac679b56f50bfd54dd924fe45a8dca7a1c2dced254b03dac22afc03adb9127
        # For example: c7ac679b56f50bfd54dd924fe45a8dca7a1c2dced254b03dac22afc03adb9127
        private_key_hex = inputs.lower().replace('0x', '')
        private_key = bytes.fromhex(private_key_hex)
        private_key_wif = wif_util.encode_wif(private_key, wif_version_bytes)
        private_key_wif_compressed = wif_util.encode_wif(private_key, wif_version_bytes, compressed_wif=True)
        public_key_uncompressed = common_util.prikey_to_pubkey(private_key, compressed=False)
        public_key_compressed = common_util.pubkey_uncompressed_to_compressed(public_key_uncompressed)
        addr_p2pkh_uncompressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_uncompressed, pubkey_version_bytes)
        addr_p2pkh_compressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_compressed, pubkey_version_bytes)
        addr_p2sh_p2wpkh = p2sh_p2wpkh_util.pubkey_to_p2sh_p2wpkh_addr(public_key_compressed, script_version_bytes)
        addr_p2wpkh = p2wpkh_util.pubkey_to_segwit_addr(human_readable_part, public_key_compressed)
    elif (len(inputs) == 130 and inputs.startswith("0x")) or len(inputs) == 128 \
            or (len(inputs) == 132 and inputs.startswith("0x04")) \
            or (len(inputs) == 130 and inputs.startswith("04")):
        # sys.stderr.write("you input uncompressed public key\n")
        # public key
        # For example: 0x4cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
        # For example: 4cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
        # For example: 0x044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
        # For example: 044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
        public_key_hex = inputs[-128:]  # keep last 128 (remove leading 0x04, 0x, 04)
        public_key_uncompressed = b'\04' + bytes.fromhex(public_key_hex)
        public_key_compressed = common_util.pubkey_uncompressed_to_compressed(public_key_uncompressed)
        addr_p2pkh_uncompressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_uncompressed, pubkey_version_bytes)
        addr_p2pkh_compressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_compressed, pubkey_version_bytes)
        addr_p2sh_p2wpkh = p2sh_p2wpkh_util.pubkey_to_p2sh_p2wpkh_addr(public_key_compressed, script_version_bytes)
        addr_p2wpkh = p2wpkh_util.pubkey_to_segwit_addr(human_readable_part, public_key_compressed)
    elif (len(inputs) == 68 and inputs.startswith("0x")) or len(inputs) == 66:
        # sys.stderr.write("you input compressed public key\n")
        # compressed public key
        # For example: 0x024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
        # For example: 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
        public_key_compressed_hexstr = inputs.lower().replace('0x', '')
        public_key_compressed = bytes.fromhex(public_key_compressed_hexstr)
        public_key_uncompressed = common_util.pubkey_compressed_to_uncompressed(public_key_compressed)
        addr_p2pkh_uncompressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_uncompressed, pubkey_version_bytes)
        addr_p2pkh_compressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_compressed, pubkey_version_bytes)
        addr_p2sh_p2wpkh = p2sh_p2wpkh_util.pubkey_to_p2sh_p2wpkh_addr(public_key_compressed, script_version_bytes)
        addr_p2wpkh = p2wpkh_util.pubkey_to_segwit_addr(human_readable_part, public_key_compressed)
    elif inputs.startswith("5") or inputs.startswith("K") or inputs.startswith("L"):
        private_key = wif_util.decode_wif(inputs)
        private_key_wif = wif_util.encode_wif(private_key, wif_version_bytes)
        private_key_wif_compressed = wif_util.encode_wif(private_key, wif_version_bytes, compressed_wif=True)
        public_key_uncompressed = common_util.prikey_to_pubkey(private_key, compressed=False)
        public_key_compressed = common_util.pubkey_uncompressed_to_compressed(public_key_uncompressed)
        addr_p2pkh_uncompressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_uncompressed, pubkey_version_bytes)
        addr_p2pkh_compressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_compressed, pubkey_version_bytes)
        addr_p2sh_p2wpkh = p2sh_p2wpkh_util.pubkey_to_p2sh_p2wpkh_addr(public_key_compressed, script_version_bytes)
        addr_p2wpkh = p2wpkh_util.pubkey_to_segwit_addr(human_readable_part, public_key_compressed)
    else:
        sys.stderr.write("invalid input: {0}\n".format(inputs))
        sys.exit(1)

    if mnemonic:
        print("mnemonic = {}".format(mnemonic))
    if private_key:
        print("private key (hex) = {}".format(private_key.hex()))
    if private_key_wif:
        print("private key (WIF) = {}".format(private_key_wif.decode('ascii')))
    if private_key_wif_compressed:
        print("private key (WIF compressed) = {}".format(private_key_wif_compressed.decode('ascii')))
    if public_key_uncompressed:
        print("public key (uncompressed) = {}".format(public_key_uncompressed.hex()))
    if public_key_compressed:
        print("public key (compressed) = {}".format(public_key_compressed.hex()))
    if addr_p2pkh_uncompressed:
        print("legacy address (p2pkh uncompressed) = {}".format(addr_p2pkh_uncompressed.decode('ascii')))
    if addr_p2pkh_compressed:
        print("legacy address (p2pkh compressed) = {}".format(addr_p2pkh_compressed.decode('ascii')))
    if addr_p2sh_p2wpkh:
        print("p2sh-segwit address (p2sh p2wpkh) = {}".format(addr_p2sh_p2wpkh.decode('ascii')))
    if addr_p2wpkh:
        print("bech32 address (p2wpkh) = {}".format(addr_p2wpkh))


if __name__ == '__main__':
    main_entry(sys.argv)

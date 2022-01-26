#!/usr/bin/env python3
import os
import sys
import re
import argparse
import yaml
import cashaddress
from typing import Union

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(file_path))

import mnemonic_util
import wif_util
import p2pkh_util
import p2wpkh_util
import p2sh_p2wpkh_util
import p2tr_util
import common_util


def get_base58_prefix(coins_info, chain: str, typ: str) -> Union[bytes, None]:
    if coins_info[chain]["base58_prefix"][typ] is None:
        return None
    else:
        return coins_info[chain]["base58_prefix"][typ].to_bytes(1, byteorder='big')


def get_bech32_hrp(coins_info, chain: str) -> Union[str, None]:
    return coins_info[chain]["bech32_hrp"]


def get_derivation_path(coins_info, chain: str, typ: str) -> Union[str, None]:
    try:
        derivation_path = coins_info[chain]["hd_path"][typ]
    except KeyError:
        derivation_path = None
    return derivation_path


def main_entry(argv):
    mnemonic = ''
    private_key = b''
    private_key_wif = b''
    private_key_wif_compressed = b''
    public_key_uncompressed = b''
    public_key_compressed = b''
    public_key_uncompressed_hash160 = b''
    public_key_compressed_hash160 = b''
    public_key_hash160 = b''
    taproot_tweaked_private_key = b''
    taproot_tweaked_public_key = b''
    addr_p2pkh_uncompressed = b''
    addr_p2pkh_compressed = b''
    addr_p2pkh = b''  # uncompressed or compressed
    addr_p2sh_p2wpkh = b''
    addr_p2wpkh = ''
    addr_p2tr = ''

    file = open(os.path.join(os.path.abspath(file_path), "coins.yaml"), 'r', encoding="utf-8")
    file_data = file.read()
    file.close()

    coins_info = yaml.load(file_data, Loader=yaml.FullLoader)

    parser = argparse.ArgumentParser(description='A utility for dump btc address')
    parser.add_argument(
        "-c",
        "--chain",
        help="specify chain, default is btc",
        default="btc",
        dest="chain",
        choices=coins_info.keys())
    parser.add_argument(
        "-d",
        "--derivation",
        help="specify derivation path scheme (bip44/bip49/bip84/bip86) or customized path (e.g. m/0'/0/0), default is "
             "bip44. Only applicable when input mnemonic words",
        default="bip44",
        dest="derivation")
    parser.add_argument("inputs", metavar="mnemonic-words|private-key|public-key")
    args = parser.parse_args(argv[1:])
    chain = args.chain
    derivation = args.derivation
    inputs = args.inputs

    # See https://en.bitcoin.it/wiki/List_of_address_prefixes
    pubkey_version_bytes = get_base58_prefix(coins_info, chain, 'pubkey')  # 0x00 for btc mainnet, 0x6f for testnet
    script_version_bytes = get_base58_prefix(coins_info, chain, 'script')  # 0x05 for btc mainnet, 0xc4 for testnet
    wif_version_bytes = get_base58_prefix(coins_info, chain, 'wif')  # 0x80 for btc mainnet, 0xef for testnet
    human_readable_part = get_bech32_hrp(coins_info, chain)  # "bc" for btc mainnet, and "tb" for testnet

    if re.search("^([a-zA-Z]+\\s){11}([a-zA-Z]+).*$", inputs):
        # 12 mnemonic words
        # For example: olympic wine chicken argue unaware bundle tunnel grid spider slot spell need
        # sys.stderr.write("you input mnemonic\n")
        mnemonic = inputs
        derivation_path = derivation if derivation.startswith("m/") else get_derivation_path(coins_info, chain, derivation)
        if derivation_path is None or len(derivation_path) == 0:
            sys.stderr.write("derivation path {} is not available for {}\n".format(derivation, chain))
            sys.exit(1)
        private_key = mnemonic_util.mnemonic_to_private_key(mnemonic, derivation_path)
        private_key_wif = wif_util.encode_wif(private_key, wif_version_bytes)
        private_key_wif_compressed = wif_util.encode_wif(private_key, wif_version_bytes, compressed_wif=True)
        public_key_compressed = common_util.prikey_to_pubkey(private_key, compressed=True)
        public_key_compressed_hash160 = p2pkh_util.pubkey_to_hash160(public_key_compressed)
        if derivation == "bip44":
            # For legacy address
            addr_p2pkh_compressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_compressed, pubkey_version_bytes)
        elif derivation == "bip49":
            # For p2sh-segwit address
            if script_version_bytes:
                addr_p2sh_p2wpkh = p2sh_p2wpkh_util.pubkey_to_p2sh_p2wpkh_addr(public_key_compressed,
                                                                               script_version_bytes)
        elif derivation == "bip84":
            # For bech32 address
            if human_readable_part:
                addr_p2wpkh = p2wpkh_util.pubkey_to_segwit_v0_addr(human_readable_part, public_key_compressed)
        elif derivation == "bip86":
            # For bech32m address
            if human_readable_part:
                taproot_tweaked_private_key = p2tr_util.taproot_tweak_seckey(private_key)
                public_key_x_coordinate = public_key_compressed[1:33]
                taproot_tweaked_public_key = p2tr_util.public_key_x_coordinate_to_taproot_tweaked_pubkey(public_key_x_coordinate)
                addr_p2tr = p2wpkh_util.pubkey_to_segwit_v1_addr(human_readable_part, taproot_tweaked_public_key)
        elif derivation.startswith("m/"):  # customized path
            # For legacy address
            addr_p2pkh_compressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_compressed, pubkey_version_bytes)
            # For p2sh-segwit address
            if script_version_bytes:
                addr_p2sh_p2wpkh = p2sh_p2wpkh_util.pubkey_to_p2sh_p2wpkh_addr(public_key_compressed,
                                                                               script_version_bytes)
            # For bech32 address
            if human_readable_part:
                addr_p2wpkh = p2wpkh_util.pubkey_to_segwit_v0_addr(human_readable_part, public_key_compressed)
            # For bech32m address
            if human_readable_part:
                taproot_tweaked_private_key = p2tr_util.taproot_tweak_seckey(private_key)
                public_key_x_coordinate = public_key_compressed[1:33]
                taproot_tweaked_public_key = p2tr_util.public_key_x_coordinate_to_taproot_tweaked_pubkey(public_key_x_coordinate)
                addr_p2tr = p2wpkh_util.pubkey_to_segwit_v1_addr(human_readable_part, taproot_tweaked_public_key)
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
        public_key_uncompressed_hash160 = p2pkh_util.pubkey_to_hash160(public_key_uncompressed)
        public_key_compressed_hash160 = p2pkh_util.pubkey_to_hash160(public_key_compressed)
        addr_p2pkh_uncompressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_uncompressed, pubkey_version_bytes)
        addr_p2pkh_compressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_compressed, pubkey_version_bytes)
        if script_version_bytes:
            addr_p2sh_p2wpkh = p2sh_p2wpkh_util.pubkey_to_p2sh_p2wpkh_addr(public_key_compressed, script_version_bytes)
        if human_readable_part:
            addr_p2wpkh = p2wpkh_util.pubkey_to_segwit_v0_addr(human_readable_part, public_key_compressed)
            taproot_tweaked_private_key = p2tr_util.taproot_tweak_seckey(private_key)
            public_key_x_coordinate = public_key_compressed[1:33]
            taproot_tweaked_public_key = p2tr_util.public_key_x_coordinate_to_taproot_tweaked_pubkey(public_key_x_coordinate)
            addr_p2tr = p2wpkh_util.pubkey_to_segwit_v1_addr(human_readable_part, taproot_tweaked_public_key)
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
        public_key_uncompressed_hash160 = p2pkh_util.pubkey_to_hash160(public_key_uncompressed)
        public_key_compressed_hash160 = p2pkh_util.pubkey_to_hash160(public_key_compressed)
        addr_p2pkh_uncompressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_uncompressed, pubkey_version_bytes)
        addr_p2pkh_compressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_compressed, pubkey_version_bytes)
        if script_version_bytes:
            addr_p2sh_p2wpkh = p2sh_p2wpkh_util.pubkey_to_p2sh_p2wpkh_addr(public_key_compressed, script_version_bytes)
        if human_readable_part:
            addr_p2wpkh = p2wpkh_util.pubkey_to_segwit_v0_addr(human_readable_part, public_key_compressed)
            public_key_x_coordinate = public_key_compressed[1:33]
            taproot_tweaked_public_key = p2tr_util.public_key_x_coordinate_to_taproot_tweaked_pubkey(public_key_x_coordinate)
            addr_p2tr = p2wpkh_util.pubkey_to_segwit_v1_addr(human_readable_part, taproot_tweaked_public_key)
    elif (len(inputs) == 68 and inputs.startswith("0x")) or len(inputs) == 66:
        # sys.stderr.write("you input compressed public key\n")
        # compressed public key
        # For example: 0x024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
        # For example: 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
        public_key_compressed_hexstr = inputs.lower().replace('0x', '')
        public_key_compressed = bytes.fromhex(public_key_compressed_hexstr)
        public_key_uncompressed = common_util.pubkey_compressed_to_uncompressed(public_key_compressed)
        public_key_uncompressed_hash160 = p2pkh_util.pubkey_to_hash160(public_key_uncompressed)
        public_key_compressed_hash160 = p2pkh_util.pubkey_to_hash160(public_key_compressed)
        addr_p2pkh_uncompressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_uncompressed, pubkey_version_bytes)
        addr_p2pkh_compressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_compressed, pubkey_version_bytes)
        if script_version_bytes:
            addr_p2sh_p2wpkh = p2sh_p2wpkh_util.pubkey_to_p2sh_p2wpkh_addr(public_key_compressed, script_version_bytes)
        if human_readable_part:
            addr_p2wpkh = p2wpkh_util.pubkey_to_segwit_v0_addr(human_readable_part, public_key_compressed)
            public_key_x_coordinate = public_key_compressed[1:33]
            taproot_tweaked_public_key = p2tr_util.public_key_x_coordinate_to_taproot_tweaked_pubkey(public_key_x_coordinate)
            addr_p2tr = p2wpkh_util.pubkey_to_segwit_v1_addr(human_readable_part, taproot_tweaked_public_key)
    elif (len(inputs) == 42 and inputs.startswith("0x")) or len(inputs) == 40:
        # sys.stderr.write("you input hash160 of public key\n")
        public_key_hash160 = bytes.fromhex(inputs.lower().replace('0x', ''))
        addr_p2pkh = p2pkh_util.hash160_to_p2pkh_addr(public_key_hash160, pubkey_version_bytes)
        if script_version_bytes:
            addr_p2sh_p2wpkh = p2sh_p2wpkh_util.hash160_to_p2sh_p2wpkh_addr(public_key_hash160, script_version_bytes)
        if human_readable_part:
            addr_p2wpkh = p2wpkh_util.hash160_to_segwit_v0_addr(human_readable_part, public_key_hash160)
    elif wif_util.is_valid_wif(inputs):
        if chain == "btc":
            assert inputs.startswith('5') or inputs.startswith('K') or inputs.startswith('L')
        if chain == "btc-test":
            assert inputs.startswith('9') or inputs.startswith('c')
        private_key = wif_util.decode_wif(inputs)
        private_key_wif = wif_util.encode_wif(private_key, wif_version_bytes)
        private_key_wif_compressed = wif_util.encode_wif(private_key, wif_version_bytes, compressed_wif=True)
        public_key_uncompressed = common_util.prikey_to_pubkey(private_key, compressed=False)
        public_key_compressed = common_util.pubkey_uncompressed_to_compressed(public_key_uncompressed)
        public_key_uncompressed_hash160 = p2pkh_util.pubkey_to_hash160(public_key_uncompressed)
        public_key_compressed_hash160 = p2pkh_util.pubkey_to_hash160(public_key_compressed)
        addr_p2pkh_uncompressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_uncompressed, pubkey_version_bytes)
        addr_p2pkh_compressed = p2pkh_util.pubkey_to_p2pkh_addr(public_key_compressed, pubkey_version_bytes)
        if script_version_bytes:
            addr_p2sh_p2wpkh = p2sh_p2wpkh_util.pubkey_to_p2sh_p2wpkh_addr(public_key_compressed, script_version_bytes)
        if human_readable_part:
            addr_p2wpkh = p2wpkh_util.pubkey_to_segwit_v0_addr(human_readable_part, public_key_compressed)
            taproot_tweaked_private_key = p2tr_util.taproot_tweak_seckey(private_key)
            public_key_x_coordinate = public_key_compressed[1:33]
            taproot_tweaked_public_key = p2tr_util.public_key_x_coordinate_to_taproot_tweaked_pubkey(public_key_x_coordinate)
            addr_p2tr = p2wpkh_util.pubkey_to_segwit_v1_addr(human_readable_part, taproot_tweaked_public_key)
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
    if taproot_tweaked_private_key:
        print("taproot tweaked private key = {}".format(taproot_tweaked_private_key.hex()))
    if public_key_uncompressed:
        print("public key (uncompressed) = {}".format(public_key_uncompressed.hex()))
    if public_key_compressed:
        print("public key (compressed) = {}".format(public_key_compressed.hex()))
    if public_key_uncompressed_hash160:
        print("hash160 of uncompressed public key = {}".format(public_key_uncompressed_hash160.hex()))
    if public_key_compressed_hash160:
        print("hash160 of compressed public key = {}".format(public_key_compressed_hash160.hex()))
    if public_key_hash160:
        print("hash160 of public key = {}".format(public_key_hash160.hex()))
    if taproot_tweaked_public_key:
        print("taproot tweaked public key (taproot output key) = {}".format(taproot_tweaked_public_key.hex()))
    if addr_p2pkh_uncompressed:
        print("legacy address (p2pkh uncompressed) = {}".format(addr_p2pkh_uncompressed.decode('ascii')))
        if chain == "bch":
            print("bitcoin cash address (p2pkh uncompressed) = {}".format(cashaddress.convert.to_cash_address(addr_p2pkh_uncompressed.decode('ascii'))))
    if addr_p2pkh_compressed:
        print("legacy address (p2pkh compressed) = {}".format(addr_p2pkh_compressed.decode('ascii')))
        if chain == "bch":
            print("bitcoin cash address (p2pkh compressed) = {}".format(cashaddress.convert.to_cash_address(addr_p2pkh_compressed.decode('ascii'))))
    if addr_p2pkh:
        print("legacy address (p2pkh) = {}".format(addr_p2pkh.decode('ascii')))
        if chain == "bch":
            print("bitcoin cash address (p2pkh) = {}".format(cashaddress.convert.to_cash_address(addr_p2pkh.decode('ascii'))))
    if addr_p2sh_p2wpkh:
        if public_key_hash160:
            print("p2sh-segwit address (only valid if input is hash160 of COMPRESSED public key) = {}".format(
                addr_p2sh_p2wpkh.decode('ascii')))
        else:
            print("p2sh-segwit address (p2sh p2wpkh) = {}".format(addr_p2sh_p2wpkh.decode('ascii')))
    if addr_p2wpkh:
        if public_key_hash160:
            print("bech32 address (only valid if input is hash160 of COMPRESSED public key) = {}".format(addr_p2wpkh))
        else:
            print("bech32 address (p2wpkh) = {}".format(addr_p2wpkh))
    if addr_p2tr:
        print("bech32m address (p2tr) = {}".format(addr_p2tr))


if __name__ == '__main__':
    main_entry(sys.argv)

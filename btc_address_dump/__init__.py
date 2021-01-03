"""btc-address-dump.
A utility for dump btc address from mnemonic words or private key or public key.
"""
from .btc_address_dump import main_entry

import sys


def run_main():
    main_entry(sys.argv)

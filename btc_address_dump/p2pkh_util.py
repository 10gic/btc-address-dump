import hashlib
import binascii
import base58


def sha256(hex_str: bytes) -> bytes:
    sha = hashlib.sha256()
    sha.update(hex_str)
    return sha.digest()


def ripemd160(hex_str: bytes) -> bytes:
    rip = hashlib.new('ripemd160')
    rip.update(hex_str)
    return rip.digest()


def compute_cksum(hex_str: bytes) -> bytes:
    s1 = sha256(hex_str)
    #print('s1=', binascii.hexlify(s1)) # d094b259d52d874cf084aaece4251e5d3b731fe66fe2dc21564106330d25f278
    s2 = sha256(s1)
    # print('s2=', binascii.hexlify(s2)) # 37fefcd01823fdbce992747702d2420b11a5d266b92d516a93aa83f336ce8241
    checksum = s2[0:4]
    return checksum


def pubkey_to_addr(pubkey: bytes) -> bytes:
    out1 = sha256(pubkey)
    #print(binascii.hexlify(out1)) # 448997ae8759eb23d6c6b67de6fc3419006cbf061617c3e07323aaf5bcd53476
    out2 = ripemd160(out1)
    #print(binascii.hexlify(out2)) # bbc1e42a39d05a4cc61752d6963b7f69d09bb27b

    version = b'\x00'              # 0x00 for Main Network, 0x6f for Test Network

    checksum = compute_cksum(version + out2)
    #print('checksum', binascii.hexlify(checksum))  # 37fefcd0

    out3 = version + out2 + checksum
    #print(binascii.hexlify(out3))

    address = base58.b58encode(out3)
    return address

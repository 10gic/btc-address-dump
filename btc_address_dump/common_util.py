import ecdsa
import hashlib
from ecdsa.ellipticcurve import PointJacobi


def sha256(inputs: bytes) -> bytes:
    """ Computes sha256 """
    sha = hashlib.sha256()
    sha.update(inputs)
    return sha.digest()


def ripemd160(inputs: bytes) -> bytes:
    """ Computes ripemd160 """
    rip = hashlib.new('ripemd160')
    rip.update(inputs)
    return rip.digest()


def base58_cksum(inputs: bytes) -> bytes:
    """ Computes base 58 four bytes check sum """
    s1 = sha256(inputs)
    s2 = sha256(s1)
    checksum = s2[0:4]
    return checksum


def pubkey_compressed_to_uncompressed(compressed_pubkey: bytes) -> bytes:
    """ Converts compressed pubkey to uncompressed format """
    assert len(compressed_pubkey) == 33
    # modulo p which is defined by secp256k1's spec
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    x = int.from_bytes(compressed_pubkey[1:33], byteorder='big')
    y_sq = (pow(x, 3, p) + 7) % p
    y = pow(y_sq, (p + 1) // 4, p)
    if compressed_pubkey[0] % 2 != y % 2:
        y = p - y
    y_bytes = y.to_bytes(32, byteorder='big')
    return b'\04' + compressed_pubkey[1:33] + y_bytes  # x + y


def pubkey_uncompressed_to_compressed(uncompressed_pubkey: bytes) -> bytes:
    """ Converts uncompressed pubkey to compressed format """
    assert len(uncompressed_pubkey) == 65
    # Compressed public key is:
    # 0x02 + x - coordinate if y is even
    # 0x03 + x - coordinate if y is odd
    x = int.from_bytes(uncompressed_pubkey[1:33], byteorder='big')  # uncompressed_pubkey must contain prefix b'\04'
    y = int.from_bytes(uncompressed_pubkey[33:65], byteorder='big')
    parity = y & 1
    compressed_public_key = (2 + parity).to_bytes(1, byteorder='big') + x.to_bytes(32, byteorder='big')
    return compressed_public_key


def pubkey_from_bytes_to_point(pubkey: bytes) -> tuple[int, int]:
    """ Returns the x y coordinate of a pubkey (can be uncompressed or compressed) """
    assert len(pubkey) == 33 or len(pubkey) == 65
    if len(pubkey) == 33:  # compressed pubkey
        uncompressed_pubkey = pubkey_compressed_to_uncompressed(pubkey)
    else:
        uncompressed_pubkey = pubkey
    x = int.from_bytes(uncompressed_pubkey[1:33], byteorder='big')  # uncompressed_pubkey must contain prefix b'\04'
    y = int.from_bytes(uncompressed_pubkey[33:65], byteorder='big')
    return x, y


def pubkey_from_point_to_bytes(x: int, y: int, compressed: bool = True) -> bytes:
    """ Constructs pubkey from its x y coordinates """
    x_bytes = x.to_bytes(32, byteorder='big')
    y_bytes = y.to_bytes(32, byteorder='big')
    if compressed:
        parity = y & 1
        return (2 + parity).to_bytes(1, byteorder='big') + x_bytes
    else:
        return b'\04' + x_bytes + y_bytes


def prikey_to_pubkey(private_key: bytes, compressed: bool = True) -> bytes:
    """ Derives pubkey from private key """
    pubkey_point: PointJacobi = int.from_bytes(private_key, byteorder='big') * ecdsa.curves.SECP256k1.generator
    return pubkey_from_point_to_bytes(pubkey_point.x(), pubkey_point.y(), compressed)

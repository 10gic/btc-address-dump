import ecdsa
from ecdsa.ellipticcurve import PointJacobi


def pubkey_compressed_to_uncompressed(compressed_pubkey: bytes) -> bytes:
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
    # Compressed public key is:
    # 0x02 + x - coordinate if y is even
    # 0x03 + x - coordinate if y is odd
    x = int.from_bytes(uncompressed_pubkey[1:33], byteorder='big')  # uncompressed_pubkey must contain prefix b'\04'
    y = int.from_bytes(uncompressed_pubkey[33:65], byteorder='big')
    parity = y & 1
    compressed_public_key = (2 + parity).to_bytes(1, byteorder='big') + x.to_bytes(32, byteorder='big')
    return compressed_public_key


def pubkey_from_bytes_to_point(pubkey: bytes) -> tuple[int, int]:
    assert len(pubkey) == 33 or len(pubkey) == 65
    if len(pubkey) == 33:  # compressed pubkey
        uncompressed_pubkey = pubkey_compressed_to_uncompressed(pubkey)
    else:
        uncompressed_pubkey = pubkey
    x = int.from_bytes(uncompressed_pubkey[1:33], byteorder='big')  # uncompressed_pubkey must contain prefix b'\04'
    y = int.from_bytes(uncompressed_pubkey[33:65], byteorder='big')
    return x, y


def pubkey_from_point_to_bytes(x: int, y: int, compressed: bool = True) -> bytes:
    x_bytes = x.to_bytes(32, byteorder='big')
    y_bytes = y.to_bytes(32, byteorder='big')
    if compressed:
        parity = y & 1
        return (2 + parity).to_bytes(1, byteorder='big') + x_bytes
    else:
        return b'\04' + x_bytes + y_bytes


def prikey_to_pubkey(private_key: bytes, compressed_pubkey: bool = True) -> bytes:
    Q: PointJacobi = int.from_bytes(private_key, byteorder='big') * ecdsa.curves.SECP256k1.generator
    return pubkey_from_point_to_bytes(Q.x(), Q.y(), compressed_pubkey)

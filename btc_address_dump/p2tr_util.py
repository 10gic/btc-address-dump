import hashlib
from typing import Tuple, Optional

import ecdsa
from ecdsa.ellipticcurve import PointJacobi, Point


def bytes_from_int(x: int) -> bytes:
    return x.to_bytes(32, byteorder="big")


def int_from_bytes(b: bytes) -> int:
    return int.from_bytes(b, byteorder="big")


def tagged_hash(tag: str, msg: bytes) -> bytes:
    tag_hash = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256(tag_hash + tag_hash + msg).digest()


def lift_x(b: bytes) -> Optional[PointJacobi]:
    """ Define in BIP 340, see https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki
    """
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    x = int_from_bytes(b)
    if x >= p:
        return None
    y_sq = (pow(x, 3, p) + 7) % p
    y = pow(y_sq, (p + 1) // 4, p)
    if pow(y, 2, p) != y_sq:
        return None
    return PointJacobi.from_affine(Point(ecdsa.curves.SECP256k1.curve, x, y if y & 1 == 0 else p - y))


def public_key_x_coordinate_to_taproot_output_key(public_key_x_coordinate: bytes) -> bytes:
    """
    See https://github.com/bitcoin/bips/blob/master/bip-0086.mediawiki

    P:                  lift_x(public_key_x_coordinate)
    internal_key:       P.x()
    Q:                  P + int(HashTapTweak(bytes(P.x()))) * G
    32_byte_output_key: bytes(Q.x())
    """
    P: PointJacobi = lift_x(public_key_x_coordinate)
    assert P is not None
    Q: PointJacobi = P + int_from_bytes(tagged_hash("TapTweak", bytes_from_int(P.x()))) * ecdsa.curves.SECP256k1.generator
    return bytes_from_int(Q.x())

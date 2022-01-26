import hashlib
from typing import Optional

import ecdsa
from ecdsa.ellipticcurve import PointJacobi, Point


def bytes_from_int(x: int) -> bytes:
    return x.to_bytes(32, byteorder="big")


def int_from_bytes(b: bytes) -> int:
    return int.from_bytes(b, byteorder="big")


def tagged_hash(tag: str, msg: bytes) -> bytes:
    tag_hash = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256(tag_hash + tag_hash + msg).digest()


def lift_x(x: bytes) -> Optional[PointJacobi]:
    """
    Define in BIP 340, see https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki

    :param x: an integer in range 0..p-1,
    :return: the point P for which P.x() = x and has_even_y(P), or None if no such point exists.
    """
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    x = int_from_bytes(x)
    if x >= p:
        return None
    y_sq = (pow(x, 3, p) + 7) % p
    y = pow(y_sq, (p + 1) // 4, p)
    if pow(y, 2, p) != y_sq:
        return None
    P: PointJacobi = PointJacobi.from_affine(Point(ecdsa.curves.SECP256k1.curve, x, y if y % 2 == 0 else p - y))
    return P


def has_even_y(P: PointJacobi) -> bool:
    return P.y() % 2 == 0


def taproot_tweak_seckey(seckey0: bytes) -> bytes:
    """
    See https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki
    :param seckey0: the private key
    :return: tweaked private key
    """
    P = int_from_bytes(seckey0) * ecdsa.curves.SECP256k1.generator
    seckey = int_from_bytes(seckey0) if has_even_y(P) else ecdsa.curves.SECP256k1.order - int_from_bytes(seckey0)
    t = int_from_bytes(tagged_hash("TapTweak", bytes_from_int(P.x())))
    if t >= ecdsa.curves.SECP256k1.order:
        raise ValueError
    return bytes_from_int((seckey + t) % ecdsa.curves.SECP256k1.order)


def public_key_x_coordinate_to_taproot_tweaked_pubkey(public_key_x_coordinate: bytes) -> bytes:
    """
    See https://github.com/bitcoin/bips/blob/master/bip-0086.mediawiki

    P:                  lift_x(public_key_x_coordinate)
    internal_key:       P.x()
    Q:                  P + int(HashTapTweak(bytes(P.x()))) * G
    32_byte_output_key: bytes(Q.x())
    """
    P: PointJacobi = lift_x(public_key_x_coordinate)
    assert P is not None
    t = int_from_bytes(tagged_hash("TapTweak", bytes_from_int(P.x())))
    if t >= ecdsa.curves.SECP256k1.order:
        raise ValueError
    Q: PointJacobi = P + t * ecdsa.curves.SECP256k1.generator
    return bytes_from_int(Q.x())

================
btc-address-dump
================

btc-address-dump is a utility for dump btc address from mnemonic words or private key or public key.


Example
=======

Dump btc address from mnemonic words (bip44)::

  $ btc_address_dump "olympic wine chicken argue unaware bundle tunnel grid spider slot spell need"
  mnemonic = olympic wine chicken argue unaware bundle tunnel grid spider slot spell need
  private key (hex) = c7ac679b56f50bfd54dd924fe45a8dca7a1c2dced254b03dac22afc03adb9127
  private key (WIF) = 5KLDyKtrScLYsKMJzVCt8Mf6Nn9DEV7V3fg8njfSZnqe7ZEMqzK
  private key (WIF compressed) = L3urFcPsE2yHf5zeQjVSfUB8j8FEzX5cnmhjNsJfqjKgowPP4tmg
  public key (compressed) = 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
  hash160 of compressed public key = 1075f16844287d6d1c6fefbe2486cd3325127424
  legacy address (p2pkh compressed) = 12W36tm2jnreFiYdrzfE6cvRaKRbicEpnA

Dump btc address from mnemonic words (bip49, P2WPKH-nested-in-P2SH)::

  $ btc_address_dump -d bip49 "olympic wine chicken argue unaware bundle tunnel grid spider slot spell need"
  mnemonic = olympic wine chicken argue unaware bundle tunnel grid spider slot spell need
  private key (hex) = 50b9428b804254993449ce9732728b086b3faf9df8ad49d227473034974dba9e
  private key (WIF) = 5JRqZPwGYSimsreJEZxDoz32b3AqrtbBJ5meE5AFXJoRHSmtL6e
  private key (WIF compressed) = KyvdKzEXbnXP5U7d4tSjYNjx1EaSfChrSQ43JhMq6mZtBUGLshFi
  public key (compressed) = 030edc38bbc13d7aa7afac33ad485c8d4b057661aedb91eb23935be007c57cfa57
  hash160 of compressed public key = 9f2681aefa569e23c031c1719f4635c6dd393b0c
  p2sh-segwit address (p2sh p2wpkh) = 3G3MUYikYqnTLYDzAa1PwxnughktzJydJw

Dump btc address from mnemonic words (bip84, P2WPKH)::

  $ btc_address_dump -d bip84 "olympic wine chicken argue unaware bundle tunnel grid spider slot spell need"
  mnemonic = olympic wine chicken argue unaware bundle tunnel grid spider slot spell need
  private key (hex) = 87d563c902808568dbed8f52eabaf51e5cc7c3e59ec747b5efc0ed2e3cafabeb
  private key (WIF) = 5Jr7GTZpRWRWpSjq6F3u9ekToTyonBcutWS3njTWSfp3RzXxZyF
  private key (WIF compressed) = L1mkfEFrKAsCcQc3G91oBBcqJ65jURsWSLuZJrPzxJJdjFj4uLdu
  public key (compressed) = 03d8468a0d63d215a3650694b5aa68e0186eead5f91ff3abc22319272e0180eb83
  hash160 of compressed public key = 2ca1cb8b4981d03249d741e3dedd0e5f2da65027
  bech32 address (p2wpkh) = bc1q9jsuhz6fs8gryjwhg83aahgwtuk6v5p8h54899

Dump btc address from hex private key::

  $ btc_address_dump c7ac679b56f50bfd54dd924fe45a8dca7a1c2dced254b03dac22afc03adb9127
  private key (hex) = c7ac679b56f50bfd54dd924fe45a8dca7a1c2dced254b03dac22afc03adb9127
  private key (WIF) = 5KLDyKtrScLYsKMJzVCt8Mf6Nn9DEV7V3fg8njfSZnqe7ZEMqzK
  private key (WIF compressed) = L3urFcPsE2yHf5zeQjVSfUB8j8FEzX5cnmhjNsJfqjKgowPP4tmg
  public key (uncompressed) = 044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
  public key (compressed) = 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
  hash160 of uncompressed public key = fd214a3d033c82b307532018ac15ff6e06e62111
  hash160 of compressed public key = 1075f16844287d6d1c6fefbe2486cd3325127424
  legacy address (p2pkh uncompressed) = 1Q5RqZctfcNkTPad2tuJSREByd2gB8xs63
  legacy address (p2pkh compressed) = 12W36tm2jnreFiYdrzfE6cvRaKRbicEpnA
  p2sh-segwit address (p2sh p2wpkh) = 3AzXxVUqdzvzEqVmdtmeVqRwc98uqwyh76
  bech32 address (p2wpkh) = bc1qzp6lz6zy9p7k68r0a7lzfpkdxvj3yapynzuatt

Dump btc address from WIF private key::

  $ btc_address_dump 5KLDyKtrScLYsKMJzVCt8Mf6Nn9DEV7V3fg8njfSZnqe7ZEMqzK
  private key (hex) = c7ac679b56f50bfd54dd924fe45a8dca7a1c2dced254b03dac22afc03adb9127
  private key (WIF) = 5KLDyKtrScLYsKMJzVCt8Mf6Nn9DEV7V3fg8njfSZnqe7ZEMqzK
  private key (WIF compressed) = L3urFcPsE2yHf5zeQjVSfUB8j8FEzX5cnmhjNsJfqjKgowPP4tmg
  public key (uncompressed) = 044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
  public key (compressed) = 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
  hash160 of uncompressed public key = fd214a3d033c82b307532018ac15ff6e06e62111
  hash160 of compressed public key = 1075f16844287d6d1c6fefbe2486cd3325127424
  legacy address (p2pkh uncompressed) = 1Q5RqZctfcNkTPad2tuJSREByd2gB8xs63
  legacy address (p2pkh compressed) = 12W36tm2jnreFiYdrzfE6cvRaKRbicEpnA
  p2sh-segwit address (p2sh p2wpkh) = 3AzXxVUqdzvzEqVmdtmeVqRwc98uqwyh76
  bech32 address (p2wpkh) = bc1qzp6lz6zy9p7k68r0a7lzfpkdxvj3yapynzuatt

Dump btc address from public key::

  $ btc_address_dump 044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
  public key (uncompressed) = 044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
  public key (compressed) = 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
  hash160 of uncompressed public key = fd214a3d033c82b307532018ac15ff6e06e62111
  hash160 of compressed public key = 1075f16844287d6d1c6fefbe2486cd3325127424
  legacy address (p2pkh uncompressed) = 1Q5RqZctfcNkTPad2tuJSREByd2gB8xs63
  legacy address (p2pkh compressed) = 12W36tm2jnreFiYdrzfE6cvRaKRbicEpnA
  p2sh-segwit address (p2sh p2wpkh) = 3AzXxVUqdzvzEqVmdtmeVqRwc98uqwyh76
  bech32 address (p2wpkh) = bc1qzp6lz6zy9p7k68r0a7lzfpkdxvj3yapynzuatt

Dump btc address from compressed public key::

  $ btc_address_dump 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
  public key (uncompressed) = 044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
  public key (compressed) = 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
  hash160 of uncompressed public key = fd214a3d033c82b307532018ac15ff6e06e62111
  hash160 of compressed public key = 1075f16844287d6d1c6fefbe2486cd3325127424
  legacy address (p2pkh uncompressed) = 1Q5RqZctfcNkTPad2tuJSREByd2gB8xs63
  legacy address (p2pkh compressed) = 12W36tm2jnreFiYdrzfE6cvRaKRbicEpnA
  p2sh-segwit address (p2sh p2wpkh) = 3AzXxVUqdzvzEqVmdtmeVqRwc98uqwyh76
  bech32 address (p2wpkh) = bc1qzp6lz6zy9p7k68r0a7lzfpkdxvj3yapynzuatt

Dump btc address from hash160 of public key::

  $ btc_address_dump 1075f16844287d6d1c6fefbe2486cd3325127424
  hash160 of public key = 1075f16844287d6d1c6fefbe2486cd3325127424
  legacy address (p2pkh) = 12W36tm2jnreFiYdrzfE6cvRaKRbicEpnA
  p2sh-segwit address (only valid if input is hash160 of COMPRESSED public key) = 3AzXxVUqdzvzEqVmdtmeVqRwc98uqwyh76
  bech32 address (only valid if input is hash160 of COMPRESSED public key) = bc1qzp6lz6zy9p7k68r0a7lzfpkdxvj3yapynzuatt

Bitcoin forks
=============

Bitcoin forks are supported. You can use `-c` to change chain. Here is an example of litecoin:

  $ btc_address_dump -c ltc 6vazLaTvDG6Nh1CkhMTeLN5dPHjSq3cZAoET8FvDut9FUH71pp9
  private key (hex) = c0ef9854e33b0037c88c861fdf32d3df33f6a74f0cef9b696a31f5452b2aaa54
  private key (WIF) = 6vazLaTvDG6Nh1CkhMTeLN5dPHjSq3cZAoET8FvDut9FUH71pp9
  private key (WIF compressed) = T9X25Qhos7cijZtss7JbnU3RbNrM14XvzF4NK2quzQjQsEQw8iVL
  public key (uncompressed) = 043a0b64eee7e82b80e3e5a02cc9df3f08e1c534bd8b64846f5d556d38af6d9eb2a1729dcb14b66fbb8b57caa7d27f9852096a14c9cb8dc65093f9135d5b6e17a8
  public key (compressed) = 023a0b64eee7e82b80e3e5a02cc9df3f08e1c534bd8b64846f5d556d38af6d9eb2
  hash160 of uncompressed public key = ffd04e9fca28b32ef5656e4e224d06256fca20ea
  hash160 of compressed public key = 3c49068b96181b8d40a4272f69faadc5f722e8b9
  legacy address (p2pkh uncompressed) = LiYa7ZaqerPbbtad6oxds4wCqYF9v1XH83
  legacy address (p2pkh compressed) = LQiiHdPZmAsHNwSngex6fQgPUDDd1Ky47j
  p2sh-segwit address (p2sh p2wpkh) = MNNZtmjz5HehvjvLxM89c5oXRp1g9hRT9E
  bech32 address (p2wpkh) = ltc1q83ysdzukrqdc6s9yyuhkn74dchmj969e8tjw92

If your favorite coin is not supported, just add it to coins.yaml, and create a pull request.

Installation
============

To install btc-address-dump from PyPI::

  $ pip3 install btc-address-dump

Known Issue
===========

The last word in mnemonic word list is not arbitrary, it contains checksum info. However, this tool do not check it. In other words, this tool accept invalid mnemonic words.

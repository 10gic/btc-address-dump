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

Dump btc address from mnemonic words (bip86, P2TR)::

  $ btc_address_dump -d bip86 "olympic wine chicken argue unaware bundle tunnel grid spider slot spell need"
  mnemonic = olympic wine chicken argue unaware bundle tunnel grid spider slot spell need
  private key (hex) = 666c57341ca198f7f9e821af23c4688d233deda501922ed9f4c54084bff47693
  private key (WIF) = 5JbPqxGCGR75Movygz29XuNYukSKbqnzz97FKwkfChgZjs2odq6
  private key (WIF compressed) = Kzeoq4v4j3PpEr9FDUg4fQA7qpim6nN2wCnaEcfhceZdVrgPziFd
  taproot tweaked private key = a4242e9d5046485bef61d6788e01e6f9805f9f66a8bb54f332057907cc1f2889
  public key (compressed) = 02cb24ba2caf40b51fd72b395fe96794e6cdeec8fb5811ff1e6625af5fa3e0d587
  hash160 of compressed public key = 0e1f80bffb15cf157420c004c3fe173edc035b5a
  taproot tweaked public key (taproot output key) = fe2cff97d4abadb1590c7c4321afd25e0ed2a741c87772b7bb335fa4100c4d48
  bech32m address (p2tr) = bc1plck0l9754wkmzkgv03pjrt7jtc8d9f6pepmh9damxd06gyqvf4yqe3wewn

Dump btc address from hex private key::

  $ btc_address_dump c7ac679b56f50bfd54dd924fe45a8dca7a1c2dced254b03dac22afc03adb9127
  private key (hex) = c7ac679b56f50bfd54dd924fe45a8dca7a1c2dced254b03dac22afc03adb9127
  private key (WIF) = 5KLDyKtrScLYsKMJzVCt8Mf6Nn9DEV7V3fg8njfSZnqe7ZEMqzK
  private key (WIF compressed) = L3urFcPsE2yHf5zeQjVSfUB8j8FEzX5cnmhjNsJfqjKgowPP4tmg
  taproot tweaked private key = d5fda04f7d24a3ed5ead21148a34577fa42010563a5b99cbfc20f89c9e29438a
  public key (uncompressed) = 044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
  public key (compressed) = 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
  hash160 of uncompressed public key = fd214a3d033c82b307532018ac15ff6e06e62111
  hash160 of compressed public key = 1075f16844287d6d1c6fefbe2486cd3325127424
  taproot tweaked public key (taproot output key) = 1aea318388d939fff861ee264c7446d839580b07212c4c2ac2fb9cdd656237c3
  legacy address (p2pkh uncompressed) = 1Q5RqZctfcNkTPad2tuJSREByd2gB8xs63
  legacy address (p2pkh compressed) = 12W36tm2jnreFiYdrzfE6cvRaKRbicEpnA
  p2sh-segwit address (p2sh p2wpkh) = 3AzXxVUqdzvzEqVmdtmeVqRwc98uqwyh76
  bech32 address (p2wpkh) = bc1qzp6lz6zy9p7k68r0a7lzfpkdxvj3yapynzuatt
  bech32m address (p2tr) = bc1prt4rrqugmyull7rpacnycazxmqu4szc8yykyc2kzlwwd6etzxlpskwl7qz

Dump btc address from WIF private key::

  $ btc_address_dump 5KLDyKtrScLYsKMJzVCt8Mf6Nn9DEV7V3fg8njfSZnqe7ZEMqzK
  private key (hex) = c7ac679b56f50bfd54dd924fe45a8dca7a1c2dced254b03dac22afc03adb9127
  private key (WIF) = 5KLDyKtrScLYsKMJzVCt8Mf6Nn9DEV7V3fg8njfSZnqe7ZEMqzK
  private key (WIF compressed) = L3urFcPsE2yHf5zeQjVSfUB8j8FEzX5cnmhjNsJfqjKgowPP4tmg
  taproot tweaked private key = d5fda04f7d24a3ed5ead21148a34577fa42010563a5b99cbfc20f89c9e29438a
  public key (uncompressed) = 044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
  public key (compressed) = 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
  hash160 of uncompressed public key = fd214a3d033c82b307532018ac15ff6e06e62111
  hash160 of compressed public key = 1075f16844287d6d1c6fefbe2486cd3325127424
  taproot tweaked public key (taproot output key) = 1aea318388d939fff861ee264c7446d839580b07212c4c2ac2fb9cdd656237c3
  legacy address (p2pkh uncompressed) = 1Q5RqZctfcNkTPad2tuJSREByd2gB8xs63
  legacy address (p2pkh compressed) = 12W36tm2jnreFiYdrzfE6cvRaKRbicEpnA
  p2sh-segwit address (p2sh p2wpkh) = 3AzXxVUqdzvzEqVmdtmeVqRwc98uqwyh76
  bech32 address (p2wpkh) = bc1qzp6lz6zy9p7k68r0a7lzfpkdxvj3yapynzuatt
  bech32m address (p2tr) = bc1prt4rrqugmyull7rpacnycazxmqu4szc8yykyc2kzlwwd6etzxlpskwl7qz

Dump btc address from public key::

  $ btc_address_dump 044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
  public key (uncompressed) = 044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
  public key (compressed) = 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
  hash160 of uncompressed public key = fd214a3d033c82b307532018ac15ff6e06e62111
  hash160 of compressed public key = 1075f16844287d6d1c6fefbe2486cd3325127424
  taproot tweaked public key (taproot output key) = 1aea318388d939fff861ee264c7446d839580b07212c4c2ac2fb9cdd656237c3
  legacy address (p2pkh uncompressed) = 1Q5RqZctfcNkTPad2tuJSREByd2gB8xs63
  legacy address (p2pkh compressed) = 12W36tm2jnreFiYdrzfE6cvRaKRbicEpnA
  p2sh-segwit address (p2sh p2wpkh) = 3AzXxVUqdzvzEqVmdtmeVqRwc98uqwyh76
  bech32 address (p2wpkh) = bc1qzp6lz6zy9p7k68r0a7lzfpkdxvj3yapynzuatt
  bech32m address (p2tr) = bc1prt4rrqugmyull7rpacnycazxmqu4szc8yykyc2kzlwwd6etzxlpskwl7qz

Dump btc address from compressed public key::

  $ btc_address_dump 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
  public key (uncompressed) = 044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
  public key (compressed) = 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
  hash160 of uncompressed public key = fd214a3d033c82b307532018ac15ff6e06e62111
  hash160 of compressed public key = 1075f16844287d6d1c6fefbe2486cd3325127424
  taproot tweaked public key (taproot output key) = 1aea318388d939fff861ee264c7446d839580b07212c4c2ac2fb9cdd656237c3
  legacy address (p2pkh uncompressed) = 1Q5RqZctfcNkTPad2tuJSREByd2gB8xs63
  legacy address (p2pkh compressed) = 12W36tm2jnreFiYdrzfE6cvRaKRbicEpnA
  p2sh-segwit address (p2sh p2wpkh) = 3AzXxVUqdzvzEqVmdtmeVqRwc98uqwyh76
  bech32 address (p2wpkh) = bc1qzp6lz6zy9p7k68r0a7lzfpkdxvj3yapynzuatt
  bech32m address (p2tr) = bc1prt4rrqugmyull7rpacnycazxmqu4szc8yykyc2kzlwwd6etzxlpskwl7qz

Dump taproot address from taproot output sec key::

  $ btc_address_dump --taproot-output-seckey d5fda04f7d24a3ed5ead21148a34577fa42010563a5b99cbfc20f89c9e29438a
  taproot output seckey = d5fda04f7d24a3ed5ead21148a34577fa42010563a5b99cbfc20f89c9e29438a
  taproot output pubkey = 1aea318388d939fff861ee264c7446d839580b07212c4c2ac2fb9cdd656237c3
  bech32m address (p2tr) = bc1prt4rrqugmyull7rpacnycazxmqu4szc8yykyc2kzlwwd6etzxlpskwl7qz

Dump taproot address from taproot output pub key::

  $ btc_address_dump --taproot-output-pubkey 1aea318388d939fff861ee264c7446d839580b07212c4c2ac2fb9cdd656237c3
  taproot output pubkey = 1aea318388d939fff861ee264c7446d839580b07212c4c2ac2fb9cdd656237c3
  bech32m address (p2tr) = bc1prt4rrqugmyull7rpacnycazxmqu4szc8yykyc2kzlwwd6etzxlpskwl7qz

Dump btc address from hash160 of public key::

  $ btc_address_dump 1075f16844287d6d1c6fefbe2486cd3325127424
  hash160 of public key = 1075f16844287d6d1c6fefbe2486cd3325127424
  legacy address (p2pkh) = 12W36tm2jnreFiYdrzfE6cvRaKRbicEpnA
  p2sh-segwit address (only valid if input is hash160 of COMPRESSED public key) = 3AzXxVUqdzvzEqVmdtmeVqRwc98uqwyh76
  bech32 address (only valid if input is hash160 of COMPRESSED public key) = bc1qzp6lz6zy9p7k68r0a7lzfpkdxvj3yapynzuatt

Bitcoin forks
=============

Bitcoin forks are supported. You can use `-c` to change chain. Here is an example of litecoin::

  $ btc_address_dump -c ltc 6vazLaTvDG6Nh1CkhMTeLN5dPHjSq3cZAoET8FvDut9FUH71pp9
  private key (hex) = c0ef9854e33b0037c88c861fdf32d3df33f6a74f0cef9b696a31f5452b2aaa54
  private key (WIF) = 6vazLaTvDG6Nh1CkhMTeLN5dPHjSq3cZAoET8FvDut9FUH71pp9
  private key (WIF compressed) = T9X25Qhos7cijZtss7JbnU3RbNrM14XvzF4NK2quzQjQsEQw8iVL
  public key (uncompressed) = 043a0b64eee7e82b80e3e5a02cc9df3f08e1c534bd8b64846f5d556d38af6d9eb2a1729dcb14b66fbb8b57caa7d27f9852096a14c9cb8dc65093f9135d5b6e17a8
  public key (compressed) = 023a0b64eee7e82b80e3e5a02cc9df3f08e1c534bd8b64846f5d556d38af6d9eb2
  hash160 of uncompressed public key = ffd04e9fca28b32ef5656e4e224d06256fca20ea
  hash160 of compressed public key = 3c49068b96181b8d40a4272f69faadc5f722e8b9
  taproot output key = 456e7dae52bae03cad9ddc8de61c3248236f8ae2786081c1eadcd1614eae7f69
  legacy address (p2pkh uncompressed) = LiYa7ZaqerPbbtad6oxds4wCqYF9v1XH83
  legacy address (p2pkh compressed) = LQiiHdPZmAsHNwSngex6fQgPUDDd1Ky47j
  p2sh-segwit address (p2sh p2wpkh) = MNNZtmjz5HehvjvLxM89c5oXRp1g9hRT9E
  bech32 address (p2wpkh) = ltc1q83ysdzukrqdc6s9yyuhkn74dchmj969e8tjw92
  bech32m address (p2tr) = ltc1pg4h8mtjjhtsretvamjx7v8pjfq3klzhz0psgrs02mngkzn4w0a5srs49v4

If your favorite coin is not supported, just add it to coins.yaml, and create a pull request.

Installation
============

To install btc-address-dump from PyPI::

  $ pip3 install btc-address-dump

Known Issue
===========

The last word in mnemonic word list is not arbitrary, it contains checksum info. However, this tool do not check it. In other words, this tool accept invalid mnemonic words.

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

Installation
============

To install btc-address-dump from PyPI::

  $ pip3 install btc-address-dump

Known Issue
===========

The last word in mnemonic word list is not arbitrary, it contains checksum info. However, this tool do not check it. In other words, this tool accept invalid mnemonic words.

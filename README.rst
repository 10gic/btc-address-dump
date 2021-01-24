================
btc-address-dump
================

btc-address-dump is a utility for dump btc address from mnemonic words or private key or public key.


Example
=======

Dump btc address from mnemonic words::

  $ btc_address_dump "olympic wine chicken argue unaware bundle tunnel grid spider slot spell need"
  mnemonic = olympic wine chicken argue unaware bundle tunnel grid spider slot spell need
  private key (hex) = c7ac679b56f50bfd54dd924fe45a8dca7a1c2dced254b03dac22afc03adb9127
  private key (WIF) = 5KLDyKtrScLYsKMJzVCt8Mf6Nn9DEV7V3fg8njfSZnqe7ZEMqzK
  private key (WIF compressed) = L3urFcPsE2yHf5zeQjVSfUB8j8FEzX5cnmhjNsJfqjKgowPP4tmg
  public key (uncompressed) = 044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
  public key (compressed) = 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
  legacy address (p2pkh uncompressed) = 1Q5RqZctfcNkTPad2tuJSREByd2gB8xs63
  legacy address (p2pkh compressed) = 12W36tm2jnreFiYdrzfE6cvRaKRbicEpnA
  p2sh-segwit address (p2sh p2wpkh) = 3AzXxVUqdzvzEqVmdtmeVqRwc98uqwyh76
  bech32 address (p2wpkh) = bc1qzp6lz6zy9p7k68r0a7lzfpkdxvj3yapynzuatt

Dump btc address from hex private key::

  $ btc_address_dump c7ac679b56f50bfd54dd924fe45a8dca7a1c2dced254b03dac22afc03adb9127
  private key (hex) = c7ac679b56f50bfd54dd924fe45a8dca7a1c2dced254b03dac22afc03adb9127
  private key (WIF) = 5KLDyKtrScLYsKMJzVCt8Mf6Nn9DEV7V3fg8njfSZnqe7ZEMqzK
  private key (WIF compressed) = L3urFcPsE2yHf5zeQjVSfUB8j8FEzX5cnmhjNsJfqjKgowPP4tmg
  public key (uncompressed) = 044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
  public key (compressed) = 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
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
  legacy address (p2pkh uncompressed) = 1Q5RqZctfcNkTPad2tuJSREByd2gB8xs63
  legacy address (p2pkh compressed) = 12W36tm2jnreFiYdrzfE6cvRaKRbicEpnA
  p2sh-segwit address (p2sh p2wpkh) = 3AzXxVUqdzvzEqVmdtmeVqRwc98uqwyh76
  bech32 address (p2wpkh) = bc1qzp6lz6zy9p7k68r0a7lzfpkdxvj3yapynzuatt

Dump btc address from public key::

  $ btc_address_dump 044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
  public key (uncompressed) = 044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
  public key (compressed) = 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
  legacy address (p2pkh uncompressed) = 1Q5RqZctfcNkTPad2tuJSREByd2gB8xs63
  legacy address (p2pkh compressed) = 12W36tm2jnreFiYdrzfE6cvRaKRbicEpnA
  p2sh-segwit address (p2sh p2wpkh) = 3AzXxVUqdzvzEqVmdtmeVqRwc98uqwyh76
  bech32 address (p2wpkh) = bc1qzp6lz6zy9p7k68r0a7lzfpkdxvj3yapynzuatt

Dump btc address from compressed public key::

  $ btc_address_dump 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
  public key (uncompressed) = 044cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1087190d91e26af594e3f8ecd3f4d3596c03c45d3b235da916903c930c6593cc4
  public key (compressed) = 024cd0aaeca3b636078583408e75edd77307b5190ca7a48bb9fbc1f2576c17dff1
  legacy address (p2pkh uncompressed) = 1Q5RqZctfcNkTPad2tuJSREByd2gB8xs63
  legacy address (p2pkh compressed) = 12W36tm2jnreFiYdrzfE6cvRaKRbicEpnA
  p2sh-segwit address (p2sh p2wpkh) = 3AzXxVUqdzvzEqVmdtmeVqRwc98uqwyh76
  bech32 address (p2wpkh) = bc1qzp6lz6zy9p7k68r0a7lzfpkdxvj3yapynzuatt

Installation
============

To install btc-address-dump from PyPI::

  $ pip3 install btc-address-dump

# Jigsxor - Shellcode Obfuscation Tool

Jigsxor takes raw shellcode and applies dual-layer obfuscation (XOR encryption + byte shuffling), outputting:
- Randomized shellcode array
- Position lookup table
- C/C++ reconstruction stub
- XOR decryption key

## Usage
```bash
python3 jigsxor.py inputfile.bin

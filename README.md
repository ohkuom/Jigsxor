# Jigxor - Shellcode Obfuscation Tool
Jigxor provides multi-layered shellcode obfuscation through:
- XOR Encryption - Each byte is XORed with a random key
- Jigsaw Shuffling - Encrypted bytes are randomly shuffled
- Payload Splitting - Shuffled payload is divided into two parts

## Usage
```bash
python3 jigxor.py inputfile.bin

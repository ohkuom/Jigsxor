import random
import sys
import math

def getShellcode(input_file):
    file_shellcode = b''
    try:
        with open(input_file, 'rb') as shellcode_file:
            file_shellcode = shellcode_file.read()
            file_shellcode = file_shellcode.strip()
            binary_code = ''
            sc_array = []

            for byte in file_shellcode:
                binary_code += "\\x" + hex(byte)[2:].zfill(2)

            raw_shellcode = "0" + ",0".join(binary_code.split("\\")[1:])
        for byte in raw_shellcode.split(','):
            sc_array.append(byte)

        return sc_array
    
    except FileNotFoundError:
        sys.exit("\n\nThe input file you specified does not exist! Please specify a valid file path.\nExiting...\n")

def generateSplitJigxor(filename):
    shellcode = getShellcode(filename)
    sc_len = len(shellcode)
    
    xor_key = random.randint(0x01, 0xFF)  # Avoid 0x00 for security
    
    xor_shellcode = [f"0x{(byte ^ xor_key):02x}" for byte in map(lambda x: int(x, 0), shellcode)]
    
    raw_positions = list(range(0, sc_len))
    random.shuffle(raw_positions)
    
    jigsaw = []
    for position in raw_positions:
        jigsaw.append(xor_shellcode[position])

    split_point = math.ceil(sc_len / 2)
    jigsaw_part1 = jigsaw[:split_point]
    jigsaw_part2 = jigsaw[split_point:]
    
    positions_part1 = raw_positions[:split_point]
    positions_part2 = raw_positions[split_point:]

    jigsaw_array1 = f'unsigned char jigsaw_part1[{len(jigsaw_part1)}] = {{ {", ".join(jigsaw_part1)} }};'
    jigsaw_array2 = f'unsigned char jigsaw_part2[{len(jigsaw_part2)}] = {{ {", ".join(jigsaw_part2)} }};'
    
    position_array1 = f'int positions_part1[{len(positions_part1)}] = {{ {", ".join(map(str, positions_part1))} }};'
    position_array2 = f'int positions_part2[{len(positions_part2)}] = {{ {", ".join(map(str, positions_part2))} }};'

    code = f'''

const unsigned char xor_key = 0x{xor_key:02x};

{jigsaw_array1}

{jigsaw_array2}

{position_array1}

{position_array2}

int calc_len = {sc_len};
unsigned char calc_payload[{sc_len}] = {{ 0x00 }};
int position;

for (int idx = 0; idx < sizeof(positions_part1) / sizeof(positions_part1[0]); idx++) {{
    position = positions_part1[idx];
    calc_payload[position] = jigsaw_part1[idx] ^ xor_key;
}}

for (int idx = 0; idx < sizeof(positions_part2) / sizeof(positions_part2[0]); idx++) {{
    position = positions_part2[idx];
    calc_payload[position] = jigsaw_part2[idx] ^ xor_key;
}}

'''
    with open('jigsaw_split_random.txt', 'w') as outfile:
        outfile.write(code)
    print(f"[+] File generated with random XOR key: 0x{xor_key:02x}")

if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print("[x] Script requires one argument: the filename of your shellcode .bin file.")
        sys.exit()
    generateSplitJigsaw(sys.argv[1])

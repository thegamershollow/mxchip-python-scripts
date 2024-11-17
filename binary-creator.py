import os
import sys

def binary_hook(binf, outf):
    try:
        with open(binf, 'rb') as f:
            appbin = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{binf}' not found.")
        sys.exit(1)

    try:
        with open('boot.bin', 'rb') as f:
            bootbin = f.read()
    except FileNotFoundError:
        print("Error: 'boot.bin' not found.")
        sys.exit(1)

    # Pad with 0xFF bytes if necessary to make the total size 0xc000
    padding_size = 0xc000 - len(bootbin)
    if padding_size < 0:
        print(f"Error: 'boot.bin' is too large, it exceeds {0xc000} bytes.")
        sys.exit(1)

    padded_bootbin = bootbin + b'\xFF' * padding_size

    try:
        with open(outf, 'wb') as f:
            f.write(padded_bootbin + appbin)
        print(f"Output written to {outf}")
    except IOError as e:
        print(f"Error writing output file '{outf}': {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_binary> <output_binary>")
        sys.exit(1)

    binary_hook(sys.argv[1], sys.argv[2])

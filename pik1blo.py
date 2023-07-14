# Pikmin 1 BLO text editor by EpochFlame
# 32-byte alignment by Roeming

import argparse
import struct

# Byte sequences to find string
STRING_MAGIC = b"\x02\xFF\xFB\x00\x1C\x00\x18\x00\x18"

# Example invocation: ./pik1blo.py vanilla.blo newtext.txt output.blo
parser = argparse.ArgumentParser()
parser.add_argument("vanilla", help="Path to the vanilla blo", type=argparse.FileType('rb'))
parser.add_argument("newstring", help="Path to the new text file", type=argparse.FileType('rb'))
parser.add_argument("target", help="Path to the target blo (to write)")

args = parser.parse_args()

# Read contents into bytearrays and close files
vanilla_bytes = args.vanilla.read()
args.vanilla.close()
newstring_bytes = args.newstring.read()
args.newstring.close()

# Find string size and position
string_size_offset = (vanilla_bytes.find(STRING_MAGIC) + 9)
string_size_bytes = vanilla_bytes[string_size_offset:string_size_offset+2]
string_size = int.from_bytes(string_size_bytes, byteorder='big')

# Start of String and End of String positions
sos_offset = string_size_offset + 2
eos_offset = sos_offset + string_size

# Break if the eos is not found
assert(eos_offset != len(vanilla_bytes))

# Align newstring to 4 bytes
align = 4
additions = (align - (len(newstring_bytes) % align)) % align
necessary_alignment = len(newstring_bytes) % align
aa = bytearray(newstring_bytes)
aa.extend(0 for _ in range(additions))
newstring_bytes = aa

# Replace sos - eos in vanilla with bytes from new
final_bytes = vanilla_bytes[:sos_offset] + newstring_bytes + vanilla_bytes[eos_offset:]

# Adjust string size
newsize = struct.pack('>H', len(newstring_bytes))
final_bytes = final_bytes[:string_size_offset] + newsize + final_bytes[string_size_offset+2:]

# Align to 32 bytes
align = 32
additions = (align - (len(final_bytes) % align)) % align
necessary_alignment = len(final_bytes) % align
bb = bytearray(final_bytes)
bb.extend(0 for _ in range(additions))

with open(args.target, "wb") as f:
    f.write(bb)

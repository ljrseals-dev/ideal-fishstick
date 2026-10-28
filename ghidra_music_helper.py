#@category Analysis.Music
#@description Find Pascal strings and music-related functions in the current binary.

from ghidra.app.script import GhidraScript
from ghidra.program.model.data import PascalString255DataType
from ghidra.program.model.listing import CodeUnit

MUSIC_KEYWORDS = [
    "bgm", "music", "seq", "snd", "sound", "note", "tempo",
    "track", "instrument", "voice", "pitch", "midi", "driver",
    "song", "pattern", "order"
]

data_type_manager = currentProgram.getDataTypeManager()
memory = currentProgram.getMemory()
listing = currentProgram.getListing()

print("=== Ghidra Music Helper ===")
print("Program: %s" % currentProgram.getName())

print("\n[1] Music-related symbols:")
symbols = currentProgram.getSymbolTable().getAllSymbols(True)
found = 0
while symbols.hasNext():
    sym = symbols.next()
    name = sym.getName().lower()
    if any(kw in name for kw in MUSIC_KEYWORDS):
        addr = sym.getAddress()
        print("  %s  %s  %s" % (addr, sym.getSymbolType(), sym.getName()))
        found += 1
if found == 0:
    print("  (none found by name)")

print("\n[2] Pascal string candidates (length-prefixed):")
pascal_strings = []
iter_data = listing.getDefinedData(True)
count = 0
for d in iter_data:
    if isinstance(d.getDataType(), PascalString255DataType):
        pascal_strings.append(d)
        val = d.getValue()
        if val is not None:
            text = str(val)
            if any(kw in text.lower() for kw in MUSIC_KEYWORDS):
                print("  %s  %s" % (d.getAddress(), text))
                count += 1
print("  Total Pascal strings: %d (music-related shown above: %d)"
      % (len(pascal_strings), count))

print("\n[3] Suggested next steps:")
print("  1. Right click each music-related symbol → Rename")
print("  2. Open the function → Decompile window")
print("  3. Copy the pseudocode to a text file for review")
print("  4. Export with Haruspex (Tools → Haruspex) for a full dump")

print("\n=== Done ===")

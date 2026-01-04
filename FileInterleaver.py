ROM_EVEN = "la8_smash_tv_game_rom_u105.u105"
ROM_ODD = "la8_smash_tv_game_rom_u89.u89"
with open(ROM_EVEN, "rb") as f:
    even = f.read()

with open(ROM_ODD, "rb") as f:
    odd = f.read()

assert len(even) == len(odd), "ROM sizes do not match"

i = 0
completed = bytearray()
while i < len(even):
    completed.append(even[i])
    completed.append(odd[i])
    i += 1

with open("completeRom", "wb") as f:
    f.write(completed)

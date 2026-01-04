ROM_ODD = "la8_smash_tv_game_rom_u105.u105"
ROM_EVEN = "la8_smash_tv_game_rom_u89.u89"

WAVE_START_INDEX = 0x137F
NAME_START_INDEX = 0x65D7
MAX_WAVES = 50  # safety limit

# -----------------------------
# Load ROMs
# -----------------------------
with open(ROM_EVEN, "rb") as f:
    even = f.read()

with open(ROM_ODD, "rb") as f:
    odd = f.read()

assert len(even) == len(odd), "ROM sizes do not match"

enemyTypes = ["ATRAIN", "Orb", "Tank", "Fat Bomber", "Wall Gunner", "Grunt", "Mine", "Mutoid Man", "Scarface", "Robot Droid", "Balls of Death", "Galagas1", "Space Train", "Purple Galaga", "Die Cobras", "Snake Traps"]
# -----------------------------
# Helpers
# -----------------------------
def get_word(index):
    return (even[index] << 8) | odd[index]

def get_word2(index):
    return (odd[index] << 8) | even[index]
def set_word(index, value):
    hi = (value >> 8) & 0xFF
    lo = value & 0xFF
    global even, odd
    even = bytearray(even)
    odd = bytearray(odd)
    even[index] = hi
    odd[index] = lo
# -----------------------------
# Dump Names
# -----------------------------

nameIndex = NAME_START_INDEX
name_number = 0
word_number = 1
names = []
while word_number < 49:
    ended = False
    textBytes = bytearray()
    while ended != True:
        if odd[nameIndex+name_number] != 0:
            textBytes.append(odd[nameIndex+name_number])
        else:
            ended = True
        if even[nameIndex + name_number] != 0:
            textBytes.append(even[nameIndex+name_number])
        else:
            ended = True
        name_number += 1
    utf8_string = textBytes.decode('utf-8')
    names.append({
        "name": utf8_string,
        "start": nameIndex,
        "max_bytes": len(utf8_string)
    })
    nameIndex = nameIndex + name_number
    name_number = 0
    #print(str(word_number) + utf8_string)
    word_number += 1
names.insert(19, {"name": "Unused Room 1", "start": None, "max_bytes": 0})
names.insert(37, {"name": "Unused Room 2", "start": None, "max_bytes": 0})


# -----------------------------
# Dump Waves
# -----------------------------
index = WAVE_START_INDEX
wave_number = 1
waves = []
while wave_number <= MAX_WAVES:
    #print(f"\n=== WAVE {wave_number} ===")
    #print(words[wave_number-1])
    entries = []
    while True:
        word = get_word(index)

        # Wave terminator
        if word == 0x0000:
            index += 1
            break

        if index + 5 >= len(even):
            print("Reached end of ROM unexpectedly")
            exit(1)

        entry = {
            "enemy": get_word(index),
            "count": get_word(index + 1),
            "difficulty": get_word(index + 2),
            "rate": get_word(index + 3),
            "onscreen": get_word(index + 4),
            "counter": get_word(index + 5),
            "address": index
        }

        entries.append(entry)
        index += 6

    # if not entries:
    #     print("No entries — assuming end of wave table")
    #     break
    #
    # for i, e in enumerate(entries):
    #     print(
    #         f"  Entry {i}: "
    #         f"enemy={e['enemy']}, "
    #         f"count={e['count']}, "
    #         f"diff={e['difficulty']}, "
    #         f"rate={e['rate']}, "
    #         f"onscreen={e['onscreen']}, "
    #         f"counter={e['counter']}"
    #     )
    wave = {
        "name": names[wave_number-1],
        "number": wave_number,
        "entries": entries,
        "address": entries[0]['address']
    }
    waves.append(wave)
    wave_number += 1

#GUI CODE
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

root = tk.Tk()
root.title("Smash TV Wave Editor")
selected_wave = None
selected_entry = None
current_wave_index = None
def on_wave_select(evt):
    global selected_wave, current_wave_index

    sel = wave_list.curselection()
    if not sel:
        return

    if sel[0] == current_wave_index:
        return  # <-- STOP redundant refresh
    tree.delete(*tree.get_children())
    current_wave_index = sel[0]
    selected_wave = waves[current_wave_index]
    name_var.set(names[current_wave_index]["name"])

    for e in selected_wave["entries"]:
        tree.insert("", "end", values=(
            enemyTypes[e["enemy"] - 1],
            e["count"],
            e["difficulty"],
            e["rate"],
            e["onscreen"],
            e["counter"]
        ))


def on_entry_select(evt):
    global selected_entry
    sel = tree.selection()
    if not sel:
        return

    idx = tree.index(sel[0])
    selected_entry = selected_wave["entries"][idx]

    enemy_var.set(enemyTypes[selected_entry["enemy"] - 1])
    count_var.set(selected_entry["count"])
    diff_var.set(selected_entry["difficulty"])
    rate_var.set(selected_entry["rate"])
    ons_var.set(selected_entry["onscreen"])
    ctr_var.set(selected_entry["counter"])
def apply_name_change():
    idx = current_wave_index
    meta = names[idx]

    if meta["start"] is None:
        return

    new_text = name_var.get()
    encoded = new_text.encode("utf-8")

    if len(encoded) > meta["max_bytes"]:
        messagebox.showerror(
            "Error",
            f"Name too long! Max {meta['max_bytes']//2} characters."
        )
        return
    global even, odd
    even = bytearray(even)
    odd = bytearray(odd)
    # Write characters
    pos = meta["start"]
    for i in range(0, len(encoded), 2):
        odd[pos] = encoded[i]
        even[pos] = encoded[i + 1] if i + 1 < len(encoded) else 0
        pos += 1

    # Null terminate
    #odd[pos] = 0
    #even[pos] = 0

    with open(ROM_EVEN, "wb") as f:
        f.write(even)

    with open(ROM_ODD, "wb") as f:
        f.write(odd)
    # Update model
    meta["name"] = new_text
    wave_list.delete(idx)
    wave_list.insert(idx, f"{idx+1}: {new_text}")

# Wave list
wave_list = tk.Listbox(root, width=30)
wave_list.pack(side="left", fill="y")
wave_list.bind("<<ListboxSelect>>", on_wave_select)

for i, wave in enumerate(waves):
    wave_list.insert("end", f"{i+1}: {wave['name']['name']}")

# Entry table
columns = ("Enemy", "Count", "Diff", "Rate", "OnScr", "Counter")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=80)

tree.pack(side="right", fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", on_entry_select)

#editor
editor = tk.Frame(root)
editor.pack(side="bottom", fill="x")
#level name
tk.Label(editor, text="Level Name").grid(row=0, column=2, sticky="w")

name_var = tk.StringVar()
name_entry = tk.Entry(editor, textvariable=name_var, width=30)
name_entry.grid(row=0, column=3, padx=4)

tk.Button(editor, text="Apply Name", command=apply_name_change)\
  .grid(row=1, column=3, pady=2)

#entry data
enemy_var = tk.StringVar()
enemy_menu = ttk.Combobox(editor, textvariable=enemy_var, values=enemyTypes, state="readonly")

count_var = tk.IntVar()
diff_var = tk.IntVar()
rate_var = tk.IntVar()
ons_var = tk.IntVar()
ctr_var = tk.IntVar()

enemy_menu.grid(row=0, column=1)
tk.Label(editor, text="Enemy").grid(row=0, column=0)

tk.Label(editor, text="Count").grid(row=1, column=0)
tk.Entry(editor, textvariable=count_var, width=6).grid(row=1, column=1)

tk.Label(editor, text="Difficulty").grid(row=2, column=0)
tk.Entry(editor, textvariable=diff_var, width=6).grid(row=2, column=1)

tk.Label(editor, text="Rate").grid(row=3, column=0)
tk.Entry(editor, textvariable=rate_var, width=6).grid(row=3, column=1)

tk.Label(editor, text="On Screen").grid(row=4, column=0)
tk.Entry(editor, textvariable=ons_var, width=6).grid(row=4, column=1)

tk.Label(editor, text="Counter").grid(row=5, column=0)
tk.Entry(editor, textvariable=ctr_var, width=6).grid(row=5, column=1)

def apply_changes():
    if not selected_entry:
        return

    selected_entry["enemy"] = enemyTypes.index(enemy_var.get()) + 1
    selected_entry["count"] = count_var.get()
    selected_entry["difficulty"] = diff_var.get()
    selected_entry["rate"] = rate_var.get()
    selected_entry["onscreen"] = ons_var.get()
    selected_entry["counter"] = ctr_var.get()

    base = selected_entry["address"]
    set_word(base + 0, selected_entry["enemy"])
    set_word(base + 1, selected_entry["count"])
    set_word(base + 2, selected_entry["difficulty"])
    set_word(base + 3, selected_entry["rate"])
    set_word(base + 4, selected_entry["onscreen"])
    set_word(base + 5, selected_entry["counter"])
    with open(ROM_EVEN, "wb") as f:
        f.write(even)

    with open(ROM_ODD, "wb") as f:
        f.write(odd)
    # Refresh view
    sel = tree.selection()
    if sel:
        tree.item(sel[0], values=(
            enemy_var.get(),
            count_var.get(),
            diff_var.get(),
            rate_var.get(),
            ons_var.get(),
            ctr_var.get()
        ))

tk.Button(editor, text="Apply Changes", command=apply_changes).grid(row=6, column=0, columnspan=2, pady=4)

root.mainloop()

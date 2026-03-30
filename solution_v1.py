"""
mini-diary v1 — Geliştirilmiş Sürüm
Öğrenci: Semih Oktay KARAOĞLU (241478004)

V1 İÇİN BELİRLENEN 3 SOMUT GÖREV (TASK LIST):
1. 'list' komutu eklendi: Kayıtları döngü kullanmadan ham formatta ekrana basar.
2. Hata mesajları SPEC ile eşitlendi: Hatalı girişlerde (init/add) SPEC'teki uyarılar verilir.
3. Hazır olmayan komutlar güncellendi: 'delete' ve 'search' mesajları v1 sürümüne çekildi.
"""

import sys
import os
from datetime import date

def initialize():
    """Dizini ve veri dosyasını hazırlar."""
    if os.path.exists(".minidiary"):
        return "Already initialized"

    os.mkdir(".minidiary")
    with open(".minidiary/entries.dat", "w") as f:
        pass
    return "Initialized empty mini-diary in .minidiary/"

def add_entry(entry_text):
    """Yeni kayıt ekler. ID ve Tarih otomatik hesaplanır (Döngüsüz)."""
    if not os.path.exists(".minidiary"):
        return "Not initialized. Run: python minidiary.py init"

    with open(".minidiary/entries.dat", "r") as f:
        content = f.read()

    if content:
        last_newline = content.rfind("\n", 0, -1)
        last_line = content[last_newline+1:].strip() if last_newline != -1 else content.strip()
        last_id = int(last_line.split("|")[0])
        entry_id = last_id + 1
    else:
        entry_id = 1

    today = date.today().isoformat()
    with open(".minidiary/entries.dat", "a") as f:
        f.write(str(entry_id) + "|" + entry_text + "|" + today + "\n")

    return "Added entry #" + str(entry_id) + ": " + entry_text + " (" + today + ")"

def list_entries():
    """V1 YENİ: Kayıtları listeler (Döngüsüz)."""
    if not os.path.exists(".minidiary"):
        return "Not initialized. Run: python minidiary.py init"

    with open(".minidiary/entries.dat", "r") as f:
        content = f.read().strip()

    if not content:
        return "No entries found."

    return content

def show_not_implemented(command_name):
    """V1 YENİ: Tamamlanmamış komutlar için v1 bilgilendirme mesajı."""
    return "Command '" + command_name + "' will be implemented in future weeks (v2 or later)."

# --- Ana Program Akışı ---
if len(sys.argv) < 2:
    print("Usage: python minidiary.py <command> [args]")
else:
    cmd = sys.argv[1]

    if cmd == "init":
        print(initialize())

    elif cmd == "add":
        if len(sys.argv) < 3:
            print("Usage: python minidiary.py add <entry_text>")
        else:
            print(add_entry(sys.argv[2]))

    elif cmd == "list":
        # V1: Artık hata mesajı yerine fonksiyonu çağırıyoruz
        print(list_entries())

    elif cmd == "delete" or cmd == "search":
        # V1: Mesaj sürüm bilgisiyle güncellendi
        print(show_not_implemented(cmd))

    else:
        print("Unknown command: " + cmd)
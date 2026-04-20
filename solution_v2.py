"""
mini-diary v2 — Tamamlanmış Sürüm
Öğrenci: Semih Oktay KARAOĞLU (241478004)

V2 İÇİN BELİRLENEN 3 SOMUT GÖREV (TASK LIST):
1. 'delete' komutu eklendi: Belirtilen ID'ye sahip kaydı bulur ve siler.
2. 'search' komutu eklendi: İstenen tarihteki günlük kayıtlarını listeler.
3. Hata Yönetimi: 'search' komutu için YYYY-MM-DD tarih formatı kontrolü eklendi.
"""

import sys
import os
import re
from datetime import date


def initialize():
    """Dizini ve veri dosyasını hazırlar."""
    if os.path.exists(".minidiary"):
        return "Already initialized"

    os.mkdir(".minidiary")
    # Dosya oluştururken utf-8 kuralını SPEC'e uygun olarak ekledik
    with open(".minidiary/entries.dat", "w", encoding="utf-8") as f:
        pass
    return "Initialized empty mini-diary in .minidiary/"


def add_entry(entry_text):
    """Yeni kayıt ekler. ID ve Tarih otomatik hesaplanır."""
    if not os.path.exists(".minidiary"):
        return "Not initialized. Run: python minidiary.py init"

    with open(".minidiary/entries.dat", "r", encoding="utf-8") as f:
        content = f.read()

    if content:
        last_newline = content.rfind("\n", 0, -1)
        last_line = content[last_newline + 1:].strip() if last_newline != -1 else content.strip()
        last_id = int(last_line.split("|")[0])
        entry_id = last_id + 1
    else:
        entry_id = 1

    today = date.today().isoformat()
    with open(".minidiary/entries.dat", "a", encoding="utf-8") as f:
        f.write(str(entry_id) + "|" + entry_text + "|" + today + "\n")

    return "Added entry #" + str(entry_id) + ": " + entry_text + " (" + today + ")"


def list_entries():
    """Kayıtları listeler."""
    if not os.path.exists(".minidiary"):
        return "Not initialized. Run: python minidiary.py init"

    with open(".minidiary/entries.dat", "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        return "No entries found."

    # Kayıtları SPEC'te istenen formatta [ID] Metin (Tarih) olarak basıyoruz
    lines = content.split('\n')
    formatted_lines = []
    for line in lines:
        if line:
            parts = line.split('|')
            formatted_lines.append(f"[{parts[0]}] {parts[1]} ({parts[2]})")

    return "\n".join(formatted_lines)


def delete_entry(entry_id):
    """V2 YENİ: Verilen ID'ye sahip kaydı siler."""
    if not os.path.exists(".minidiary"):
        return "Not initialized. Run: python minidiary.py init"

    with open(".minidiary/entries.dat", "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    deleted = False
    for line in lines:
        if line.startswith(str(entry_id) + "|"):
            deleted = True
        else:
            new_lines.append(line)

    if not deleted:
        return f"Entry #{entry_id} not found."

    with open(".minidiary/entries.dat", "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    return f"Deleted entry #{entry_id}."


def search_entries(search_date):
    """V2 YENİ: Verilen tarihe göre kayıtları filtreler ve listeler."""
    if not os.path.exists(".minidiary"):
        return "Not initialized. Run: python minidiary.py init"

    # SPEC'te istenen hata mesajı için format kontrolü
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", search_date):
        return "Invalid date format.\nUse YYYY-MM-DD"

    with open(".minidiary/entries.dat", "r", encoding="utf-8") as f:
        lines = f.readlines()

    found_entries = []
    for line in lines:
        if line.strip().endswith(search_date):
            parts = line.strip().split("|")
            found_entries.append(f"[{parts[0]}] {parts[1]} ({parts[2]})")

    if not found_entries:
        return f"No entries found for {search_date}."

    return "\n".join(found_entries)


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
        print(list_entries())

    elif cmd == "delete":
        if len(sys.argv) < 3:
            print("Usage: python minidiary.py delete <id>")
        else:
            print(delete_entry(sys.argv[2]))

    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: python minidiary.py search <YYYY-MM-DD>")
        else:
            print(search_entries(sys.argv[2]))

    else:
        print("Unknown command: " + cmd)
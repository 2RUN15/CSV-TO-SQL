#!/usr/bin/env python3
import csv, random, uuid
from datetime import datetime, timedelta
import os

random.seed(42)

FIRST_NAMES = [
    "Ahmet","Mehmet","Can","Deniz","Elif","Zeynep","Mert","Emir","Ece","Buse",
    "Ali","Ayşe","Fatma","Hakan","Kerem","Seda","Ozan","Leyla","Berk","Erdem",
    "Mina","Derya","Onur","Tunç","Melek","Sena","Gökhan","İrem","Naz","Bora",
    "Cem","Burcu","Fırat","Selin","Serkan","Melis","Tolga","Pelin","Umut","Aslı",
    "Barış","Simay","Ege","Yusuf","Maya","Tolun","Hande","Sibel","İlker","Pınar"
]

LAST_NAMES = [
    "Yılmaz","Kaya","Demir","Çelik","Şahin","Yıldız","Yılmazer","Arslan","Aydın","Öztürk",
    "Polat","Kurt","Koç","Aksoy","Çetin","Güneş","Özkan","Kılıç","Yalçın","Kara",
    "Doğan","Kaplan","Erdoğan","Özdemir","Karaoğlu","Taş","Gür","Korkmaz","Kuru","Bayram",
    "Parlak","Mutlu","Sever","Balcı","Eren","Acar","Çoban","Çelikten","Sarı","Işık",
    "Güler","Toprak","Vural","Soylu","Özpolat","Kayaer","Türkmen","Gök","Kayaçiçek","Ulus"
]

CITIES = [
    "İstanbul","Ankara","İzmir","Bursa","Antalya","Adana","Konya","Gaziantep","Mersin","Eskişehir",
    "Diyarbakır","Samsun","Kayseri","Trabzon","Balıkesir","Sakarya","Hatay","Manisa","Aydın","Denizli"
]

def random_date(start_days_ago=365*5):
    base = datetime.now() - timedelta(days=start_days_ago)
    d = random.randint(0, start_days_ago)
    s = random.randint(0, 24*3600-1)
    return (base + timedelta(days=d, seconds=s)).date().isoformat()

def gen_rows(n):
    for _ in range(n):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        full = f"{first} {last}"
        email = f"{first.lower()}.{last.lower()}{random.randint(1,9999)}@example.com"
        age = random.randint(18, 75)
        city = random.choice(CITIES)
        signup = random_date()
        is_active = random.choice((0,1))
        balance = f"{random.uniform(0,20000):.2f}"
        score = random.randint(0, 100)
        yield [str(uuid.uuid4()), first, last, full, email, age, city, signup, is_active, balance, score]

def write_csv_semicolon(path, rows_total, chunk=100_000):
    headers = ["uuid","first_name","last_name","full_name","email","age","city","signup_date","is_active","balance","score"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(headers)
        remaining = rows_total
        while remaining > 0:
            cur = min(chunk, remaining)
            for row in gen_rows(cur):
                w.writerow(row)
            remaining -= cur

if __name__ == "__main__":
    ROWS = 1_000_000          # 1M için
    # ROWS = 1_000_000_000     # 1 milyar için (diske ~50–120 GB CSV yazar)
    OUT = "random_uuid_semicolon.csv"
    CHUNK = 100_000           # İstersen 1_000_000 yapıp daha hızlı IO alabilirsin
    write_csv_semicolon(OUT, ROWS, CHUNK)
    print("Done ->", OUT)

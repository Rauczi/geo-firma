import warnings

warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    module="openpyxl"
)

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time
import os

# ========== Konfiguracja ==========
INPUT_FILE = "input.xlsx"
OUTPUT_FILE = "output.xlsx"
CACHE_FILE = "cache_geokodowanie.csv"

POSTAL_COL = "kod"
CITY_COL = "miasto"

# ========== Wczytanie danych ==========
df = pd.read_excel(INPUT_FILE, dtype={POSTAL_COL: str})
print(f"Wczytano {len(df)} rekordów")

# ========== Wczytanie bufora ==========
if os.path.exists(CACHE_FILE):
    cache = pd.read_csv(CACHE_FILE, dtype={POSTAL_COL: str})
    cache_map = {
        (str(r[POSTAL_COL]).strip(), str(r[CITY_COL]).strip()):
        (r["szerokosc"], r["dlugosc"])
        for _, r in cache.iterrows()
    }
    print(f"Wczytano {len(cache_map)} wpisów z bufora")
else:
    cache_map = {}

# ========== Inicjalizacja geokodera ==========
geolocator = Nominatim(user_agent="pracownicy_geokodowanie_2026")

latitudes = []
longitudes = []
statuses = []
nowe_wpisy = []

for idx, row in df.iterrows():

    postal = str(row[POSTAL_COL]).strip()
    city = str(row[CITY_COL]).strip()
    key = (postal, city)

    # 1) Sprawdzenie bufora
    if key in cache_map:
        lat, lon = cache_map[key]
        latitudes.append(lat)
        longitudes.append(lon)
        statuses.append("OK (z bufora)")
        print(f"[{idx + 1}/{len(df)}] {postal} {city} -> z bufora")
        continue

    # 2) Zapytania do Nominatim
    location = None
    status = None

    try:
        # Próba 1: kod + miasto
        location = geolocator.geocode(
            f"{postal}, {city}, Poland",
            timeout=10,
            addressdetails=False
        )
        if location:
            status = "OK (kod+miasto)"

        # Próba 2: sam kod
        if not location:
            location = geolocator.geocode(
                f"{postal}, Poland",
                timeout=10,
                addressdetails=False
            )
            if location:
                status = "OK (kod)"

        # Próba 3: samo miasto
        if not location:
            location = geolocator.geocode(
                f"{city}, Poland",
                timeout=10,
                addressdetails=False
            )
            if location:
                status = "OK (miasto)"

        if location:
            lat = location.latitude
            lon = location.longitude

            latitudes.append(lat)
            longitudes.append(lon)
            statuses.append(status)

            nowe_wpisy.append({
                POSTAL_COL: postal,
                CITY_COL: city,
                "szerokosc": lat,
                "dlugosc": lon
            })

            print(
                f"[{idx+1}/{len(df)}] "
                f"{postal} {city} -> {lat:.6f}, {lon:.6f} ({status})"
            )
        else:
            latitudes.append(None)
            longitudes.append(None)
            statuses.append("Nie znaleziono")
            print(
                f"[{idx+1}/{len(df)}] "
                f"{postal} {city} -> NIE ZNALEZIONO"
            )

    except (GeocoderTimedOut, GeocoderServiceError) as e:
        latitudes.append(None)
        longitudes.append(None)
        statuses.append(f"Błąd: {e}")
        print(
            f"[{idx+1}/{len(df)}] "
            f"{postal} {city} -> BŁĄD: {e}"
        )

    # Wymóg Nominatim: maks. 1 zapytanie/s — POZA try/except, po każdym rekordzie
    time.sleep(1.5)

# ========== Zapis wyników ==========
df["szerokosc"] = latitudes
df["dlugosc"] = longitudes
df["status"] = statuses

df.to_excel(OUTPUT_FILE, index=False)
print(f"\nZapisano wynik do {OUTPUT_FILE}")

# ========== Aktualizacja bufora ==========
if nowe_wpisy:
    new_cache = pd.DataFrame(nowe_wpisy)
    if os.path.exists(CACHE_FILE):
        old_cache = pd.read_csv(CACHE_FILE, dtype={POSTAL_COL: str})
        combined = pd.concat([old_cache, new_cache]).drop_duplicates(
            subset=[POSTAL_COL, CITY_COL],
            keep="last"
        )
    else:
        combined = new_cache
    combined.to_csv(CACHE_FILE, index=False)
    print(f"Zaktualizowano bufor: {CACHE_FILE}")

# ========== Podsumowanie ==========
ok = sum(s.startswith("OK") for s in statuses)
print(f"\nSukces: {ok}/{len(df)}")

if ok < len(df):
    print("\nRekordy do ręcznej weryfikacji:")
    print(
        df[~df["status"].str.startswith("OK")][
            [POSTAL_COL, CITY_COL, "status"]
        ].to_string()
    )

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

import pandas as pd

# ========== Konfiguracja ==========
INPUT_FILE = "input.xlsx"
OUTPUT_FILE = "output.xlsx"
REFERENCE_FILE = "PL.txt"

POSTAL_COL = "kod"
CITY_COL = "miasto"

# ========== Wczytanie bazy referencyjnej ==========
# 0=kraj, 1=kod, 2=miejscowość, 3=woj., 4=kod_woj, 5=powiat, 6=kod_pow, 7=gmina (główna miejscowość), 8=kod_gminy, 9=szer., 10=dług., 11=dokł.
ref = pd.read_csv(
    REFERENCE_FILE, sep="\t", header=None, dtype=str,
    names=["kraj", "kod", "miejscowosc", "wojewodztwo", "kod_woj",
           "powiat", "kod_pow", "gmina", "kod_gminy",
           "szerokosc", "dlugosc", "dokladnosc"]
)

ref["kod"] = ref["kod"].str.strip()
ref["miejscowosc_norm"] = ref["miejscowosc"].str.strip().str.lower()
ref["gmina_norm"] = ref["gmina"].str.strip().str.lower()
ref["szerokosc"] = pd.to_numeric(ref["szerokosc"], errors="coerce")
ref["dlugosc"] = pd.to_numeric(ref["dlugosc"], errors="coerce")
ref = ref.dropna(subset=["szerokosc", "dlugosc"])

# Słownik 1: (kod, miejscowość) -> (lat, lon)
slownik_kod_miejsc = {
    (r["kod"], r["miejscowosc_norm"]): (r["szerokosc"], r["dlugosc"])
    for _, r in ref.iterrows()
}

# Słownik 2: kod -> (lat, lon) dla głównej miejscowości (gminy z kolumny 7)
# Szukamy wiersza, w którym miejscowość (kolumna 2) == gmina (kolumna 7) dla danego kodu.
# Jeśli takiego nie ma, bierzemy po prostu pierwszą współrzędną przypisaną do gminy.
slownik_kod_glowna = {}
for kod, grupa in ref.groupby("kod"):
    # 1. Próbujemy znaleźć wiersz, gdzie miejscowość to ta sama nazwa co gmina
    glowna = grupa[grupa["miejscowosc_norm"] == grupa["gmina_norm"]]
    if not glowna.empty:
        r = glowna.iloc[0]
        slownik_kod_glowna[kod] = (r["szerokosc"], r["dlugosc"])
    else:
        # 2. Jeśli nie ma takiego wiersza, bierzemy pierwszą współrzędną z kolumny 7 (gmina)
        # (np. bierzemy pierwszą napotkaną współrzędną dla tego kodu, która jest przypisana do gminy)
        r = grupa.iloc[0]
        slownik_kod_glowna[kod] = (r["szerokosc"], r["dlugosc"])

# Słownik 3: kod -> dowolna współrzędna (jako ostateczność)
slownik_kod_dowolna = {}
for _, r in ref.iterrows():
    slownik_kod_dowolna.setdefault(r["kod"], (r["szerokosc"], r["dlugosc"]))

print(f"Baza: {len(ref)} wierszy, {len(slownik_kod_miejsc)} par (kod, miejscowość)")

# ========== Wczytanie input ==========
df = pd.read_excel(INPUT_FILE, dtype={POSTAL_COL: str})
print(f"Wczytano {len(df)} rekordów")

latitudes, longitudes, statuses, typy = [], [], [], []

for idx, row in df.iterrows():
    postal = str(row[POSTAL_COL]).strip()
    city = str(row[CITY_COL]).strip()
    city_norm = city.lower()

    # Poziom 1: kod + miejscowość (dokładne dopasowanie)
    if (postal, city_norm) in slownik_kod_miejsc:
        lat, lon = slownik_kod_miejsc[(postal, city_norm)]
        status = "OK (kod+miejscowość)"
        typ = "dokladna"          # ● niebieska

    # Poziom 2: kod istnieje, ale miejscowość nie pasuje -> bierzemy główną miejscowość (gminę)
    elif postal in slownik_kod_glowna:
        lat, lon = slownik_kod_glowna[postal]
        status = "OK (główna miejscowość dla kodu)"
        typ = "przybliżona"       # ● pomarańczowa

    # Poziom 3: jeśli z jakiegoś powodu nie ma głównej, bierzemy dowolną dla kodu
    elif postal in slownik_kod_dowolna:
        lat, lon = slownik_kod_dowolna[postal]
        status = "OK (dowolna miejscowość dla kodu)"
        typ = "niepewna"          # X

    # Poziom 4: brak kodu
    else:
        lat, lon = None, None
        status = "Nie znaleziono kodu"
        typ = "brak"

    latitudes.append(lat)
    longitudes.append(lon)
    statuses.append(status)
    typy.append(typ)

    print(f"[{idx+1}/{len(df)}] {postal} {city} -> {status}")

# ========== Zapis ==========
df["szerokosc"] = latitudes
df["dlugosc"] = longitudes
df["status"] = statuses
df["typ_dopasowania"] = typy
df.to_excel(OUTPUT_FILE, index=False)
print(f"\nZapisano wynik do {OUTPUT_FILE}")

ok = sum(s.startswith("OK") for s in statuses)
print(f"Sukces: {ok}/{len(df)}")

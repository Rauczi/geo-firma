import pandas as pd
import folium

# ========== Konfiguracja ==========
INPUT_FILE = "output.xlsx"        # plik z wynikami geokodowania
OUTPUT_HTML = "mapa.html"

# Nazwy kolumn (zgodnie z Twoim plikiem wynikowym)
LAT_COL = "szerokosc"
LON_COL = "dlugosc"
NAME_COL = "imie_nazwisko"
STATUS_COL = "status"

# ========== Odczyt danych ==========
df = pd.read_excel(INPUT_FILE)

# Odfiltruj rekordy bez współrzędnych
df_map = df.dropna(subset=[LAT_COL, LON_COL]).copy()
print(f"Rekordów z współrzędnymi: {len(df_map)} / {len(df)}")

if df_map.empty:
    print("Brak danych do wyświetlenia na mapie.")
    exit()

# ========== Utworzenie mapy ==========
# Wyśrodkuj mapę na średniej współrzędnych
center_lat = df_map[LAT_COL].mean()
center_lon = df_map[LON_COL].mean()
# Opcja 1: OpenStreetMap (zalecane, stabilne i bezpłatne)
m = folium.Map(location=[center_lat, center_lon], zoom_start=8, tiles="OpenStreetMap")

# Opcja 2: Esri World Gray Canvas (szary styl, również bez klucza)
# Należy zaimportować xyzservices i przekazać obiekt
import xyzservices.providers as xyz
m = folium.Map(location=[center_lat, center_lon], zoom_start=8, tiles=xyz.Esri.WorldGrayCanvas)

# ========= Dodawanie punktów =========

grupy = df_map.groupby(
    ["szerokosc", "dlugosc"]
)

for (lat, lon), grupa in grupy:

    popup = ""

    for _, row in grupa.iterrows():

        popup += (
            f"{row['nrosobowy']} "
            f"{row['imie_nazwisko']}<br>"
        )

    folium.Marker(
        [lat, lon],
        popup=folium.Popup(popup, max_width=400)
    ).add_to(m)

# ========= Zapis =========

m.save(OUTPUT_HTML)

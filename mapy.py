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

import folium

grupy = df_map.groupby([LAT_COL, LON_COL])

for (lat, lon), grupa in grupy:
    ile = len(grupa)
    popup = "".join(f"{r['nrosobowy']} {r[NAME_COL]}<br>" for _, r in grupa.iterrows())

    if ile == 1:
        # Pojedyncza osoba — mała kropka bez liczby
        folium.CircleMarker(
            location=[lat, lon],
            radius=6,
            color="#1f77b4",
            fill=True,
            fill_color="#1f77b4",
            fill_opacity=0.8,
            popup=folium.Popup(popup, max_width=400),
        ).add_to(m)
    else:
        # Grupa — większa kropka z liczbą osób w środku
        folium.CircleMarker(
            location=[lat, lon],
            radius=10 + 2 * ile,
            color="#d62728",
            fill=True,
            fill_color="#d62728",
            fill_opacity=0.9,
            popup=folium.Popup(popup, max_width=400),
        ).add_to(m)

        # Liczba osób na wierzchu kropki
        folium.Marker(
            [lat, lon],
            icon=folium.DivIcon(
                html=f'<div style="font-size:12px; color:white; font-weight:bold; '
                     f'text-align:center; line-height:20px;">{ile}</div>',
                icon_size=(20, 20),
                icon_anchor=(10, 10),
            ),
        ).add_to(m)

# ========= Zapis =========

m.save(OUTPUT_HTML)

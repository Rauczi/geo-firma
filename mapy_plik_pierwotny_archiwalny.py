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

# ========== Dodanie punktów ==========
for _, row in df_map.iterrows():
    lat = row[LAT_COL]
    lon = row[LON_COL]
    name = str(row[NAME_COL]).strip()
    status = str(row[STATUS_COL]).strip()

    # Treść etykiety (imię i nazwisko)
    label_html = f'<div style="font-size: 13px; color: #333; font-weight: bold; white-space: nowrap;">{name}</div>'

    # Użyj DivIcon, aby wyświetlić tekst bezpośrednio na mapie (bez klikania)
for _, row in df_map.iterrows():
    lat = row[LAT_COL]
    lon = row[LON_COL]
    name = str(row[NAME_COL]).strip()
    status = str(row[STATUS_COL]).strip()
    kod = str(row.get("kod", "")).strip()
    miasto = str(row.get("miasto", "")).strip()

    popup_html = f"""
    <b>{name}</b><br>
    Kod pocztowy: {kod}<br>
    Miejscowość: {miasto}<br>
    Szerokość: {lat:.6f}<br>
    Długość: {lon:.6f}<br>
    Status: {status}
    """

    # Kropka – bez popup, tylko znacznik wizualny
    folium.CircleMarker(
        location=[lat, lon],
        radius=6,
        color="#d62728",
        fill=True,
        fill_color="#d62728",
        fill_opacity=0.9,
    ).add_to(m)

    # Etykieta – tutaj przypisujemy popup, bo ten marker jest na wierzchu i przechwytuje kliknięcia
    label_html = (
        f'<div style="font-size: 12px; color: #222; font-weight: bold; '
        f'white-space: nowrap; text-shadow: 1px 1px 2px white;">{name}</div>'
    )
    folium.Marker(
        location=[lat, lon],
        icon=folium.DivIcon(
            html=label_html,
            icon_size=(160, 20),
            icon_anchor=(-10, 10),
        ),
        popup=folium.Popup(popup_html, max_width=300),  # ← popup tutaj
    ).add_to(m)


# ========== Zapis ==========
m.save(OUTPUT_HTML)
print(f"Zapisano mapę do: {OUTPUT_HTML}")

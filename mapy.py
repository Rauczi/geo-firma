import pandas as pd
import folium
import xyzservices.providers as xyz

# ========== Konfiguracja ==========
INPUT_FILE = "output.xlsx"
OUTPUT_HTML = "mapa.html"

LAT_COL = "szerokosc"
LON_COL = "dlugosc"
NAME_COL = "imie_nazwisko"
STATUS_COL = "status"
TYP_COL = "typ_dopasowania"

# ========== Odczyt ==========
df = pd.read_excel(INPUT_FILE)
df_map = df.dropna(subset=[LAT_COL, LON_COL]).copy()
print(f"Rekordów z współrzędnymi: {len(df_map)} / {len(df)}")

if df_map.empty:
    print("Brak danych do wyświetlenia na mapie.")
    exit()

# ========== Mapa ==========
center_lat = df_map[LAT_COL].mean()
center_lon = df_map[LON_COL].mean()



# Używamy Esri World Gray Canvas - nie wymaga klucza API
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=8,
    tiles=xyz.Esri.WorldGrayCanvas
)

# ========== Hierarchia typów ==========
# im wyższa liczba, tym wyższy priorytet (rysowany na wierzchu)
PRIORYTET = {
    "dokladna": 1,
    "przybliżona": 2,
    "niepewna": 3,
    "brak": 3,
}

STYL = {
    "dokladna":     {"kolor": "#1f77b4", "etykieta": "dokładna"},
    "przybliżona":  {"kolor": "#ff7f0e", "etykieta": "przybliżona"},
    "niepewna":     {"kolor": "#d62728", "etykieta": "niepewna"},
    "brak":         {"kolor": "#d62728", "etykieta": "brak"},
}

# ========== Grupowanie po (lat, lon) — nie po typie ==========
grupy = df_map.groupby([LAT_COL, LON_COL])

for (lat, lon), grupa in grupy:
    ile = len(grupa)

    # Ustal najwyższy priorytet w grupie
    typy = grupa[TYP_COL].fillna("brak").tolist()
    typ_glowny = max(typy, key=lambda t: PRIORYTET.get(t, 3))

    styl = STYL.get(typ_glowny, STYL["brak"])
    kolor = styl["kolor"]
    promien = 7 + 2 * ile

    # Popup: wszyscy w grupie, z typem dopasowania przy każdym
    popup = f"<b>{ile} osoba(e) w tym punkcie</b><br><br>"
    for _, row in grupa.iterrows():
        t = row.get(TYP_COL, "brak")
        t_label = STYL.get(t, {}).get("etykieta", t)
        popup += (
            f"{row['nrosobowy']} {row[NAME_COL]} "
            f"<span style='color:#888; font-size:11px;'>({t_label})</span><br>"
        )

    # Kropka
    folium.CircleMarker(
        location=[lat, lon],
        radius=promien,
        color=kolor,
        fill=True,
        fill_color=kolor,
        fill_opacity=0.85,
        popup=folium.Popup(popup, max_width=400),
    ).add_to(m)

    # X dla niepewnych / brak
    if typ_glowny in ("niepewna", "brak"):
        folium.Marker(
            [lat, lon],
            icon=folium.DivIcon(
                html='<div style="font-size:12px; color:white; font-weight:bold; '
                     'text-align:center; line-height:20px;">X</div>',
                icon_size=(20, 20),
                icon_anchor=(10, 10),
            ),
        ).add_to(m)

    # Etykieta z nazwiskami tylko dla małych grup (<= 3)
    if ile <= 3:
        names = "<br>".join(str(n) for n in grupa[NAME_COL])
        folium.Marker(
            [lat, lon],
            icon=folium.DivIcon(
                html=f'<div style="font-size:11px; color:#222; font-weight:bold; '
                     f'white-space:nowrap; text-shadow:1px 1px 2px white;">{names}</div>',
                icon_size=(160, 20),
                icon_anchor=(-10, 10),
            ),
        ).add_to(m)

# ========== Legenda ==========
legenda = """
<div style="position: fixed; bottom: 30px; left: 30px; z-index: 9999;
            background: white; padding: 10px 15px; border: 1px solid #999;
            border-radius: 5px; font-size: 13px; font-family: sans-serif;">
<b>Legenda</b><br>
<span style="color:#1f77b4; font-size:18px;">●</span> dokładna (kod + miejscowość)<br>
<span style="color:#ff7f0e; font-size:18px;">●</span> przybliżona (kod + gmina)<br>
<span style="color:#d62728; font-size:18px;">X</span> niepewna (dowolna z kodu)<br>
<br>
<small>Przy nakładaniu: X zasłania pomarańczową,<br>
pomarańczowa zasłania niebieską.</small>
</div>
"""
m.get_root().html.add_child(folium.Element(legenda))

# ========== Zapis ==========
m.save(OUTPUT_HTML)
print(f"Zapisano mapę do: {OUTPUT_HTML}")

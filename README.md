# geo-firma
Geokodowanie adresów pracowników → mapa

Skrypt wczytuje plik Excel z adresami (kod pocztowy + miejscowość), pobiera współrzędne geograficzne przez Nominatim (OpenStreetMap) i generuje:

    output.xlsx — dane wejściowe + kolumny szerokosc, dlugosc, status,

    mapa.html — interaktywną mapę z kropkami, etykietami (imię i nazwisko) i popupami (kod, miejscowość, współrzędne).

    Uwaga o danych wrażliwych: skrypt wysyła do Nominatim wyłącznie kod pocztowy i miejscowość — nigdy imię, nazwisko, ulicę ani numer domu. Przed uruchomieniem zapoznaj się z polityką Nominatim (limit 1 żądanie/s, wymagany User-Agent).

Wymagania

    Python 3.10+

    Połączenie z Internetem (Nominatim + kafle mapy)

    Plik input.xlsx z kolumnami: kod, miasto (oraz dowolnymi innymi — zostaną przepisane do wyniku)

Arch Linux
1. Instalacja Pythona i pip

    sudo pacman -S python python-pip

2. Klonowanie repozytorium

    git clone https://github.com/TWOJ_LOGIN/geo-firma.git
    cd geo-firma

3. Środowisko wirtualne (zalecane — zgodnie z ArchWiki)

    python -m venv venv
   
    source venv/bin/activate

5. Instalacja zależności

    pip install -r requirements.txt

6. Przygotowanie danych

    Umieść plik input.xlsx w katalogu projektu. Kolumny muszą nazywać się dokładnie kod i miasto (lub zmień POSTAL_COL / CITY_COL w geokoduj.py).
7. Uruchomienie geokodowania

    python geokoduj.py

    Wynik: output.xlsx oraz cache_geokodowanie.csv (bufor — nie usuwaj).
8. Wygenerowanie mapy

    python mapy.py

    Wynik: mapa.html — otwórz w przeglądarce.
9. Dezaktywacja środowiska (po zakończeniu pracy)

    deactivate

Windows
1. Instalacja Pythona

    Pobierz instalator ze strony python.org i zaznacz opcję „Add Python to PATH" podczas instalacji.

    Sprawdź w PowerShell:
    powershell

    python --version
    pip --version

2. Klonowanie repozytorium
    powershell

  do  >cd geo-firma

3. Środowisko wirtualne
    powershell

    py -m venv venv
    venv\Scripts\activate

    Po aktywacji w promptcie pojawi się (venv).
4. Instalacja zależności
    powershell

    pip install -r requirements.txt

5. Przygotowanie danych

    Umieść input.xlsx w katalogu projektu. Kolumny muszą nazywać się dokładnie kod i miasto.
   
7. Uruchomienie geokodowania
    powershell

    py geokoduj.py

7. Wygenerowanie mapy
    powershell

    python mapy.py

    Otwórz mapa.html w przeglądarce.
8. Dezaktywacja środowiska
    powershell

    deactivate

    Plik requirements.txt

    W katalogu projektu utwórz plik requirements.txt z zawartością:
    txt

    pandas
    openpyxl
    geopy
    folium

    Wersje nie są przypięte — jeśli chcesz je ustabilizować, użyj pip freeze > requirements.txt po instalacji.

Struktura projektu
text

geo-firma/
├── geokoduj.py              # geokodowanie: input.xlsx → output.xlsx
├── mapy.py                  # generowanie mapy: output.xlsx → mapa.html
├── requirements.txt         # zależności
├── input.xlsx               # dane wejściowe (nie commituj z danymi wrażliwymi!)
├── output.xlsx              # wynik geokodowania (generowany)
├── cache_geokodowanie.csv   # bufor Nominatim (generowany, nie usuwaj)
├── mapa.html                # wynik mapy (generowany)
└── README.md

Rozwiązywanie problemów
Problem	Rozwiązanie
KeyError: 'kod'	Nazwy kolumn w input.xlsx nie pasują. Sprawdź POSTAL_COL / CITY_COL w geokoduj.py.
TypeError: PatternFill.__init__() got an unexpected keyword argument 'extLst'	Plik Excel zapisany przez narzędzie niezgodne z openpyxl (np. SoftMaker). Otwórz w LibreOffice i zapisz ponownie jako .xlsx.
UserWarning: CartoDB tiles now require an API key	Zmień tiles="OpenStreetMap" w mapy.py.
Mapa pusta / szare tło	Otwórz mapa.html przez lokalny serwer: python -m http.server 8000 → http://localhost:8000/mapa.html. Sprawdź też, czy nie blokuje adblock.
Popupy nie działają	Upewnij się, że popup= jest przypisany do folium.Marker (etykiety), a nie do CircleMarker.
403 Forbidden / blokada Nominatim	Skrypt ma time.sleep(1.1) — nie usuwaj go. Nie uruchamiaj równolegle.
Bezpieczeństwo danych

    Nie commituj input.xlsx, output.xlsx, cache_geokodowanie.csv ani mapa.html — zawierają dane osobowe. Dodaj je do .gitignore.

    Do Nominatim wysyłane są tylko kod pocztowy i miejscowość — bez imienia, nazwiska, ulicy i numeru domu.

    Przed uruchomieniem zapoznaj się z polityką użytkowania Nominatim.

Przykładowy .gitignore
gitignore

venv/
__pycache__/
*.pyc
input.xlsx
output.xlsx
cache_geokodowanie.csv
mapa.html
.env

Licencja

Projekt do użytku wewnętrznego. Dane pochodzą z OpenStreetMap (© współtwórcy OpenStreetMap, licencja ODbL).

To wszystko — możesz wrzucić tę instrukcję jako README.md do repozytorium. Jeśli chcesz, mogę też przygotować wersję angielską (przydatną, jeśli repo ma być publiczne) albo skrypt setup.sh / setup.ps1, który automatycznie tworzy venv i instaluje zależności jednym poleceniem. Daj znać! 🚀

# geo-firma
Geokodowanie adresów pracowników → mapa

Skrypt wczytuje plik Excel z adresami (kod pocztowy + miejscowość), pobiera współrzędne bez wysyłania danych typu imię i nazwisko na jakikolwiek serwer, efektem działania jest wygenerowana lista "output" z danymi geolokalizacyjnymi miejscowości zamieszkania (nie ulicy i numeru domu):

   geokoduj.py >> output.xlsx — dane wejściowe + kolumny szerokosc, dlugosc, status,

   mapy.py >> mapa.html — interaktywną mapę z kropkami, etykietami (imię i nazwisko) i popupami (kod, miejscowość, współrzędne).


UWAGA! Należy przygotować plik wsadowy "input.xlsx" nie wolno zmieniać jego nazwy oraz nazw w wierszu 1.

Wymagania

    Python 3.10+ <<Należy go zainstalować przed uruchomieniem>>

    Połączenie z Internetem (Nominatim + kafle mapy)

    Plik input.xlsx z kolumnami: kod, miasto (oraz dowolnymi innymi — zostaną przepisane do wyniku)

# Uruchomienie

1. Pobieramy całe repozytorium Github, rozpakowujemy do dodwolnego folderu
2. Uruchamianie przy pomocy komend (poniżej) w terminalu dla Linux ; w PowerShell dla Windows



Arch Linux pierwsze uruchomienie >> UWAGA Kolejne uruchamianie tylko kroki 1,3,4,5,6

1. Środowisko wirtualne
   
    python -m venv venv   
    source venv/bin/activate

2. Instalacja zależności

    pip install -r requirements.txt\
    python -m pip install --upgrade pip 
3. Przygotowanie danych

    Umieść plik input.xlsx w katalogu projektu. Kolumny muszą nazywać się dokładnie kod i miasto (lub zmień POSTAL_COL / CITY_COL w geokoduj.py).
   
4. Uruchomienie geokodowania

    python geokoduj.py

    Wynik: output.xlsx
   
5. Wygenerowanie mapy

    python mapy.py

    Wynik: mapa.html — otwórz w przeglądarce.
   
6. Dezaktywacja środowiska (po zakończeniu pracy)

    deactivate

Windows pierwsze uruchomienie >> UWAGA Kolejne uruchamianie tylko kroki 1,3,4,5,6

1. Środowisko wirtualne "POWERSHELL"
   
    py -m venv .venv 
   
    .venv\Scripts\activate

    Po aktywacji w promptcie pojawi się (venv).
3. Instalacja zależności

    pip install -r requirements.txt

4. Aktualizacja pip

   python -m pip install --upgrade pip 

5. Przygotowanie danych

    Umieść input.xlsx w katalogu projektu. Kolumny muszą nazywać się dokładnie kod i miasto.
   
7. Uruchomienie geokodowania
 
    py geokoduj.py

7. Wygenerowanie mapy

    py mapy.py   >>>> generuje plik mapa.html

    Otwórz mapa.html w przeglądarce.

8. Dezaktywacja środowiska
 
    deactivate

# Zasady prywatności i ochrony danych   

	
3. Wg. powyższego uruchamiamy mapy.py która ganeruje widok mapy Polski z oznaczeniami lokalizacji wszystkich adresów.

	UWAGA mapy.py nie wysyła danych z excela - outpot na żaden zewnętrzny serwer
	Mapa generwoana jest na komputerze 	jedynie pobierane są kafelki mapy jako podkład



#########################################################

Licencja MIT

Stworzone przy pomocy AI - DeepSeek oraz Copilot

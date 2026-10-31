# geo-firma wymaga aktualizacji o nowe mapy.py i wymaga testów
Geokodowanie adresów pracowników → mapa

Skrypt wczytuje plik Excel z adresami (kod pocztowy + miejscowość), pobiera współrzędne geograficzne przez Nominatim (OpenStreetMap) i generuje:

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


Arch Linux

1. Środowisko wirtualne
   
    python -m venv venv   
    source venv/bin/activate

2. Instalacja zależności

    pip install -r requirements.txt

3. Przygotowanie danych

    Umieść plik input.xlsx w katalogu projektu. Kolumny muszą nazywać się dokładnie kod i miasto (lub zmień POSTAL_COL / CITY_COL w geokoduj.py).
   
4. Uruchomienie geokodowania

    python geokoduj_Linux.py

    Wynik: output.xlsx oraz cache_geokodowanie.csv (bufor — nie usuwaj).
   
5. Wygenerowanie mapy

    python mapy.py

    Wynik: mapa.html — otwórz w przeglądarce.
   
6. Dezaktywacja środowiska (po zakończeniu pracy)

    deactivate

Windows

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

    Uwaga o danych wrażliwych: skrypt wysyła do Nominatim wyłącznie kod pocztowy i 	miejscowość — nigdy imię, nazwisko, ulicę ani numer domu. Przed uruchomieniem 	zapoznaj się z polityką Nominatim (limit 1 żądanie/s, wymagany User-Agent).

1. geokoduj.py korzysta z pliku input,xlsx
	
	Na serwer wysyłany jest kod pocztowy i miejscowość bez imienia i nazwiska, jednak 	dla bezpieczeństwa należy wpisać jedynie numer osobowy.

2. Po wykonaniu geokoduj.py generowany jest plik output.xlsx

	UWAGA Może być tak że program nie znajduje wszystkich lokalizacji, możliwe że 	trzeba będzie cześć danych wprowadzić ręcznie.
	nawet pomimo zastosowania logiki sprawdzania:
		1. Sprawdzany jest kod pocztowy + miejscowość < jeżeli nie znajdzie idziemy dalej
		2. sprawdzany jest kod kod pocztowy < jeżeli nie znajdzie idziemy dalej
		3. sprawdzana jest miejscowość < jeżeli nie znajdzie idziemy dalej
		4. uzyskujemy wpis "nie znaleziono"


	na podstawie wpisu "nie znaleziono" w pliki output.xlsx wiemy które adresy nie będą 	wrysowywane na mapie możemy im ręcznie nadać wartości długości i szerokości 	geograficznej.
	
3. Wg. powyższego uruchamiamy mapy.py która ganeruje widok mapy Polski z oznaczeniami lokalizacji wszystkich adresów.

	UWAGA mapy.py nie wysyła danych z excela - outpot na żaden zewnętrzny serwer, 	jedynie pobierane są kafelki mapy jako podkład
	
	!! jeżeli chcemy by na mapie pojawiły się imiona i nazwiska należy edytować ręcznie 	plik outpot.xlsx i za pomocą funkcji lub osobiście dopisać do każdego numeru 	osobowego - imię i nazwisko

#########################################################

Licencja MIT

Stworzone przy pomocy AI - DeepSeek oraz Copilot

# AutoMailer

Przygotowanie projektu do działania:

## Środowisko
- aplikacja wymaga pythona 3 oraz pip3 (albo pip zależnie od dystrubucji)
- instalujemy sobie virtualenv ```python3 -m pip install --user virtualenv```
- tworzymy virtualenv ```python3 -m venv env```
- aktywujemy virtualenv ```source env/bin/activate```
- wymagane moduły pythona mozna zainstalowac komenda pip ```install -r requirements.txt```

Samo uruchomienie aplikacji to ustawienie zmiennej środowiskowej `APP_SETTINGS` na odpowiednią wartość odpowiadającą zestawowi konfiguracyjnemu z config.py i uruchomienie polecenia `python mailer_run.py`

Przykład:
> APP_SETTINGS=config.DevelopmentConfig; python mailer_run.py

Inne ustawienia można zmieniać wchodząc do pliku `config.py` i edytując odpowiednie zmienne.

## Konfiguracja obsługi arkuszy google:

1. Wejdź na <https://console.developers.google.com/> i utwórz nowy projekt
2. W projekcie wybierz "Dane Logowania" i utwórz Konto Usługi
3. Utwórz klucz prywatny
4. Pobierz go jako plik .json i zmień jego nazwę na "keyfile_do_listy_odbiorcow.json"
5. Nadaj danemu kontu (przykładowa nazwa to: "jakieskonto@whatever-2812012.iam.gserviceaccount.com") dostęp do plików templatki i arkusza google którego planujesz uywać.
6. Wejdź na <https://console.developers.google.com/apis/api/sheets.googleapis.com/> wybierz swój projekt i kliknij "Włącz"
7. Wejdź na <https://console.developers.google.com/apis/api/docs.googleapis.com/> wybierz swój projekt i kliknij "Włącz"

Uwaga: nazwy jsonów mona oczywiście zmienić w `config.py`

## Konfiguracja obsługi gmaila:

1. Wejdź na <https://console.developers.google.com/apis/api/gmail.googleapis.com/> wybierz swój projekt i kliknij "Włącz"
2. W <https://console.developers.com> stwórz ekran akceptacji OAuth (podaj tylko nazwę aplikacji)
3. W sekcji Dane Logowania stwórz nowe dane logowania, wybierając "Identyfikator klienta OAuth" a następnie Typ Aplikacji "Inna" (nazwa nie ma znaczenia)
4. Pobierz plik wynikowy (nazwa zaczyna się od "client_secret_") i zmień jego nazwę na "klucz_do_gmaila.json"
5. Po pierwszym testowym uruchomieniu aplikacja zarząda od ciebie autoryzacji (w konsoli wyświetli się URL), wejdź tam i potwierdź potrzebne uprawnienia
6. Przeglądarka zostanie przekierowana na stronę podaną w konfiguracji pod pozycją `GMAIL_AUTH_HOSTNAME` i `GMAIL_AUTH_PORT` (na której aplikacja uruchomiła tymczasowy serwer www)
7. Aplikacja utworzy plik `gmail_token.pickle`

## Uzywanie samej aplikacji
Uwaga, ID dokumentu google to (np.) w przypadku linka
`https://docs.google.com/document/d/1lx4UIPg8XQkFo7SHuqOTMgxlHewM08pgu2dMtng/edit`
ciąg `1lx4UIPg8XQkFo7SHuqOTMgxlHewM08pgu2dMtng`

1. Wzór podstawowej templatki jest w pliku Odbiorcy.ods naley go zaimportować do google docs jako arkusz.
2. Przykładowy wzór templatki podstawowego maila jest w pliku Template1.txt nalezy go zaimportowac jako google docs. Wzór obsługuje składnię HTML.
3. ID dokumentu Odbiorcy nalezy wkleic w plik config.py w pozycję MAILLIST_GDOCS_ID
4. ID dokumentów templatki podaje się przy danym emailu
5. Mailing uruchamia się zmieniając pozychę "Czy wysyłać" na TAK w drugim arkuszu, a następnie wchodząc na URL o wzorcu <http://SERVER_NAME/api/mailrun> gdzie SERVER_NAME to wartość ustawiona w config.py


# sqlDeveloperConnector
Aplikacja konsolowa napisana w języku Python, służąca do nawiązywania połączenia z baza danych Oracle

Menu pozwala na dokonanie wyboru połączenia zadeklarowanego w pliku 
konfiguracyjnym programu do zarządzania "SQL Developer" (DBMS m.in. dla 
Oracle, MySQL czy SQL Server), poprzez parsowanie pliku connections.xml i 
zapisanie własnego pliku konfiguracyjnego konfig.py do postaci zredukowanej 
JSON.
Plik uruchomieniowy: sampleConnection.py, główny plik logiki programu: 
konnekt.py, plik pomocniczy walidacja.py (nie został napisany od podstaw a 
jedynie dostosowany do działania reszty aplikacji).
Załączony przykładowy plik połączenia connections.xml  z zadeklarowanym 
jednym skonfigurowanym połączeniem.


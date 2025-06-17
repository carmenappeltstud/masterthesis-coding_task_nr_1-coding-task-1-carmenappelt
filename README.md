Aufgabe 1 – Weiterentwicklung der Wetter-Applikation:
Die bestehende Wetter-App bezieht über die NOAA-API die Wetterdaten des jeweils vergangenen Kalenderjahres und visualisiert diese bislang als Säulen- und horizontale Säulen¬diagramme. Im Rahmen dieser Arbeit sind die folgenden Erweiterungen und Korrekturen umzusetzen:
1.	Mehrfachselektion von Standorten:
Erlauben Sie die gleichzeitige Auswahl mehrerer Orte. Die Daten aller ausgewählten Orte sind im gewählten Diagramm gemeinsam darzustellen. Ergänzen Sie dafür eine Legende, aus der die Zuordnung der Linien bzw. Balken zu den jeweiligen Orten eindeutig hervorgeht (z. B. anhand von Farbcodierung).
 
2.	Fehlende Daten ergänzen:
Den UX-Testern ist aufgefallen, dass bei einigen Abfragen einige Tage nicht visualisiert werden. Deshalb soll python-weather, das für einen gegebenen Städenamen die aktuelle Temperatur lieft, als weitere Datenquelle vewendet werden.
Wenn für den heutigen Tag von der NOAA-API für die gewählte Station keine Daten zur Verfügung stehen, soll die aktuelle Temperatur für die Station von python-weather als Tagesdurchschnitt verwendet werden. Überprüfen Sie hierfür ob es NaN Werte für den aktuellen Tag gibt, bevor der bestehende Dataframe für die Visualisierung genutzt wird.

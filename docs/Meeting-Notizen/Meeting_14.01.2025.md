# Abschlussmeeting

## Vorbereitung
* Vorstellen der Applikation

* Vorstellung Benchmark-Reflektion:
    * 17 Risikomatrizen, wovon die meisten die Axiome erfüllen, die wir zur Benutzung des Benchmarks empfohlen/vorrausgesetzt haben
    * Vorstellung der Matrizen mit schlechtesten Scores
        * Range Compression: keine gute Wertaufteilung, da rote Risikoklasse sehr großen Wertebereich hat und grünen sehr kleinen
        * allg. Score/ Quantifying Errors: 3x3 reicht nicht aus, um mögllichst wenig Informationsverlust zu erreichen und auch nicht für eine gute Risikoklassentrennung (grün grenzt an rot) -> diese Matrix erfüllt nicht alle Axiome, ist daher auch sehr niedrig vom Score
    * Vorstellung beste Matrix Nr. 17 (selbst erstellt) inkl. Begründung dieser Wahl der Matrix als Optimierung der optimalen Matrix: 
        * Hinzufügen von mehr Zeilen/Spalten bei gleich bleibender Skala (von 0-1) bewirkt Annäheurng der Matrix an eine quanitative Matrix -> Sachverhalt wird genauer dargestellt
        * mit höherer Dimension der Matrix ist eventuell eine weitere Risikoklasse sinnvoll um die RangeCompression zu erhöhen - während zeitgleich das Ordnungsmaß nicht verringert wird

    * Vorstellung Intervalle je Score und Verteilung auf die Matrizen
    * evtl. Vorstellung von Matrizen, die Scores optimiert gut und mit absicht sehr schlecht abschneiden lassen
    * Selbstkritik:
        * Wichtungsfaktoren beim gewichteten Mittelwert nur auf Basis der optimalen Matrix-Ausgabe erstellen nicht die beste Lösung:
            * siehe hohen Gesamtscore, trotz schlechten RangeCompression-Wert bei Negativ-RangeCompression-Beispiel, da QuantifyingErrors-Wert mit sehr großen Wert durch die Skalierungsfaktoren sehr stark in Mittwelwert einzählt
            * dabei aber Frage was genau das Ziel ist:
                * eigenen unabhängigen Matrixvergleich erstellen (optimale Matrix nach Cox als Richtwert verwenden schlecht)
                * auf Annahme, dass optimale Matrix nach Cox sehr gut ist und damit Vergleich von Matrizen, die durch Erfüllung der Axiome ersteinmal nicht so schlecht sein könnnen -> nicht so ein enormes Problem, diese optimale Matrix als Richtwert zu nehmen
        * Overlap-Score:
            * verfehlt bei der zufällig durchwürfelten Matrix mit pxp-Matrix und p*p Risikoklassen seinen Zweck und gibt dennoch gute Werte aus -> Warum?
            * Normierung des Scores mit MaxOverlap (damit zw. 0 und 1) als Problem: Die eigentlich recht hohen Überschneidungen werden durch eine sehr hohe Zahl geteilt und der Score so marginal klein wird(da MaxOverlap einen Overlap von 1 pro Klassenkombination annimmt -> bei sehr vielen Klassen sehr hoch). Es existieren dennoch viele Überschneidungen, die zwar klein, aber addiert aufeinander sehr hoch werden
            * das ist Schwäche von Benchmark, welche aber bei Matrizen, die die Axiome erfüllen, recht selten tatsächlich auffällt (da dies dann meist sinnvolle, praktisch anwendbare Matrix ist)
        * beschränkende Annahme bei allen Matrizen: lineare Achseneinteilung

* evtl. kleine Benchmark-Änderung bei RangeCompression
* Frage, was wir in Doku reinpacken sollen und wie Abgabe von statten gehen soll

## Notizen

## ToDos für Abgabe
* Abgabe Ende Februar
* ca. 10 seitige Dokumentation des Projektseminars erstellen
    * Einführung mit Ziel und Motivation
    * Erkenntnisse, die man gewonnen hat
    * Benchmark-Erklärung
    * Statistische Auswertung des Benchmarks mit ca. 20 Matrizen
    * Benchmark-Selbstkritik (inkl. Meeting-Feedback vom Professor) und Verbesserungsvorschlägen
        * Verbesserungsvorschlag: ab bestimmten minimalen Wert wird Matrix aus Wertung rausgenommen
    * Beschreibung des Programms (kleine Programmdokumentation)
    * Benutzerdokumentation
* Programm inkl. (evt. kleine Programmdokumentation)/ Benutzerdokumentation abgeben (soll von ihm benutzt werden können)




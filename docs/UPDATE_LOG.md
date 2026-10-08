<!-- Format streng (webui/updates.py :: parse_update_log()): "## <YYYY-MM-DD>" beginnt einen
     Eintrag, "- " beginnt eine Zeile. JEDE Zeile ist EIN Eintrag im Banner/Update-Log --
     KEIN weiches Zeilenumbrechen einer einzelnen Aussage über mehrere physische Zeilen, der
     Parser ignoriert alles, was nicht mit "## " oder "- " beginnt (Live-Fund 2026-08-10: eine
     über vier Zeilen umgebrochene Aussage wurde nach der ersten Zeile abgeschnitten). Lieber
     mehrere kurze "- "-Zeilen als eine lange, umgebrochene. Zwei "## "-Blöcke mit demselben
     Datum sind erlaubt und bewusst genutzt (parse_update_log()s Docstring: "disambiguiert zwei
     `## <selbes Datum>`-Blöcke") -- das Banner zeigt IMMER nur den obersten Eintrag
     (entries[0]), ein zweiter Deploy am selben Tag bekommt so seinen eigenen, frischen Eintrag
     statt stillschweigend an den ersten drangehängt zu werden. -->

## 2026-10-08
- Neue Notizen und Aufgaben landen jetzt in dem Space, in dem du gerade arbeitest — vorher wanderten sie aus einem Team-Space still in deinen eigenen. Der Anlegen-Dialog nennt oben das Ziel.
- In Team-Spaces kann jedes Mitglied mit Schreibrecht Items verschieben, archivieren und löschen, auch solche, die jemand anderes angelegt hat. Der Löschdialog nennt, von wem das Item zuletzt geändert wurde.
- Enter bestätigt jetzt in den Dialogen die Hauptaktion. Im Passwortfeld und bei gesperrten Knöpfen passiert nichts.
- Der Löschdialog zeigt den Titel des Items als eigene Zeile über dem Feld, in das du ihn eintippen musst.
- Behoben: Nach „Abbrechen" im Löschdialog schickte der nächste Löschvorgang zwei Anfragen ab, und die zweite meldete „Item nicht gefunden".
- Das Einstellungsmenü hat einen „Schließen"-Knopf. In „Spaces verwalten" haben die Mitgliederzeilen Abstand, „Entfernen" steht rechts.
- In der Übersicht bleibt der Space-Name lesbar, auch wenn der Space viele Zähler hat — die Zähler rutschen bei Platzmangel in eine zweite Zeile.

## 2026-10-07
- Die Einstellungen sind jetzt eine Fensterkette: das Menü bleibt sichtbar, während das Passwort-, das Spaces- und das Update-Log-Fenster daneben aufgehen. Aus „Spaces verwalten" öffnet ein Klick auf einen Space ein drittes Fenster.
- Im Passwort-Fenster steht der Code aus der Authenticator-App jetzt als letztes Feld, direkt über „Ändern“ — vorher stand er zwischen altem und neuem Passwort.
- Zwei Items, die über einen Tag oder einen Ordner verknüpft sind, zeigen jetzt **eine** Linie. Die ausdrückliche Verknüpfung gewinnt, die daraus abgeleitete entfällt.
- Die alte Adresse funktioniert bis auf Weiteres wieder vollständig, auch zum Schreiben — für Netze, die die neue Adresse noch nicht erreichen (z. B. ein Firmen-VPN). Der Hinweis dort sagt das jetzt so und nennt keinen Abschalttermin mehr.

## 2026-10-03
- Die Kopfdaten haben ein neues Feld „Bei“: damit steht, wer eine Aufgabe übernommen hat. Setzt du den Status auf „In Arbeit“ und das Feld ist noch leer, trägt die Oberfläche deinen eigenen Space selbst ein.
- In der Liste und in der Nur-lesen-Ansicht steht jetzt „bei <Name>“ mit drin, und im Editor darunter, von wem die Notiz zuletzt geändert wurde.
- Der Knopf „Archivieren“ trägt jetzt dieselbe Fläche wie die übrigen Knöpfe — die Vorsichtfarbe sitzt nur noch an der Beschriftung.

## 2026-10-02
- Aufgaben können jetzt den Status „In Arbeit" bekommen und tauchen in einem eigenen Ordner „In Arbeit" in der Navigation auf — vorher war eine so markierte Aufgabe in keinem einzigen Ordner mehr auffindbar.
- Claude kann einer Aufgabe jetzt zuweisen, wer sie übernimmt; die Zuweisung steht in den Kopfdaten und überlebt das Bearbeiten im Browser.
- Notizen und Aufgaben lassen sich jetzt wirklich löschen statt nur zu archivieren — es fragt zweimal nach, beim zweiten Mal muss der Titel abgetippt werden. In der Oberfläche lässt sich ein gelöschtes Item nicht zurückholen.
- Die Verknüpfungs-Karte springt bei jeder Änderung nicht mehr neu an, und bekannte Notizen behalten ihren Platz.
- Ziehst du eine Notiz in der Navigation auf den Space-Namen, landet sie wieder auf der obersten Ebene des Space statt in einem Unterordner.
- Die Formatierleiste im Editor sieht jetzt genauso aus wie die übrigen Knöpfe statt als eigene graue Fläche.

## 2026-09-18
- Die Übersicht zeigt deine Spaces jetzt direkt neben der Verknüpfungs-Karte statt darüber — beides auf einen Blick, kein Umschalten mehr nötig.
- Ein Klick auf eine Notiz oder einen Punkt in der Karte öffnet den Editor an derselben Stelle; Escape oder das Kreuz oben rechts bringt dich sauber zur Karte zurück.
- Space-Zeilen in der Übersicht sind jetzt über ihre ganze Breite klickbar, nicht nur am Namen.
- Die Karte „fliegt" nicht mehr bei jedem Öffnen — Notizen behalten ihre Position, doppelte Linien zwischen zwei verknüpften Notizen sind verschwunden.
- Einstellungen und Abmelden sitzen wieder unten in der Navigation, mit einer deutlicheren Markierung, dass es klickbare Menüpunkte sind.
- Auf schmaleren Bildschirmen (bis 1024 Pixel Breite) zeigt die Ansicht jetzt entweder deine Liste oder den geöffneten Editor in voller Breite, nicht mehr beides gleichzeitig zusammengequetscht.

## 2026-09-05
- Im Suchdialog für Verknüpfungen kannst du wählen, ob eine Notiz als Text-Link im Notiztext oder als Eintrag im Links-Feld angelegt wird — die letzte Wahl wird gemerkt.
- Im Suchdialog für Verknüpfungen kannst du mit Pfeiltasten und Enter durch die Treffer navigieren — das Suchfeld behält den Fokus, die Maus brauchst du dafür nicht.
- Claude nennt dir Notizen konsequent beim Titel statt bei der internen Kennung — jetzt ausnahmslos in jeder Textform (auch in Tabellen, Klammern und Aufzählungen).

## 2026-09-02
- Die Übersicht ist jetzt tabellos: jede deiner Spaces bekommt eine eigene Zeile mit Zähler-Chips für „Offen", „Erledigt", „Notizen" und „Archiv" — ein Klick auf einen Chip öffnet die zugehörige Liste. Vier gleiche Kacheln gibt es nicht mehr.
- Die Übersicht bekommt einen neuen Abschnitt „Verknüpfungen": ein Graph zeigt, welche Notizen aufeinander verweisen (über das Links-Feld oder eine `itm_…`-Referenz im Text) — gemeinsame Tags oder Ordner kannst du bei Bedarf zuschalten, Standard sind nur die echten Verweise.
- Klick auf „Übersicht" zeigt jetzt alle lesbaren Items als Liste (eigene und geteilte Spaces zusammen) — vorher blättertest du in den zuletzt geöffneten Space zurück.
- Eine kleine Legende über der Space-Liste zeigt die drei Kategoriefarben: eigener Space, geteilter Space, fremder Space.

## 2026-09-01
- Links zwischen Notizen werden anklickbar: ein `#item/...`-Link im Text einer Notiz öffnet direkt das verlinkte Gegenstück — vorher waren die Links sichtbar, aber ohne Funktion.
- Im Editor erscheint neben dem Links-Feld eine kleine Lupe zum Suchen und bequemen Anhängen einer Notiz per Klick.

## 2026-09-01
- Claude nennt dir gegenüber jetzt den Titel einer Notiz statt einer internen ID — die Kennung bleibt im Hintergrund, der Titel ist, was du im Browser siehst.

## 2026-08-31
- Mehrere Notizen gleichzeitig in einen anderen Space verschieben: reicht jetzt ein Passwort und ein Code für alle aus, auch wenn die Aktion Schreibrechte erweitert — der Code wird intern genau einmal verwendet, danach ist für jede weitere Verschiebe-Aktion ein neuer Code nötig.
- Spaces entfernen räumt jetzt den internen Suchindex mit auf — die Übersicht funktioniert danach wieder zuverlässig.

## 2026-08-27
- Neuer Menüpunkt "Spaces verwalten": eigene Spaces anlegen oder entfernen, Mitglieder mit Schreibrecht hinzufügen oder entfernen — direkt im Konto-Menü, ohne Kommandozeile.
- Entfernen eines Space und größere Mitgliederänderungen fragen zur Sicherheit noch einmal Passwort und Code ab.
- Mehrere Notizen auf einmal verschieben: mit Strg+Klick (oder lange gedrückt halten) mehrere Zeilen auswählen, dann in einem Rutsch in einen anderen Ordner oder Space verschieben.

## 2026-08-25
- Neuer Knopf zum Entfernen von Bildern aus einer Notiz — das Bild wandert in den Papierkorb, die Textstelle bleibt als reiner Bildname stehen.

## 2026-08-23
- Interner Aufräumschritt: jede bestehende Notiz trägt jetzt explizit "privat" in ihren Metadaten — das war schon vorher der geltende Standardwert, sichtbar ändert sich für dich nichts.

## 2026-08-21
- Bilder in Notizen: hochladen, ansehen, im Text einfügen — direkt im Editor.
- Claude beschreibt seine Werkzeuge jetzt klarer: weniger Rateversuche, weniger Fehlversuche.

## 2026-08-14
- Echte Ordner: anlegen und Notizen per Menü oder per Ziehen (Drag & Drop) hineinverschieben.
- Jede Notiz zeigt jetzt an, ob sie privat ist oder mit welchem Space sie geteilt ist.
- Neuer "Freigeben"-Knopf pro Notiz — wird eine Freigabe dabei erweitert, fragt sharefyx zur Sicherheit noch einmal Passwort und Code ab.

## 2026-08-13
- Grauer Text (Platzhalter, Meta-Angaben, Versionsband) ist jetzt deutlich besser lesbar — Kontrast auf WCAG AA angehoben.
- Der Schriftzug "sharefyx" oben links samt Versionsnummer (jetzt v2.1) und alle Versionsnummern deiner Dateien sind jetzt weiß statt grau.

## 2026-08-13
- Die angekündigte Umstellung ist jetzt live: fremde Spaces sind nicht mehr automatisch mitlesbar — nur noch, wo eine ausdrückliche Freigabe besteht.
- Eure beiden Spaces bleiben füreinander lesbar wie bisher, per neu eingerichteter Freigabe.
- Neu: gemeinsame Spaces sind jetzt möglich — als erstes Beispiel gibt es "IT-Sekus-Projekt" für gemeinsames Arbeiten.
- hotfixed Rechte für shared space
- hotfixed: Anlegen-Knopf und Bearbeiten fehlten in geteilten Spaces trotz Schreibrecht

## 2026-08-09
- Deine Notizen werden bald **standardmäßig privat**: alles Bestehende und alles Neue ist nach der nächsten Umstellung nur noch für dich sichtbar.
- Was du weiterhin teilen willst, legst du in einem gemeinsamen Space ab oder gibst es einzeln frei — nichts geht verloren, aber ohne dein Zutun sieht ab dann niemand sonst mehr mit.

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

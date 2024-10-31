# Baby Sokoban Progrmm für die Übungen Einführung in CE 

## Vorbereitungen: python, pip und pygame

### allgemeine Tipps 
- Installationen verändern das System. Manchmal müssen sie ein Progrmm oder den ganzen Computer neu starten, damit diese Änderungen wirksam werden. 
- Sie sind nicht allein. Hören sie sich bei ihren Kommilitonen um, wer schon Erfolg hatte und versuchen sie gemeinsam die Installation zu meistern.
- KI Prompts sind für Basisdinge die auf diesem Planeten schon millionenfach gemacht wurden ein guter Startpunkt, z.B.: "wie installiere ich pip auf ubuntu 22.04?"
- Möglicherweise gibt es für Ihr Betriebssystem spezielle Anleitungen die sie auf den Webseiten des Anbieters finden.
- Wenn Sie "irgendwo" im Web suchen, achten sie stets auf aktuelle und vertrauenswürdige Quellen.
- Die Welt der Informatik dreht sich schnell und ihr Computer wird durch seine Nutzung zu einem Individuum für das sie selbst die Verantwortung tragen.
- Versuchen Sie am Beginn Ihrer Reise auf den bewährten und oft gegangenen Wegen zu bleiben und so wenig wie möglich individuell anzupassen. 

### python
Der Programmcode benötigt zur Ausführung den python Interpreter. 
Sie können testen ob python bereits installiert ist, indem sie in einem Terminal das Kommando `python --version` aufrufen.
Wenn python bereits installiert ist, erhalten wird die installierte Version ausgegeben, z.B.: `Python 3.12.7`.

Falls python aber nicht gefunden wird, müssen sie es installieren.
Infos zum Download und Installation von python gibt es auf https://www.python.org/downloads/

### pip
Wenn python installiert ist, wird normalerweise auch der python Paketmanager `pip` mit installiert.
Geben sie zum Testen in einem Terminal `pip --version` ein. 
Wenn pip bereits installiert ist, erhalten wird die installierte Version ausgegeben, z.B.: 
`pip 24.2 from C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2032.0_x64__qbz5n2kfra8p0\Lib\site-packages\pip (python 3.12)`.
Falls pip aber nicht gefunden wird, müssen sie es installieren.
Infos zum Download und Installation von pip gibt es auf https://pip.pypa.io/en/stable/installation/

### pygame
Der Programmcode benutzt das Python Paket pygame. Dieses muss ebenfalls installiert werden.
Das geschieht einmalig durch den Aufruf von `pip install pygame` in einem Terminal.
Weitere Infos gibt es auf https://www.pygame.org/docs/


## Visual Studio Code als Entwicklungsumgebung
Zum Bearbeiten (editieren) der Quelltexte benötigt man ein Editor Programm. Empfehlenswert ist die Benutzung von Visual Studio Code was es für alle relevanten Beriebssystem gibt.
Links:
- Download und Einrichtung (Setup) https://code.visualstudio.com/docs/setup/setup-overview
- Python in Visual Studio Code https://code.visualstudio.com/docs/languages/python
- Erweiterungen (Extensions) https://code.visualstudio.com/docs/editor/extension-marketplace

Für Visual Studio Code gibt es viele Erweiterungen. Installieren sie im Visaul Studio nur den "Code Python language support" von Microsoft (für alle OS). 

## my_sokoban1 Quellcode
Laden sie die .zip Datei herunter und entpacken sie diese in einem neuen, leeren Verzeichnis `my_sokoban1`. Suchen sie dafür einen Ort in ihrem persönlichen Bereich des Dateisystems (home Verzeichnis, Documents, ...) auf den sie volle Zugriffsrechte haben. Bedenken Sie, dass sich im Verlauf des Studiums viele solche Verzeichnisse mit vieln Daten ansammeln werden. Die meisten Studierenden ordnen diese Verzeichnisse nach Semester und/oder Modulname (CE59) in einer Hierarchie von Unterverzeichnissen an. Machen sie sich auch kundig, wie diese Verzeichnisse gesichert werden können (lokales Backup, Clouddienste). Wir erleben gelegentlich Verzweiflung und Panikattacken wenn wieder einmal "der Hund" den Quelltext oder das ganze Laptop "gefressen" hat. Kein Backup, kein Mitleid. Tipp: Die HTW betreibt einen gitlab Server https://gitlab.rz.htw-berlin.de/. Die Benutzung wird noch erklärt und ist hier nur für Fortgeschrittene gedacht.

Sie müssen im Visual Studio Code immer zuerst das Verzeichnis (== Ordner, folder, directory,...) des Projektes (`my_sokoban1`) öffnen, nicht nur die einzelnen Dateien oder ein anderes Verzeichnis.



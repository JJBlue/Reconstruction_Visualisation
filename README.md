# Visualization of Cherry Trees

## Beschreibung

Das Programm dient zur Darstellung 3-Dimensionaler Punktwolken.
<br>

## Installation

### Vorraussetzung

- Python

### Abhängigkeiten

Abhängigkeiten werden automatisch gesucht und gegebenfalls mit einer Bestätigung des Benutzer heruntergeladen und installiert.
Dazu muss das Programm einfach gestartet werden. Siehe Kapitel "**Ausführen**"

Benötigte Abhängigkeit:
- PyQt6
- ConfigParser
- PyGLM
- Numpy
- Pillow
- Open3D
- PyColmap

Für Python 3.11:
	- PyColmap muss manuell installiert werden
	- Open3D muss manuell installiert werden
	- Colmap-Wrapper von Branch "JJBlue" installieren

Für Python 3.9:
	- ```pip install StrEnum```
	- PyColmap für Windows muss manuell installiert werden
    - Colmap-Wrapper von Branch "JJBlue" installieren

Um die benötigten Abhängigkeiten zu installieren, führen sie folgendes Python Befehle aus:

- `pip install PyQt6`
- `pip install configparser`
- `pip install PyGLM`
- `pip install numpy`
- `pip install Pillow`
- `pip install open3d`
- `pip install pycolmap`

<br>

## Ausführen

Um das Programm zu starten führen sie folgenden Befehl aus:

`python src/main/python/main.py -workdir ".\config"`
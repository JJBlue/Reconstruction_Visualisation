# Visualization of Cherry Trees

## Beschreibung

Das Programm dient zur Darstellung von COLMAP Daten.
<br>

## Installation

### Vorraussetzung

- Python 3.9 oder höher

### Abhängigkeiten

Abhängigkeiten werden automatisch gesucht und gegebenfalls mit einer Bestätigung des Benutzer heruntergeladen und installiert.
Dazu muss das Programm einfach gestartet werden. Siehe Kapitel "**Ausführen**"

Benötigte Abhängigkeit:

- COLMAP Wrapper
- ConfigParser
- Numpy
- Open3D
- Pillow
- PyCOLMAP
- PyGLM
- PyOpenGL
- PyQt6
- scikit-learn


Für Python 3.11:
	- PyColmap muss manuell installiert werden
	- Open3D muss manuell installiert werden

Für Python 3.9:
	- ```pip install StrEnum```
	- PyColmap für Windows muss manuell installiert werden

Um die benötigten Abhängigkeiten zu installieren, führen sie folgendes Python Befehle aus:

- `pip install configparser`
- `pip install numpy`
- `pip install open3d`
- `pip install Pillow`
- `pip install pycolmap`
- `pip install PyGLM`
- `pip install PyOpenGL`
- `pip install PyQt6`
- `pip install colmap-wrapper`
- `pip install scikit-learn`

<br>

## Ausführen

Um das Programm zu starten führen sie folgenden Befehl aus:

`python src/main/python/main.py -workdir ".\config"`
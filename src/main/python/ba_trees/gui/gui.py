###############
### Imports ###
###############
import sys

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon

############
### Main ###
############

app = QApplication(sys.argv)

w = QWidget()
w.setGeometry(50, 50, 500, 500)
w.setWindowTitle("Visualisation Software")
w.setWindowIcon(QIcon("icon.png"))

w.show()

sys.exit(app.exec_())
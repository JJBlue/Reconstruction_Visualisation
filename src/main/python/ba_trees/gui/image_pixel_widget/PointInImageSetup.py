from PyQt6 import QtCore, QtWidgets


class Ui_point_in_image_form(object):
    def setupUi(self, point_in_image_form):
        point_in_image_form.setObjectName("point_in_image_form")
        point_in_image_form.resize(940, 708)
        self.verticalLayout = QtWidgets.QVBoxLayout(point_in_image_form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.table = PointInImageTableWidget(point_in_image_form)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setObjectName("table")
        self.verticalLayout.addWidget(self.table)

        self.retranslateUi(point_in_image_form)
        QtCore.QMetaObject.connectSlotsByName(point_in_image_form)

    def retranslateUi(self, point_in_image_form):
        _translate = QtCore.QCoreApplication.translate
        point_in_image_form.setWindowTitle(_translate("point_in_image_form", "Form"))
from ba_trees.gui.image_pixel_widget.PointInImageWidget import PointInImageTableWidget
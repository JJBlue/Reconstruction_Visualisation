from PyQt6 import QtCore, QtWidgets


class Ui_point_in_image_form(object):
    def setupUi(self, point_in_image_form):
        point_in_image_form.setObjectName("point_in_image_form")
        point_in_image_form.resize(940, 687)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(point_in_image_form.sizePolicy().hasHeightForWidth())
        point_in_image_form.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(point_in_image_form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(point_in_image_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter.setObjectName("splitter")
        self.point_information = PointInImagePointInformationWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.point_information.sizePolicy().hasHeightForWidth())
        self.point_information.setSizePolicy(sizePolicy)
        self.point_information.setObjectName("point_information")
        #self.point_information.setColumnCount(0)
        #self.point_information.setRowCount(0)
        self.point_information.horizontalHeader().setVisible(False)
        self.point_information.verticalHeader().setVisible(False)
        self.table = PointInImageTableWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.table.sizePolicy().hasHeightForWidth())
        self.table.setSizePolicy(sizePolicy)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setObjectName("table")
        #self.table.setColumnCount(0)
        #self.table.setRowCount(0)
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(point_in_image_form)
        QtCore.QMetaObject.connectSlotsByName(point_in_image_form)

    def retranslateUi(self, point_in_image_form):
        _translate = QtCore.QCoreApplication.translate
        point_in_image_form.setWindowTitle(_translate("point_in_image_form", "Form"))
from ba_trees.gui.image_pixel_widget.PointInImageWidget import PointInImagePointInformationWidget, PointInImageTableWidget
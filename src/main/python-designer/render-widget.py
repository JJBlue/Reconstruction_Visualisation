# Form implementation generated from reading ui file 'render-widget.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_root(object):
    def setupUi(self, root):
        root.setObjectName("root")
        root.resize(952, 592)
        self.verticalLayout = QtWidgets.QVBoxLayout(root)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(root)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter_2 = QtWidgets.QSplitter(self.widget)
        self.splitter_2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter.setObjectName("splitter")
        self.opengl_widget = RenderWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.opengl_widget.sizePolicy().hasHeightForWidth())
        self.opengl_widget.setSizePolicy(sizePolicy)
        self.opengl_widget.setObjectName("opengl_widget")
        self.widget_2 = QtWidgets.QWidget(self.splitter)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())
        self.tabWidget_2.setSizePolicy(sizePolicy)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget_2.addTab(self.tab_4, "")
        self.verticalLayout_4.addWidget(self.tabWidget_2)
        self.widget_3 = QtWidgets.QWidget(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.toolBox = QtWidgets.QToolBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 173, 473))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page.sizePolicy().hasHeightForWidth())
        self.page.setSizePolicy(sizePolicy)
        self.page.setObjectName("page")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.checkBox = QtWidgets.QCheckBox(self.page)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_6.addWidget(self.checkBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_6.addItem(spacerItem)
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 169, 473))
        self.page_2.setObjectName("page_2")
        self.formLayout = QtWidgets.QFormLayout(self.page_2)
        self.formLayout.setObjectName("formLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 454, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.formLayout.setItem(1, QtWidgets.QFormLayout.ItemRole.LabelRole, spacerItem1)
        self.label = QtWidgets.QLabel(self.page_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.setting_point_cloud = QtWidgets.QDoubleSpinBox(self.page_2)
        self.setting_point_cloud.setSingleStep(0.1)
        self.setting_point_cloud.setObjectName("setting_point_cloud")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.setting_point_cloud)
        self.toolBox.addItem(self.page_2, "")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 169, 473))
        self.page_3.setObjectName("page_3")
        self.formLayout_2 = QtWidgets.QFormLayout(self.page_3)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_2 = QtWidgets.QLabel(self.page_3)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.setting_camera_speed = QtWidgets.QDoubleSpinBox(self.page_3)
        self.setting_camera_speed.setMaximum(10.0)
        self.setting_camera_speed.setSingleStep(0.01)
        self.setting_camera_speed.setObjectName("setting_camera_speed")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.setting_camera_speed)
        spacerItem2 = QtWidgets.QSpacerItem(20, 374, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.formLayout_2.setItem(3, QtWidgets.QFormLayout.ItemRole.LabelRole, spacerItem2)
        self.label_3 = QtWidgets.QLabel(self.page_3)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.checkBox_2 = QtWidgets.QCheckBox(self.page_3)
        self.checkBox_2.setText("")
        self.checkBox_2.setObjectName("checkBox_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.checkBox_2)
        self.label_4 = QtWidgets.QLabel(self.page_3)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.page_3)
        self.doubleSpinBox.setMaximum(360.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.doubleSpinBox)
        self.toolBox.addItem(self.page_3, "")
        self.verticalLayout_5.addWidget(self.toolBox)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.toolBox_2 = QtWidgets.QToolBox(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox_2.sizePolicy().hasHeightForWidth())
        self.toolBox_2.setSizePolicy(sizePolicy)
        self.toolBox_2.setObjectName("toolBox_2")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 169, 533))
        self.page_4.setObjectName("page_4")
        self.formLayout_3 = QtWidgets.QFormLayout(self.page_4)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_5 = QtWidgets.QLabel(self.page_4)
        self.label_5.setObjectName("label_5")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5)
        self.label_8 = QtWidgets.QLabel(self.page_4)
        self.label_8.setObjectName("label_8")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_8)
        self.label_6 = QtWidgets.QLabel(self.page_4)
        self.label_6.setObjectName("label_6")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_6)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.formLayout_3.setItem(8, QtWidgets.QFormLayout.ItemRole.LabelRole, spacerItem3)
        self.label_7 = QtWidgets.QLabel(self.page_4)
        self.label_7.setObjectName("label_7")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_7)
        self.label_9 = QtWidgets.QLabel(self.page_4)
        self.label_9.setObjectName("label_9")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_9)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.page_4)
        self.doubleSpinBox_2.setMinimum(-16777215.0)
        self.doubleSpinBox_2.setMaximum(16777215.0)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.doubleSpinBox_2)
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(self.page_4)
        self.doubleSpinBox_3.setObjectName("doubleSpinBox_3")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.doubleSpinBox_3)
        self.doubleSpinBox_4 = QtWidgets.QDoubleSpinBox(self.page_4)
        self.doubleSpinBox_4.setObjectName("doubleSpinBox_4")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.doubleSpinBox_4)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.formLayout_3.setItem(0, QtWidgets.QFormLayout.ItemRole.FieldRole, spacerItem4)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.formLayout_3.setItem(4, QtWidgets.QFormLayout.ItemRole.FieldRole, spacerItem5)
        self.label_10 = QtWidgets.QLabel(self.page_4)
        self.label_10.setObjectName("label_10")
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_10)
        self.label_11 = QtWidgets.QLabel(self.page_4)
        self.label_11.setObjectName("label_11")
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_11)
        self.label_12 = QtWidgets.QLabel(self.page_4)
        self.label_12.setObjectName("label_12")
        self.formLayout_3.setWidget(7, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_12)
        self.doubleSpinBox_5 = QtWidgets.QDoubleSpinBox(self.page_4)
        self.doubleSpinBox_5.setMaximum(360.0)
        self.doubleSpinBox_5.setObjectName("doubleSpinBox_5")
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.doubleSpinBox_5)
        self.doubleSpinBox_6 = QtWidgets.QDoubleSpinBox(self.page_4)
        self.doubleSpinBox_6.setMaximum(360.0)
        self.doubleSpinBox_6.setObjectName("doubleSpinBox_6")
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.ItemRole.FieldRole, self.doubleSpinBox_6)
        self.doubleSpinBox_7 = QtWidgets.QDoubleSpinBox(self.page_4)
        self.doubleSpinBox_7.setMaximum(360.0)
        self.doubleSpinBox_7.setObjectName("doubleSpinBox_7")
        self.formLayout_3.setWidget(7, QtWidgets.QFormLayout.ItemRole.FieldRole, self.doubleSpinBox_7)
        self.toolBox_2.addItem(self.page_4, "")
        self.verticalLayout_7.addWidget(self.toolBox_2)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.verticalLayout_2.addWidget(self.splitter_2)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(root)
        self.tabWidget_2.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(1)
        self.toolBox.setCurrentIndex(2)
        self.toolBox_2.setCurrentIndex(0)
        self.checkBox.toggled['bool'].connect(self.opengl_widget.show_coordinate_system)
        self.opengl_widget.showCoordinateSystemChanged['bool'].connect(self.checkBox.setChecked)
        self.opengl_widget.pointSizeChanged['double'].connect(self.setting_point_cloud.setValue)
        self.setting_point_cloud.valueChanged['double'].connect(self.opengl_widget.setPointSize)
        self.setting_camera_speed.valueChanged['double'].connect(self.opengl_widget.setCameraSpeed)
        self.opengl_widget.cameraSpeedChanged['double'].connect(self.setting_camera_speed.setValue)
        self.checkBox_2.toggled['bool'].connect(self.opengl_widget.enableMovementChanged)
        self.opengl_widget.cameraEnableMovementChanged['bool'].connect(self.checkBox_2.setChecked)
        self.opengl_widget.cameraFOVChanged['double'].connect(self.doubleSpinBox.setValue)
        self.doubleSpinBox.valueChanged['double'].connect(self.opengl_widget.setCameraFOV)
        QtCore.QMetaObject.connectSlotsByName(root)

    def retranslateUi(self, root):
        _translate = QtCore.QCoreApplication.translate
        root.setWindowTitle(_translate("root", "Form"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), _translate("root", "Tab 1"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("root", "Tab 2"))
        self.checkBox.setText(_translate("root", "Show Coordinate System"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("root", "Default System"))
        self.label.setText(_translate("root", "Point Size:"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("root", "Point Cloud"))
        self.label_2.setText(_translate("root", "Speed:"))
        self.label_3.setText(_translate("root", "Fixed Position:"))
        self.label_4.setText(_translate("root", "FOV:"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("root", "Camera"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("root", "Render Settings"))
        self.label_5.setText(_translate("root", "Position"))
        self.label_8.setText(_translate("root", "y:"))
        self.label_6.setText(_translate("root", "Rotation"))
        self.label_7.setText(_translate("root", "x:"))
        self.label_9.setText(_translate("root", "z:"))
        self.label_10.setText(_translate("root", "pitch:"))
        self.label_11.setText(_translate("root", "yaw:"))
        self.label_12.setText(_translate("root", "roll:"))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_4), _translate("root", "Model Matrix"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("root", "Models"))
from ba_trees.gui.project_widget.RenderWidget import RenderWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    root = QtWidgets.QWidget()
    ui = Ui_root()
    ui.setupUi(root)
    root.show()
    sys.exit(app.exec())

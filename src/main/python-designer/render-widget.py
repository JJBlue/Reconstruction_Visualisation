# Form implementation generated from reading ui file 'render-widget.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
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
        self.page.setGeometry(QtCore.QRect(0, 0, 173, 503))
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
        self.page_2.setGeometry(QtCore.QRect(0, 0, 157, 503))
        self.page_2.setObjectName("page_2")
        self.formLayout = QtWidgets.QFormLayout(self.page_2)
        self.formLayout.setObjectName("formLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 454, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.formLayout.setItem(1, QtWidgets.QFormLayout.ItemRole.LabelRole, spacerItem1)
        self.label = QtWidgets.QLabel(self.page_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.setting_point_cloud = QtWidgets.QSpinBox(self.page_2)
        self.setting_point_cloud.setObjectName("setting_point_cloud")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.setting_point_cloud)
        self.toolBox.addItem(self.page_2, "")
        self.verticalLayout_5.addWidget(self.toolBox)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.verticalLayout_2.addWidget(self.splitter_2)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(root)
        self.tabWidget_2.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(1)
        self.setting_point_cloud.valueChanged['int'].connect(self.opengl_widget.change_point_cloud_point_size) # type: ignore
        self.checkBox.toggled['bool'].connect(self.opengl_widget.show_coordinate_system) # type: ignore
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("root", "Render Settings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("root", "Tab 2"))
from ba_trees.gui.project_widget.RenderWidget import RenderWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    root = QtWidgets.QWidget()
    ui = Ui_root()
    ui.setupUi(root)
    root.show()
    sys.exit(app.exec())
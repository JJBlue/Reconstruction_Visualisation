# Form implementation generated from reading ui file 'project-widget.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_root(object):
    def setupUi(self, root):
        root.setObjectName("root")
        root.resize(952, 666)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
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
        self.tab_3 = SelectionPointsInImageWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_3.sizePolicy().hasHeightForWidth())
        self.tab_3.setSizePolicy(sizePolicy)
        self.tab_3.setObjectName("tab_3")
        self.tabWidget_2.addTab(self.tab_3, "")
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
        self.page.setGeometry(QtCore.QRect(0, 0, 173, 84))
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
        self.page_2.setGeometry(QtCore.QRect(0, 0, 126, 46))
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
        self.page_3.setGeometry(QtCore.QRect(0, 0, 155, 96))
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
        self.splitter_3 = QtWidgets.QSplitter(self.tab_2)
        self.splitter_3.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter_3.setObjectName("splitter_3")
        self.tree_view_models = ModelsTreeView(self.splitter_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_view_models.sizePolicy().hasHeightForWidth())
        self.tree_view_models.setSizePolicy(sizePolicy)
        self.tree_view_models.setObjectName("tree_view_models")
        self.tree_view_models.header().setVisible(False)
        self.model_settings = ModelToolBox(self.splitter_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.model_settings.sizePolicy().hasHeightForWidth())
        self.model_settings.setSizePolicy(sizePolicy)
        self.model_settings.setObjectName("model_settings")
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setGeometry(QtCore.QRect(0, 0, 256, 410))
        self.page_6.setObjectName("page_6")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.page_6)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.root_default_settings_tab = ModelSettingDefault(self.page_6)
        self.root_default_settings_tab.setObjectName("root_default_settings_tab")
        self.formLayout_4 = QtWidgets.QFormLayout(self.root_default_settings_tab)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_15 = QtWidgets.QLabel(self.root_default_settings_tab)
        self.label_15.setObjectName("label_15")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_15)
        self.checkBox_3 = QtWidgets.QCheckBox(self.root_default_settings_tab)
        self.checkBox_3.setText("")
        self.checkBox_3.setObjectName("checkBox_3")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.checkBox_3)
        self.verticalLayout_8.addWidget(self.root_default_settings_tab)
        self.model_settings.addItem(self.page_6, "")
        self.verticalLayout_7.addWidget(self.splitter_3)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.verticalLayout_2.addWidget(self.splitter_2)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(root)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(1)
        self.toolBox.setCurrentIndex(2)
        self.model_settings.setCurrentIndex(0)
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
        self.opengl_widget.renderStructureChanged['PyQt_PyObject'].connect(self.tree_view_models.updateRoot)
        self.tree_view_models.selectionChangedRenderStructure['PyQt_PyObject'].connect(self.model_settings.selectCurrentModel)
        self.checkBox_3.toggled['bool'].connect(self.root_default_settings_tab.setModelVisible)
        self.root_default_settings_tab.modelVisibleChanged['bool'].connect(self.checkBox_3.setChecked)
        self.model_settings.repaintWorld.connect(self.opengl_widget.repaintInBackground)
        QtCore.QMetaObject.connectSlotsByName(root)

    def retranslateUi(self, root):
        _translate = QtCore.QCoreApplication.translate
        root.setWindowTitle(_translate("root", "Form"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), _translate("root", "Selection"))
        self.checkBox.setText(_translate("root", "Show Coordinate System"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("root", "Default System"))
        self.label.setText(_translate("root", "Point Size:"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("root", "Point Cloud"))
        self.label_2.setText(_translate("root", "Speed:"))
        self.label_3.setText(_translate("root", "Fixed Position:"))
        self.label_4.setText(_translate("root", "FOV:"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("root", "Camera"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("root", "Render Settings"))
        self.label_15.setText(_translate("root", "Visible:"))
        self.model_settings.setItemText(self.model_settings.indexOf(self.page_6), _translate("root", "Settings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("root", "Models"))
from ba_trees.gui.project_widget.ModelsTreeView import ModelsTreeView
from ba_trees.gui.project_widget.RenderWidget import RenderWidget
from ba_trees.gui.project_widget.model_settings.ModelSettingDefault import ModelSettingDefault
from ba_trees.gui.project_widget.model_settings.ModelToolBox import ModelToolBox
from ba_trees.gui.selection_widget.SelectionPointsInImageWidget import SelectionPointsInImageWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    root = QtWidgets.QWidget()
    ui = Ui_root()
    ui.setupUi(root)
    root.show()
    sys.exit(app.exec())

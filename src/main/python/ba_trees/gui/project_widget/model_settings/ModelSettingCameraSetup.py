from PyQt6 import QtCore, QtWidgets


class Ui_settings_tab(object):
    def setupUi(self, settings_tab):
        settings_tab.setObjectName("settings_tab")
        settings_tab.resize(840, 587)
        self.verticalLayout = QtWidgets.QVBoxLayout(settings_tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.root_setting_tab = ModelSettingCamera(settings_tab)
        self.root_setting_tab.setObjectName("root_setting_tab")
        self.formLayout = QtWidgets.QFormLayout(self.root_setting_tab)
        self.formLayout.setContentsMargins(0, 0, 0, -1)
        self.formLayout.setObjectName("formLayout")
        self.label_18 = QtWidgets.QLabel(self.root_setting_tab)
        self.label_18.setObjectName("label_18")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_18)
        self.doubleSpinBox_11 = QtWidgets.QDoubleSpinBox(self.root_setting_tab)
        self.doubleSpinBox_11.setMaximum(100.0)
        self.doubleSpinBox_11.setSingleStep(0.1)
        self.doubleSpinBox_11.setObjectName("doubleSpinBox_11")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.doubleSpinBox_11)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.formLayout.setItem(1, QtWidgets.QFormLayout.ItemRole.LabelRole, spacerItem)
        self.verticalLayout.addWidget(self.root_setting_tab)

        self.retranslateUi(settings_tab)
        self.doubleSpinBox_11.valueChanged['double'].connect(self.root_setting_tab.setModelScale)
        self.root_setting_tab.modelScaleChanged['double'].connect(self.doubleSpinBox_11.setValue)
        QtCore.QMetaObject.connectSlotsByName(settings_tab)

    def retranslateUi(self, settings_tab):
        _translate = QtCore.QCoreApplication.translate
        settings_tab.setWindowTitle(_translate("settings_tab", "Form"))
        self.label_18.setText(_translate("settings_tab", "Scale:"))
from ba_trees.gui.project_widget.model_settings.ModelSettingCamera import ModelSettingCamera
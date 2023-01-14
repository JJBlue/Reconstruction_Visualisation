# Form implementation generated from reading ui file 'main-window.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_window(object):
    def setupUi(self, window):
        window.setObjectName("window")
        window.resize(1137, 704)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(window.sizePolicy().hasHeightForWidth())
        window.setSizePolicy(sizePolicy)
        window.setAutoFillBackground(False)
        window.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        window.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(window)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")
        self.projects = ProjectTreeView(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.projects.sizePolicy().hasHeightForWidth())
        self.projects.setSizePolicy(sizePolicy)
        self.projects.setHeaderHidden(True)
        self.projects.setObjectName("projects")
        self.tabs = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabs.sizePolicy().hasHeightForWidth())
        self.tabs.setSizePolicy(sizePolicy)
        self.tabs.setTabsClosable(True)
        self.tabs.setObjectName("tabs")
        self.verticalLayout.addWidget(self.splitter)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.widget_2 = StatusWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMinimumSize(QtCore.QSize(200, 0))
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout_2.addWidget(self.widget_2)
        self.verticalLayout.addWidget(self.widget)
        window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1137, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuWorkspace = QtWidgets.QMenu(self.menuFile)
        self.menuWorkspace.setObjectName("menuWorkspace")
        self.menuHilfe = QtWidgets.QMenu(self.menubar)
        self.menuHilfe.setObjectName("menuHilfe")
        window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(window)
        self.actionOpen.setObjectName("actionOpen")
        self.actionInfo = QtGui.QAction(window)
        self.actionInfo.setObjectName("actionInfo")
        self.open_workspace = QtGui.QAction(window)
        self.open_workspace.setObjectName("open_workspace")
        self.close_workspace = QtGui.QAction(window)
        self.close_workspace.setObjectName("close_workspace")
        self.import_reconstruction = QtGui.QAction(window)
        self.import_reconstruction.setObjectName("import_reconstruction")
        self.create_workspace = QtGui.QAction(window)
        self.create_workspace.setObjectName("create_workspace")
        self.menuWorkspace.addAction(self.create_workspace)
        self.menuWorkspace.addAction(self.open_workspace)
        self.menuWorkspace.addAction(self.close_workspace)
        self.menuFile.addAction(self.menuWorkspace.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.import_reconstruction)
        self.menuHilfe.addAction(self.actionInfo)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHilfe.menuAction())

        self.retranslateUi(window)
        self.tabs.setCurrentIndex(-1)
        self.import_reconstruction.triggered.connect(window.importReconstruction)
        self.close_workspace.triggered.connect(window.closeWorkspace)
        self.open_workspace.triggered.connect(window.openWorkspace)
        self.create_workspace.triggered.connect(window.createWorkspace)
        self.projects.doubleClicked['QModelIndex'].connect(self.projects.doubleClickedEvent)
        self.tabs.tabCloseRequested['int'].connect(window.tabClose)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "Visualization"))
        self.label.setText(_translate("window", "Status ..."))
        self.menuFile.setTitle(_translate("window", "File"))
        self.menuWorkspace.setTitle(_translate("window", "Workspace"))
        self.menuHilfe.setTitle(_translate("window", "Hilfe"))
        self.actionOpen.setText(_translate("window", "Open"))
        self.actionInfo.setText(_translate("window", "Info"))
        self.open_workspace.setText(_translate("window", "Open"))
        self.close_workspace.setText(_translate("window", "Close"))
        self.import_reconstruction.setText(_translate("window", "Import"))
        self.create_workspace.setText(_translate("window", "Create"))
from ba_trees.gui.main_window.ProjectTreeView import ProjectTreeView
from ba_trees.gui.status.StatusWidget import StatusWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_window()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())

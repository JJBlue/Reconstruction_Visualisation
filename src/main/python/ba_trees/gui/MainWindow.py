from pathlib import Path
from typing import List

from PyQt6.QtWidgets import QMainWindow, QFileDialog

from ba_trees.config.ConfigDirectories import ConfigDirectories
from ba_trees.gui.MainWindowSetup import Ui_window
from ba_trees.workspace import Workspace, Workspaces, WorkspaceJSONFile


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        ui = Ui_window()
        ui.setupUi(self)
    
    def createWorkspace(self):
        dialog: QFileDialog = QFileDialog()
        dialog.setDirectory(str(ConfigDirectories.getConfigDirectories().getWorkspaceFolder()))
        
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialog.setNameFilter(self.tr("Workspace (*.json)")) # Name1 (*.ending1 *.ending2);;Name2 (*.ending1)
        
        filenames: List[str] = None
        
        if dialog.exec():
            filenames = dialog.selectedFiles()
            
            workspace_file = Path(filenames[0])
            workspace: Workspace = self.openWorkspacePath(workspace_file)
            
            WorkspaceJSONFile.saveWorkspace(workspace, workspace_file)
    
    def openWorkspace(self):
        dialog: QFileDialog = QFileDialog()
        dialog.setDirectory(str(ConfigDirectories.getConfigDirectories().getWorkspaceFolder()))
        
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter(self.tr("Workspace (*.json)")) # Name1 (*.ending1 *.ending2);;Name2 (*.ending1)
        
        filenames: List[str] = None
        
        if dialog.exec():
            filenames = dialog.selectedFiles()
            
            workspace_file = Path(filenames[0])
            self.openWorkspacePath(workspace_file)
    
    def openWorkspacePath(self, file: Path) -> Workspace:
        workspace: Workspace =  WorkspaceJSONFile.readWorkspace(file)
        Workspaces.setWorkspace(workspace)
        
        # TODO
        
        return workspace
    
    def closeWorkspace(self):
        Workspaces.setWorkspace(None)
        
        # TODO
    
    def importReconstruction(self):
        # TODO
        print("importReconstruction")
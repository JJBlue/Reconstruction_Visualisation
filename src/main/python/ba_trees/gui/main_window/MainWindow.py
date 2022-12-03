from pathlib import Path
from typing import List

from PyQt6.QtWidgets import QMainWindow, QFileDialog

from ba_trees.config.ConfigDirectories import ConfigDirectories
from ba_trees.gui.main_window.MainWindowSetup import Ui_window
from ba_trees.workspace import Workspace, Workspaces
from ba_trees.workspace.colmap.ColmapProject import ColmapProject


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_window()
        self.ui.setupUi(self)
        
        # Open Last Session
        workspace: Workspace = Workspaces.reopenLastSession()
        self.updateWorkspaceGui(workspace)
    
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
            workspace.save()
    
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
        workspace: Workspace = Workspaces.openWorkspace(file)
        self.updateWorkspaceGui(workspace)
        return workspace
    
    def updateWorkspaceGui(self, workspace: Workspace):
        self.ui.projects.updateWorkspaceGui(workspace)
    
    def closeWorkspace(self):
        Workspaces.setWorkspace(None)
        self.updateWorkspaceGui(None)
    
    def importReconstruction(self):
        workspace: Workspace = Workspaces.getWorkspace()
        
        if workspace == None:
            print("No Workpsace opened")
            return
        
        dialog: QFileDialog = QFileDialog()
        dialog.setDirectory(str(ConfigDirectories.getConfigDirectories().getWorkspaceFolder()))
        
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        
        filenames: List[str] = None
        
        if dialog.exec():
            filenames = dialog.selectedFiles()
            
            project_folder = Path(filenames[0])
            workspace.addProject(ColmapProject(project_folder))
            workspace.save()
            
            self.updateWorkspaceGui(workspace) # TODO not build all again
    
    def tabClose(self, index: int):
        self.ui.tabs.removeTab(index)
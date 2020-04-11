from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import maya.cmds as cmds
from ctypes import windll, Structure, c_long, byref
from PySide2.QtCore import *
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import os
from datetime import datetime
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.mel as mm

WIDTH, HEIGHT = 770, 350
SET = 0
BGCOLOR = 'rgb(43,43,43)'
PATH = "D:\\maya\\Arnold_Test\\cache\\alembic\\"

print PATH

class MainWindow(MayaQWidgetDockableMixin, QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.resize(WIDTH, HEIGHT)
        self.setWindowTitle("Fast Alembic Importer" + "")

        # self.move(pos[0] - 5, pos[1] - 2)

        self.setWindowFlags(Qt.Tool)

        self.fileList = QTreeWidget()
        self.fileList.setHeaderLabels(['File Name', 'Modified'])
        self.fileList.setRootIsDecorated(False)
        self.fileList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.fileList.header().resizeSection(0, 600)
        self.fileList.header().resizeSection(1, 50)
        self.fileList.setSortingEnabled(True)
        self.fileList.itemSelectionChanged.connect(self.onItemClicked)

        self.getAlembic()

        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Start typing an alembic file name!")
        self.searchBar.textChanged.connect(self.searchFunction)

        self.importAlembic = QPushButton("Import selected")
        importIcon = QPixmap(":/extendSurface.png")
        self.importAlembic.setIcon(QIcon(importIcon))
        self.importAlembic.clicked.connect(self.importAlembicFile)
        self.fileList.itemDoubleClicked.connect(self.importAlembicFile)
        self.importAlembic.setEnabled(False)

        self.writeAlembic = QPushButton("Export selection")
        exportIcon = QPixmap(":/greasePencilSoftPencil.png")
        self.writeAlembic.setIcon(QIcon(exportIcon))
        self.writeAlembic.clicked.connect(self.exportAlembicFile)

        self.foundItemLabel = QLabel("Found items: " + str(self.fileList.topLevelItemCount()))

        self.layout.addWidget(self.searchBar, 1, 0, 1, 0)
        self.layout.addWidget(self.fileList, 2, 0, 1, 0)
        self.layout.addWidget(self.importAlembic, 3, 1)
        self.layout.addWidget(self.writeAlembic, 3, 0)
        self.layout.addWidget(self.foundItemLabel, 4, 0)

        self.setStyleSheet(
            "QTreeWidget {background: 'silver'; color: 'black';  font-size: 10pt; } QTreeView::item:hover{background-color:grey; padding: 5px;}")

    def getListOfFiles(self, dirName):
        # create a list of file and sub directories
        # names in the given directory
        listOfFile = os.listdir(dirName)
        allFiles = list()
        # Iterate over all the entries
        for entry in listOfFile:
            # Create full path
            fullPath = os.path.join(dirName, entry)
            # If entry is a directory then get the list of files in this directory
            if os.path.isdir(fullPath):
                allFiles = allFiles + self.getListOfFiles(fullPath)
            else:
                allFiles.append(fullPath)

        return allFiles

    def getAlembic(self):
        self.fileList.clear()
        listOfFile = os.listdir(PATH)
        allFiles = list()

        listOfFiles = self.getListOfFiles(PATH)

        # Print the files
        for elem in listOfFiles:
            if elem.endswith(".abc"):
                fajl = str(elem)
                fajl = elem.split('\\')
                s = QTreeWidgetItem()
                s.setText(0, fajl[-1].split(".abc")[0])
                s.setIcon(0, QIcon(':/Foamy.png'))

                s.setText(1, str(datetime.fromtimestamp(os.stat(elem)[-2])))
                self.fileList.addTopLevelItem(s)


    def exportAlembicFile(self):
        print "Alembic importalas!"
        mm.eval(
            'doAlembicExportArgList 6 {"0","2","1220","1384","1","0","-0.2","0.2","0","0","","","0","0","0","0","1","0","1","0","","","","","0","0","0","2","1"};')

        self.getAlembic()

    def importAlembicFile(self):
        
        for i in self.fileList.selectedItems():
            command = 'AbcImport -mode import "' + PATH.replace('\\', '/')+ i.text(0) + '.abc";'
            mm.eval(command)

            print i.text(0) + " is imported!"
        self.importAlembic.setEnabled(True)

    def searchFunction(self):
        # print self.searchBar.text()
        self.fileList.clear()
        searchedObj = self.searchBar.text()

        listOfFile = os.listdir(PATH)
        allFiles = list()

        listOfFiles = self.getListOfFiles(PATH)

        # Print the files
        for elem in listOfFiles:
            if elem.endswith(".abc"):
                if searchedObj in elem:
                    fajl = str(elem)
                    fajl = elem.split('\\')
                    s = QTreeWidgetItem()
                    s.setText(0, fajl[-1].split(".abc")[0])
                    s.setIcon(0, QIcon(':/Foamy.png'))

                    s.setText(1, str(datetime.fromtimestamp(os.stat(elem)[-2])))
                    self.fileList.addTopLevelItem(s)

        self.foundItemLabel.setText("Found items: " + str(self.fileList.topLevelItemCount()))

    def onItemClicked(self):
        if True:
            try:
                index = self.fileList.selectedIndexes()[0]

                item = self.fileList.itemFromIndex(index).text(0)
                print item
                self.importAlembic.setEnabled(True)
            except:
                self.importAlembic.setEnabled(False)

    def run(self):
        self.show(dockable = True)


a = MainWindow()
a.run()

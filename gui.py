import sys, os
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog
from PyQt5.QtCore import QSize

import rar

FILEDIALOGFILTER = 'CBR (*.cbr); CBZ (*.cbz);All files (*)'
FILEDIALOGDIRECTORY = ''


class ComicsFile:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename, self.fileextension = os.path.splitext(filepath)
        if self.fileextension == '.cbr':
            pass



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.initUi()
        self.setTitle('')

    def initUi(self):
        self.createActions()
        self.createMenus()
        self.show()

    def createActions(self):
        self.actOpen = QAction('&Open', self, shortcut='Ctrl+O',
                               statusTip='Open file', triggered=self.onFileOpen)

    def createMenus(self):
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&File')
        self.fileMenu.addAction(self.actOpen)

    def onFileOpen(self):
        """Open OpenFileDialog"""
        # OpenFile dialog
        fname, filter = QFileDialog.getOpenFileName(self, 'Open', FILEDIALOGDIRECTORY, FILEDIALOGFILTER)
        if fname == '':
            return

        if os.path.isfile(fname):
            self.setTitle(fname)

    def sizeHint(self):
        return QSize(800, 600)

    def setTitle(self, filename):
        """Handle title change updon modification of the scene"""
        self.setWindowTitle(filename)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec_())

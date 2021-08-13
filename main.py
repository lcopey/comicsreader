from PyQt5.QtWidgets import QApplication
import sys
from gui import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # screen = app.screens()[0]
    # dpi = screen.physicalDotsPerInch()
    # print(dpi)
    # dpi 267.54
    # classic dpi 70.00351648351648

    app.setStyle('Fusion')
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec_())

from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5.QtGui import QImage
from EditWidgets import LineEditView, LineEditScene


class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.initUI()
    img = QImage("/home/brown0730s/workspace/LineAnnotation/test/test.jpg")
    self._scene.setBackgroundImage(img)

  def initUI(self):
    self._scene = LineEditScene()
    self._view = LineEditView(self._scene)

    self.setCentralWidget(self._view)

    #self._edit_line_field = LineEditField(self)

    add_line_act = QAction("Add line mode", self)
    add_line_act.setShortcut("Ctrl+R")
    add_line_act.triggered.connect(self.startAddLineMode)

    menubar = self.menuBar()
    #file_menu = menubar.addMenu('&File')

    tool_menu = menubar.addMenu("&Tool")
    tool_menu.addAction(add_line_act)

    self.setWindowTitle("LineAnnotation")
    self.show()

  def startAddLineMode(self):
    self._scene.requestAddLineMode()

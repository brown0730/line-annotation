import time
from enum import Enum
from PyQt5.QtCore import Qt, QRectF, QLineF
from PyQt5.QtWidgets import (QWidget, QSizePolicy, QGraphicsScene,
                             QGraphicsView, QGraphicsPixmapItem)
from PyQt5.QtGui import QImage, QPainter, QPixmap, QPen, QColor, QCursor
#from PyQt5.QtGui import QPainter


class LineEditMode(Enum):
  kSelectMode = 0
  kAddLineMode = 1


class LineEditScene(QGraphicsScene):
  def __init__(self, parent=None):
    self._edit_mode = LineEditMode.kSelectMode
    super().__init__(QRectF(0, 0, 100, 100), parent)
    self._bg_pixmap = None
    self._lines = []
    self._anker_pt = None
    self._line_pen = QPen(QColor(255, 0, 0))

  def _enter_add_line_mode(self):
    for view in self.views():
      view.setCursor(QCursor(Qt.CrossCursor))

  def _leave_add_line_mode(self):
    for view in self.views():
      view.setCursor(QCursor(Qt.ArrowCursor))
    self._anker_pt = None
    print(self._lines)

  def setBackgroundImage(self, q_img):
    pixmap = QPixmap.fromImage(
        QImage.convertToFormat(q_img, QImage.Format_ARGB32))
    self.setSceneRect(QRectF(0, 0, pixmap.width(), pixmap.height()))
    if self._bg_pixmap is None:
      self._bg_pixmap = self.addPixmap(pixmap)
      self._bg_pixmap.setZValue(0)
    else:
      self._bg_pixmap.setPixmap(pixmap)

  def requestAddLineMode(self):
    if self._edit_mode == LineEditMode.kSelectMode:
      self._enter_add_line_mode()
      self._edit_mode = LineEditMode.kAddLineMode
      return True
    return False

  def requestSelectMode(self):
    pass

  def mousePressEvent(self, event):
    if self._edit_mode == LineEditMode.kAddLineMode:
      pt = event.scenePos()
      rect_item = self.addRect(
          QRectF(pt.x() - 5, pt.y() - 5, 10, 10), self._line_pen)
      if self._anker_pt is not None:
        line_item = self.addLine(
            QLineF(self._anker_pt[0], self._anker_pt[1], pt.x(), pt.y()),
            self._line_pen)
        self._lines[-1]["point"].append([pt.x(), pt.y()])
      else:
        self._lines.append({"point": [[pt.x(), pt.y()]]})
      self._anker_pt = [pt.x(), pt.y()]
      print(self._lines[-1]["point"])

  def mouseDoubleClickEvent(self, event):
    if self._edit_mode == LineEditMode.kAddLineMode:
      self._leave_add_line_mode()
      self._edit_mode = LineEditMode.kSelectMode


class LineEditView(QGraphicsView):
  def __init__(self, scene, parent=None):
    super().__init__(scene, parent)

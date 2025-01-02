import io
import sys
import math

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPainter, QColor, QPolygonF, QPen
from PyQt6.QtWidgets import QApplication, QMainWindow, QColorDialog

template = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>500</width>
    <height>500</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>500</width>
    <height>500</height>
   </size>
  </property>
  <property name="maximumSize">
   <size>
    <width>500</width>
    <height>500</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>Квадрат-объектив — 2</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>10</y>
      <width>55</width>
      <height>16</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>K = </string>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>110</x>
      <y>10</y>
      <width>55</width>
      <height>16</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>N = </string>
    </property>
   </widget>
   <widget class="QPushButton" name="draw">
    <property name="geometry">
     <rect>
      <x>350</x>
      <y>0</y>
      <width>101</width>
      <height>41</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Рисовать</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="k">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>10</y>
      <width>51</width>
      <height>21</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
   </widget>
   <widget class="QLineEdit" name="n">
    <property name="geometry">
     <rect>
      <x>150</x>
      <y>10</y>
      <width>41</width>
      <height>22</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string/>
    </property>
   </widget>
   <widget class="QLabel" name="label_3">
    <property name="geometry">
     <rect>
      <x>200</x>
      <y>0</y>
      <width>51</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>M = </string>
    </property>
   </widget>
   <widget class="QLineEdit" name="m">
    <property name="geometry">
     <rect>
      <x>240</x>
      <y>10</y>
      <width>51</width>
      <height>22</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
   </widget>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
'''


class NoTSquare(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)  # Загружаем дизайн
        self.color = QColor(0, 0, 0)
        self.start_point = [350, 250]
        self.draw.clicked.connect(self.color_choose)

    def color_choose(self):
        dialog = QColorDialog()
        color = dialog.getColor()
        if color.isValid():
            self.color = color
            self.update()

    def paintEvent(self, event):
        if self.m.text() and self.k.text() and self.n.text():
            qp = QPainter(self)  # Передаем self для инициализации QPainter
            qp.begin(self)
            self.draw_squares(qp)
            qp.end()

    def draw_squares(self, qp):
        # Вычисляем центр и радиус
        center = QPointF(250, 250)
        radius = 100
        num_points = int(self.n.text())  # Число точек
        points = []

        for i in range(num_points):
            angle = 2 * math.pi * i / num_points  # Угол в радианах
            x = center.x() + radius * math.cos(angle)
            y = center.y() + radius * math.sin(angle)
            if i == 0:
                self.start_point = [x, y]
            points.append(QPointF(x, y))  # Используем QPointF для удобства
        polygon = QPolygonF(points)
        qp.drawPolygon(polygon)

        coeff = float(self.k.text())
        # Изменяем цвет линии
        pen = QPen(self.color)
        qp.setPen(pen)

        for i in range(int(self.m.text())):
            polygon = QPolygonF(points)
            qp.drawPolygon(polygon)

            if i < int(self.m.text()) - 1:
                # Пересчитываем точки для следующего полигона
                points = [
                    QPointF(points[n].x() + (points[n + 1].x() - points[n].x()) * (1 - coeff),
                            points[n].y() + (points[n + 1].y() - points[n].y()) *
                            (1 - coeff)) if n != len(points) - 1 else QPointF(
                        points[n].x() + (points[0].x() - points[n].x()) * (1 - coeff),
                        points[n].y() + (points[0].y() - points[n].y()) *
                        (1 - coeff)) for n in range(len(points))]
                self.start_point = [points[0].x(), points[0].y()]


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NoTSquare()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

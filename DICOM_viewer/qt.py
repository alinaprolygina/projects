import os
import pydicom
import numpy as np
import cv2
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QWidget, QScrollArea

class DicomViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setMinimumSize(1, 1)
        self.image_label.setScaledContents(True)
        self.image_label.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setMinimumSize(1, 1)
        self.scroll_area.viewport().installEventFilter(self)

        self.patient_name_label = QtWidgets.QLabel(self)
        self.patient_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.patient_name_label.setMinimumHeight(20)

        self.load_button = QtWidgets.QPushButton('Load', self)
        self.load_button.clicked.connect(self.load_files)

        self.images = []
        self.current_image = None
        self.current_index = 0
        
        # Создание кнопок "Влево" и "Вправо"
        self.button_left = QPushButton("<")
        self.button_right = QPushButton(">")

        # Назначение обработчиков событий клика на кнопки
        self.button_left.clicked.connect(self.previous_image)
        self.button_right.clicked.connect(self.next_image)

        # Создание горизонтального контейнера для кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_left)
        button_layout.addWidget(self.button_right)

        # Создание вертикального контейнера для изображения и кнопок
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.scroll_area)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.patient_name_label)
        main_layout.addWidget(self.load_button)

        # Установка главного компоновщика для окна
        self.setLayout(main_layout)

    def load_files(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')

        if directory:
            files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.dcm')]
            self.images = [pydicom.dcmread(f) for f in files]
            self.show_image(0)

    def show_image(self, index):
        self.current_index = index
        self.current_image = self.images[index]
        if not isinstance(self.current_image, np.ndarray):
            self.current_image = self.current_image.pixel_array
        qimage = QImage(self.current_image.tobytes(), self.current_image.shape[1], self.current_image.shape[0], QImage.Format_Grayscale8)
        self.image_label.setPixmap(QPixmap.fromImage(qimage))
        self.resize_image()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            self.previous_image()
        elif event.key() == QtCore.Qt.Key_Right:
            self.next_image()

    def previous_image(self):
        if self.current_image is not None:
            index = self.current_index - 1
            if index >= 0:
                self.show_image(index)

    def next_image(self):
        if self.current_image is not None:
            index = self.current_index + 1
            if index < len(self.images):
                self.show_image(index)
            
    def eventFilter(self, obj, event):
        if obj is self.scroll_area.viewport() and event.type() == QtCore.QEvent.Resize:
            self.resize_image()
        return super().eventFilter(obj, event)

    def resize_image(self):
        if self.current_image is not None:
            image = self.images[self.current_index]
            if not isinstance(image, np.ndarray):
                image = image.pixel_array

            # Получаем размеры виджета и изображения
            widget_size = self.image_label.size()
            image_size = QtCore.QSize(image.shape[1], image.shape[0])

            # Вычисляем соотношение сторон
            widget_aspect_ratio = widget_size.width() / widget_size.height()
            image_aspect_ratio = image_size.width() / image_size.height()

            if widget_aspect_ratio > image_aspect_ratio:
                # Масштабируем по высоте с сохранением соотношения сторон
                scale_factor = widget_size.height() / image_size.height()
            else:
                # Масштабируем по ширине с сохранением соотношения сторон
                scale_factor = widget_size.width() / image_size.width()

            scaled_image = cv2.resize(image, (0, 0), fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

            # Создаем pixmap и устанавливаем его в качестве изображения для label
            qimage = QImage(scaled_image.tobytes(), scaled_image.shape[1], scaled_image.shape[0], QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qimage)
            self.image_label.setPixmap(pixmap)




if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    viewer = DicomViewer()
    viewer.show()
    app.exec_()


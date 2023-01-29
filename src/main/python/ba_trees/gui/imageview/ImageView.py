from pathlib import Path

from PIL import Image as Img
from PyQt6.QtCore import Qt, QSize, QPoint
from PyQt6.QtGui import QImage, QPixmap, QPainter, QPalette, QCursor
from PyQt6.QtWidgets import QScrollArea, QLabel, QSizePolicy


class ImageView(QScrollArea):
    def __init__(self, *args):
        super().__init__(*args)
        
        # Variables
        self.image: QPixmap = None
        self.scale_factor: float = 1.0
        self.boundWidth = False # TODO
        self.boundHeight = False
        
        self.boundsSizeFunctions = []
        self.boundsWidthFunctions = []
        self.boundsHeightFunctions = []
        
        self.disableScroll = False
        
        self.__resized = False
        self.__resizeevent = False
        
        
        # Qt Widgets
        self.setBackgroundRole(QPalette.ColorRole.Dark)
        self.setWidgetResizable(True)
        
        self.image_widget = QLabel()
        self.image_widget.setScaledContents(True)
        self.image_widget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.setWidget(self.image_widget)
        
        self.painter: QPainter = None
        self.pixmap: QPixmap = None
        
        self.size_hint = QSize(1, 1)
    
    def __del__(self):
        del self.painter
        del self.pixmap
    
    def resizeEvent(self, event):
        if self.image == None or self.__resizeevent:
            return
        
        self.__resizeevent = True
        
        size: QSize = event.size()
        
        
        if self.boundWidth:
            scale = size.width() / self.image.width()
        elif self.boundHeight:
            scale = size.height() / self.image.height()
        else:
            scaleWidth = size.width() / self.image.width()
            scaleHeight = size.height() / self.image.height()
            
            scale = scaleWidth if scaleWidth < scaleHeight or scaleHeight <= 0 else scaleHeight
            scale = scale if scale > 0 else self.scale_factor
        
        self.resizeImage(scale)
        
        self.size_hint.setWidth(size.width() if self.boundWidth else self.pixmap.width())
        self.size_hint.setHeight(size.height() if self.boundHeight else self.pixmap.height())
        
        self.resize(self.size_hint)
        
        for func in self.boundsSizeFunctions:
            func(self.size_hint)
        
        for func in self.boundsWidthFunctions:
            func(QSize(self.size_hint.width(), 0))
        
        for func in self.boundsHeightFunctions:
            func(QSize(0, self.size_hint.height()))
        
        self.__resizeevent = False
    
    def sizeHint(self):
        return self.size_hint
    
    def setImage(self, image):
        if isinstance(image, str):
            image = Path(image)
            
        if isinstance(image, Path):
            with Img.open(image) as img:
                img2 = img.convert("RGBA")
                data = img2.tobytes("raw", "BGRA")
                qimg = QImage(data, img2.width, img2.height, QImage.Format.Format_ARGB32)
                image = QPixmap(qimg)
        
        if isinstance(image, QPixmap):
            self.image = image
            
            self.resizeImage(self.scale_factor)
    
    def resizeImage(self, scaleFactor: float = 1.0):
        if scaleFactor <= 0 and self.image != None:
            return
        
        self.__resized = True
        self.scale_factor = scaleFactor
        
        self.repaintImage()
    
    def repaintImage(self):
        image = self.image
        
        width, height = int(image.width() * self.scale_factor), int(image.height() * self.scale_factor)
        new_image = image.scaled(QSize(width, height), Qt.AspectRatioMode.KeepAspectRatio)
        
        if self.__resized:
            del self.painter
            del self.pixmap
            
            self.pixmap = QPixmap(new_image.width(), new_image.height())
            self.painter = QPainter(self.pixmap)
            
            self.image_widget.resize(self.pixmap.size())
        
        
        painter = self.painter
        
        painter.setViewport(0, 0, new_image.width(), new_image.height())
        painter.drawPixmap(0, 0, new_image)
        
        self.repaintImageOverride(painter)
        
        self.image_widget.setPixmap(self.pixmap)
    
    
    def repaintImageOverride(self, painter: QPainter):
        pass
    
    def wheelEvent(self, event):
        if self.disableScroll:
            return
        
        delta = event.angleDelta().y() / 2400.0
        pos = self.mapFromGlobal(QCursor.pos())
        
        image_point = [(self.horizontalScrollBar().value() + pos.x()) / self.scale_factor, (self.verticalScrollBar().value() + pos.y()) / self.scale_factor]
        
        self.painter.drawEllipse(QPoint(int(image_point[0] * self.scale_factor), int(image_point[1] * self.scale_factor)), 5, 5)
        self.image_widget.setPixmap(self.pixmap)
        
        self.resizeImage(self.scale_factor + delta)
        
        self.horizontalScrollBar().setValue(int(image_point[0] * self.scale_factor - pos.x()))
        self.verticalScrollBar().setValue(int(image_point[1] * self.scale_factor - pos.y()))
        
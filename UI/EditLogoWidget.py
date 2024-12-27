from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame,QPushButton,QFileDialog,QDialogButtonBox
from PySide6.QtCore import Qt, QPoint,QRect,Signal
from PySide6.QtGui import QPixmap, QPainter, QWheelEvent,QColor,QShowEvent
import sys
from UI.ui_LogoEdit import Ui_LogoEditWindow  # Replace with your actual .ui file's converted Python class



class LogoFrame(QFrame):

    def __init__(self, parent=None,safeMargEnabled=None):
        super().__init__(parent)

        self.setStyleSheet("background-color: lightgray;")
        self.original_pixmap = None  # Store the original pixmap for resizing
        self.logo_pixmap = None
        self.logo_position = QPoint(100, 100)  # Initial position
        self.scale_factor = 0.5  # Initial scale factor
       
        self.logoPath = None
        self.is_dragging = False
        self.drag_start_pos = None
        self.safeMarginEnabled = safeMargEnabled
        self.setMouseTracking(True)

    def load_image(self, image_path):
        try:
            self.original_pixmap = QPixmap(image_path)  # Load the original
            self.resize_pixmap()  # Resize the image to the initial size
            self.logoPath = image_path
            self.update()
        except Exception as e:
            print(f"Error: {e}")

    def resize_pixmap(self):
        if self.original_pixmap:
            new_size = self.original_pixmap.size() * self.scale_factor
            self.logo_pixmap = self.original_pixmap.scaled(
                new_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            #print("new logo size: ",new_size)

    def mousePressEvent(self, event):  
        if event.button() == Qt.MouseButton.LeftButton and self.logo_pixmap:
            rect = self.logo_pixmap.rect().translated(self.logo_position)
            if rect.contains(event.position().toPoint()):
                self.is_dragging = True
                self.drag_start_pos = event.position().toPoint() - self.logo_position

    def mouseMoveEvent(self, event):
        
        if self.is_dragging:
            
            new_position = event.position().toPoint() - self.drag_start_pos

            max_x = self.width() - self.logo_pixmap.width()
            max_y = self.height() - self.logo_pixmap.height()

            new_position.setX(min(max(new_position.x(), 0), max_x))
            new_position.setY(min(max(new_position.y(), 0), max_y))
                
            self.logo_position = new_position
            self.update()

    def mouseReleaseEvent(self, event):
        self.is_dragging = False
     
        #print(f"Logo position: x={self.logo_position.x()*2}, y={self.logo_position.y()*2}")

    def wheelEvent(self, event: QWheelEvent):
        if self.logo_pixmap:
            delta = event.angleDelta().y()
            if delta > 0:
                self.scale_factor *= 1.1  # Increase size by 10%
            else:
                self.scale_factor *= 0.9  # Decrease size by 10%

            self.scale_factor = max(0.1, min(self.scale_factor, 5.0))  # Limit scale factor

            self.resize_pixmap()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        if(self.safeMarginEnabled.isChecked()):
            self.paintSafeZone()
        else:
            self.update()
        if self.logo_pixmap:
            painter = QPainter(self)
            painter.drawPixmap(self.logo_position, self.logo_pixmap)

    def paintSafeZone(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set the color for the safe zone marks (white for visibility)
        painter.setPen(QColor(255, 255, 255))

        # Define the frame size
        frame_width = self.width()
        frame_height = self.height()

        # Define the safe zones (percentage of width and height)
        action_safe_width = frame_width * 0.9
        action_safe_height = frame_height * 0.9

        title_safe_width = frame_width * 0.8
        title_safe_height = frame_height * 0.8

        # Calculate the margins for the action and title safe zones
        action_safe_margin_x = (frame_width - action_safe_width) / 2
        action_safe_margin_y = (frame_height - action_safe_height) / 2

        title_safe_margin_x = (frame_width - title_safe_width) / 2
        title_safe_margin_y = (frame_height - title_safe_height) / 2

        # Draw action safe zone
        painter.drawRect(QRect(int(action_safe_margin_x), int(action_safe_margin_y), 
                               int(action_safe_width), int(action_safe_height)))

        # Draw title safe zone
        painter.drawRect(QRect(int(title_safe_margin_x), int(title_safe_margin_y), 
                               int(title_safe_width), int(title_safe_height)))

        painter.end()

class LogoEditWindow(QMainWindow):
    trigger_saveToConfigFile = Signal()
    trigger_LoadConfigFile = Signal()
    def __init__(self,resource_path):
        super().__init__()
        self.ui = Ui_LogoEditWindow()
        self.ui.setupUi(self)
        self.ui.safeMargCB.setParent(self)

        # Replace the frame from Designer with a LogoFrame
        self.logo_frame = LogoFrame(self.ui.video_frame, self.ui.safeMargCB)
        self.logo_frame.setGeometry(self.ui.video_frame.geometry())
        self.bars_img = (resource_path / "UI/resources/SMPTE_COLOR_BAR960540.jpg").as_posix()

        self.logo_frame.setStyleSheet(f"background-image: url({self.bars_img});")
        self.logo_frame.setParent(self)
        

        self.ui.select_file_button.clicked.connect(self.open_file_dialog)
        self.ui.select_file_button.setParent(self)


        self.ui.save_button.clicked.connect(self.onSave)
        self.ui.discard_button.clicked.connect(self.onDiscard)

    def emit_saveToConfigFile_signal(self):      
        self.trigger_saveToConfigFile.emit()  # Emit the signal
    def emit_LoadConfigFile_signal(self):
        self.trigger_LoadConfigFile.emit()
    def onSave(self):
        self.emit_saveToConfigFile_signal()
        self.close()

    def onDiscard(self):

        self.emit_LoadConfigFile_signal()
        self.close()

    def getX(self):
        #Normolaized 
        return  self.logo_frame.logo_position.x()*2
    def setX(self,new_x):
        self.logo_frame.logo_position.setX(new_x/2)

    def getY(self):
        #Normolaized 
        return self.logo_frame.logo_position.y()*2
    def setY(self,new_y):
        self.logo_frame.logo_position.setY(new_y/2)

    def getLogoPath(self):
        return self.logo_frame.logoPath
    def setLogoPath(self,path):
        self.logo_frame.logoPath = path
        if(path):
            self.logo_frame.load_image(path)
    def getScaleFactor(self):
        return self.logo_frame.scale_factor
    def setScaleFactor(self,sf):
        self.logo_frame.scale_factor = sf
        self.logo_frame.resize_pixmap()
    def setSafeMarginState(self,state):
        self.logo_frame.safeMarginEnabled.setCheckState(state)
    def open_file_dialog(self):
        # Open the file dialog

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File",  # Dialog title
            "",               # Starting directory
            "PNG Files (*.png);;All Files (*);",  # File types
            options=QFileDialog.Option.ReadOnly
        )
        if file_path:   
            self.logo_frame.load_image(file_path)
            #print(f"Selected file: {file_path}")

    # def showEvent(self, event: QShowEvent):
    #     super().showEvent(event)  # Important: Call the base class implementation
        
        # self.prevSettings =  {"position":self.logo_frame.logo_position,
        #                 "scaleFactor": self.logo_frame.scale_factor,
        #                 "logoPath": self.logo_frame.logoPath,
        #                 "marginSafeState": self.logo_frame.safeMarginEnabled.checkState()
        #                 }
    
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = LogoEditWindow()
#     window.show()
#     sys.exit(app.exec())

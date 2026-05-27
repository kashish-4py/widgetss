import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QPoint, QSize, QUrl
from PyQt6.QtGui import QMovie, QColor
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer

# --- CONFIGURATION ---
WIDGET_WIDTH = 200
WIDGET_HEIGHT = 200
CORNER_RADIUS = 30         
BORDER_WIDTH = 5           
BORDER_COLOR = "#FFB7C5"   # Cherry Blossom Pink
BG_COLOR = "#FFF0F5"       # Lavender Blush
TEXT_COLOR = "#6B5B95"     # Cozy Muted Purple
GIF_FILE = "pet"           # Your black cat GIF file name
SOUND_FILE = "sound"       # Your mp3 sound file name
# ----------------------------------------------------

class CuteAnimatedWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool                 
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) 
        self.setFixedSize(WIDGET_WIDTH, WIDGET_HEIGHT)

        self._drag_pos = QPoint()

        # SETUP SOUND PLAYER
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.5) # 50% Volume

        # Custom Styling (Borders & Round Corners)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {BG_COLOR};
                border: {BORDER_WIDTH}px solid {BORDER_COLOR};
                border-radius: {CORNER_RADIUS}px;
            }}
            QLabel {{
                background-color: transparent; 
                border: none;
                color: {TEXT_COLOR};
                font-family: 'Arial';
                font-size: 14px;
                font-weight: bold;
            }}
        """)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 15, 15, 15) 
        self.setLayout(self.layout)

        # The GIF Mascot Display Area
        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gif_label.setFixedSize(QSize(120, 120)) 
        self.layout.addWidget(self.gif_label)

        # Automatically locate the widgetss folder path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Smart Check for the GIF file
        full_gif_path = os.path.join(script_dir, GIF_FILE)
        if not os.path.exists(full_gif_path) and os.path.exists(full_gif_path + ".gif"):
            full_gif_path = full_gif_path + ".gif"

        # Smart Check for the Sound file (handles sound vs sound.mp3)
        self.full_sound_path = os.path.join(script_dir, SOUND_FILE)
        if not os.path.exists(self.full_sound_path) and os.path.exists(self.full_sound_path + ".mp3"):
            self.full_sound_path = self.full_sound_path + ".mp3"

        # Start the GIF animation loop
        if os.path.exists(full_gif_path):
            self.movie = QMovie(full_gif_path)
            self.gif_label.setMovie(self.movie)
            self.movie.start() 
        else:
            self.gif_label.setText("[ GIF Not Found ]")

        # Text Label
        self.status_label = QLabel("Cheering you on! ✨")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.status_label)

        self.add_shadow()
        
        # Play the sound once right when it boots up!
        self.play_cute_sound()
        
        self.show()

    def add_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20) 
        shadow.setXOffset(5)    
        shadow.setYOffset(5)    
        shadow.setColor(QColor(0, 0, 0, 80)) 
        self.setGraphicsEffect(shadow)

    # Audio playback logic
    def play_cute_sound(self):
        if os.path.exists(self.full_sound_path):
            self.media_player.setSource(QUrl.fromLocalFile(self.full_sound_path))
            self.media_player.play()

    # Mouse Dragging & Sound Trigger Controls
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()
            # Plays sound whenever you click on the widget!
            self.play_cute_sound()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = event.globalPosition().toPoint()
            move = new_pos - self._drag_pos
            self.move(self.pos() + move)
            self._drag_pos = new_pos

    # Right-Click Anywhere to Close
    def contextMenuEvent(self, event):
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = CuteAnimatedWidget()
    sys.exit(app.exec())
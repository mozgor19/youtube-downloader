import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from video_downloader import VideoDownloader
from playlist_downloader import PlaylistDownloader
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("YouTube Çaycı v1")
        self.setGeometry(100, 100, 300, 150)

        icon_path = "video.png"  # İkon dosyasının yolu
        app_icon = QIcon(icon_path)
        self.setWindowIcon(app_icon)

        layout = QVBoxLayout()

        self.label = QLabel(
            "YouTube Çaycı Uygulamasına Hoşgeldiniz!\n\n\nLütfen video ya da playlist indirme seçeneklerinden birini seçin:"
        )
        layout.addWidget(self.label)

        self.video_button = QPushButton("YouTube Video İndirici")
        self.video_button.clicked.connect(self.openVideoDownloader)
        layout.addWidget(self.video_button)

        self.playlist_button = QPushButton("YouTube Playlist İndirici")
        self.playlist_button.clicked.connect(self.openPlaylistDownloader)
        layout.addWidget(self.playlist_button)

        self.setLayout(layout)
        self.show()

    def openVideoDownloader(self):
        self.video_downloader = VideoDownloader()
        self.video_downloader.show()

    def openPlaylistDownloader(self):
        self.playlist_downloader = PlaylistDownloader()
        self.playlist_downloader.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

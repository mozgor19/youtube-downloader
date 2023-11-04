import sys
import os
import platform
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QComboBox,
)
from pytube import Playlist
from threading import Thread
import subprocess

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class PlaylistDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.indirme_yeri = os.path.join(
            os.path.expanduser("~"), "Downloads", "YouTube Playlist Downloader"
        )

    def initUI(self):
        self.setWindowTitle("YouTube Çaycı (Playlist)")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.url_label = QLabel("Playlist Linki:")
        layout.addWidget(self.url_label)

        self.url_entry = QLineEdit()
        layout.addWidget(self.url_entry)

        self.quality_label = QLabel("İndirme Kalitesi:")
        layout.addWidget(self.quality_label)

        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["144p", "240p", "360p", "480p", "720p", "1080p"])
        layout.addWidget(self.quality_combo)

        self.indirme_yeri_label = QLabel("İndirme Yeri:")
        layout.addWidget(self.indirme_yeri_label)
        self.indirme_yeri = None

        self.indirme_yeri_button = QPushButton("Dizin Seç")
        self.indirme_yeri_button.clicked.connect(self.dizinSec)
        layout.addWidget(self.indirme_yeri_button)

        self.indir_button = QPushButton("İndir")
        self.indir_button.clicked.connect(self.basla)
        layout.addWidget(self.indir_button)

        self.message_label = QLabel("")
        layout.addWidget(self.message_label)

        self.videoya_git_button = QPushButton("Videoya Git")
        self.videoya_git_button.clicked.connect(self.videoyaGit)
        self.videoya_git_button.setDisabled(True)
        layout.addWidget(self.videoya_git_button)

        self.setLayout(layout)

    def dizinSec(self):
        indirme_yeri = QFileDialog.getExistingDirectory(self, "İndirme Yeri Seç")
        if indirme_yeri:
            self.indirme_yeri = indirme_yeri
        else:
            default_download_folder = os.path.join(
                os.path.expanduser("~"), "Downloads", "Youtube Video Downloader"
            )
            os.makedirs(default_download_folder, exist_ok=True)
            self.indirme_yeri = default_download_folder

        self.indirme_yeri_label.setText(f"İndirme Yeri: {self.indirme_yeri}")

    def basla(self):
        self.url = self.url_entry.text()
        if not self.url:
            self.message_label.setText("Lütfen bir playlist linki girin!")
            return

        quality = self.quality_combo.currentText()

        def indirmeThread():
            try:
                self.message_label.setText("Playlist indiriliyor...")
                playlist = Playlist(self.url)
                total_videos = len(playlist.videos)
                downloaded_videos = 0

                for idx, video in enumerate(playlist.videos, start=1):
                    video_stream = (
                        video.streams.filter(progressive=True, file_extension="mp4")
                        .order_by("resolution")
                        .desc()
                        .first()
                    )
                    if not video_stream:
                        video_stream = video.streams.filter(
                            progressive=True, file_extension="mp4"
                        ).first()
                    if video_stream:
                        if video_stream.resolution == quality:
                            video_stream.download(output_path=self.indirme_yeri)
                        else:
                            alternative_stream = (
                                video.streams.filter(
                                    progressive=True, file_extension="mp4"
                                )
                                .order_by("resolution")
                                .asc()
                                .first()
                            )
                            if (
                                alternative_stream
                                and alternative_stream.resolution
                                != video_stream.resolution
                            ):
                                alternative_stream.download(
                                    output_path=self.indirme_yeri
                                )
                                self.message_label.setText(
                                    f"{video.title} videosu istenilen kalitede bulunamadığı için {alternative_stream.resolution} kalitesinde indirildi."
                                )
                            else:
                                video_stream.download(output_path=self.indirme_yeri)
                                self.message_label.setText(
                                    f"{video.title} videosu istenilen kalitede bulunamadığı için {video_stream.resolution} kalitesinde indirildi."
                                )
                        downloaded_videos += 1
                        self.message_label.setText(
                            f"Playlist indirme işlemi devam ediyor {downloaded_videos}/{total_videos} - {video.title} videosu indirildi."
                        )
                    else:
                        self.message_label.setText(
                            f"Playlist indirme işlemi devam ediyor {downloaded_videos}/{total_videos} - {video.title} videosu indirilemedi."
                        )

                self.message_label.setText("Playlist başarıyla indirildi!")
                self.videoya_git_button.setEnabled(True)
            except Exception as e:
                self.message_label.setText(
                    f"İndirme sırasında bir hata oluştu: {str(e)}"
                )

        Thread(target=indirmeThread).start()

    def videoyaGit(self):
        try:
            file_path = self.indirme_yeri
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", file_path])
            else:
                subprocess.Popen(["xdg-open", file_path])
        except Exception as e:
            self.message_label.setText(f"Hata: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlaylistDownloader()
    window.show()
    sys.exit(app.exec_())

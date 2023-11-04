import sys
import os
import platform
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QComboBox,
    QFileDialog,
    QLineEdit,
)
from pytube import YouTube
from threading import Thread
import subprocess

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class VideoDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("YouTube Çaycı (Video)")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.url_label = QLabel("Video Linki:")
        layout.addWidget(self.url_label)

        self.url_entry = QLineEdit()
        layout.addWidget(self.url_entry)

        self.kalite_sec_button = QPushButton("İndirme Kalitesi Seç")
        self.kalite_sec_button.clicked.connect(self.kaliteSec)
        layout.addWidget(self.kalite_sec_button)

        self.quality_label = QLabel("İndirme Kalitesi:")
        layout.addWidget(self.quality_label)
        self.quality_label.setVisible(False)

        self.quality_combo = QComboBox()
        layout.addWidget(self.quality_combo)
        self.quality_combo.setVisible(False)

        self.indirme_yeri_label = QLabel("İndirme Yeri:")
        layout.addWidget(self.indirme_yeri_label)
        self.indirme_yeri = (
            None  # indirme_yeri değişkenini başlangıçta None olarak tanımla
        )

        self.indirme_yeri_button = QPushButton("Dizin Seç")
        self.indirme_yeri_button.clicked.connect(self.dizinSec)
        layout.addWidget(self.indirme_yeri_button)

        self.indir_button = QPushButton("İndir")
        self.indir_button.clicked.connect(self.basla)
        layout.addWidget(self.indir_button)

        self.message_label = QLabel("")
        layout.addWidget(self.message_label)

        self.progress_label = QLabel("")
        layout.addWidget(self.progress_label)

        self.videoya_git_button = QPushButton("Videoya Git")
        self.videoya_git_button.clicked.connect(self.videoyaGit)
        self.videoya_git_button.setEnabled(False)
        layout.addWidget(self.videoya_git_button)

        self.setLayout(layout)

    def kaliteSec(self):
        self.analizEt()
        self.quality_label.setVisible(True)
        self.quality_combo.setVisible(True)
        self.kalite_sec_button.setVisible(False)

    def dizinSec(self):
        indirme_yeri = QFileDialog.getExistingDirectory(self, "İndirme Yeri Seç")
        if indirme_yeri:
            self.indirme_yeri = indirme_yeri
            self.indirme_yeri_label.setText(f"İndirme Yeri: {self.indirme_yeri}")

    def analizEt(self):
        self.quality_combo.clear()

        try:
            yt = YouTube(self.url_entry.text())
            video_streams = (
                yt.streams.filter(progressive=True, file_extension="mp4")
                .order_by("resolution")
                .desc()
            )
            available_qualities = set()
            for stream in video_streams:
                available_qualities.add(stream.resolution)
            self.quality_combo.addItems(list(available_qualities))
            self.message_label.setText("Kalite seçin ve indirme başlatın.")
        except Exception as e:
            self.message_label.setText(
                f"Video analiz sırasında bir hata oluştu: {str(e)}"
            )

    def basla(self):
        self.url = self.url_entry.text()
        if not self.url:
            self.message_label.setText("Lütfen bir video linki girin!")
            return

        quality = self.quality_combo.currentText()

        def indirmeThread():
            self.indirme_yeri_button.setDisabled(True)
            self.indir_button.setDisabled(True)
            self.videoya_git_button.setDisabled(True)

            try:
                self.message_label.setText("Video indiriliyor...")
                yt = YouTube(self.url)
                video_stream = yt.streams.filter(
                    progressive=True, file_extension="mp4", resolution=quality
                ).first()
                if video_stream:
                    if not self.indirme_yeri or not os.path.isdir(self.indirme_yeri):
                        default_download_folder = os.path.join(
                            os.path.expanduser("~"),
                            "Downloads",
                            "Youtube Video Downloader",
                        )
                        os.makedirs(default_download_folder, exist_ok=True)
                        self.indirme_yeri = default_download_folder
                        self.indirme_yeri_label.setText(
                            f"İndirme Yeri: {self.indirme_yeri}"
                        )
                    video_stream.download(output_path=self.indirme_yeri)
                    self.message_label.setText(
                        "Video indirme başarılı bir şekilde tamamlandı."
                    )
                else:
                    self.message_label.setText(
                        f"{yt.title} videosu istenilen kalitede bulunamadığı için indirilemedi."
                    )
                self.videoya_git_button.setEnabled(True)
            except Exception as e:
                self.message_label.setText(
                    f"İndirme sırasında bir hata oluştu: {str(e)}"
                )

            self.indirme_yeri_button.setEnabled(True)
            self.indir_button.setEnabled(True)
            self.videoya_git_button.setEnabled(True)

        download_thread = Thread(target=indirmeThread)
        download_thread.start()

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
    window = VideoDownloader()
    window.show()
    sys.exit(app.exec_())

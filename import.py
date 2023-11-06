# The used libraries:

import sys
import os
import platform
import subprocess
import ssl

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
from pytube import YouTube
from threading import Thread

# Youtube Video Downloader v1
## Youtube Çaycı v1

Welcome to Youtube Çaycı App!

With this application, you can download playlists or videos from YouTube.

## How to use it?

Download the files to your computer to run the application on your computer. For the application to run smoothly, you need to install the pytube and pyqt5 libraries if you don't have them. You can do this from the terminal screen as follows:

`pip install pytube
pip install pyqt5`

Apart from these, the libraries used come installed with Python 3. However, if you have a problem with this, you can look at the file named *import.py* to view the libraries used.

## How to Make an Application?

Once you've made it this far, you'll need the pyinstaller library to turn it into an application that you can run directly on your computer. You can install it as follows:

`pip install pyinstaller`

Once the library is installed, to run the application anywhere without the code screen, you need to go to the directory where the *main.py* file is located and type the following on the terminal screen:

`pyinstaller --onefile --noconsole icon=tea.ico main.py`

After typing this command, two folders named **dist** and **build** and a file named *main.spec* are created. Here;

- build: contains the files needed for the application to run.
- dist: contains the version of the application needed for deployment.
- main.spec: contains additional files during the compilation of the application file.

It is very likely that the application will not run in the output obtained in this way. The main reason for this is that we are using libraries that Python does not include by default. For this reason, the main.spec file should be opened and the following should be written in the relevant sections:

`datas = [('*file path of pytube library*','pytube'),('*file path of cacert.pem file*','certifi')],
hiddenimports = ['json','xml.etree','xml.etree.ElementTree','html'],`

Also, to give the app a logo and a name, the relevant places can be edited as follows:

`name ='Youtube Çaycı.app',
icon ='tea.ico',`

The errors you get in these steps may vary depending on the Python version, filing structure and compiler on your computer. Therefore, it is recommended to use the latest version.

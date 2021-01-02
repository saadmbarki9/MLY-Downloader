from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

import os
from os import path
import sys
import urllib.request
import pafy
import humanize



form_class,_ = loadUiType(path.join(path.dirname(__file__),'main.ui'))

class Mainapp(QMainWindow , form_class):
    def __init__(self, parent=None):
        super(Mainapp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.h_UI()
        self.h_Buttons()

    
    def h_UI(self):
        self.setWindowTitle('MLY_Downloader')
        self.setFixedSize(743,349)
    
    def h_Buttons(self):
        self.pushButton.clicked.connect(self.Download)
        self.toolButton.clicked.connect(self.h_Brows)
        self.pushButton_4.clicked.connect(self.get_YT_vid)
        self.pushButton_2.clicked.connect(self.Download_YT_vid)
        self.toolButton_2.clicked.connect(self.Save_brows)
        self.pushButton_3.clicked.connect(self.Playlist_YT)
        self.toolButton_3.clicked.connect(self.Save_brows_playlist)
    





    def h_Brows(self):
        save_place=QFileDialog.getSaveFileName(self,caption='Save As',directory='.',filter='All Files (*.*)')
        r=str(save_place)
        n=(r[2:].split(',')[0].replace("'",""))
        self.lineEdit_2.setText(n)



    def h_Progress(self, blocknum,blocksize,totalsize):
        read=blocknum*blocksize
        if totalsize>0:
            percent=read*100/totalsize
            self.progressBar.setValue(percent)
            QApplication.processEvents()  #7al mo2a9at binma nt3lm l "threading" bash mayb9ash itplenta lprogramme 
    
    def Download(self):
        url=self.lineEdit.text()
        save_location=self.lineEdit_2.text()
       
        try:
            urllib.request.urlretrieve(url, save_location, self.h_Progress)
        except Exception:
            QMessageBox.warning(self,'Error','Download Faild')
            return
        
        
        QMessageBox.information(self,'Don','Download Accomplished')
        self.progressBar.setValue(0)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
    
  
    def Save_brows(self):
        save=QFileDialog.getExistingDirectory(self,'Select Download Directory')
        self.lineEdit_4.setText(save)
        
    
    
    def Save_brows_playlist(self):
        save=QFileDialog.getExistingDirectory(self,'Select Download Directory')
        self.lineEdit_6.setText(save)





    def get_YT_vid(self):
        try:
            video_link=self.lineEdit_3.text()
            v=pafy.new(video_link)
            st=v.allstreams
            for s in st:
                size=humanize.naturalsize(s.get_filesize())
                d='{} {} {} {} '.format(s.mediatype,s.extension,s.quality,size)
                self.comboBox.addItem(d)
        except Exception:
            QMessageBox.warning(self,'Error','no URL')
            return





    def Download_YT_vid(self):
        try:
            video_link=self.lineEdit_3.text()
            save_location=self.lineEdit_4.text()
            v=pafy.new(video_link)
            st=v.allstreams
            quality=self.comboBox.currentIndex()
            down=st[quality].download(filepath=save_location)
        except Exception:
            QMessageBox.warning(self,'Error','Download Faild')
            return
        
        QMessageBox.information(self,'Don','Download Accomplished')
    



    def Playlist_YT(self):
        palylist_urll=self.lineEdit_5.text()
        save_location=self.lineEdit_6.text()
        playlist=pafy.get_playlist(palylist_urll)
        videos=playlist['items']

        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])) :
            os.chdir(str(playlist['title']))
        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        for video in videos:
            p=video['pafy']
            best=p.getbest(preftype='mp4')
            best.download()
        
        QMessageBox.information(self,'Don','Download Accomplished')



def main():
    app=QApplication(sys.argv)
    window=Mainapp()
    window.show()
    app.exec_()


if __name__=='__main__':
    main()
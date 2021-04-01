
"""

   Copyright 2021 Theodore Klaus Storl-Desmond

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""



import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import tkinter as tk
from tkinter import messagebox, Button, Label
from PIL import ImageGrab
from pytesseract import pytesseract
import pyperclip

class startMenu(Label, Button):
    
    userDecision = False
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('500x275')
        self.root.title("image-to-text")
        self.root.configure(bg='black')
        herolabel = Label(self.root, text="\nCapture text from image/pdf/etc\nand copy directly to the clipboard", background='black', foreground='white', font=("Lato", 20)).pack()
        contentlabel = Label(self.root, text="Click, drag, and release your mouse\nover the text you wish to copy", pady=20, background='black', foreground='white',font=("Lato", 15)).pack()
        button = tk.Button(self.root,text = 'Copy text', font=("Lato", 12), command=self.startCapture, height=2, width=10).pack()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def startCapture(self):
        self.userDecision = True
        self.root.destroy()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.userDecision = False
            self.root.destroy()


class doneMenu(Label, Button):
    
    userDecision = False
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1000x250')
        self.root.title("image-to-text")
        self.root.configure(bg='black')
        label = Label(self.root, text="All Done! Text has been copied to clipboard.", background='black', foreground='white', pady=20, font=("Lato", 30)).pack()
        button = tk.Button(self.root,text = 'Copy more text', font=("Lato", 20), command=self.startCapture, height=2, width=20).pack()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def startCapture(self):
        self.userDecision = True
        self.root.destroy()

    def on_closing(self):
        self.userDecision = False
        self.root.destroy()

    

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width*2, screen_height*2)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.7)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        print('capture the screen...')
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))

        ##reading text from image
        path_to_tesseract = r'tesseract.exe'
        pytesseract.tesseract_cmd = path_to_tesseract   
        text = pytesseract.image_to_string(img, lang='eng')

        ##copying text to clipboard and exiting
        pyperclip.copy(text[:-1])
        print('text copied...')

        ##closing all windows
        self.root.destroy()


if __name__ == '__main__':

    def screenshot():
        app = QtWidgets.QApplication(sys.argv)
        window = MyWidget()
        window.show()
        app.exec_()

    start = startMenu()

    if (start.userDecision == True):
        takingScreenshots = True
        while (takingScreenshots == True):
            screenshot()
            done = doneMenu()
            if (done.userDecision == True):
                takingScreenshots = True
            else:
                takingScreenshots = False
                sys.exit()
    else:
         sys.exit()

    
            
            
        

    

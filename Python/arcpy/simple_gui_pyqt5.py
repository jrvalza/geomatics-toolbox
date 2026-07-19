
import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QDoubleValidator

# py file path
py_path = os.path.dirname(__file__)

# ui file path
ui_name = os.path.join(py_path, "simple_gui_pyqt5.ui")

# load form
form_class = uic.loadUiType(ui_name)[0]

# dialog class
class MyDialogClass(QtWidgets.QDialog, form_class):
    # init function
    def __init__(self, parent=None):
        # init class dialog
        QtWidgets.QDialog.__init__(self, parent)
        
        # run dialog
        self.setupUi(self)

        #Check input data
        self.txt_uno.setValidator(QDoubleValidator())
        self.txt_dos.setValidator(QDoubleValidator())

        #buttons
        self.btn_sumar.clicked.connect(self.sumar)
        self.btn_restar.clicked.connect(self.restar)
        self.btn_multiplicar.clicked.connect(self.multiplicar)
        self.btn_dividir.clicked.connect(self.dividir)
        self.btn_cerrar.clicked.connect(self.cerrar)
    
    def sumar(self):
        try:
            result = float(self.txt_uno.text()) + float(self.txt_dos.text())
            self.txt_resultado.setText(str(result))
        except:
            self.txt_resultado.setText('')

    def restar(self):
        try:
            result = float(self.txt_uno.text()) - float(self.txt_dos.text())
            self.txt_resultado.setText(str(result))
        except:
            self.txt_resultado.setText('')

    def multiplicar(self):
        try:
            result = float(self.txt_uno.text()) * float(self.txt_dos.text())
            self.txt_resultado.setText(str(result))
        except:
            self.txt_resultado.setText('')

    def dividir(self):
        try:
            result = float(self.txt_uno.text()) / float(self.txt_dos.text())
            self.txt_resultado.setText(str(result))

        except ZeroDivisionError as ex:
            self.txt_resultado.setText('Error: Division por cero')
        except:
            self.txt_resultado.setText('')

    def cerrar(self):
        app.quit()

app = QtWidgets.QApplication(sys.argv)
myDialog = MyDialogClass(None)
myDialog.show()
app.exec_()

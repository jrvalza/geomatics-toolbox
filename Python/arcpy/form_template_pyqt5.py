
import os
import sys
from PyQt5 import QtWidgets, uic

# py file path
py_path = os.path.dirname(__file__) # current python file path

# ui file path
ui_name = os.path.join(py_path, "form_template_gui.ui")

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

app = QtWidgets.QApplication(sys.argv)
myDialog = MyDialogClass(None)
myDialog.show()
app.exec_()

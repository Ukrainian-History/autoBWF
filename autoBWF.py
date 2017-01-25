import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from main import Ui_Dialog

config = None

class MainWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


        ###############
        ##### configure dropdowns
        ###############

        self.speedSelect.addItems(config["speed"])
        self.mediaSelect.addItems(config["media"])
        self.eqSelect.addItems(config["eq"])
        self.typeSelect.addItems(config["type"])
        self.technicianBox.addItems(config["technician"])
        self.deckSelect.addItems(config["deck"].keys())
        self.adcSelect.addItems(config["adc"].keys())
        self.softwareSelect.addItems(config["software"].keys())
        self.copyrightSelect.addItems(config["copyright"].keys())



        ###############
        ##### set up signals/slots
        ###############

        ##### GUI elements

        ## "add" buttons
        #self.title_addbutton.clicked.connect(lambda: self.genericInputbox(self.titles))
        

    def genericInputbox(self, listobj):
        from itertools import groupby

        dlg = StartGenericInputbox()

        all_attributes = listobj.options

        # deal with end delimiter
        attributes = [list(group) for k, group in groupby(all_attributes, lambda x: x == "#") if not k][0]

        # deal with separators
        attributes = [list(group) for k, group in groupby(attributes, lambda x: x == "-") if not k]
        attributes = attributes[::-1]

        this_list = attributes.pop()
        dlg.attribute.addItems(this_list)

        while (len(attributes) > 0):
            dlg.attribute.insertSeparator(dlg.attribute.count())
            this_list = attributes.pop()
            dlg.attribute.addItems(this_list)

        if dlg.exec_():
            # input = dlg.getValues()
            # listbox = listobj.list_element
            # listbox.addItem(str(data))
            # listobj.append(data)
            pass
        else:
            return

    def removeButtonToggle(self, listbox, button):
        if len(listbox.selectedItems()) > 0:
            button.setEnabled(True)
        else:
            button.setEnabled(False)


    def removeElement(self, listobj):
        listbox = listobj.list_element
        current_item = listbox.currentItem()
        current_row = listbox.row(current_item)
        del listobj[current_row]
        listbox.takeItem(current_row)



if __name__ == "__main__":
    import json

    with open('config.json') as data_file:    
        config = json.load(data_file)

    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.show()

    sys.exit(app.exec_())


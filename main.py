#!/usr/bin/env python3

import sys
import subprocess

from PyQt5.QtWidgets import *
from PyQt5 import uic

class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi('rufus_linux_gui.ui', self)
        self.show()
        self.select.clicked.connect(self.select_btn)
        self.start.clicked.connect(self.start_prog)
        self.exit.clicked.connect(self.close)

        self.methods_list = ['Незагрузочный образ', 'FreeDOS', 'Диск или ISO-образ (Выберите файл)']

    def select_btn(self):
        wb_patch = QFileDialog.getOpenFileName()
        self.boot_method.addItem(wb_patch[0])
        self.label_12.setText(f'Добавлен файл {wb_patch[0]}')

    def close(self):
        sys.exit()

    def start_prog(self):
        method = self.boot_method.currentText()
        if method in self.methods_list:
            self.format_disk()
        else:
            self.install_iso()

    def format_disk(self):
        proc = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        flash = self.devise.currentText()
        name = self.tom_name.text()
        stdout = proc.communicate(f'sudo umount {flash}')
        self.status_bar.setText(stdout)
        form = self.file_system.currentText()
        stdout = proc.communicate(f'sudo mkfs -t {form} -L {name} {flash}')
        self.status_bar.setText(stdout)

    def install_iso(self):
        proc = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        flash = self.devise.currentText()
        form = self.file_system.currentText()
        path = self.boot_method.currentText()
        stdout = proc.communicate(f'sudo umount {flash}')
        self.status_bar.setText(stdout)
        stdout = proc.communicate(f'sudo dd if={path} of={flash}')
        self.status_bar.setText(stdout)
        stdout = proc.communicate(f'sync')
        self.status_bar.setText(stdout)

app = QApplication([])
windows = MyGUI()
app.exec_()

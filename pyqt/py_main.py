# -*- coding: utf-8 -*-


import sys
from PyQt5.QtWidgets import QApplication,QtWidget


if __name__ == '__main__':
	app = QApplication(sys.argv)


	w = QtWidget()
	w.resize(250,150)
	w.move(300,300)
	w.setWindowTitle('Simple')
	w.show()

	sys.exit(app.exec_())
#!/usr/bin/env python

#
# Mxd2Qgs
# Created on 3/12/17 - Allan Oware
#

import os
import sys
import time
import math

import arcpy

from PyQt4 import QtGui, QtCore

sys.path.append("ui")

import mainapp

class MainApp(QtGui.QMainWindow, mainapp.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.files_to_convert = []
        self.openFilesPath = ''
        self.output_folder = ''

        # set icons
        self.addFile.setIcon(QtGui.QIcon("ui/images/2_060.ico"))
        self.addFolder.setIcon(QtGui.QIcon("ui/images/folder-add.ico"))
        self.removeItem.setIcon(QtGui.QIcon("ui/images/1_004.ico"))
        self.removeAll.setIcon(QtGui.QIcon("ui/images/remove-item.ico"))
        self.runConverter.setIcon(QtGui.QIcon("ui/images/converter.ico"))
        self.helpPage.setIcon(QtGui.QIcon("ui/images/help.ico"))
        self.selectDir.setIcon(QtGui.QIcon("ui/images/folder-open.ico"))

        # capture click events
        self.addFile.clicked.connect(self.add_files)
        self.addFolder.clicked.connect(self.add_folder)
        self.removeItem.clicked.connect(self.remove_item)
        self.removeAll.clicked.connect(self.remove_all)
        self.selectDir.clicked.connect(self.select_dir)
        self.helpPage.clicked.connect(self.help_page)
        self.runConverter.clicked.connect(self.run_converter)

        # files table
        self.filesTable.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.filesTable.verticalHeader().hide()
        self.filesTable.setShowGrid(False)

    def add_files(self):
        options = QtGui.QFileDialog.Options()
        #if not self.native.isChecked():
        #    options != QtGui.QFileDialog.DontUseNativeDialog
        files = QtGui.QFileDialog.getOpenFileNames(self,
                                                   "Select File(s) to Add", self.openFilesPath,
                                                   "Files (*.mxd *.qgs)")
        if files:
            self.select_files(files)

    def select_files(self, selected_files):
        #self.remove_all()
        for _file in selected_files:
            _file = str(_file)

            self.files_to_convert.append(_file)

            filename = os.path.basename(_file)
            fileNameItem = QtGui.QTableWidgetItem(filename)

            _filesize = os.path.getsize(_file)
            filesize = self.convert_size(_filesize)
            fileSizeItem = QtGui.QTableWidgetItem(filesize)

            fileformat = os.path.splitext(_file)[1]
            fileFormatItem = QtGui.QTableWidgetItem(fileformat)

            filelocation = os.path.dirname(_file)
            fileLocationItem = QtGui.QTableWidgetItem(filelocation)

            row = self.filesTable.rowCount()
            self.filesTable.insertRow(row)
            self.filesTable.setItem(row, 0, fileNameItem)
            self.filesTable.setItem(row, 1, fileFormatItem)
            self.filesTable.setItem(row, 2, fileSizeItem)
            self.filesTable.setItem(row, 3, fileLocationItem)




    def add_folder(self):
        # open dialog to add folder
        directory = QtGui.QFileDialog.getExistingDirectory(self, "Select Folder", QtCore.QDir.currentPath())
        if directory:
            self.remove_all()
            self.listFiles(directory)

    def remove_item(self):
        indexes = self.filesTable.selectionModel().selectedRows()
        for index in indexes:
            row = index.row()
            self.filesTable.removeRow(row)

    def remove_all(self):
        self.filesTable.clearContents()
        self.filesTable.setRowCount(0)
        self.files_to_convert.clear()

    def select_dir(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, "Select Output Folder", QtCore.QDir.currentPath())
        if directory:
            if self.outputFolder.findText(directory) == -1:
                self.outputFolder.addItem(directory)
        self.outputFolder.setCurrentIndex(self.outputFolder.findText(directory))


    def help_page(self):
        pass

    def run_converter(self):
        # check files to convert
        if len(self.files_to_convert) == 0:
            info = QtGui.QMessageBox.information(self,
                    "Add Files to Convert", "<p>Please Add Files to Convert!</p>")
        else:
            # check output folder
            self.output_folder = str(self.outputFolder.currentText())
            if self.output_folder == '':
                info = QtGui.QMessageBox.information(self,
                        "Select Output Folder", "<p>Please Select Output Folder!</p>")
            else:
                format = str(self.formatsCombo.currentText())
                if format == 'QGIS Project File [.QGS]':
                    # run qgis converter
                    self.qgis_converter(self.files_to_convert)
                else:
                    # run arcgis converter
                    self.mxd_converter(self.files_to_convert)

    def convert_size(self, size):
        if (size == 0):
            return '0B'
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size,1024)))
        p = math.pow(1024,i)
        s = round(size / p, 2)

        return '%s %s' % (s, size_name[i])

    def listFiles(self, path):
        # list files to be converted
        dirs = os.listdir(path)
        for file in dirs:
            fileNameItem = QtGui.QTableWidgetItem(file)
            fileformat = os.path.splitext(file)[1]

            if fileformat == ".mxd" or fileformat == ".qgs":
                # only show mxd and qgs files
                fullpath = path + "\\" + file
                _filesize = os.path.getsize(fullpath)
                filesize = self.convert_size(_filesize)

                self.files_to_convert.append(fullpath)

                fileFormatItem = QtGui.QTableWidgetItem(fileformat)
                fileSizeItem = QtGui.QTableWidgetItem(filesize)
                fileLocationItem = QtGui.QTableWidgetItem(path)

                row = self.filesTable.rowCount()
                self.filesTable.insertRow(row)
                self.filesTable.setItem(row, 0, fileNameItem)
                self.filesTable.setItem(row, 1, fileFormatItem)
                self.filesTable.setItem(row, 2, fileSizeItem)
                self.filesTable.setItem(row, 3, fileLocationItem)

    def qgis_converter(self, mxd_files):
        for mxd_file in mxd_files:
            if '.mxd' in mxd_file:
                # convert to qgis project file
                pass
            else:
                pass

    def mxd_converter(self, qgs_files):
        for qgs_file in qgs_files:
            if '.qgs' in qgs_file:
                # convert to mxd map document
                pass
            else:
                pass



def main():
    app = QtGui.QApplication(sys.argv)
    gui = MainApp()
    gui.show()
    app.exec_()


if __name__ == '__main__':
    main()
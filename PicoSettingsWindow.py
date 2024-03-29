# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PicoSettingsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PicoscopeSettings(object):
    def setupUi(self, PicoscopeSettings):
        #Picoscope Settings window
        PicoscopeSettings.setObjectName("PicoscopeSettings")
        PicoscopeSettings.setFixedSize(820,540)
        PicoscopeSettings.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.buttonBox = QtWidgets.QDialogButtonBox(PicoscopeSettings)
        self.buttonBox.setGeometry(QtCore.QRect(460, 480, 341, 32))
        self.buttonBox.setFont(QtGui.QFont("Lucida Grande",11))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtWidgets.QWidget(PicoscopeSettings)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 520, 801, 20))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setMinimumSize(QtCore.QSize(110, 14))
        self.label.setMaximumSize(QtCore.QSize(110, 14))
        self.label.setFont(QtGui.QFont("Lucida Grande",8))
        self.label.setStyleSheet("color:rgb(85, 87, 83);")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.line = QtWidgets.QFrame(self.layoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.label_3 = QtWidgets.QLabel(PicoscopeSettings)
        self.label_3.setGeometry(QtCore.QRect(10, 0, 130, 19))
        self.label_3.setMinimumSize(QtCore.QSize(130, 19))
        self.label_3.setMaximumSize(QtCore.QSize(130, 19))
        self.label_3.setFont(QtGui.QFont("DejaVu Sans Mono",9, 75))
        self.label_3.setStyleSheet("color: rgb(186, 189, 182);")
        self.label_3.setObjectName("label_3")

        # Main Widget
        self.layoutWidget1 = QtWidgets.QWidget(PicoscopeSettings)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 40, 803, 411))
        self.layoutWidget1.setObjectName("layoutWidget1")

        # Main Layout
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")

        # Channels GroupBox
        self.Channels_groupBox = QtWidgets.QGroupBox()
        self.Channels_groupBox.setFont(QtGui.QFont("Lucida Grande", 10))
        self.Channels_groupBox.setObjectName("Channels_groupBox")
        self.checkBox_CHA = QtWidgets.QCheckBox(self.Channels_groupBox)
        self.checkBox_CHA.setGeometry(QtCore.QRect(150, 55, 109, 27))
        self.checkBox_CHA.setFont(QtGui.QFont("Lucida Grande", 11))
        self.checkBox_CHA.setObjectName("checkBox_CHA")
        self.checkBox_CHB = QtWidgets.QCheckBox(self.Channels_groupBox)
        self.checkBox_CHB.setGeometry(QtCore.QRect(500, 55, 109, 27))
        self.checkBox_CHB.setFont(QtGui.QFont("Lucida Grande", 11))
        self.checkBox_CHB.setObjectName("checkBox_CHB")
        self.gridLayout.addWidget(self.Channels_groupBox, 0, 0, 1, 2)
        
        # Sample frequency GroupBox
        self.sample_frequency_groupBox = QtWidgets.QGroupBox()
        self.sample_frequency_groupBox.setFont(QtGui.QFont("Lucida Grande", 10))
        self.sample_frequency_groupBox.setObjectName("sample_frequency_groupBox")
        self.sample_frequency_comboBox = QtWidgets.QComboBox(self.sample_frequency_groupBox)
        self.sample_frequency_comboBox.setGeometry(QtCore.QRect(120, 60, 150, 29))
        self.sample_frequency_comboBox.setFont(QtGui.QFont("Lucida Grande", 11))
        self.sample_frequency_comboBox.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.sample_frequency_comboBox.setObjectName("sample_frequency_comboBox")
        self.gridLayout.addWidget(self.sample_frequency_groupBox, 1, 0)

        # Sample acquisition period GroupBox
        self.sample_acquisition_period_groupBox = QtWidgets.QGroupBox()
        self.sample_acquisition_period_groupBox.setFont(QtGui.QFont("Lucida Grande", 10))
        self.sample_acquisition_period_groupBox.setObjectName("sample_acquisition_period_groupBox")
        self.gridLayout.addWidget(self.sample_acquisition_period_groupBox, 1, 1)
        #SpinBox PreTrigger 
        self.sample_acquisition_pretrigger_period_spinBox = QtWidgets.QSpinBox(self.sample_acquisition_period_groupBox)
        self.sample_acquisition_pretrigger_period_spinBox.setGeometry(QtCore.QRect(70, 60, 100, 29))
        self.sample_acquisition_pretrigger_period_spinBox.setFont(QtGui.QFont("Lucida Grande", 11))
        self.sample_acquisition_pretrigger_period_spinBox.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.sample_acquisition_pretrigger_period_spinBox.setObjectName("sample_acquisition_pretrigger_period_spinBox")
        #SpinBox PostTrigger 
        self.sample_acquisition_posttrigger_period_spinBox = QtWidgets.QSpinBox(self.sample_acquisition_period_groupBox)
        self.sample_acquisition_posttrigger_period_spinBox.setGeometry(QtCore.QRect(225, 60, 100, 29))
        self.sample_acquisition_posttrigger_period_spinBox.setFont(QtGui.QFont("Lucida Grande", 11))
        self.sample_acquisition_posttrigger_period_spinBox.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.sample_acquisition_posttrigger_period_spinBox.setObjectName("sample_acquisition_posttrigger_period_spinBox")
        #Label PreTrigger
        self.pre_trigger_label = QtWidgets.QLabel(self.sample_acquisition_period_groupBox)
        self.pre_trigger_label.move(70, 38)
        self.pre_trigger_label.setFont(QtGui.QFont("Lucida Grande",9))
        self.pre_trigger_label.setObjectName("pre_trigger_label")
        #Label PostTrigger
        self.post_trigger_label = QtWidgets.QLabel(self.sample_acquisition_period_groupBox)
        self.post_trigger_label.move(225, 38)
        self.post_trigger_label.setFont(QtGui.QFont("Lucida Grande",9))
        self.post_trigger_label.setObjectName("post_trigger_label")
        
        # Trigger threshold GroupBox
        self.Threshold_groupBox = QtWidgets.QGroupBox()
        self.Threshold_groupBox.setFont(QtGui.QFont("Lucida Grande", 10))
        self.Threshold_groupBox.setObjectName("Threshold_groupBox")
        self.Threshold_spinBox = QtWidgets.QSpinBox(self.Threshold_groupBox)
        self.Threshold_spinBox.setGeometry(QtCore.QRect(120, 60, 150, 29))
        self.Threshold_spinBox.setFont(QtGui.QFont("Lucida Grande", 11))
        self.Threshold_spinBox.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.Threshold_spinBox.setObjectName("Threshold_spinBox")
        self.gridLayout.addWidget(self.Threshold_groupBox, 2, 0)

        # Picoscope Vertical Resolution GroupBox
        self.vertical_resolution_groupBox = QtWidgets.QGroupBox()
        self.vertical_resolution_groupBox.setFont(QtGui.QFont("Lucida Grande", 10))
        self.vertical_resolution_groupBox.setObjectName("vertical_resolution_groupBox")
        self.vertical_resolution_comboBox = QtWidgets.QComboBox(self.vertical_resolution_groupBox)
        self.vertical_resolution_comboBox.setGeometry(QtCore.QRect(120, 60, 150, 29))
        self.vertical_resolution_comboBox.setMinimumSize(QtCore.QSize(150, 29))
        self.vertical_resolution_comboBox.setMaximumSize(QtCore.QSize(150, 29))
        self.vertical_resolution_comboBox.setFont(QtGui.QFont("Lucida Grande", 11))
        self.vertical_resolution_comboBox.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.vertical_resolution_comboBox.setObjectName("vertical_resolution_comboBox")
        self.gridLayout.addWidget(self.vertical_resolution_groupBox, 2, 1)
        
        self.retranslateUi(PicoscopeSettings)
        self.buttonBox.accepted.connect(PicoscopeSettings.accept) # type: ignore
        self.buttonBox.rejected.connect(PicoscopeSettings.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(PicoscopeSettings)

    def retranslateUi(self, PicoscopeSettings):
        _translate = QtCore.QCoreApplication.translate
        PicoscopeSettings.setWindowTitle(_translate("PicoscopeSettings", "Picoscope Settings"))
        self.label.setText(_translate("PicoscopeSettings", "Picoscope Settings"))
        self.label_3.setText(_translate("PicoscopeSettings", "PicoScope 2206B"))
        self.Channels_groupBox.setTitle(_translate("PicoscopeSettings", "Channels"))
        self.checkBox_CHA.setText(_translate("PicoscopeSettings", "Channel A"))
        self.checkBox_CHB.setText(_translate("PicoscopeSettings", "Channel B"))
        self.sample_frequency_groupBox.setTitle(_translate("PicoscopeSettings", "Sample frequency"))
        self.sample_acquisition_period_groupBox.setTitle(_translate("PicoscopeSettings", "Acquisition period"))
        self.pre_trigger_label.setText(_translate("PicoscopeSettings", "Pre-trigger"))
        self.post_trigger_label.setText(_translate("PicoscopeSettings", "Post-trigger"))
        self.Threshold_groupBox.setTitle(_translate("PicoscopeSettings", "Trigger threshold"))
        self.vertical_resolution_groupBox.setTitle(_translate("PicoscopeSettings", "Vertical resolution"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PicoscopeSettings = QtWidgets.QDialog()
    ui = Ui_PicoscopeSettings()
    ui.setupUi(PicoscopeSettings)
    PicoscopeSettings.show()
    sys.exit(app.exec_())

from PyQt5 import QtCore, QtWidgets
import PicoSettingsWindow
import picoscope_communication as pico_com
import json

class PicoSettingsWindow(QtWidgets.QDialog, PicoSettingsWindow.Ui_PicoscopeSettings):
	def __init__(self, parent=None):
		super(PicoSettingsWindow, self).__init__(parent)
		self.setupUi(self)

		############################################
		##              Class variables           ##
		############################################
		sample_frequency_list = ["250 MSa/s", "125 MSa/s", "62.5 MSa/s", "31.25 MSa/s"]
		self.sample_frequency_comboBox.addItems(sample_frequency_list)
		vertical_resolution_list = ["20 mV", "50 mV", "100 mV", "200 mV", "500 mV", "1000 mV", "2000 mV", "5000 mV"]
		self.vertical_resolution_comboBox.addItems(vertical_resolution_list)
		self.sample_acquisition_pretrigger_period_spinBox.setRange(0, 10)
		self.sample_acquisition_pretrigger_period_spinBox.setSingleStep(1)
		self.sample_acquisition_pretrigger_period_spinBox.setSuffix(" µs")
		self.sample_acquisition_posttrigger_period_spinBox.setRange(20, 150)
		self.sample_acquisition_posttrigger_period_spinBox.setSingleStep(10)
		self.sample_acquisition_posttrigger_period_spinBox.setSuffix(" µs")
		self.Threshold_spinBox.setRange(0, 5)
		self.Threshold_spinBox.setSingleStep(1)
		self.Threshold_spinBox.setSuffix(" V")

		############################################
		##              Load Settings             ##
		############################################
		self.loadSettings()

		############################################
		##              Bind buttons              ##
		############################################
		QtCore.QMetaObject.connectSlotsByName(self)

	def accept(self):
		""" 
		In Settings window, on accept click, save the settings in Settings.json and update parameters of the Picoscope
		"""
		
		Settings = {}
		Settings["ChannelA_en"] = self.checkBox_CHA.checkState()
		Settings["ChannelB_en"] = self.checkBox_CHB.checkState()
		Settings["SamplingFrequency"] = self.sample_frequency_comboBox.currentText()
		Settings["VerticalResolution"] = self.vertical_resolution_comboBox.currentText()
		Settings["TriggerThreshold"] = self.Threshold_spinBox.value()
		Settings["AcquisitionPeriod_PreTrigger"] = self.sample_acquisition_pretrigger_period_spinBox.value()
		Settings["AcquisitionPeriod_PostTrigger"] = self.sample_acquisition_posttrigger_period_spinBox.value()

		with open('Settings.json', 'w') as f:
			json.dump(Settings, f)

		try:
			pico_com.update_frequency(float(Settings["SamplingFrequency"].split()[0]))
			pico_com.update_channelB_range(int(float(Settings["VerticalResolution"].split()[0])))
			pico_com.update_trigger_threshold(Settings["TriggerThreshold"])
			pico_com.update_sample_interval_preTrigger(Settings["AcquisitionPeriod_PreTrigger"])
			pico_com.update_sample_interval_postTrigger(Settings["AcquisitionPeriod_PostTrigger"])
			print(f"Updated Picoscope Settings: {Settings}")
		except:
			print("Picoscope settings could not be updated")

		self.close()

	def loadSettings(self):
		"""Load settings from Settings.json"""

		with open("Settings.json", "r") as f:
			SettingsDict = json.load(f)
			
		self.checkBox_CHA.setCheckState(SettingsDict["ChannelA_en"])
		self.checkBox_CHB.setCheckState(SettingsDict["ChannelB_en"])
		self.sample_frequency_comboBox.setCurrentText(SettingsDict["SamplingFrequency"])
		self.vertical_resolution_comboBox.setCurrentText(SettingsDict["VerticalResolution"])
		self.Threshold_spinBox.setValue(int(SettingsDict["TriggerThreshold"]))
		self.sample_acquisition_pretrigger_period_spinBox.setValue(int(SettingsDict["AcquisitionPeriod_PreTrigger"]))
		self.sample_acquisition_posttrigger_period_spinBox.setValue(int(SettingsDict["AcquisitionPeriod_PostTrigger"]))

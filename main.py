from PyQt5 import QtWidgets, QtGui, QtTest
from PyQt5.QtWidgets import QApplication, QShortcut, QMessageBox
from PyQt5.QtGui import QKeySequence
import pyqtgraph
import pyqtgraph.exporters
from PyQt5.QtCore import QTimer
import threading

import mainWindow
import AboutWindow
from PicoSettings import PicoSettingsWindow

import picoscope_communication as pico_com
from helper import set_logging

import serial
import sys
import os
import RPi.GPIO as GPIO
import time
import json
import os, glob

from functools import partial

from mainWindow import RED_COLOR, BLUE_COLOR, VIOLET_COLOR, LIGHT_BLUE_COLOR

SUCCESS = 0
FAILURE = -1



class MainWindow(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		
		############################################
		##            Class variables             ##
		############################################

		self.pico_connected = True # set to false if it is not connected (for debugging)
		
		
		self.channelA_checked = None
		self.channelB_checked = None
		
		self.time = [None for _ in range(3)]
		self.default_signal_array = [None for _ in range(3)]
		self.default_trigger_array = [None for _ in range(3)]
		
		# Pens for plots
		self.red_pen = pyqtgraph.mkPen(RED_COLOR)
		self.blue_pen = pyqtgraph.mkPen(BLUE_COLOR)
		self.violet_pen = pyqtgraph.mkPen(VIOLET_COLOR)
		self.light_blue_pen = pyqtgraph.mkPen(LIGHT_BLUE_COLOR)
		self.trigger_pen = self.red_pen
		self.signals_pens = [self.blue_pen, self.light_blue_pen, self.violet_pen, self.blue_pen, self.light_blue_pen, self.violet_pen]
		
		self.time_interval_ns = 0
		
		self.first_measure_done = [False for _ in range(3)]
		
		self.uart_port_array = [None for _ in range(3)]
		self.uart_serial_array = [None for _ in range(3)]
		
		#Plot windows
		self.signal_plots = [pyqtgraph.PlotWidget() for _ in range(6)]
		self.trigger_plots = [None for _ in range(6)]
		self.x_range = (0, 1000)
		self.y_range_signal = (-0.5, 0.5)
		self.y_range_trigger = (0, 5)
		
		# Number of acquisitions spinBox definition
		self.number_acquisitions_spinBox.setRange(1, 1000)
		self.number_acquisitions_spinBox.setSingleStep(1)
		self.number_acquisitions_spinBox.setValue(1)
		self.number_acquisitions = self.number_acquisitions_spinBox.value()
		
		###########################################################################################################################
		###########################################################################################################################
		###########################################################################################################################
		###########################################################################################################################
		###########################################################################################################################
		self.number_AES = [0 for i in range(16)]
		#AES spinBox definition
		standardKey = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
		for i in range(16):
			self.number_AES_spinBox[i].setRange(0, 255)
			self.number_AES_spinBox[i].setSingleStep(1)
			self.number_AES_spinBox[i].setValue(standardKey[i])
			self.number_AES = self.number_AES_spinBox[i].value()

		
		

		self.acquisition_loop_running = False
		self.number_acquisitions_done = 0
		self.acquisition_period_ms = 1000
		
		self.analysis_plain_text = []
		self.analysis_cipher_text = []
		
		############################################
		##             Init functions             ##
		############################################
		self.init_UART()
		self.init_GPIO()
		self.import_default_traces() # run before init_graphs() to have a proper data range in the plots
		self.init_graphs()
		self.set_signal_resolution(None)
		self.stackedWidget.setCurrentIndex(1)
		# self.CB_PicoSettingsButton.hide()
		self.StopAES_Button.hide()
		# self.sidebar_widget.hide()
		############################################
		##               Picoscope                ##
		############################################

		try:
			pico_com.init_picoscope()
		except:
			self.show_alert("Picoscope not found! Please restart the application after plugging in the Picoscope.")
			self.pico_connected = False
		
		############################################
		##              Bind buttons              ##
		############################################

		self.StartAES_Button.clicked.connect(self.on_start_AES_button)
		self.StopAES_Button.clicked.connect(self.on_stop_AES_button)
		self.CB_PicoSettingsButton.clicked.connect(self.open_PicoSettingsWindow)
		self.PlainText_random_Button.clicked.connect(self.on_plain_text_random_button)
		self.actionQuit.triggered.connect(self.close)
		self.actionAbout_the_app.triggered.connect(self.open_AboutAppWindow)
		self.Home_LaunchButton.clicked.connect(self.home_launch_button_clicked)
		self.PlainText_input.textChanged.connect(self.text_changed)
		for index in range(4):
			self.default_trace_check_box[index].stateChanged.connect(self.check_default_trace)
		for i in range(3):
			self.start_analysis_buttons[i].clicked.connect(partial(self.OnStartAnalysisButton,i))
		
		self.Change_AES_Key_Button.clicked.connect(self.AES_Change_Button_Clicked)

		############################################
		##              Shortcuts                 ##
		############################################

		self.HomeShortcutEnter = QShortcut(QKeySequence("o"), self)
		self.HomeShortcutEnter.activated.connect(self.home_launch_button_clicked)

		self.SendShortcut = QShortcut(QKeySequence("s"), self)
		self.SendShortcut.activated.connect(self.on_start_AES_button)
		
		self.QuitShortcut = QShortcut(QKeySequence("q"), self)
		self.QuitShortcut.activated.connect(self.close)
		
		self.tabWidget.currentChanged.connect(self.on_change_tab)
		
	def closeEvent(self, event):
		"""
		Callback function to handle closing events: closes serial ports, picoscope and GPIOs
		
		Parameters:
		- event
		
		Return:
		None
		"""
		
		close = QtWidgets.QMessageBox.question(self, 'Message',"Are you sure to quit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		if close == QtWidgets.QMessageBox.Yes:
			
			# close picoscope
			try: 
				if self.pico_connected:
					pico_com.close_picoscope()
					logger.debug("Picoscope closed")
			except:
				logger.debug(f"Picoscope could not be closed")
				
			
			# Shut down all LEDs
			for i in range(3):
				self.send_char('L', i)
			
			# Close all serial ports
			for i in range(3):
				if self.uart_port_array[i]:
					try:
						self.uart_serial_array[i].close()
						logger.debug(f"{self.uart_port_array[i]} closed")
					except:
						logger.debug(f"{self.uart_port_array[i]} could not be closed")
			
			GPIO.cleanup() # Disable GPIO safely before quitting
			logger.debug("GPIOs disabled")
			event.accept()
		else:
			event.ignore()
		
	def show_alert(self, message: str) -> None:
		"""
		open an alert window with a message
		
		Parameters:
		- message:			string
							message to show in the alert
		
		Return:
		None
		"""
		alert = QMessageBox(self)
		alert.setWindowTitle("Alert")
		alert.setText(message)
		alert.setIcon(QMessageBox.Critical)
		alert.setStandardButtons(QMessageBox.Ok)
		alert.exec()

	def init_graph(self, index: int) -> None:
		"""
		Init a plot window
		
		Parameters:
		- index:			int
							index of the plot window (0 to 2 for single plots and 3 to 5 for the last tab)
		
		Return:
		None
		"""
		show_context_menu = False
		
		tick_font = QtGui.QFont()
		tick_font.setPixelSize(12)
		axis_style = {'font-size':'12px'}
		if 2 < index < 6: # last tab
			axis_style = {'font-size':'9px'}
			tick_font.setPixelSize(8)
		
		self.signal_plots[index].setLabel('bottom', 'Time (µs)', **axis_style)
		self.signal_plots[index].setLabel('left', 'Electromagnetic field', units='V', **axis_style)
		self.signal_plots[index].setLabel('right', 'Trigger', units='V', **axis_style)
		
		self.signal_plots[index].getAxis('left').setPen(self.signals_pens[index])
		self.signal_plots[index].getAxis('right').setPen(self.trigger_pen)
		self.signal_plots[index].getAxis('bottom').setStyle(tickFont = tick_font)
		self.signal_plots[index].getAxis('left').setStyle(tickFont = tick_font)
		self.signal_plots[index].getAxis('right').setStyle(tickFont = tick_font)
		
		self.trigger_plots[index] = pyqtgraph.ViewBox(enableMenu=show_context_menu)
		self.signal_plots[index].scene().addItem(self.trigger_plots[index])
		self.signal_plots[index].getAxis("right").linkToView(self.trigger_plots[index])
		self.trigger_plots[index].setXLink(self.signal_plots[index])
		
		self.signal_plots[index].setBackground('w')
		self.signal_plots[index].setRange(xRange=self.x_range, yRange=self.y_range_signal, padding=0, disableAutoRange=True)
		self.trigger_plots[index].setRange(xRange=self.x_range, yRange=self.y_range_trigger, padding=0, disableAutoRange=True)
		
		# update view if the window is changed
		self.signal_plots[index].getViewBox().sigResized.connect(self.view_updated_callback)
		
		# disable scrolling, panning and context menu
		self.signal_plots[index].setMouseEnabled(x=False, y=False)
		self.trigger_plots[index].setMouseEnabled(x=False, y=False)
		self.signal_plots[index].hideButtons()
		self.signal_plots[index].setMenuEnabled(show_context_menu)
		
		if 0 <= index < 3: #individual plot
			exec(f"self.gridLayout_tab{index+1}.addWidget(self.signal_plots[{index}], 0, 0, 2, 3)")
			
		elif 2 < index < 6: # last tab
			self.gridLayout_tab4.addWidget(self.signal_plots[index], index, 0, 1, 2)

	def init_graphs(self) -> None:
		"""Initialise 6 empty graphs"""
		
		for index in range(6):
			self.init_graph(index)
		
		# update view if the window is changed
		self.view_updated_callback()
		
	def view_updated_callback(self) -> None:
		"""update the 6 plot views if the window has changed"""

		# setup for all graphs in the last tab
		for i in range(6):
			self.trigger_plots[i].setGeometry(self.signal_plots[i].getViewBox().sceneBoundingRect())
			self.trigger_plots[i].linkedViewChanged(self.signal_plots[i].getViewBox(), self.trigger_plots[i].XAxis)
			self.signal_plots[i].setRange(xRange=self.x_range, yRange=self.y_range_signal, padding=0, disableAutoRange=True)
			self.trigger_plots[i].setRange(xRange=self.x_range, yRange=self.y_range_trigger, padding=0, disableAutoRange=True)
		
	def save_trace(self, filename: str, microcontroller: int, signal_only_filename: str="") -> int:
		"""
		Stop the picoscope and store the captured data to a file
		
		Parameters:
		- filename:				str
								path of the file to save
		- microcontroller:		int
								index of the plot window (from 0 to 2)
		- signal_only_filename:	str
								path to the file to save only the channel B data
								if no argument is provided or it is "", the file won't be created
		
		Return:
		int: either SUCCESS or FAILURE if an issue appeared with the picoscope
		"""
		
		
		time, trigger, signal = pico_com.postcapture(self.time_interval_ns) # ALWAYS AFTER PRECAPTURE
		
		if time is None:
			pico_com.stop_picoscope()
			self.show_alert("Picoscope could not retrieve values. If problem persists, restart your Raspberry Pi!")
			return FAILURE
		
		
		pico_com.store_capture_in_file(time, trigger, signal, filename)
		
		if signal_only_filename != "":
			self.save_signal_only(signal, signal_only_filename)

		self.first_measure_done[microcontroller] = True
		return SUCCESS
		
	def plot_latest_trace(self, index: int, take_new_measure: bool) -> None:
		"""
		If take_new_measure is true, take a new measure with the picoscope.
		Otherwise, load and plot the latest file saved in the raspberry pi
		plot the latest measure in the given index tab and save 
		
		Parameters:
		- index:				int
								index of the plot window (from 0 to 2)
		- take_new_measure:		bool
								set to False to load the latest file and plot it without new measure
		
		Return:
		None
		"""
		
		names = ["Unprotected", "Passive", "ChaXa"]
		filename = f"Traces/{names[index]}_latest.txt"
		
		if take_new_measure:
			success = self.save_trace(filename, index)
			if success != SUCCESS:
				return None
		self.plot_trace(index, filename)
		logger.debug("Acquisition completed!")
		
	def plot_trace(self, index: int, filename: str) -> None:
		"""
		Plot the latest measure in the given index
		
		Parameters:
		- index:			int
							index of the plot window (0 to 2)
		- filename:			str
							path of the file to plot
		
		Return:
		None
		"""
		
		time, trigger, signal = pico_com.retrieve_data_from_file(filename)
		self.default_trace_check_box[index].setChecked(False)
		self.default_trace_check_box[3].setChecked(False)
		
		self.set_signal_resolution(None)
		self.set_temporal_resolution(time)
		self.view_updated_callback()
		
		# clear the previous plots
		self.signal_plots[index].clear()
		self.signal_plots[index+3].clear()
		self.trigger_plots[index].clear()
		self.trigger_plots[index+3].clear()
		
		# plot in main tab
		if self.channelB_checked:
			self.signal_plots[index].plot(time, signal, pen=self.signals_pens[index]) # Channel B
		if self.channelA_checked:
			self.trigger_plots[index].addItem(pyqtgraph.PlotCurveItem(x=time, y=trigger, pen=self.trigger_pen)) # Channel A
			
		# plot in last tab
		if self.channelB_checked:
			self.signal_plots[index+3].plot(time, signal, pen=self.signals_pens[index+3])
		if self.channelA_checked:
			self.trigger_plots[index+3].addItem(pyqtgraph.PlotCurveItem(x=time, y=trigger, pen=self.trigger_pen))
		
	def plot_default_trace(self, index: int) -> None:
		"""
		Plot the default trace in the given index tab
		
		Parameters:
		- index:			int
							index of the plot window (0 to 3)
		
		Return:
		None
		"""
	
		if index == 3: # plot all traces in last tab
			for i in range(3):
				self.signal_plots[i+3].clear()
				self.trigger_plots[i+3].clear()
				self.signal_plots[i+3].plot(self.time[i], self.default_signal_array[i], pen=self.signals_pens[i])
				self.trigger_plots[i+3].addItem(pyqtgraph.PlotCurveItem(x=self.time[i], y=self.default_trigger_array[i], pen=self.trigger_pen))
			
			self.set_temporal_resolution(self.time[0]) # use the unprotected window as reference for the other windows
			self.set_signal_resolution(None)
			#self.set_signal_resolution(self.default_signal_array[0])
		else:
			self.signal_plots[index].clear()
			self.trigger_plots[index].clear()
			self.signal_plots[index].plot(self.time[index], self.default_signal_array[index], pen=self.signals_pens[index])
			self.trigger_plots[index].addItem(pyqtgraph.PlotCurveItem(x=self.time[index], y=self.default_trigger_array[index], pen=self.trigger_pen))
		
			self.set_temporal_resolution(self.time[index])
			self.set_signal_resolution(None)
			#self.set_signal_resolution(self.default_signal_array[0])
		self.view_updated_callback()
	
	def on_change_tab(self, currentIndex):
		"""
		Callback launched when the tab is changed
		
		Parameters:
		- currentIndex:		int
							index of the plot window (0 to 3)
		
		Return:
		None
		"""
		
		
		for i in range(3):
			self.send_char('L', i) # shut down all LEDs
		
		if currentIndex < 3:
			self.send_char('H', currentIndex) # turn on the current LED
		
		if currentIndex in range (3):
			self.Text_encryption_groupBox.show()
			self.StartAES_Button.show()
			self.number_acquisitions_label.show()
			self.number_acquisitions_spinBox.show()
			#self.sidebar_layout.show()
		else:
			self.Text_encryption_groupBox.hide()
			self.StartAES_Button.hide()
			self.number_acquisitions_label.hide()
			self.number_acquisitions_spinBox.hide()
			#self.sidebar_layout.hide()
	
	def is_plaintext_correct(self) -> bool:
		""" Return True if the plaintext has 32 hexa characters """
		
		# do nothing if plain text is empty
		if self.PlainText_input.text() == "":
			self.show_alert("Plain text is empty!")
			return False
		
		if len(self.PlainText_input.text()) == 1:
			self.show_alert(f"Missing characters in plain text (1 was found but 32 are expected).")
			return False
		elif len(self.PlainText_input.text()) == 31:
			self.show_alert(f"Missing character in plain text (31 were found but 32 are expected).")
			return False
		elif len(self.PlainText_input.text()) < 31:
			self.show_alert(f"Missing characters in plain text ({len(self.PlainText_input.text())} were found but 32 are expected).")
			return False
		
		try:
			int(self.PlainText_input.text(), 16)
		except ValueError:
			self.show_alert("Unknown character found in plain text.")
			return False
		
		return True

	def on_start_AES_button(self) -> None:
		"""Callback of the Start AES Button"""
		self.number_acquisitions = self.number_acquisitions_spinBox.value()
		self.channelA_checked = self.import_pico_settings("ChannelA_en") != 0.0
		self.channelB_checked = self.import_pico_settings("ChannelB_en") != 0.0
		
		if self.number_acquisitions == 1:
			success = self.start_single_acquisition()
			if success != SUCCESS:
				return None
			self.plot_latest_trace(self.tabWidget.currentIndex(), self.pico_connected)
		else:
			success = self.init_multiple_acquisitions()
			if success != SUCCESS:
				return None
			self.perform_multiple_acquisitions()

	def on_stop_AES_button(self) -> None:
		"""Callback of the Stop AES Button"""
		logger.debug("Stop AES Button clicked")
		self.stop_multiple_acquisitions()

	def start_single_acquisition(self) -> int:
		"""
		Start an acquisition, return SUCCESS if the acquisition was successful and FAILURE otherwise
		"""
		if not self.is_plaintext_correct():
			self.CipherText_display_label.setText("") # set cipher text to empty string to reset the textbox if an error occured
			return FAILURE

		if self.stackedWidget.currentIndex():
			return FAILURE

		currentIndex = self.tabWidget.currentIndex()
		
		if currentIndex == 0:
			logger.debug(f"Sending data for signal 1")
			self.set_mux(1)

		elif currentIndex == 1:
			logger.debug(f"Sending data for signal 2")
			self.set_mux(2)

		elif currentIndex == 2:
			logger.debug(f"Sending data for signal 3")
			self.set_mux(3)

		else:
			return FAILURE
		
		"""Configure the Picoscope"""
		
		if self.pico_connected:
			self.time_interval_ns = pico_com.precapture() # RUN ALWAYS POSTCAPTURE OR STOP_PICOSCOPE AFTER PRECAPTURE
				
		success = self.send_plain_text(currentIndex) # Once Picoscope is ready, send command to ATMega
		if success != SUCCESS:
			logger.debug(f"Could not send plain text")
			pico_com.stop_picoscope()
			return FAILURE
		
		if self.receive_cipher_text(currentIndex):
			logger.debug(f"Could not receive cipher text")
			pico_com.stop_picoscope()
			return FAILURE
			
		return SUCCESS

	def init_multiple_acquisitions(self) -> int:
		"""
		Prepare a multiple acquisition
		return SUCCESS if the multiple acquisitions can start properly, FAILURE otherwise
		"""
		if not self.is_plaintext_correct():
			self.CipherText_display_label.setText("") # set cipher text to empty string to reset the textbox if an error occured
			return FAILURE
		
		if not self.pico_connected:
			logger.debug("Picoscope is not connected!")
			return FAILURE
			
		names = ["Unprotected", "Passive", "ChaXa"]
		directory = f"./Traces/Analysis/{names[self.tabWidget.currentIndex()]}/*"
		for item in glob.glob(directory, recursive=True):
			os.remove(item)
		
		self.acquisition_loop_running = True
		self.number_acquisitions_done = 0
		
		self.analysis_plain_text = []
		self.analysis_cipher_text = []
		
		self.CB_PicoSettingsButton.setEnabled(False)
		self.PlainText_random_Button.setEnabled(False)
		self.tabWidget.setEnabled(False)
		self.number_acquisitions_spinBox.setEnabled(False)
		self.PlainText_input.setEnabled(False)
		
		self.StopAES_Button.show()
		self.StartAES_Button.hide()
		return SUCCESS
		
	def can_take_new_measure(self) -> bool:
		"""
		Return True if a new acquisition can start and launch a new acquisition
		Otherwise, stop the acquisitions and return false
		"""
		if self.number_acquisitions_done < self.number_acquisitions and self.acquisition_loop_running:
			QTimer.singleShot(self.acquisition_period_ms, self.perform_multiple_acquisitions)
			return True
		else:
			self.stop_multiple_acquisitions()
			return False

	def perform_multiple_acquisitions(self) -> None:
		"""
		perform acquisitions in a row
		this function is launched by QTimer.singleShot() with a period self.acquisition_period_ms
		"""
		
		index = self.tabWidget.currentIndex()
		names = ["Unprotected", "Passive", "ChaXa"]
		
		if self.can_take_new_measure():
			
			trace_filename = f"Traces/{names[index]}_latest.txt"
			signal_only_filename = f"Traces/Analysis/{names[index]}/{names[index]}{self.number_acquisitions_done}.txt"
			
			# generate new random plain text and save it
			self.on_plain_text_random_button()
			self.analysis_plain_text.append(self.PlainText_input.text())
			
			logger.debug(trace_filename)
			logger.debug(signal_only_filename)
			self.number_acquisitions_done += 1
			self.number_acquisitions_spinBox.setValue(self.number_acquisitions_done)
			
			success_start = self.start_single_acquisition()
			if success_start != SUCCESS:
				# if an error occurs, stop acquisition
				self.acquisition_loop_running = False
				self.stop_multiple_acquisitions()
				return None
			
			
			success_save = self.save_trace(trace_filename, index, signal_only_filename)
			if success_save != SUCCESS:
				# if an error occurs, stop acquisition
				self.acquisition_loop_running = False
				self.stop_multiple_acquisitions()
				return None
			
			# save cipher text
			self.analysis_cipher_text.append(self.CipherText_display_label.text())
			
			self.plot_trace(index, trace_filename)
		
	def stop_multiple_acquisitions(self) -> None:
		"""Handle the interruption of multiple acquisitions"""
		self.StopAES_Button.hide()
		self.StartAES_Button.show()
		self.acquisition_loop_running = False
		
		#save plain and cipher texts
		self.save_plain_and_cipher_texts()
		
		self.CB_PicoSettingsButton.setEnabled(True)
		self.PlainText_random_Button.setEnabled(True)
		self.tabWidget.setEnabled(True)
		self.number_acquisitions_spinBox.setEnabled(True)
		self.PlainText_input.setEnabled(True)
	
	def save_plain_and_cipher_texts(self) -> None:
		"""
		Save plain and cipher texts to the file "Traces/Analysis/MICROCONTROLLER/MICROCONTROLLER_plain_cipher_texts.txt"
		depending on the opened tab
		"""
		
		index = self.tabWidget.currentIndex()
		names = ["Unprotected", "Passive", "ChaXa"]
		filename = f"Traces/Analysis/{names[index]}/{names[index]}_plain_cipher_texts.txt"
		
		with open(filename,'w') as data_file:
			data_file.write(str(len(self.analysis_plain_text))+'\n')
			
			for plain_text in self.analysis_plain_text:
				data_file.write(plain_text+'\n')
			for cipher_text in self.analysis_cipher_text:
				data_file.write(cipher_text+'\n')
	
	def save_signal_only(self, signal: list[float], filename: str) -> None:
		"""Save to @filename the data contained in @signal"""
		with open(filename,'w') as data_file:
			data_file.write(str(len(signal))+'\n')
			
			for point in signal:
				data_file.write(f"{point}\n")
		
	def set_mux(self, index: int) -> None:
		"""Change both mux pins to select trigger source"""
		assert index in range(1,4), "Index of Mux is not equal to 1, 2 or 3"
		MUX_CHA1 = 2	#GPIO2
		MUX_CHB1 = 3	#GPIO3

		try:
			if index == 1:
				GPIO.output(MUX_CHA1, GPIO.LOW)
				GPIO.output(MUX_CHB1, GPIO.LOW)
				logger.debug("Mux Set to MCU1")
			elif index == 2:
				GPIO.output(MUX_CHA1, GPIO.HIGH)
				GPIO.output(MUX_CHB1, GPIO.LOW)
				logger.debug("Mux Set to MCU2")
			elif index == 3:
				GPIO.output(MUX_CHA1, GPIO.LOW)
				GPIO.output(MUX_CHB1, GPIO.HIGH)
				logger.debug("Mux Set to MCU3")

		except:
			logger.error("Failed to set mux")

	def listen_uart(self, index):
		"""Listen to the UART and print the received data"""
		ser = self.uart_serial_array[index]
			
		while True:
			if ser:
				try:
					logger.debug(ser.readline().decode('utf-8').rstrip())
				except:
					#wait 0.001s before trying again
					time.sleep(0.001)
				
	
	
	def init_UART(self) -> None:
		"""Uart initialisation. Check on which port is connected each microcontroller"""
		PORTLIST = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2"]
		for port in PORTLIST:
			try:
				with serial.Serial(port, baudrate=115200, timeout=0.5) as ser:
					ser.write(b'T')
					ser.reset_input_buffer()
					start = time.time()
					while (ser.in_waiting <= 0) and (time.time() - start <= 1): # wait until 1 second
						continue
					response = ser.readline().decode('utf-8').rstrip()
					logger.debug(f"Microcontroller type: {response}")
					if response == "Unprotected":
						self.uart_port_array[0] = port
					elif response == "Passive":
						self.uart_port_array[1] = port
					elif response == "ChaXa" or response == "IChaXa" or response == "ChaXaI" or response == "IChaXaI":
						self.uart_port_array[2] = port
					else:
						raise NameError(f"Microcontroller on port {port} doesn't have the right name")
							
			except :
				logger.warning(f"Failed to initialise {port}")


		port_names = ["UnprotectedSerial", "PassiveSerial", "ChaXaSerial"]
		for i in range(3):
			try:
				self.uart_serial_array[i] = serial.Serial(self.uart_port_array[i], baudrate=115200)
				logger.debug(f"{port_names[i]} on port {self.uart_port_array[i]}")
			except:
				logger.warning(f"Failed to set {port_names[i]}")
		
		# #begin listenging thread
		# self.uart_thread = [None for _ in range(3)]
		# for i in range(3):
		# 	self.uart_thread[i] = threading.Thread(target=self.listen_uart, args=(i,))
		# 	self.uart_thread[i].start()
		# logger.debug("UART threads started. Waiting for messages...")
		
	def init_GPIO(self) -> None:
		""" Init GPIOs 2 and 3 to pilot the mux"""
		GPIO.setmode(GPIO.BCM)
		try:
			for i in range(2,4):
				GPIO.setup(i, GPIO.OUT)
				logger.debug(f"GPIO number {i} initialized")
		except:
			logger.warning('Failed to initialise GPIO')
		
	def home_launch_button_clicked(self) -> None:
		"""Show and initialise signal visualisation window"""

		self.stackedWidget.setCurrentIndex(0)
		self.tabWidget.setCurrentIndex(0)
		self.on_change_tab(0)
		self.CB_PicoSettingsButton.show()



	def open_PicoSettingsWindow(self) -> None:
		"""Open Picoscope settings window"""

		self._pico_window = PicoSettingsWindow()
		self._pico_window.show()

	def on_plain_text_random_button(self) -> None:
		"""Randomly generate 16 bytes and udpate the PlainText widget"""

		self.PlainText_input.setText(os.urandom(16).hex().upper())
		self.CipherText_display_label.setText("")
	
	def text_changed(self) -> None:
		"""Detect text changes in Plain text selection"""
		self.CipherText_display_label.setText("")
		
	def check_default_trace(self) -> None:
		"""
		Check state of CheckBox for Default trace
		"""
		index = self.tabWidget.currentIndex()
		if self.default_trace_check_box[index].isChecked():
			if index == 3:
				self.plot_default_trace(index)
			else:
				self.plot_default_trace(index)
		else:
			if index == 3:
				for i in range(3):
					self.signal_plots[i+3].clear()
					self.trigger_plots[i+3].clear()
					
					logger.debug(self.first_measure_done)
					# plot the last graph if the box is unchecked and a previous acquisition has been performed
					if self.first_measure_done[i]:
						self.plot_latest_trace(i, False)
						
			else:
				self.signal_plots[index].clear()
				self.trigger_plots[index].clear()
					
				# plot the last graph if the box is unchecked and a previous acquisition has been performed
				if self.first_measure_done[index]:
					self.plot_latest_trace(index, False)
	
	def open_AboutAppWindow(self) -> None:
		"""Show About window"""
		self._about_window = AboutAppWindow()
		self._about_window.show()
	
	def send_char(self, char: str, index: int) -> None:
		"""Send a @char to the microcontroller @index"""
		assert len(char) == 1, "Char must contain exactly one character"
		assert index in range(3), "Index of microcontroller is not equal to 0, 1 or 2"
		port = self.uart_port_array[index]
		ser = self.uart_serial_array[index]
		
		try:
			ser.reset_input_buffer() # reset buffer to avoid receiving a wrong cipher text remaining in the buffer
			ser.write(char.encode("ASCII")) # self.PlainText_input.text() need to be converted to ascii
		except: 
			logger.error(f"Failed to send {char} on port {port}")
		
	def send_plain_text(self, index: int) -> int:
		"""Send the value from the PlainText_input widget to the three microcontrollers
		
		Parameters:
		- index:				int
								index of the microcontroller (from 0 to 2)
		
		Return:
		int: either SUCCESS or FAILURE if the plaintext is not sent properly
		"""
		
		assert index in range(3), "Index of microcontroller is not equal to 0, 1 or 2"
		port = self.uart_port_array[index]
		ser = self.uart_serial_array[index]
		plainText = self.PlainText_input.text().encode("ASCII") # self.PlainText_input.text() need to be converted to ascii
		
		try:
			ser.reset_input_buffer() # reset buffer to avoid receiving a wrong cipher text remaining in the buffer
			ser.write(b'E')
			ser.write(plainText)
			logger.debug(f'Plain text : {plainText}')
			return SUCCESS
		except: 
			logger.error(f'Failed to send PlainText on port {port}')
			return FAILURE
			
	def receive_cipher_text(self, index: int) -> int:
		"""Receive the cipher text from one of the microcontrollers
		
		Parameters:
		- index:				int
								index of the microcontroller (from 0 to 2)
		
		Return:
		int: either SUCCESS or FAILURE if the ciphertext has not an appropriate format
		"""
		assert index in range(3), "Index of microcontroller is not equal to 0, 1 or 2"
		port = self.uart_port_array[index]
		ser = self.uart_serial_array[index]
		
		try:
			start = time.time()
			while (ser.in_waiting <= 0) and (time.time() - start <= 1) :
				continue
			cipher = ser.readline().decode('utf-8').rstrip()
			
			if index == 2: # if chaxa microcontroller sent "I", remove it
				cipher = cipher.replace("I", "")
			
			if cipher == "Missing character(s)! Please try again.":
				ser.reset_input_buffer()
				logger.warning("Missing character(s)! Please try again.")
				cipher = ""
				self.show_alert(f"Missing character(s) in plain text ({len(self.PlainText_input.text())} were found but 32 are expected).")
				return FAILURE
			elif cipher == "One character wasn't between neither 0-9, nor A-F. Please try again.":
				ser.reset_input_buffer() # reset buffer to avoid receiving a wrong cipher text remaining in the buffer
				logger.warning("One character wasn't between neither 0-9, nor A-F. Please try again.")
				cipher = ""
				self.show_alert("Unknown character found in plain text.")
				return FAILURE
			else:
				logger.debug(f"Cipher Text: {cipher}")
			
			self.CipherText_display_label.setText(cipher) # set cipher text to empty string to reset the textbox if an error occured
				
		except:
			logger.error(f'Failed to receive CipherText on port {port}')
			self.CipherText_display_label.setText("") # set cipher text to empty string to reset the textbox if an error occured
			return FAILURE
		return SUCCESS
		
	def import_default_traces(self) -> None:
		"""Import the three default traces at start"""
		
		names = ["Unprotected", "Passive", "ChaXa"]
		for i in range(3):
			self.time[i], self.default_trigger_array[i], self.default_signal_array[i] = pico_com.retrieve_data_from_file(f"Traces/{names[i]}_default.txt")
		
	
	def import_pico_settings(self, setting : str) -> float:
		""" Open Settings.json and return the corresponding @setting converted to float
		
		Parameters:
		- setting:			str
							name of the setting to import in the JSON file
		
		Return:
		float: parameter converted to float or 0.0 by default
		"""
		with open("Settings.json", "r") as f:
			settings_dict = json.load(f)
			parameter = settings_dict[setting]
			if isinstance(parameter, str):
				return float(parameter.split()[0])
			elif isinstance(parameter, int):
				return float(parameter)
			else:
				raise TypeError("Parameter's type should be int or str")
		return 0.0
	
	def set_temporal_resolution(self, data: list[float]) -> None:
		"""
		adapt the x-axis to the data
		"""
		self.x_range = (data[0], data[-1])

	def set_signal_resolution(self, data: list[float]) -> None:
		"""
		adapt y-axis to the channel B (signal)
		if data is None, adapt the window to the Picoscope settings in the JSON file
		"""
		if data is None:
			vertical_resolution = self.import_pico_settings("VerticalResolution") / 1000 # convert to mV
			self.y_range_signal = (-vertical_resolution, vertical_resolution)
		else:
			max_value = max(abs(min(data)), abs(max(data)))
			enlargement_factor = 4
			self.y_range_signal = (-max_value*enlargement_factor, max_value*enlargement_factor)
	
	def OnStartAnalysisButton(self, index) -> None:
		logger.debug(f"Button {index} clicked")
		self.loading_bars_labels[index].show()
		self.loading_bars[index].show()
		self.key_groupbox[index].show()


	def base10tohex(self, base10: int) -> str:
		"""Convert a base 10 number to a 2 characters hexa string"""
		hexa = hex(base10)[2:]
		if len(hexa) == 1:
			hexa = "0" + hexa
		return hexa



	def AES_Change_Button_Clicked(self) -> None:
		new_key = [i.value() for i in self.number_AES_spinBox]
		

		try:
			#change of key
			for i in range(3):			
				self.send_char('J', i)

			for j in self.number_AES_spinBox:
				for i in range(3):

					self.send_char(self.base10tohex(j.value())[0], i)
					self.send_char(self.base10tohex(j.value())[1], i)
				
			logger.debug('AES Key changed')
		except:
			logger.debug('Unable to change AES Key')




		

class AboutAppWindow(QtWidgets.QDialog, AboutWindow.Ui_AboutAppDialog):
	def __init__(self, parent=None):
		super(AboutAppWindow, self).__init__(parent)
		self.setupUi(self)



if __name__ == "__main__":
	logger = set_logging(logging_level="DEBUG", logging_file=False)
	app = QApplication(sys.argv)
	form = MainWindow()
	
	form.show()
	app.exec_()

	

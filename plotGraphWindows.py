from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

class MainWindow(QtWidgets.QMainWindow):

	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.graphWidget = pg.PlotWidget()
		self.setCentralWidget(self.graphWidget)

		
		self.time = [None for i in range(3)]
		self.default_channelA_array = [None for i in range(3)]
		self.default_channelB_array = [None for i in range(3)]
		

		limits = {"xMin": 0, "xMax": 60, "yMin": 0, "yMax": 5}
		limits["minXRange"] = limits["xMin"]
		limits["maxXRange"] = limits["xMax"]
		limits["minYRange"] = limits["yMin"]
		limits["maxYRange"] = limits["yMax"]
		self.graphWidget.setLimits(**limits)
		print(limits)
		self.graphWidget.setBackground('w')
		# self.graphWidget.setDefaultPadding(padding=0.1)





		self.import_default_traces()
		self.graphWidget.plot(self.time[0], self.default_channelA_array[0], pen=pg.mkPen(color=(255, 0, 0)))
		self.graphWidget.plot(self.time[0], self.default_channelB_array[0], pen=pg.mkPen(color=(0, 255, 0)))
	

	
	"""
	Return the three data blocks stored in filename (time, PCB and probe measures)

	Parameters:
	- filename:			String
						Path of the file to be opened

	Return:
	- time:				Float list
						Time signatures of the measures
	- PCB_measures:		Float list
						Measures of the picoscope's channel A corresponding to the PCB measures
	- probe_measures:	Float list
						Measures of the picoscope's channel B corresponding to the probe measures

	"""
	def retrieve_data_from_file(self, filename):
		time=[]
		PCB_measures=[]
		probe_measures=[]

		try:
			data_file = open(filename,'r')
		except:
			print(f"{filename} has not been found")
			# ShowAlert()
			return None
		
		data_text = data_file.read()
		
		data = data_text.split('\n')
		len_data = int(float(data[0]))
		i=1
		for j in range(len_data):
			time.append(float(data[i]))
			i+=1
		for j in range(len_data):
			PCB_measures.append(float(data[i]))
			i+=1
		for j in range(len_data):
			probe_measures.append(float(data[i]))
			i+=1
		
		data_file.close()
		
		return time, PCB_measures, probe_measures

	def import_default_traces(self) -> None:
		names = ["Unprotected", "Passive", "ChaXa"]
		for i in range(3):
			self.time[i], self.default_channelA_array[i], self.default_channelB_array[i] = self.retrieve_data_from_file(f"D:/Documents/Ecole/EMSE/PE/pe-chaxa-2023/Raspberry/Traces/{names[i]}_default.txt")


def main():
	app = QtWidgets.QApplication(sys.argv)
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
"""
Created on Thu Mar  2 11:39:05 2023

PE ChaXa 2023
Ecole des Mines de Saint-Etienne ISMIN & CEA
By: Bastien Joachim, Sam Fiette, Delphine Gesse

@author: delph

@description: (for Picoscope 2000 device)
    Provides functions allowing to open a 2000 driver device, initialise it for block mode capture and capture measures. The picoscope's parameters can be changed by calling one of the update functions.
    

Resource used:

Copyright © 2018-2019 Pico Technology Ltd.
Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""
# This example opens a 2000a driver device, sets up two channels and a trigger then collects a block of data.

"""
Import
"""
import ctypes
import numpy as np
from picosdk.ps2000a import ps2000a as ps
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok
import logging
import json
import time

"""
Global variables
"""
chARange = 8 # range = PS2000A_5V = 8
chBRange = 4 # range = PS2000A_200MV = 4
timebase = 2 # freq = 125 MHz
preTriggerSamples = 500
postTriggerSamples = 6500
threshold = 8192 # ADC counts
# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}



""" __________________Update Picoscope parameters____________________"""

def update_frequency(freq):
	"""
	Update the picoscope's sampling frequency

	Parameters:
	- freq:		Float
				Frequency in MHz

	Good to know:
	- timebase = 1	-->	freq = 250 MHz
	- timebase = 2	-->	freq = 125 MHz
	- timebase = 3	-->	freq = 62.5 MHz
	- timebase = 4	-->	freq = 31.25 MHz

	"""
	global timebase
	if(freq==250):
		timebase = 1
	elif(freq==125):
		timebase = 2
	elif(freq==62.5):
		timebase = 3
	elif(freq==31.25):
		timebase = 4
	else:
		print("Frequency could not be updated")



def update_preTriggerSamples(number):
	"""
	Update the picoscope's number of preTriggerSamples

	Parameters:
	- number:	int
				Number of pre trigger sample to acquire
	"""
	global preTriggerSamples
	preTriggerSamples = number

def update_channelB_range(Vrange):
	"""
	Update the picoscope' volt range for its channel B
	
	Parametrers:
	- Vrange:	int
				Maximum range in mV (+/-Vrange)
	"""
	global chBRange
	
	if(Vrange==20):
		chBRange = 1
	elif(Vrange==50):
		chBRange = 2
	elif(Vrange==100):
		chBRange = 3
	elif(Vrange==200):
		chBRange = 4
	elif(Vrange==500):
		chBRange = 5
	elif(Vrange==1000):
		chBRange = 6
	elif(Vrange==2000):
		chBRange = 7
	elif(Vrange==5000):
		chBRange = 8
	else:
		print("Channel range could not be updated")
	
	# Set up channel B --> connected to probe
	""" Parameters
	handle = chandle
	channel = PS2000A_CHANNEL_B = 1
	enabled = 1
	coupling type = PS2000A_DC = 1
	range = PS2000A_5V = 8
	analogue offset = 0 V
	"""
	status["setChB"] = ps.ps2000aSetChannel(chandle, 1, 1, 1, chBRange, 0)
	assert_pico_ok(status["setChB"])

def update_sample_interval_preTrigger(time):
	"""
	Update the picoscope's number of preTrigger samples through its sample inverval value
	number of pre trigger samples = frequency * time interval [MHz*µs]

	Parameters:
	- time:		int
				Acquisition time in µs
	
	"""
	if(timebase==1):
		freq=250
	elif(timebase==2):
		freq=125
	elif(timebase==3):
		freq=62.5
	elif(timebase==4):
		freq=31.25
	else:
		freq = 0
		print("Error: picoscope timebase configuration is faulty")
	pre = int(time*freq)
	update_preTriggerSamples(pre)

def update_sample_interval_postTrigger(time):
	"""
	Update the picoscope's number of postTrigger samples through its sample inverval value
	number of post trigger samples = frequency * time interval [MHz*µs]

	Parameters:
	- time:		int
				Acquisition time in µs
	
	"""
	if(timebase==1):
		freq=250
	elif(timebase==2):
		freq=125
	elif(timebase==3):
		freq=62.5
	elif(timebase==4):
		freq=31.25
	else:
		freq = 0
		print("Error: picoscope timebase configuration is faulty")
	post = int(time*freq)
	update_postTriggerSamples(post)
	

def update_postTriggerSamples(number):
	"""
	Update the picoscope's number of postTriggerSamples

	Parameters:
	- number:	int
				Number of post trigger sample to acquire
	"""
	global postTriggerSamples
	postTriggerSamples = number


def update_trigger_threshold(volt_threshold):
	"""
	Update the trigger's threshold

	Parameters:
	- volt_threshold:	float
						Trigger threshod in volts
	
	Caution: use only in case the channel range is set to 5V
	"""
	global threshold
	global chandle
	
	# find maximum ADC count value
	"""
	handle = chandle
	pointer to value = ctypes.byref(maxADC)
	"""
	maxADC = ctypes.c_int16()
	status["maximumValue"] = ps.ps2000aMaximumValue(chandle, ctypes.byref(maxADC))
	assert_pico_ok(status["maximumValue"])
		
	#calculate threshold
	threshold = int (volt_threshold * maxADC.value / 5)
	


""" __________________Picoscope capture functions____________________"""


def init_picoscope():
	"""
	Initialize the picoscope to have 2 active channels and a trigger set on channel A
	"""
	global chARange
	global chBRange
	global chandle
	global status
	
	# Open 2000 series PicoScope
	# Returns handle to chandle for use in future API functions
	status["openunit"] = ps.ps2000aOpenUnit(ctypes.byref(chandle), None)
	assert_pico_ok(status["openunit"])

	# Initialize picoscope parameters with Settings.json file
	with open("Settings.json", "r") as f:
			Settings = json.load(f)

	update_frequency(float(Settings["SamplingFrequency"].split()[0]))
	update_channelB_range(int(float(Settings["VerticalResolution"].split()[0])))
	update_trigger_threshold(Settings["TriggerThreshold"])
	update_sample_interval_preTrigger(Settings["AcquisitionPeriod_PreTrigger"])
	update_sample_interval_postTrigger(Settings["AcquisitionPeriod_PostTrigger"])

    # Set up channel A --> connected to PCB
	""" Parameters
	handle = chandle
	channel = PS2000A_CHANNEL_A = 0
	enabled = 1
	coupling type = PS2000A_DC = 1
	range = PS2000A_5V = 8
	analogue offset = 0 V
	"""
	status["setChA"] = ps.ps2000aSetChannel(chandle, 0, 1, 1, chARange, 0)
	assert_pico_ok(status["setChA"])

	# Set up channel B --> connected to probe
	""" Parameters
	handle = chandle
	channel = PS2000A_CHANNEL_B = 1
	enabled = 1
	coupling type = PS2000A_DC = 1
	range = PS2000A_200mV = 4
	analogue offset = 0 V
	"""
	status["setChB"] = ps.ps2000aSetChannel(chandle, 1, 1, 1, chBRange, 0)
	assert_pico_ok(status["setChB"])	

def precapture():
	"""
	Prepare a capture with the picoscope
	
	Return:
	- timeIntervalns:	Time interval between readings at the selected timebase
	"""	
	global threshold
	global timebase
	global preTriggerSamples
	global postTriggerSamples
	global chandle
	global status
	
	# Set up single trigger --> on PCB (Channel A)
	""" Parameters
	handle = chandle
	enabled = 1
	source = PS2000A_CHANNEL_A = 0
	threshold = 8192 ADC counts
	direction = PS2000A_RISING = 2
	delay = 0 s
	auto Trigger = 0 ms --> device waits indefinitively for a trigger
	"""
	status["trigger"] = ps.ps2000aSetSimpleTrigger(chandle, 1, 0, threshold, 2, 0, 0)
	assert_pico_ok(status["trigger"])
	
	# number of pre and post trigger samples to be collected
	totalSamples = preTriggerSamples + postTriggerSamples

	# Get timebase information
	# WARNING: When using this example it may not be possible to access all Timebases as all channels are enabled by default when opening the scope.  
	# To access these Timebases, set any unused analogue channels to off.
	"""
	handle = chandle
	timebase --> defined in the change_frequency function
	noSamples = totalSamples
	pointer to timeIntervalNanoseconds = ctypes.byref(timeIntervalNs)
	pointer to totalSamples = ctypes.byref(returnedMaxSamples)
	segment index = 0
	"""
	timeIntervalns = ctypes.c_float()
	returnedMaxSamples = ctypes.c_int32()
	oversample = ctypes.c_int16(0)
	status["getTimebase2"] = ps.ps2000aGetTimebase2(chandle,timebase,totalSamples,ctypes.byref(timeIntervalns),oversample,ctypes.byref(returnedMaxSamples),0)
	assert_pico_ok(status["getTimebase2"])

	# Run block capture
	"""
	handle = chandle
	number of pre-trigger samples = preTriggerSamples
	number of post-trigger samples = PostTriggerSamples
	timebase
	oversample = 0 = oversample
	time indisposed ms = None (not needed in the example)
	segment index = 0
	lpReady = None (using ps2000aIsReady rather than ps2000aBlockReady)
	pParameter = None
	"""
	status["runBlock"] = ps.ps2000aRunBlock(chandle,preTriggerSamples,postTriggerSamples,timebase,oversample,None,0,None,None)
	assert_pico_ok(status["runBlock"])
	
	print("Device ready for capture")
	
	return(timeIntervalns)


def postcapture(timeIntervalns):
	"""
	Retrieve Data after a capture with the picoscope
	
	Parameters:
	- timeIntervalns:	Time interval between readings at the selected timebase
	
	Return:
	- time_s:			Float list
						Time signatures of the measures
	- adc2mVChAMax_V:	Float list
						Measures of the picoscope's channel A corresponding to the PCB measures
	- adc2mVChBMax_V:	Float list
						Measures of the picoscope's channel B corresponding to the probe measures
	"""

	global chARange
	global chBRange
	global preTriggerSamples
	global postTriggerSamples
	global chandle
	global status
	
	# number of pre and post trigger samples to be collected
	totalSamples = preTriggerSamples + postTriggerSamples

	# Check for data collection to finish using ps2000aIsReady
	ready = ctypes.c_int16(0)
	check = ctypes.c_int16(0)
	
	startTime = time.time()
	while ready.value == check.value:
		status["isReady"] = ps.ps2000aIsReady(chandle, ctypes.byref(ready))
		
		# if a problem occurs in the trigger detection
		if time.time() - startTime > 2.0:
			return (None, None, None)

	# Create buffers ready for assigning pointers for data collection
	buffer_trigger_Max = (ctypes.c_int16 * totalSamples)()
	buffer_trigger_Min = (ctypes.c_int16 * totalSamples)() # used for downsampling
	buffer_probe_Max = (ctypes.c_int16 * totalSamples)()
	buffer_probe_Min = (ctypes.c_int16 * totalSamples)() # used for downsampling

	# Set data buffer location for data collection from channel A
	"""
	handle = chandle
	source = PS2000A_CHANNEL_A = 0
	pointer to buffer max = ctypes.byref(bufferDPort0Max)
	pointer to buffer min = ctypes.byref(bufferDPort0Min)
	buffer length = totalSamples
	segment index = 0
	ratio mode = PS2000A_RATIO_MODE_NONE = 0
	"""
	status["setDataBuffersA"] = ps.ps2000aSetDataBuffers(chandle,0,ctypes.byref(buffer_trigger_Max),ctypes.byref(buffer_trigger_Min),totalSamples,0,0)
	assert_pico_ok(status["setDataBuffersA"])

	# Set data buffer location for data collection from channel B
	"""
	handle = chandle
	source = PS2000A_CHANNEL_B = 1
	pointer to buffer max = ctypes.byref(buffer_probe_Max)
	pointer to buffer min = ctypes.byref(buffer_probe_Min)
	buffer length = totalSamples
	segment index = 0
	ratio mode = PS2000A_RATIO_MODE_NONE = 0
	"""
	status["setDataBuffersB"] = ps.ps2000aSetDataBuffers(chandle,1,ctypes.byref(buffer_probe_Max),ctypes.byref(buffer_probe_Min),totalSamples,0,0)
	assert_pico_ok(status["setDataBuffersB"])

	# Create overflow location
	overflow = ctypes.c_int16()
	# create converted type totalSamples
	cTotalSamples = ctypes.c_int32(totalSamples)

	# Retried data from scope to buffers assigned above
	"""
	handle = chandle
	start index = 0
	pointer to number of samples = ctypes.byref(cTotalSamples)
	downsample ratio = 0
	downsample ratio mode = PS2000A_RATIO_MODE_NONE
	pointer to overflow = ctypes.byref(overflow))
	"""
	status["getValues"] = ps.ps2000aGetValues(chandle, 0, ctypes.byref(cTotalSamples), 0, 0, 0, ctypes.byref(overflow))
	assert_pico_ok(status["getValues"])


	# find maximum ADC count value
	"""
	handle = chandle
	pointer to value = ctypes.byref(maxADC)
	"""
	maxADC = ctypes.c_int16()
	status["maximumValue"] = ps.ps2000aMaximumValue(chandle, ctypes.byref(maxADC))
	assert_pico_ok(status["maximumValue"])

	# convert ADC counts data to mV
	adc2mVChAMax =  adc2mV(buffer_trigger_Max, chARange, maxADC)
	adc2mVChBMax =  adc2mV(buffer_probe_Max, chBRange, maxADC)

	# Create time data
	timeSignature = np.linspace(0, ((cTotalSamples.value)-1) * timeIntervalns.value, cTotalSamples.value)
	
	# Convertions
	time_s = convert_table(timeSignature,1000)
	adc2mVChAMax_V = convert_table(adc2mVChAMax,1000)
	adc2mVChBMax_V = convert_table(adc2mVChBMax,1000)
	
	return time_s, adc2mVChAMax_V, adc2mVChBMax_V

def stop_picoscope():
	"""
	Stop the picoscope if it is waiting for a trigger
	"""
	global chandle
	global status
	status["stop"] = ps.ps2000aStop(chandle)
	
	try:
		assert_pico_ok(status["stop"])
	except:
		pass

def close_picoscope():
	"""
	Stop the picoscope and close it
	"""
	global chandle
	global status

	stop_picoscope()

	# Close unit & Disconnect the scope
	status["close"] = ps.ps2000aCloseUnit(chandle)
	assert_pico_ok(status["close"])

	#print(status)


""" __________________Picoscope support functions____________________"""


def convert_table(table,scale):
	"""
	Convert data by dividing all its values by scale

	Parameters:
	- table:	Float list
				Data that is to be converted
	- scale:	int
				Number by which each value of the table will be divided

	Return:
	- result:	Float list
				Converted data
	"""
	result=[]
	for element in table:
		result.append(element/scale)
	return result


def plot_picoscope_output(time, PCB_measures, probe_measures,name):
	"""
	Display measures

	Parameters:
	- time:				Float list
						Time signatures of the measures
	- PCB_measures:		Float list
						Measures of the picoscope's channel A corresponding to the PCB measures
	- probe_measures:	Float list
						Measures of the picoscope's channel B corresponding to the probe measures
	- name:				String
						Title of the graph that is to be displayed
	"""
	# plot data from channel A and B
	plt.title(name)
	plt.plot(time, PCB_measures[:])
	plt.plot(time, probe_measures[:])
	plt.xlabel('Time (µs)')
	plt.ylabel('Voltage (V)')
	plt.show()


def store_capture_in_file(time, PCB_measures, probe_measures, filename):
	"""
	Write the three data blocks (time, PCB and probe measures) in a file in order to store them in filename

	Parameters:
	- time:				Float list
						Time signatures of the measures
	- PCB_measures:		Float list
						Measures of the picoscope's channel A corresponding to the PCB measures
	- probe_measures:	Float list
						Measures of the picoscope's channel B corresponding to the probe measures
	- filename:			String
						Path of the file to be opened
	"""
	
	try:
		data_file = open(filename,'w')
	except:
		logging.debug(f"{filename} can not be writen")
		return None
	
	data_file.write(str(len(time))+'\n')
	
	for element in time:
		data_file.write(str(element)+'\n')
	for element in PCB_measures:
		data_file.write(str(element)+'\n')
	for element in probe_measures:
		data_file.write(str(element)+'\n')
	
	data_file.close()


def retrieve_data_from_file(filename):
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
	
	try:
		data_file = open(filename,'r')
	except:
		logging.debug(f"{filename} has not been found")
		return None
		
	data_text = data_file.read()
	time=[]
	PCB_measures=[]
	probe_measures=[]
	
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


""" ________________________Tests functions__________________________"""


def capture_save_display(title, filename):
	"""
	Capture data, save data in a file, retrieve data from file, display data in a graph

	Parameters:
	- title:	String
				Title to give to the graph
	- filename:	String
				Path of the file to save the data into
	"""
	# get captures
	timeIntervalns = precapture()
	# send AES instruction
	time, PCB_measures, probe_measures = postcapture(timeIntervalns)
	
	# store data
	store_capture_in_file(time, PCB_measures, probe_measures, filename)
	
	# retrieve data
	time, PCB_measures, probe_measures = retrieve_data_from_file(filename)
	
	# display data
	plot_picoscope_output(time, PCB_measures, probe_measures,title)
	return time, PCB_measures, probe_measures
	

def run_picoscope():
	"""
	Run the complete picoscope process (initialisation, capture, storage and closure)
	"""	
	# Variable initialisation
	capture_to_occur = True
	microcontroller = 0 # possible values are 0: unprotected ; 1:protected ; 2: ChaXa
	
	# initialisation
	init_picoscope()
	
	# capture several measures in a row
	while(True):
		# unprotected
		time_unprotected = []
		PCB_measures_unprotected = []
		probe_measures_unprotected = []
		time_unprotected, PCB_measures_unprotected, probe_measures_unprotected = capture_save_display("Unprotected",'/home/pechaxa/Documents/Unprotected.txt')
		
	
	"""
	# protected
	time_protected = []
	PCB_measures_protected = []
	probe_measures_protected = []
	time_protected, PCB_measures_protected, probe_measures_protected = capture_save_display("Protected", '/home/pechaxa/Documents/Protected.txt')
	
	# ChaXa
	time_ChaXa = []
	PCB_measures_ChaXa = []
	probe_measures_ChaXa = []
	time_ChaXa, PCB_measures_ChaXa, probe_measures_ChaXa = capture_save_display("ChaXa", '/home/pechaxa/Documents/ChaXa.txt')
	"""
	
	close_picoscope()

def main():
	run_picoscope()

if __name__ == "__main__":
	main()

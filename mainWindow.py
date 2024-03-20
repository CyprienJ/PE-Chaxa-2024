# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

RED_COLOR = (255, 0, 0)
BLUE_COLOR = (0, 0, 255)
VIOLET_COLOR = (166,0, 255)
LIGHT_BLUE_COLOR = (8, 196, 222)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1225, 810)
        MainWindow.setMinimumSize(QtCore.QSize(1425, 810))

        # Central Widget = Home page Widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.841, y2: 1.5, stop:0 rgba(204, 0, 0, 255), stop:0.3 rgba(255, 250, 250, 255));")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_5.setContentsMargins(1, 1, 1, 1)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setStyleSheet("background-color: transparent;")
        self.stackedWidget.setObjectName("stackedWidget")

        # Signal visualization Widget
        self.signals_visualization_page = QtWidgets.QWidget()
        self.signals_visualization_page.setObjectName("signals_visualization_page")

        # Main vertical Layout
        self.main_vertical_layout = QtWidgets.QVBoxLayout(self.signals_visualization_page)
        self.main_vertical_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.main_vertical_layout.setContentsMargins(9, 6, 9, 6)
        self.main_vertical_layout.setObjectName("main_vertical_layout")

        # Picoscope Settings Button
        self.CB_PicoSettingsButton = QtWidgets.QPushButton(self.stackedWidget)
        self.CB_PicoSettingsButton.move(15,15)
        self.CB_PicoSettingsButton.setMinimumSize(QtCore.QSize(160, 30))
        self.CB_PicoSettingsButton.setMaximumSize(QtCore.QSize(500, 16777215))
        self.CB_PicoSettingsButton.setFont(QtGui.QFont("Lucida Grande", 11))
        self.CB_PicoSettingsButton.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.CB_PicoSettingsButton.setObjectName("CB_PicoSettingsButton")

        # Sidebar with QVBoxLayout
        self.sidebar_widget = QtWidgets.QWidget(self.centralwidget)
        self.sidebar_widget.setMinimumSize(QtCore.QSize(70, 30))
        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setContentsMargins(10, 10, 10, 10)  # Left, top, right, bottom
        self.sidebar_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.sidebar_layout.addWidget(QtWidgets.QLabel("AES Key"))
        self.gridLayout_5.addWidget(self.sidebar_widget, 1, 1, 1, 1)

        # Change the AES key
        self.number_AES_spinBox = [QtWidgets.QSpinBox() for _ in range(16)]
        for i in range(16):
            self.number_AES_spinBox[i].setMinimumSize(QtCore.QSize(40, 30))
            self.number_AES_spinBox[i].setMaximumSize(QtCore.QSize(100, 100))
            self.number_AES_spinBox[i].setFont(QtGui.QFont("Lucida Grande", 11))
            self.number_AES_spinBox[i].setStyleSheet("background-color: rgb(238, 238, 236);")
            self.number_AES_spinBox[i].setObjectName("number_AES" + str(i) + "_spinBox")
            self.number_AES_spinBox[i].setDisplayIntegerBase(16)
            self.sidebar_layout.addWidget(self.number_AES_spinBox[i])

        # Change button
        self.Change_AES_Key_Button = QtWidgets.QPushButton(self.sidebar_widget)
        self.Change_AES_Key_Button.setMinimumSize(QtCore.QSize(220, 23))
        self.Change_AES_Key_Button.setMaximumSize(QtCore.QSize(220, 23))
        self.Change_AES_Key_Button.setFont(QtGui.QFont("Lucida Grande", 10))
        self.Change_AES_Key_Button.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.Change_AES_Key_Button.setObjectName("Apply_New_AES_key")
        self.sidebar_layout.addWidget(self.Change_AES_Key_Button)


        # Bottom Horizontal Layout
        self.bottom_horizontal_layout = QtWidgets.QHBoxLayout()
        self.main_vertical_layout.addLayout(self.bottom_horizontal_layout)
        
        
        # Text encryption GroupBox
        self.Text_encryption_groupBox = QtWidgets.QGroupBox(self.signals_visualization_page)
        self.Text_encryption_groupBox.setMinimumSize(QtCore.QSize(800, 100))
        self.Text_encryption_groupBox.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.Text_encryption_groupBox.setFont(QtGui.QFont("Lucida Grande", 10))
        self.Text_encryption_groupBox.setStyleSheet("background-color: transparent;")
        self.Text_encryption_groupBox.setObjectName("Text_encryption_groupBox")
        self.bottom_horizontal_layout.addWidget(self.Text_encryption_groupBox) # Add PlainText GroupBox to the layout
        # Layout in PlainText GroupBox
        self.gridLayout = QtWidgets.QGridLayout(self.Text_encryption_groupBox)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        # PlainText Label
        self.labelPlainText = QtWidgets.QLabel(self.Text_encryption_groupBox)
        self.labelPlainText.setMinimumSize(QtCore.QSize(110, 0))
        self.labelPlainText.setMaximumSize(QtCore.QSize(110, 16777215))
        self.labelPlainText.setFont(QtGui.QFont("Lucida Grande", 9))
        self.labelPlainText.setObjectName("labelPlainText")
        self.gridLayout.addWidget(self.labelPlainText, 1, 0, 1, 1)

        # CipherText Label
        self.labelCipherText = QtWidgets.QLabel(self.Text_encryption_groupBox)
        self.labelCipherText.setMinimumSize(QtCore.QSize(110, 0))
        self.labelCipherText.setMaximumSize(QtCore.QSize(110, 16777215))
        self.labelCipherText.setFont(QtGui.QFont("Lucida Grande", 9))
        self.labelCipherText.setObjectName("labelCipherText")
        self.gridLayout.addWidget(self.labelCipherText, 2, 0, 1, 1)

        # CipherText label zone
        self.CipherText_display_label = QtWidgets.QLabel(self.Text_encryption_groupBox)
        self.CipherText_display_label.setMinimumSize(QtCore.QSize(500, 23))
        self.CipherText_display_label.setMaximumSize(QtCore.QSize(500, 23))
        self.CipherText_display_label.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.CipherText_display_label.setText("")
        self.CipherText_display_label.setObjectName("CipherText_display_label")
        self.gridLayout.addWidget(self.CipherText_display_label, 2, 2, 1, 1)

        # Generate PlainText randomly Button
        self.PlainText_random_Button = QtWidgets.QPushButton(self.Text_encryption_groupBox)
        self.PlainText_random_Button.setMinimumSize(QtCore.QSize(220, 23))
        self.PlainText_random_Button.setMaximumSize(QtCore.QSize(220, 23))
        self.PlainText_random_Button.setFont(QtGui.QFont("Lucida Grande", 10))
        self.PlainText_random_Button.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.PlainText_random_Button.setObjectName("PlainText_random_Button")
        self.gridLayout.addWidget(self.PlainText_random_Button, 1, 5, 1, 1)

        # PlainText input zone
        self.PlainText_input = QtWidgets.QLineEdit(self.Text_encryption_groupBox)
        self.PlainText_input.setMinimumSize(QtCore.QSize(500, 23))
        self.PlainText_input.setMaximumSize(QtCore.QSize(500, 23))
        self.PlainText_input.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.PlainText_input.setObjectName("PlainText_input")
        self.gridLayout.addWidget(self.PlainText_input, 1, 2, 1, 1)

        # Start AES vertical layout
        self.StartAES_vertical_layout = QtWidgets.QVBoxLayout()
        self.bottom_horizontal_layout.addLayout(self.StartAES_vertical_layout)

        # Number of acquisitions layout
        self.number_acquisitions_layout = QtWidgets.QHBoxLayout()
        self.StartAES_vertical_layout.addLayout(self.number_acquisitions_layout)

        # Number of acquisitions label
        self.number_acquisitions_label = QtWidgets.QLabel()
        self.number_acquisitions_label.setObjectName("number_acquisitions_label")
        self.number_acquisitions_label.setMinimumSize(QtCore.QSize(170, 10))
        self.number_acquisitions_label.setMaximumSize(QtCore.QSize(200, 20))
        self.number_acquisitions_label.setFont(QtGui.QFont("Lucida Grande", 10))
        self.number_acquisitions_layout.addWidget(self.number_acquisitions_label)
        
        # Number of acquisitions SpinBox
        self.number_acquisitions_spinBox = QtWidgets.QSpinBox()
        self.number_acquisitions_spinBox.setMinimumSize(QtCore.QSize(80, 30))
        self.number_acquisitions_spinBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.number_acquisitions_spinBox.setFont(QtGui.QFont("Lucida Grande", 11))
        self.number_acquisitions_spinBox.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.number_acquisitions_spinBox.setObjectName("number_acquisitions_spinBox")
        self.number_acquisitions_layout.addWidget(self.number_acquisitions_spinBox)

        # Start AES encryption button
        self.StartAES_Button = QtWidgets.QPushButton()
        self.StartAES_Button.setMinimumSize(QtCore.QSize(200, 40))
        self.StartAES_Button.setMaximumSize(QtCore.QSize(300, 16777215))
        self.StartAES_Button.setFont(QtGui.QFont("Lucida Grande", 12, QtGui.QFont.Bold))
        self.StartAES_Button.setStyleSheet("background-color: rgb(230, 0, 0);""color: rgb(255, 255, 255);")
        self.StartAES_Button.setObjectName("StartAES_Button")
        self.StartAES_vertical_layout.addWidget(self.StartAES_Button)

        # Stop AES encryption button
        self.StopAES_Button = QtWidgets.QPushButton()
        self.StopAES_Button.setMinimumSize(QtCore.QSize(200, 40))
        self.StopAES_Button.setMaximumSize(QtCore.QSize(300, 16777215))
        self.StopAES_Button.setFont(QtGui.QFont("Lucida Grande", 12, QtGui.QFont.Bold))
        self.StopAES_Button.setStyleSheet("background-color: rgb(255, 100, 0);""color: rgb(255, 255, 255);")
        self.StopAES_Button.setObjectName("StopAES_Button")
        self.StartAES_vertical_layout.addWidget(self.StopAES_Button)


        # Tab Widget
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setMinimumSize(QtCore.QSize(1025, 520))
        self.tabWidget.setMaximumSize(QtCore.QSize(1700, 850))
        self.tabWidget.setFont(QtGui.QFont("Lucida Grande", 10))
        self.tabWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tabWidget.setObjectName("tabWidget")

        #Tab 1
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_1)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_tab1 = QtWidgets.QGridLayout()
        self.gridLayout_tab1.setContentsMargins(6, -1, -1, 1)
        self.gridLayout_tab1.setObjectName("gridLayout_tab1")
        self.gridLayout_7.addLayout(self.gridLayout_tab1, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_1, "")

        # Tab 2
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_tab2 = QtWidgets.QGridLayout()
        self.gridLayout_tab2.setContentsMargins(6, -1, -1, -1)
        self.gridLayout_tab2.setObjectName("gridLayout_tab2")
        self.gridLayout_2.addLayout(self.gridLayout_tab2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")

        # Tab 3
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_tab3 = QtWidgets.QGridLayout()
        self.gridLayout_tab3.setContentsMargins(6, -1, -1, -1)
        self.gridLayout_tab3.setObjectName("gridLayout_tab3")
        self.gridLayout_4.addLayout(self.gridLayout_tab3, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        
        # Tab 4
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_tab4 = QtWidgets.QGridLayout()
        self.gridLayout_tab4.setContentsMargins(6, -1, -1, -1)
        self.gridLayout_tab4.setObjectName("gridLayout_tab4")
        self.gridLayout_8.addLayout(self.gridLayout_tab4, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")

        # Default Trace Check Box below each graph
        self.default_trace_check_box = [QtWidgets.QCheckBox('Default trace', self) for _ in range(3)]
        for index, gridLayout in enumerate([7, 2, 4]):
                exec(f"self.gridLayout_{gridLayout}.addWidget(self.default_trace_check_box[{index}],1,0)")
                self.default_trace_check_box[index].setStyleSheet("padding-left : 10px")

        # Legend for 4th tab
        self.legend_layout = QtWidgets.QHBoxLayout() # New Horizontal Layout at bottom
        self.gridLayout_8.addLayout(self.legend_layout,1,0)
        # Append last default trace check box
        self.default_trace_check_box.append(QtWidgets.QCheckBox('Default traces', self))
        self.legend_layout.addWidget(self.default_trace_check_box[3])
        self.default_trace_check_box[3].setStyleSheet("padding-left : 10px")
        # Generates label for differents signals
        for microcontroller in ["unprotected", "passive", "chaxa"]:
            exec(f"self.{microcontroller}_frame = QtWidgets.QFrame()")
            exec(f"self.{microcontroller}_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)")
            exec(f"self.{microcontroller}_frame.setMaximumSize(QtCore.QSize(80, 3))")
            exec(f"self.{microcontroller}_frame.setStyleSheet('border: 0px;')")
            exec(f"self.legend_layout.addWidget(self.{microcontroller}_frame)")
            exec(f"self.{microcontroller}_label = QtWidgets.QLabel()")
            exec(f"self.{microcontroller}_label.setFont(QtGui.QFont('Lucida Grande', 10))")
            exec(f"self.legend_layout.addWidget(self.{microcontroller}_label)")
        self.unprotected_frame.setStyleSheet(f"background-color: rgb{str(BLUE_COLOR)};""border: 0px;")
        self.passive_frame.setStyleSheet(f"background-color: rgb{str(LIGHT_BLUE_COLOR)};""border: 0px;")
        self.chaxa_frame.setStyleSheet(f"background-color: rgb{str(VIOLET_COLOR)};""border: 0px;")

        # Tab 5
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tabWidget.addTab(self.tab_5, "")
        # Add tabWidget to the main vertical layout in first position
        self.main_vertical_layout.insertWidget(0, self.tabWidget)
        self.stackedWidget.addWidget(self.signals_visualization_page)
        # Tab 5 main vertical layout
        self.tab5_main_v_layout = QtWidgets.QVBoxLayout(self.tab_5)
        self.tab5_main_v_layout.setObjectName("tab5_main_v_layout")


        # 3 horizontals layouts in tab5_main_v_layout
        self.tab5_h_layout = [QtWidgets.QHBoxLayout() for _ in range(3)]
        self.tab5_left_v_layout = [QtWidgets.QVBoxLayout() for _ in range(3)]
        self.tab5_right_v_layout = [QtWidgets.QVBoxLayout() for _ in range(3)]
        for i in range(3):
             self.tab5_main_v_layout.addLayout(self.tab5_h_layout[i])
             self.tab5_h_layout[i].addLayout(self.tab5_left_v_layout[i])
             self.tab5_h_layout[i].addLayout(self.tab5_right_v_layout[i])

        # Two lines to separe the three main horizontals layouts
        self.tab5_h_lines = [QtWidgets.QFrame() for _ in range(2)]
        for i in range(2):
            self.tab5_h_lines[i].setFrameShape(QtWidgets.QFrame.HLine)
            self.tab5_main_v_layout.insertWidget(2*i+1, self.tab5_h_lines[i])

        # Vertical lines to separe left and right part
        self.analysis_v_lines = [QtWidgets.QFrame() for _ in range(3)]
        for i in range(3):
            self.analysis_v_lines[i].setFrameShape(QtWidgets.QFrame.VLine)
            self.tab5_h_layout[i].insertWidget(1, self.analysis_v_lines[i], alignment=QtCore.Qt.AlignLeft)

        # Labels in left part for each microcontroller
        self.analysis_label = [QtWidgets.QLabel() for _ in range(3)]
        for i in range(3):
           self.analysis_label[i].setFont(QtGui.QFont("Lucida Grande", 9))
           self.analysis_label[i].setMaximumSize(QtCore.QSize(300, 500))
           self.analysis_label[i].setAlignment(QtCore.Qt.AlignCenter)
           self.tab5_left_v_layout[i].addWidget(self.analysis_label[i], 50)
        
        # Start anlysis buttons
        self.start_analysis_buttons = [QtWidgets.QPushButton() for _ in range(3)]
        for i in range(3):
            self.start_analysis_buttons[i].setMinimumSize(QtCore.QSize(220, 50))
            self.start_analysis_buttons[i].setMaximumSize(QtCore.QSize(220, 60))
            self.start_analysis_buttons[i].setFont(QtGui.QFont("Lucida Grande", 10))
            self.start_analysis_buttons[i].setStyleSheet("background-color: rgb(230, 0, 0);""color: rgb(255, 255, 255);")
            self.tab5_left_v_layout[i].addWidget(self.start_analysis_buttons[i], 50,  alignment=QtCore.Qt.AlignmentFlag.AlignTop)

        # # Loading bar labels
        # self.loading_bars_labels = [QtWidgets.QLabel() for _ in range(3)]
        # for i in range(3):
        #    self.loading_bars_labels[i].setFont(QtGui.QFont("Lucida Grande", 9))
        #    self.loading_bars_labels[i].setVisible(False)
        #    self.tab5_right_v_layout[i].addWidget(self.loading_bars_labels[i], 20, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        
        # # Loading bar
        # self.loading_bars = [QtWidgets.QProgressBar() for _ in range(3)]
        # for i in range(3):
        #     self.loading_bars[i].setVisible(False)
        #     self.tab5_right_v_layout[i].addWidget(self.loading_bars[i], 30, alignment=QtCore.Qt.AlignmentFlag.AlignTop)

        # Key-encryption GroupBox
        self.key_groupbox = [QtWidgets.QGroupBox() for _ in range(3)]
        # Key GroupBox horizontal Layout
        self.key_h_layout = [QtWidgets.QHBoxLayout(self.key_groupbox[index]) for index in range(3)]
        for i in range(3):
            self.key_groupbox[i].setStyleSheet("QGroupBox { font-weight: bold; } ");
            #self.key_groupbox[i].setVisible(False)
            self.tab5_right_v_layout[i].addWidget(self.key_groupbox[i], 50, alignment=QtCore.Qt.AlignmentFlag.AlignTop)

        # 16 Key text labels
        self.key_labels = [[0 for j in range(16)] for i in range(3)]
        for i in range(3):
            for j in range(16):
                self.key_labels[i][j] = QtWidgets.QLabel(self.key_groupbox[i])
                self.key_labels[i][j].setMinimumSize(QtCore.QSize(65, 23))
                self.key_labels[i][j].setMaximumSize(QtCore.QSize(65, 23))
                self.key_labels[i][j].setStyleSheet("background-color: rgb(243, 243, 243);")
                self.key_h_layout[i].addWidget(self.key_labels[i][j])
                
        #Search buttons vertical layout
        self.search_h_layout = [QtWidgets.QHBoxLayout() for _ in range(3)]
        for i in range(3):
            self.tab5_right_v_layout[i].addLayout(self.search_h_layout[i])
        # Search buttons
        self.search_buttons = [[0 for j in range(16)] for _ in range(3)]
        for i in range(3):
            for j in range(16):
                self.search_buttons[i][j] = QtWidgets.QPushButton()
                self.search_buttons[i][j].setMinimumSize(QtCore.QSize(65, 60))
                self.search_buttons[i][j].setMaximumSize(QtCore.QSize(65, 60))
                self.search_buttons[i][j].setFont(QtGui.QFont("Lucida Grande", 10))
                self.search_buttons[i][j].setStyleSheet("background-color: rgb(230, 0, 0);""color: rgb(255, 255, 255);")
                #self.search_buttons[i][j].setVisible(False)
                self.search_h_layout[i].addWidget(self.search_buttons[i][j], 50, alignment=QtCore.Qt.AlignmentFlag.AlignTop)

        # Get screen size
        screen = QtWidgets.QDesktopWidget().screenGeometry()

        # Widget for injection fault
        self.injection_Fault_widget = QtWidgets.QWidget(self.centralwidget)
        self.injection_Fault_widget.setMinimumSize(QtCore.QSize(screen.width() * 0.4, screen.height() * 0.4))
        self.injection_Fault_widget.setMaximumSize(QtCore.QSize(screen.width() * 0.9, screen.height() * 0.9))

        # QVBox Layout for Injection Fault panel
        self.Injection_Fault_v_layout = QtWidgets.QVBoxLayout()
        self.Injection_Fault_v_layout.setObjectName("Injection_Fault_v_layout")
        self.injection_Fault_widget.setLayout(self.Injection_Fault_v_layout)

        #3 horizontal layouts in Injection_Fault_v_layout
        self.Injection_Fault_h_layout = [QtWidgets.QHBoxLayout() for _ in range(3)]
        self.Injection_Fault_left_v_layout = [QtWidgets.QVBoxLayout() for _ in range(3)]
        self.Injection_Fault_right_v_layout = [QtWidgets.QVBoxLayout() for _ in range(3)]
        for i in range(3):
            self.Injection_Fault_v_layout.addLayout(self.Injection_Fault_h_layout[i])
            self.Injection_Fault_h_layout[i].addLayout(self.Injection_Fault_left_v_layout[i])
            self.Injection_Fault_h_layout[i].addLayout(self.Injection_Fault_right_v_layout[i])

        # Vertical lines to separe left and right part
        self.injection_fault_v_lines = [QtWidgets.QFrame() for _ in range(3)]
        for i in range(3):
            self.injection_fault_v_lines[i].setFrameShape(QtWidgets.QFrame.VLine)
            self.Injection_Fault_h_layout[i].insertWidget(1, self.injection_fault_v_lines[i], alignment=QtCore.Qt.AlignLeft)
        
        #Two lines to separe the three main horizontals layouts
        self.injection_fault_h_lines = [QtWidgets.QFrame() for _ in range(2)]
        for i in range(2):
            self.injection_fault_h_lines[i].setFrameShape(QtWidgets.QFrame.HLine)
            self.Injection_Fault_v_layout.insertWidget(2*i+1, self.injection_fault_h_lines[i])



        # Home Page Layout/Widget
        self.home_page = QtWidgets.QWidget()
        self.home_page.setObjectName("home_page")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.home_page)
        self.gridLayout_11.setVerticalSpacing(15)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.Home_gridLayout = QtWidgets.QGridLayout()
        self.Home_gridLayout.setContentsMargins(-1, -1, 0, -1)
        self.Home_gridLayout.setObjectName("Home_gridLayout")
        spacerItem11 = QtWidgets.QSpacerItem(20, 150, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.Home_gridLayout.addItem(spacerItem11, 3, 0, 2, 1)

        # Chaxa Demonstrator App title in main page
        self.Home_label_title = QtWidgets.QLabel(self.home_page)
        self.Home_label_title.setMinimumSize(QtCore.QSize(550, 50))
        self.Home_label_title.setMaximumSize(QtCore.QSize(550, 50))
        self.Home_label_title.setFont(QtGui.QFont("Lucida Grande", 20, QtGui.QFont.Bold))
        self.Home_label_title.setStyleSheet("background-color: transparent;""color: rgb(46, 52, 54);")
        self.Home_label_title.setObjectName("Home_label_title")
        self.Home_gridLayout.addWidget(self.Home_label_title, 1, 0, 1, 1)

        # Chaxa Demonstrator App subtitle in main page
        self.Home_label_SubTitle = QtWidgets.QLabel(self.home_page)
        self.Home_label_SubTitle.setMinimumSize(QtCore.QSize(550, 30))
        self.Home_label_SubTitle.setMaximumSize(QtCore.QSize(600, 80))
        self.Home_label_SubTitle.setFont(QtGui.QFont("Lucida Grande",14))
        self.Home_label_SubTitle.setStyleSheet("background-color: transparent;")
        self.Home_label_SubTitle.setObjectName("Home_label_SubTitle")
        self.Home_gridLayout.addWidget(self.Home_label_SubTitle, 2, 0, 1, 1)

        # Home label Picture
        self.Home_label_picture = QtWidgets.QLabel(self.home_page)
        self.Home_label_picture.setMaximumSize(QtCore.QSize(190, 200))
        self.Home_label_picture.setStyleSheet("background-color: transparent;")
        self.Home_label_picture.setText("")
        self.Home_label_picture.setPixmap(QtGui.QPixmap(":/newPrefix/ressources/signal-PhotoRoom_assem.png"))
        self.Home_label_picture.setScaledContents(True)
        self.Home_label_picture.setObjectName("Home_label_picture")
        self.Home_gridLayout.addWidget(self.Home_label_picture, 1, 1, 1, 1)

        # Side Channel launch Button
        self.Side_Channel_LaunchButton = QtWidgets.QPushButton(self.home_page)
        self.Side_Channel_LaunchButton.setMinimumSize(QtCore.QSize(250, 30))
        self.Side_Channel_LaunchButton.setMaximumSize(QtCore.QSize(300, 30))
        self.Side_Channel_LaunchButton.setFont(QtGui.QFont("Lucida Grande", 12, QtGui.QFont.Bold))
        self.Side_Channel_LaunchButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(204, 0, 0, 255), stop:1 rgba(255, 183, 183, 255));""selection-color: rgb(46, 52, 54);""selection-background-color: rgb(238, 238, 236);""color: rgb(255, 255, 255);")
        self.Side_Channel_LaunchButton.setObjectName("SideChannel_LaunchButton")
        self.Home_gridLayout.addWidget(self.Side_Channel_LaunchButton, 5, 0, 1, 1)

        # Injection Fault launch Button
        self.Injection_Fault_LaunchButton = QtWidgets.QPushButton(self.home_page)
        self.Injection_Fault_LaunchButton.setMinimumSize(QtCore.QSize(250, 30))
        self.Injection_Fault_LaunchButton.setMaximumSize(QtCore.QSize(300, 30))
        self.Injection_Fault_LaunchButton.setFont(QtGui.QFont("Lucida Grande", 12, QtGui.QFont.Bold))
        self.Injection_Fault_LaunchButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(204, 0, 0, 255), stop:1 rgba(255, 183, 183, 255));""selection-color: rgb(46, 52, 54);""selection-background-color: rgb(238, 238, 236);""color: rgb(255, 255, 255);")
        self.Injection_Fault_LaunchButton.setObjectName("Injection_Fault_LaunchButton")
        self.Home_gridLayout.addWidget(self.Injection_Fault_LaunchButton, 6, 0, 1, 1) 

        # Spacer to move title in the center of the home page
        spacerItem12 = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.Home_gridLayout.addItem(spacerItem12, 0, 0, 1, 1)
        self.gridLayout_11.addLayout(self.Home_gridLayout, 0, 0, 1, 1)

        # Spacer to move title on the left of the home page
        self.Home_HLayout_bottom = QtWidgets.QHBoxLayout()
        self.Home_HLayout_bottom.setObjectName("Home_HLayout_bottom")
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.Home_HLayout_bottom.addItem(spacerItem13)
        self.gridLayout_11.addLayout(self.Home_HLayout_bottom, 2, 0, 1, 1)
        spacerItem14 = QtWidgets.QSpacerItem(20, 120, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_11.addItem(spacerItem14, 1, 0, 1, 1)
        self.stackedWidget.addWidget(self.home_page)
        self.gridLayout_5.addWidget(self.stackedWidget, 1, 0, 1, 1)

        # Layout for logo on the right part
        self.HLogoLayout = QtWidgets.QHBoxLayout()
        self.HLogoLayout.setContentsMargins(-1, 0, 0, -1)
        self.HLogoLayout.setSpacing(0)
        self.HLogoLayout.setObjectName("HLogoLayout")
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.HLogoLayout.addItem(spacerItem15)

        # CEA logo in top right corner
        self.labelCEA = QtWidgets.QLabel(self.centralwidget)
        self.labelCEA.setMaximumSize(QtCore.QSize(50, 50))
        self.labelCEA.setText("")
        self.labelCEA.setPixmap(QtGui.QPixmap(":/newPrefix/ressources/cea.jpeg"))
        self.labelCEA.setScaledContents(True)
        self.labelCEA.setObjectName("labelCEA")
        self.HLogoLayout.addWidget(self.labelCEA)
        spacerItem16 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.HLogoLayout.addItem(spacerItem16)
        self.gridLayout_5.addLayout(self.HLogoLayout, 0, 0, 1, 1)

        # Menu Bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1225, 20))
        self.menubar.setFont(QtGui.QFont("Lucida Grande",11))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setFont(QtGui.QFont("Lucida Grande",11))
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setFont(QtGui.QFont("Lucida Grande",11))
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setFont(QtGui.QFont("Lucida Grande",11))
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout_the_app = QtWidgets.QAction(MainWindow)
        self.actionAbout_the_app.setFont(QtGui.QFont("Lucida Grande",11))
        self.actionAbout_the_app.setObjectName("actionAbout_the_app")
        self.menuFile.addAction(self.actionQuit)
        self.menuAbout.addAction(self.actionAbout_the_app)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        
        # Main important functions
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ChaXa Demonstrator"))
        self.Change_AES_Key_Button.setText(_translate("MainWindow", "Apply changes"))
        self.CB_PicoSettingsButton.setText(_translate("MainWindow", "Picoscope Settings"))
        self.StartAES_Button.setText(_translate("MainWindow", "Start AES encryption"))
        self.StopAES_Button.setText(_translate("MainWindow", "Stop AES encryption"))
        self.Text_encryption_groupBox.setTitle(_translate("MainWindow", "Text encryption"))
        self.labelCipherText.setText(_translate("MainWindow", "Cipher Text:"))
        self.PlainText_random_Button.setText(_translate("MainWindow", "Generate random plain text"))
        self.labelPlainText.setText(_translate("MainWindow", "Plain Text:"))
        self.number_acquisitions_label.setText(_translate("MainWindow", "Number of acquisitions:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "Unprotected signal"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Passive shielding signal"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "ChaXa signal"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "All signals"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Analysis"))
        self.unprotected_label.setText(_translate("MainWindow", "Unprotected signal"))
        self.passive_label.setText(_translate("MainWindow", "Passive shielding signal"))
        self.chaxa_label.setText(_translate("MainWindow", "ChaXa signal"))
        self.analysis_label[0].setText(_translate("MainWindow", "You have 50 traces from\nUnprotected microcontroller"))
        self.analysis_label[1].setText(_translate("MainWindow", "You have 50 traces from\nPassive shielded microcontroller"))
        self.analysis_label[2].setText(_translate("MainWindow", "You have 50 traces from\nChaXa microcontroller"))
        self.start_analysis_buttons[0].setText(_translate("MainWindow", "Start Analysis on\nUnprotected traces"))
        self.start_analysis_buttons[1].setText(_translate("MainWindow", "Start Analysis on\nAttenuated traces"))
        self.start_analysis_buttons[2].setText(_translate("MainWindow", "Start Analysis on\nChaXa traces"))
        for i in range(3):
            #self.loading_bars_labels[i].setText(_translate("MainWindow", "Loading bar"))
            self.key_groupbox[i].setTitle(_translate("MainWindow", "The encryption key is: "))
        for i in range (3):
            for j in range(16):
                self.search_buttons[i][j].setText(_translate("MainWindow", "Search\nByte"))
        self.Home_label_SubTitle.setText(_translate("MainWindow", "Chaxa Demonstrator App aims at proving ChaXa\ndevice efficiency"))
        self.Home_label_title.setText(_translate("MainWindow", "ChaXa Demonstrator App"))
        self.Side_Channel_LaunchButton.setText(_translate("MainWindow", "Launch Side Channel Interface"))
        self.Injection_Fault_LaunchButton.setText(_translate("MainWindow", "Launch Injection Fault Interface"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionAbout_the_app.setText(_translate("MainWindow", "About the app..."))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

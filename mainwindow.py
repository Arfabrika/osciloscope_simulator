import sys
import struct
import numpy as np
from PySide6.QtCore import QThreadPool

from PySide6.QtWidgets import (
    QErrorMessage,
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QLabel,
    QSpinBox,
    QPushButton,
    QDial,
    QCheckBox
)

from SignalPlotWidget import SignalPlotWidget
from SpectrePlotWidget import SpectrePlotWidget
from amplitudeWindow import AmplitudeWindow
from frequencyWindow import FrequencyWindow
from signalData import signalData, signalDataArray
from scalefuncs import getScaleType

import serial.tools.list_ports
import time

from summationWindow import SummationWindow

signal_types = ['-', 'sine', 'cosine', 'triangle', 'sawtooth', 'square']
import time
from functools import partial, wraps
from numba import njit

class CoolDownDecorator(object):
  def __init__(self,func,interval):
    self.func = func
    self.interval = interval
    self.last_run = 0
  def __get__(self,obj,objtype=None):
    if obj is None:
      return self.func
    return partial(self,obj)
  def __call__(self,*args,**kwargs):
    now = time.time()
    if now - self.last_run > self.interval:
      self.last_run = now
      return self.func(*args,**kwargs)

# function for filtering data from controller
def CoolDown(interval):
  def applyDecorator(func):
    decorator = CoolDownDecorator(func=func,interval=interval)
    return wraps(func)(decorator)
  return applyDecorator

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.thread_manager = QThreadPool()
        
        self.stop_flag = False

        self.signalDataArray = signalDataArray([])

        self.amplitude_window = None

        self.summation_window = None
        
        self.serial_ports_combo = QComboBox(self)
        self.serial_ports = serial.tools.list_ports.comports()
        serial_ports_desc = [port.name for port in self.serial_ports]
        self.serial_ports_combo.addItems(serial_ports_desc)
        self.serial_ports_combo_label = QLabel('???????????????? ????????', self)
        self.serial_ports_combo_label.setBuddy(self.serial_ports_combo)        

        self.fs_params_label = QLabel('?????????????? ????????????', self)
        self.fs_toggle_button = QPushButton('??????/????????', self)
        self.fs_toggle_button.setCheckable(True)
        self.fs_toggle_button.clicked.connect(self.set_signal)
        self.fs_params_label.setBuddy(self.fs_toggle_button)
        
        active_label_layout = QHBoxLayout()
        active_label_layout.setDirection(QHBoxLayout.RightToLeft)
        self.active_label = QLabel('???????????????? ????????????', self)
        active_label_layout.addWidget(self.active_label)

        self.fs_signal_form_combo = QComboBox(self)
        self.fs_signal_form_combo.addItems(signal_types)
        self.fs_signal_form_combo_label = QLabel('?????????? ??????????????', self)
        self.fs_signal_form_combo_label.setBuddy(self.fs_signal_form_combo)

        self.signal_plot = SignalPlotWidget()
        self.spectre_plot = SpectrePlotWidget()

        self.fs_frequency_spin = QSpinBox()
        self.fs_frequency_spin.setRange(0, 200_000)
        self.fs_frequency_spin.setValue(1)
        self.fs_frequency_label = QLabel('??????????????')
        self.fs_frequency_label.setBuddy(self.fs_frequency_spin)

        self.fs_amplitude_spin = QSpinBox()
        self.fs_amplitude_spin.setRange(0, 200_000)
        self.fs_amplitude_spin.setValue(1)
        self.fs_amplitude_label = QLabel('??????????????????')
        self.fs_amplitude_label.setBuddy(self.fs_amplitude_spin)

        self.fs_duration_spin = QSpinBox()
        self.fs_duration_spin.setValue(5)
        self.fs_duration_label = QLabel('??????????????????????????????????')
        self.fs_duration_label.setBuddy(self.fs_duration_spin)

        
        serial_ports_layout = QHBoxLayout()
        serial_ports_layout.addWidget(self.serial_ports_combo_label)
        serial_ports_layout.addWidget(self.serial_ports_combo)

        fs_params_layout = QVBoxLayout()

        fs_switch_layout = QHBoxLayout()
        fs_switch_layout.addWidget(self.fs_params_label)
        fs_switch_layout.addWidget(self.fs_toggle_button)

        fs_signal_form_layout = QHBoxLayout()
        fs_signal_form_layout.addWidget(self.fs_signal_form_combo_label)
        fs_signal_form_layout.addWidget(self.fs_signal_form_combo)

        fs_frequency_input_layout = QHBoxLayout()
        fs_frequency_input_layout.addWidget(self.fs_frequency_label)
        fs_frequency_input_layout.addWidget(self.fs_frequency_spin)

        fs_amplitude_input_layout = QHBoxLayout()
        fs_amplitude_input_layout.addWidget(self.fs_amplitude_label)
        fs_amplitude_input_layout.addWidget(self.fs_amplitude_spin)

        fs_duration_input_layout = QHBoxLayout()
        fs_duration_input_layout.addWidget(self.fs_duration_label)
        fs_duration_input_layout.addWidget(self.fs_duration_spin)

        fs_signal_buttons_input_layout = QHBoxLayout()
        self.add_signal_button = QPushButton('???????????????? ????????????', self)
        self.edit_signal_button = QPushButton('???????????????? ?????????????? ????????????', self)
        fs_signal_buttons_input_layout.addWidget(self.add_signal_button)
        fs_signal_buttons_input_layout.addWidget(self.edit_signal_button)
        
        fs_params_layout.addLayout(fs_switch_layout)
        fs_params_layout.addLayout(active_label_layout)
        fs_params_layout.addLayout(fs_signal_form_layout)
        fs_params_layout.addLayout(fs_frequency_input_layout)
        fs_params_layout.addLayout(fs_amplitude_input_layout)
        fs_params_layout.addLayout(fs_duration_input_layout)
        fs_params_layout.addLayout(fs_signal_buttons_input_layout)
     
        self.signals_label = QLabel('???????????? ????????????????')
        self.signals_list = QComboBox(self)
        self.signals_label.setBuddy(self.signals_list)

        signals_list_layout = QHBoxLayout()
        signals_list_layout.addWidget(self.signals_label)
        signals_list_layout.addWidget(self.signals_list)
        
        ampl_layout = QVBoxLayout()
        self.ampl_create_button = QPushButton('?????????????????????? ??????????????????')
        self.ampl_create_button.clicked.connect(self.click_amplitude_event)
        self.freq_create_button = QPushButton('?????????????????? ??????????????????')
        self.freq_create_button.clicked.connect(self.click_frequency_event)
        self.sum_create_button = QPushButton('?????????????????????????? ???????????????????????? ????????????????')
        self.sum_create_button.clicked.connect(self.click_sum_event)

        self.anim_checkbox = QCheckBox("???????????????? ????????????????")
        

        ampl_layout.addLayout(signals_list_layout)
        ampl_layout.addWidget(self.ampl_create_button)
        ampl_layout.addWidget(self.freq_create_button)
        ampl_layout.addWidget(self.sum_create_button)
        ampl_layout.addWidget(self.anim_checkbox)

        params_layout = QHBoxLayout()
        params_layout.addLayout(fs_params_layout)
        params_layout.addLayout(ampl_layout)

        plot_params_layout = QVBoxLayout()
        # plot_params_scale_x = QVBoxLayout()
        # self.scale_x = QComboBox()
        # self.scale_x.addItems(['0.001', '0.005', '0.01', '0.05', '0.1', '0.5', '1', '5', '10', '50', '100', '500', '1000'])
        # self.scale_x.setCurrentIndex(6)
        # self.scale_x_label = QLabel("Max x scale")

        # plot_params_scale_x.addWidget(self.scale_x_label)
        # plot_params_scale_x.addWidget(self.scale_x)

        plot_params_scale_y = QVBoxLayout()
        # self.scale_y = QComboBox()
        # self.scale_y.addItems(['0.001', '0.005', '0.01', '0.05', '0.1', '0.5', '1', '5', '10', '50', '100', '500', '1000'])
        # self.scale_y.setCurrentIndex(6)
        self.scale_y_label = QLabel("???????????? ??????????????")

        plot_params_scale_y.addWidget(self.scale_y_label)
        # plot_params_scale_y.addWidget(self.scale_y)

        mechanical_slider_amplitude_layout = QVBoxLayout()
        self.amplitude_lable = QLabel("?????? y")
        self.mechanical_slider_amplitude = QDial()
        self.mechanical_slider_amplitude.setRange(0, 50)
        self.mechanical_slider_amplitude.setValue(1)
        mechanical_slider_amplitude_layout.addWidget(self.amplitude_lable)
        mechanical_slider_amplitude_layout.addWidget(self.mechanical_slider_amplitude)
        self.mechanical_slider_amplitude.valueChanged.connect(self.slider_frequency_move)
        self.mechanical_slider_amplitude_checkbox = QCheckBox("?????????????????? ??????????????")
        self.mechanical_slider_amplitude_checkbox.setChecked(True)
        mechanical_slider_amplitude_layout.addWidget(self.mechanical_slider_amplitude_checkbox)        
        
        mechanical_slider_frequency_layout = QVBoxLayout()
        self.frequency_lable = QLabel("?????? x")
        self.mechanical_slider_frequency = QDial()
        self.mechanical_slider_frequency.setRange(0, 50)
        self.mechanical_slider_frequency.setValue(1)
        mechanical_slider_frequency_layout.addWidget(self.frequency_lable)
        mechanical_slider_frequency_layout.addWidget(self.mechanical_slider_frequency)
        self.mechanical_slider_frequency.valueChanged.connect(self.slider_frequency_move)
        self.mechanical_slider_frequency_checkbox = QCheckBox("?????????????????? ??????????????")
        self.mechanical_slider_frequency_checkbox.setChecked(True)
        mechanical_slider_frequency_layout.addWidget(self.mechanical_slider_frequency_checkbox)

        # plot_params_layout.addLayout(plot_params_scale_x)
        plot_params_layout.addLayout(plot_params_scale_y)
        plot_params_layout.addLayout(mechanical_slider_amplitude_layout)
        plot_params_layout.addLayout(mechanical_slider_frequency_layout)
        plot_params_layout.addStretch()
        # self.scale_x.currentIndexChanged.connect(self.editScale)
        # self.scale_y.currentIndexChanged.connect(self.editScale)

        plots_layout = QHBoxLayout()
        plots_layout.addLayout(plot_params_layout)
        plots_layout.addWidget(self.signal_plot)
        plots_layout.addWidget(self.spectre_plot)        

        self.com_error_message = QErrorMessage()
        self.receive_button = QPushButton('???????????? ?????????????????? ?????????????? ???? ????')
        self.stop_listening_button = QPushButton('?????????????????? ?????????????????? ?????????????? ???? ????')
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(serial_ports_layout)
        main_layout.addLayout(params_layout)
        main_layout.addLayout(plots_layout)
        main_layout.addWidget(self.receive_button)
        main_layout.addWidget(self.stop_listening_button)

        self.setLayout(main_layout)
        self.loadSignals()
        self.add_signal_button.clicked.connect(self.addSignal)
        self.receive_button.clicked.connect(self.receive_signal_safely)
        self.stop_listening_button.clicked.connect(self.set_stop_safely)
        self.signals_list.currentIndexChanged.connect(self.showSignals)
        self.edit_signal_button.clicked.connect(self.editSignal)
        self.anim_checkbox.toggled.connect(self.changed_animation_checkbox_event)
        self.mechanical_slider_amplitude_checkbox.toggled.connect(self.change_amplitude_slider_event)
        self.mechanical_slider_frequency_checkbox.toggled.connect(self.change_frequency_slider_event)
        self.x_scale_value = 1.1
        self.y_scale_value = 1.1
        self.animation_flag = 0
        self.amplitude_slider_enabled = True
        self.frequency_slider_enabled = True

        self.amplitude_window = AmplitudeWindow(self.signalDataArray, self.animation_flag)
        self.frequency_window = FrequencyWindow(self.signalDataArray, self.animation_flag)
        self.summation_window = SummationWindow(self.signalDataArray, self.animation_flag)   
        self.showMaximized()

        #----------------------------------------------------------------------
        self.tmp = 0
        self.x = [0]
        #----------------------------------------------------------------------
        self.data = [0]
        self.data_ind = [0]
        self.data_dict = dict()
        self.first_contact = 1

    def change_amplitude_slider_event(self):
        self.amplitude_slider_enabled = not self.amplitude_slider_enabled

    def change_frequency_slider_event(self):
        self.frequency_slider_enabled = not self.frequency_slider_enabled

    def addSignal(self):
        if self.fs_signal_form_combo.currentText() == "-":
            return 

        form_name = self.fs_signal_form_combo.currentText()
        amplitude = self.fs_amplitude_spin.value()
        frequency = self.fs_frequency_spin.value()
        duration = self.fs_duration_spin.value()
        
        self.signalDataArray.appendSignal(signalData(form_name, amplitude, frequency, duration, False))
        self.loadSignals()
    
    def loadSignals(self):  
        self.signals_list.clear()      
        data = self.signalDataArray.getArray()
        if len(data) == 0:
            self.signals_list.addItem("?????????? ????????????")
        else:
            for i in range(len(data)):
                self.signals_list.addItem('???????????? ' + str(i + 1))
            self.signals_list.addItem('?????????? ????????????')

    def editSignal(self):
        form_name = self.fs_signal_form_combo.currentText()
        amplitude = self.fs_amplitude_spin.value()
        frequency = self.fs_frequency_spin.value()
        duration = self.fs_duration_spin.value()
        curInd = self.signals_list.currentIndex()
        if ((curInd != self.signalDataArray.getArraySize()) 
        and (curInd != -1)):
            self.signalDataArray.editSignalByIndex(signalData(form_name, amplitude, frequency, duration, 1), curInd)
            self.loadSignals()

    def changeSignalActivity(self):
        curInd = self.signals_list.currentIndex()
        if ((curInd != self.signalDataArray.getArraySize()) 
        and (curInd != -1)):
           self.signalDataArray.array[curInd].changeActivity() 
            
    
    def showSignals(self):
        if ((self.signals_list.currentIndex() == 0 and self.signalDataArray.getArraySize() == 0)
        or (self.signals_list.currentIndex() == self.signalDataArray.getArraySize())):
            self.fs_signal_form_combo.setCurrentIndex(1)
            self.fs_amplitude_spin.setValue(1)
            self.fs_duration_spin.setValue(5)
            self.fs_frequency_spin.setValue(1)
        elif self.signals_list.currentIndex() != -1:           
            curSignal = self.signalDataArray.getSignalByIndex(self.signals_list.currentIndex()).getData()
            self.fs_signal_form_combo.setCurrentIndex(signal_types.index(curSignal[0]))
            self.fs_amplitude_spin.setValue(curSignal[1])
            self.fs_duration_spin.setValue(curSignal[3])
            self.fs_frequency_spin.setValue(curSignal[2])
            
            if curSignal[4] == True:
                self.active_label.setText("???????????? ??????????????") 
            else:
                self.active_label.setText("???????????? ??????????????????")
    
    def set_stop(self):
        self.stop_flag = True

    def set_stop_safely(self):
        self.thread_manager.start(self.set_stop)
        self.stop_flag = True

    # @CoolDown(0.1)
    # function for drawing data from controller
    def reDraw(self):
        #print("Br", self.stop_flag)
        try:
            while not self.stop_flag:           
                self.signal_plot.axes.clear() # fixed
                self.signal_plot.axes.grid(True)
        #----------------------------------------------------------------------
                """if self.tmp != 0 and len(self.x):
                    self.x = np.append(self.x, max(self.x) + self.tmp)
                    self.x = np.delete(self.x, 0)
                else:
                    self.x = np.arange(0, len(self.data))
                self.x = self.x * (1/9.5)
                self.tmp = self.tmp + 1 """
        #----------------------------------------------------------------------
                self.x_scale_value = float(self.mechanical_slider_frequency.value())
                self.y_scale_value = float(self.mechanical_slider_amplitude.value())* 1.1

                self.signal_plot.axes.set_ylim(-self.y_scale_value, self.y_scale_value)
                #----------------------------------------------------------------------
                #self.signal_plot.axes.set_xlim(self.x.min(), self.x.max())
                #self.signal_plot.axes.set_xlim(min(self.data_ind), max(self.data_ind)+0.000000001)
                #self.signal_plot.axes.set_xlim(min(self.data_dict.keys()), max(self.data_dict.keys())+0.000000001)
                #----------------------------------------------------------------------
                # self.spectre_plot.axes.magnitude_spectrum(data, color='#1f77b4')

                #print("Data in redraw", self.data)
                #print("Inds", self.data_ind)
                
                self.signal_plot.axes.plot(self.data_dict.keys(), self.data_dict.values(), color='#1f77b4')
                self.signal_plot.view.draw()      
                
                    
            """
            print("inds", self.data_ind)
            print("data", self.data)
            print("len inds", len(self.data_ind))
            print("len data", len(self.data))
            print("dict keys", self.data_dict.keys())
            print("dict keys len", len(self.data_dict.keys()))
            print("dict values", self.data_dict.values())
            print("dict values len", len(self.data_dict.values()))
            """
            self.signal_plot.axes.plot(self.data_dict.keys(), self.data_dict.values(), color='#1f77b4')
            self.signal_plot.view.draw()
            self.data.clear()
            self.data_ind.clear()
            #self.data[0] = 0
        except Exception as e:
                print('error in draw', str(e))
        # self.spectre_plot.view.draw()

    # @njit(fastmath=True, cache=True, parallel=True)
    def receive_signal(self):
        if self.serial_ports_combo.currentText() == '-':
            self.stop_flag = True
            return         
        else:
            self.stop_flag = False
            generator_name = self.serial_ports_combo.currentText()

            #self.signal_plot.clear()
            #self.spectre_plot.clear()

            try:
                for port in self.serial_ports:
                    if generator_name == port.name:
                        print("Found serial port")
                        if 'serial' in port.description.lower() or 'VCP' in port.description.lower():
                            # init serial port and bound
                            # bound rate on two ports must be the same
                            #was 9600 // 115200
                            generator_ser = serial.Serial(generator_name, baudrate = 115200, timeout=1 )
                            generator_ser.flushInput()
                            generator_ser.flushOutput()
                            generator_ser.set_buffer_size(rx_size = 6, tx_size = 6)
                            delta = 0
                            delta_mas = 0
                            cur_time = 0

                            if self.first_contact:
                                self.first_contact = 0
                                while 1:
                                    generator_ser.write(bytearray(170))
                                    ser_bytes = generator_ser.read(1)
                                    print(ser_bytes)

                                    if (len(ser_bytes)):
                                        if ser_bytes[0] == 255:#ur_byte == 255:
                                            break
                            #print(generator_ser.portstr)

                            #data = []

                            #print('stop flag', self.stop_flag)

                            start_time = time.perf_counter()#time.time()   

                            while not self.stop_flag or (self.stop_flag and generator_ser.inWaiting() != 0): # ???????????? ???????????? ?? ??????????
                                if (self.stop_flag):
                                    generator_ser.send_break(0)
                                point_time = time.perf_counter()   
                                ser_bytes = generator_ser.read(2)
                                #print('huint', ser_bytes, len(ser_bytes) )
                                if len(ser_bytes) != 0:
                                    try:
                                       #
                                        cur_byte = int.from_bytes(ser_bytes, "little", signed=False) /1023.0*5.0
                                        #delta_mas.append(float(point_time - start_time) - cur_time)
                                        #print(delta)
                                        cur_time = float(point_time - start_time)
                                        # self.data_ind.append(cur_time)
                                        self.data.append(cur_byte)
                                        self.data_dict[cur_time] = cur_byte
                                        
                                        #print("Time", float(time.time() - start_time))
                                        #print(cur_byte)
                                    except Exception as e:
                                        print('error in input', str(e))
                                else:
                                    break
                                
                                #if(generator_ser.isOpen() and self.stop_flag): generator_ser.close()
                            
                            # print("ssss", generator_ser.read(generator_ser.inWaiting()))

                            # self.reDraw(self.data[-50:])

                            print("Stop flag:", self.stop_flag)
                            
                            """
                            self.signal_plot.clear()
                            self.spectre_plot.clear()
                            self.spectre_plot.axes.magnitude_spectrum(self.data, color='#1f77b4')
                            self.signal_plot.clear()
                            """
#----------------------------------------------------------------------
                            x = np.arange(0, len(self.data))
                            x = x * (1/9.5)
                            self.tmp = 0
                            self.x = [0]
#----------------------------------------------------------------------
                            print("Data", self.data, "len data", len(self.data), "len dict", len(self.data_dict.keys()))
                            print("Min/max data: ", min(self.data_dict), max(self.data_dict))
                            #print("Inds", self.data_ind)
                            
                            """
                            self.signal_plot.axes.plot(x, self.data, color='#1f77b4')
                            self.signal_plot.view.draw()
                            
                            self.data.clear()
                            self.data[0] = 0
                            """
                            return
                        else:
                            self.com_error_message.showMessage("?? ?????????????? ?????????? ???? ???????????????????? ???????????????? ????????????????????")
                            return    
            except Exception as e:
                print('error in common input', str(e))              

    
    def receive_signal_safely(self):
        self.stop_flag = False
        self.signal_plot.clear()
        self.spectre_plot.clear()
        self.data_dict.clear()

        self.thread_manager.start(self.receive_signal)
        #self.receive_signal()
        self.thread_manager.start(self.reDraw)


    def click_amplitude_event(self):        
        self.amplitude_window.updateSignalData(self.signalDataArray, self.animation_flag)
        self.amplitude_window.show()
         
    def click_sum_event(self):
        self.summation_window.updateSignalData(self.signalDataArray, self.animation_flag)
        self.summation_window.show()

    def click_frequency_event(self):        
        self.frequency_window.updateSignalData(self.signalDataArray, self.animation_flag)
        self.frequency_window.show()

    def changed_animation_checkbox_event(self):
        if (self.anim_checkbox.isChecked()):
            self.animation_flag = 1
        else:
            self.animation_flag = 0

    def set_signal(self):
        if self.signalDataArray.getArraySize == 0:
            return
        self.signalDataArray.array[self.signals_list.currentIndex()].changeActivity()
        if self.signalDataArray.array[self.signals_list.currentIndex()].getActivity() == True:
            self.active_label.setText("???????????? ??????????????")
            self.drawSignal()
        else:
            self.active_label.setText("???????????? ??????????????????")

            #rewrite clear part
            self.signal_plot.clear(self.x_scale_value, self.y_scale_value)
            self.spectre_plot.clear()

    def drawSignal(self):
        ind = self.signals_list.currentIndex()
        sigData = self.signalDataArray.getSignalByIndex(ind).getData()
        if (self.frequency_slider_enabled):
            freq = self.mechanical_slider_frequency.value()
        else:
            freq =  sigData[2]
        if (self.amplitude_slider_enabled):
            ampl = self.mechanical_slider_amplitude.value()
        else:
            ampl = sigData[1]
        self.signal_plot.plot(sigData[0], sigData[2], sigData[1],
        self.x_scale_value, self.y_scale_value, animation_flag=self.animation_flag)

        self.spectre_plot.plot(sigData[0], sigData[1], sigData[2], sigData[4])
    
    def slider_frequency_move(self):

        self.x_scale_value = float(self.mechanical_slider_frequency.value())* 1.1
        self.y_scale_value = float(self.mechanical_slider_amplitude.value())* 1.1


        if len(self.signalDataArray.array) and self.signalDataArray.array[self.signals_list.currentIndex()].getActivity() == True: 
            self.drawSignal() 
        
        self.signal_plot.axes.set_ylim(-self.y_scale_value, self.y_scale_value)
        self.signal_plot.axes.set_xlim(-self.x_scale_value, self.x_scale_value)

        self.signal_plot.view.draw()
        self.signal_plot.view.flush_events()


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpinBox,
    QDial,
    QCheckBox
)

from SignalPlotWidget import SignalPlotWidget
from SpectrePlotWidget import SpectrePlotWidget
from scalefuncs import *

class FrequencyWindow(QWidget):
    def __init__(self, signalDataArray, animation_flag = 1, parent=None):
        super().__init__(parent)
        self.signalDataArray = signalDataArray
        self.animation_flag = animation_flag
        
        self.fs_signals_label = QLabel('Основной сигнал')
        self.fs_signals_list = QComboBox(self)
        self.fs_signals_label.setBuddy(self.fs_signals_list)
        self.fs_signals_list.currentIndexChanged.connect(self.showSignalInfo_fs)

        fs_signals_layout = QHBoxLayout()
        fs_signals_layout.addWidget(self.fs_signals_label)
        fs_signals_layout.addWidget(self.fs_signals_list)

        self.fs_signal_form_combo = QLabel(self)
        self.fs_signal_form_combo_label = QLabel('Форма сигнала', self)
        self.fs_signal_form_combo_label.setBuddy(self.fs_signal_form_combo)

        fs_signals_form_layout = QHBoxLayout()
        fs_signals_form_layout.addWidget(self.fs_signal_form_combo_label)
        fs_signals_form_layout.addWidget(self.fs_signal_form_combo)

        self.fs_frequency_spin = QLabel()
        self.fs_frequency_label = QLabel('Частота')
        self.fs_frequency_label.setBuddy(self.fs_frequency_spin)

        fs_frequency_layout = QHBoxLayout()
        fs_frequency_layout.addWidget(self.fs_frequency_label)
        fs_frequency_layout.addWidget(self.fs_frequency_spin)

        self.fs_amplitude_spin = QLabel()
        self.fs_amplitude_label = QLabel('Амплитуда')
        self.fs_amplitude_label.setBuddy(self.fs_amplitude_spin)

        fs_amplitude_layout = QHBoxLayout()
        fs_amplitude_layout.addWidget(self.fs_amplitude_label)
        fs_amplitude_layout.addWidget(self.fs_amplitude_spin)

        self.fs_duration_spin = QLabel()
        self.fs_duration_label = QLabel('Продолжительность')
        self.fs_duration_label.setBuddy(self.fs_duration_spin)

        fs_duration_layout = QHBoxLayout()
        fs_duration_layout.addWidget(self.fs_duration_label)
        fs_duration_layout.addWidget(self.fs_duration_spin)

        self.plot1 = SignalPlotWidget(animation_flag=0)
        self.plot1.setFixedSize(350, 250)

        self.signal_plot = SignalPlotWidget()

        fs_signal = QVBoxLayout()
        fs_signal.addLayout(fs_signals_layout)
        fs_signal.addLayout(fs_signals_form_layout)
        fs_signal.addLayout(fs_frequency_layout)
        fs_signal.addLayout(fs_amplitude_layout)
        fs_signal.addLayout(fs_duration_layout)

        deviation_layout = QHBoxLayout()
        self.deviation_label = QLabel("Частота девиации:")
        self.deviation_input = QSpinBox()
        deviation_layout.addWidget(self.deviation_label)
        deviation_layout.addWidget(self.deviation_input)
        fs_signal.addLayout(deviation_layout)
        fs_signal.addWidget(self.plot1)
        fs_signal.addWidget(self.signal_plot)

        self.ss_signals_label = QLabel('Модулирующий сигнал')
        self.ss_signals_list = QComboBox(self)
        self.ss_signals_label.setBuddy(self.ss_signals_list)
        self.ss_signals_list.currentIndexChanged.connect(self.showSignalInfo_ss)

        ss_signals_layout = QHBoxLayout()
        ss_signals_layout.addWidget(self.ss_signals_label)
        ss_signals_layout.addWidget(self.ss_signals_list)

        self.ss_signal_form_combo = QLabel(self)
        self.ss_signal_form_combo_label = QLabel('Форма сигнала', self)
        self.ss_signal_form_combo_label.setBuddy(self.ss_signal_form_combo)

        ss_signals_form_layout = QHBoxLayout()
        ss_signals_form_layout.addWidget(self.ss_signal_form_combo_label)
        ss_signals_form_layout.addWidget(self.ss_signal_form_combo)

        self.ss_frequency_spin = QLabel()
        self.ss_frequency_label = QLabel('Частота')
        self.ss_frequency_label.setBuddy(self.ss_frequency_spin)

        ss_frequency_layout = QHBoxLayout()
        ss_frequency_layout.addWidget(self.ss_frequency_label)
        ss_frequency_layout.addWidget(self.ss_frequency_spin)

        self.ss_amplitude_spin = QLabel()
        self.ss_amplitude_label = QLabel('Амплитуда')
        self.ss_amplitude_label.setBuddy(self.ss_amplitude_spin)

        ss_amplitude_layout = QHBoxLayout()
        ss_amplitude_layout.addWidget(self.ss_amplitude_label)
        ss_amplitude_layout.addWidget(self.ss_amplitude_spin)

        self.ss_duration_spin = QLabel()
        self.ss_duration_label = QLabel('Продолжительность')
        self.ss_duration_label.setBuddy(self.ss_duration_spin)

        ss_duration_layout = QHBoxLayout()
        ss_duration_layout.addWidget(self.ss_duration_label)
        ss_duration_layout.addWidget(self.ss_duration_spin)

        self.plot2 = SignalPlotWidget(animation_flag=0)
        self.plot2.setFixedSize(350, 250)

        self.specter_plot = SpectrePlotWidget()

        self.ss_empty = QLabel(" ")

        ss_signal = QVBoxLayout()
        ss_signal.addLayout(ss_signals_layout)
        ss_signal.addLayout(ss_signals_form_layout)
        ss_signal.addLayout(ss_frequency_layout)
        ss_signal.addLayout(ss_amplitude_layout)
        ss_signal.addLayout(ss_duration_layout)
        ss_signal.addWidget(self.ss_empty)
        ss_signal.addWidget(self.plot2)
        ss_signal.addWidget(self.specter_plot)

        self.ok_button = QPushButton('Выполнить модуляцию')
        self.ok_button.clicked.connect(self.ok_button_clicked)

        signal_layout = QHBoxLayout()        
        
        """plot_params_layout = QVBoxLayout()
        plot_params_scale_x = QVBoxLayout()
        self.scale_x = QComboBox()
        self.scale_x.addItems(['0.001', '0.005', '0.01', '0.05', '0.1', '0.5', '1', '5', '10', '50', '100', '500', '1000'])
        self.scale_x.setCurrentIndex(6)
        self.scale_x_label = QLabel("Максимальное\nзначение частоты")

        plot_params_scale_x.addWidget(self.scale_x_label)
        plot_params_scale_x.addWidget(self.scale_x)

        plot_params_scale_y = QVBoxLayout()
        self.scale_y = QComboBox()
        self.scale_y.addItems(['0.001', '0.005', '0.01', '0.05', '0.1', '0.5', '1', '5', '10', '50', '100', '500', '1000'])
        self.scale_y.setCurrentIndex(6)
        self.scale_y_label = QLabel("Максимальноe\nзначение амплитуды")

        plot_params_scale_y.addWidget(self.scale_y_label)
        plot_params_scale_y.addWidget(self.scale_y)

        plot_params_layout.addLayout(plot_params_scale_x)
        plot_params_layout.addLayout(plot_params_scale_y)
        plot_params_layout.addStretch()
        self.scale_x.currentIndexChanged.connect(self.editScale)
        self.scale_y.currentIndexChanged.connect(self.editScale)
        """
        mechanical_slider_amplitude_layout = QVBoxLayout()
        self.amplitude_lable = QLabel("ось y")
        self.mechanical_slider_amplitude = QDial()
        self.mechanical_slider_amplitude.setRange(0, 50)
        self.mechanical_slider_amplitude.setValue(1)
        mechanical_slider_amplitude_layout.addWidget(self.amplitude_lable)
        mechanical_slider_amplitude_layout.addWidget(self.mechanical_slider_amplitude)
        self.mechanical_slider_amplitude.valueChanged.connect(self.slider_frequency_move)
        self.mechanical_slider_amplitude_checkbox = QCheckBox("Enabled")
        self.mechanical_slider_amplitude_checkbox.setChecked(True)
        mechanical_slider_amplitude_layout.addWidget(self.mechanical_slider_amplitude_checkbox)        
        
        mechanical_slider_frequency_layout = QVBoxLayout()
        self.frequency_lable = QLabel("ось x")
        self.mechanical_slider_frequency = QDial()
        self.mechanical_slider_frequency.setRange(0, 50)
        self.mechanical_slider_frequency.setValue(1)
        mechanical_slider_frequency_layout.addWidget(self.frequency_lable)
        mechanical_slider_frequency_layout.addWidget(self.mechanical_slider_frequency)
        self.mechanical_slider_frequency.valueChanged.connect(self.slider_frequency_move)
        self.mechanical_slider_frequency_checkbox = QCheckBox("Enabled")
        self.mechanical_slider_frequency_checkbox.setChecked(True)
        mechanical_slider_frequency_layout.addWidget(self.mechanical_slider_frequency_checkbox)

        mechanical_sliders = QVBoxLayout()
        mechanical_sliders.addLayout(mechanical_slider_frequency_layout)
        mechanical_sliders.addLayout(mechanical_slider_amplitude_layout)

       

        #signal_layout.addLayout(plot_params_layout)
        

        #fs_signal.addLayout(tmp)

        signal_layout.addLayout(fs_signal)
        signal_layout.addLayout(ss_signal)

        main_layout = QVBoxLayout()
        main_layout.addLayout(signal_layout)

        main_layout.addWidget(self.ok_button)
        
        tmp = QHBoxLayout() 
        tmp.addLayout(mechanical_sliders)
        tmp.addLayout(main_layout)
       
       # tmp.addWidget(self.signal_plot)

        self.x_scale_value = 1
        self.y_scale_value = 1
        self.x_scale_type = 0
        self.y_scale_type = 0

        self.deviation_input.setValue(10)
        self.setLayout(tmp)

    def updateSignalData(self, signalDataArray, animation_flag):
        self.signalDataArray = signalDataArray
        self.animation_flag = animation_flag
        self.setSignals()

    def closeEvent(self, event):
        event.accept()

    def editScale(self):
        cur_x_scale = float(self.scale_x.currentText())
        cur_y_scale = float(self.scale_y.currentText())
        self.x_scale_value = cur_x_scale * 1.1
        self.y_scale_value = cur_y_scale * 1.1                

        self.ok_button_clicked()
       
    def setSignals(self):
        self.fs_signals_list.clear()
        self.ss_signals_list.clear()
        data = self.signalDataArray.getArray()
        if len(data) == 0:
            self.fs_signals_list.addItem("Нет сигналов")
            self.ss_signals_list.addItem("Нет сигналов")
        else:
            for i in range(len(data)):
                self.fs_signals_list.addItem('Сигнал ' + str(i + 1))
                self.ss_signals_list.addItem('Сигнал ' + str(i + 1))

    def showSignalInfo_fs(self):
        if len(self.signalDataArray.getArray()) > 0:
            curSignal_fs = self.signalDataArray.getSignalByIndex(self.fs_signals_list.currentIndex()).getData() 

            self.fs_amplitude_spin.setText(str(curSignal_fs[1]))
            self.fs_duration_spin.setText(str(curSignal_fs[3]))
            self.fs_frequency_spin.setText(str(curSignal_fs[2]))
            self.fs_signal_form_combo.setText(curSignal_fs[0])

            self.plot1.plot(curSignal_fs[0], curSignal_fs[2], curSignal_fs[1], flag=0, animation_flag=0)

    def showSignalInfo_ss(self):
        if len(self.signalDataArray.getArray()) > 0:
            curSignal_ss = self.signalDataArray.getSignalByIndex(self.ss_signals_list.currentIndex()).getData() 

            self.ss_amplitude_spin.setText(str(curSignal_ss[1]))
            self.ss_duration_spin.setText(str(curSignal_ss[3]))
            self.ss_frequency_spin.setText(str(curSignal_ss[2]))
            self.ss_signal_form_combo.setText(curSignal_ss[0])
            self.plot2.plot(curSignal_ss[0], curSignal_ss[2], curSignal_ss[1], flag=0, animation_flag=0)

    def ok_button_clicked(self):
        ind_fs = self.fs_signals_list.currentIndex()
        ind_ss = self.ss_signals_list.currentIndex()
        signal_fs = self.signalDataArray.getSignalByIndex(ind_fs).getData()
        signal_ss = self.signalDataArray.getSignalByIndex(ind_ss).getData()
        freq_dev = self.deviation_input.value()
        self.signal_plot.freq_modulate(signal_fs[2], self.x_scale_value, signal_ss[1], signal_ss[2], 
        signal_fs[1], self.y_scale_value, self.animation_flag, freq_dev)
        self.specter_plot.freq_modulate(signal_fs[2], signal_ss[2], freq_dev)
    
    def slider_frequency_move(self):

        self.x_scale_value = float(self.mechanical_slider_frequency.value())* 1.1
        self.y_scale_value = float(self.mechanical_slider_amplitude.value())* 1.1

        self.signal_plot.axes.set_ylim(-self.y_scale_value, self.y_scale_value)
        self.signal_plot.axes.set_xlim(-self.x_scale_value, self.x_scale_value)

        self.signal_plot.view.draw()
        self.signal_plot.view.flush_events()
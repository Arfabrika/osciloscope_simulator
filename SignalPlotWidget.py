# This Python file uses the following encoding: utf-8
from PlotWidget import PlotWidget
from scalefuncs import *

from wave import (
    generate_sine_wave,
    generate_cosine_wave,
    generate_triangle_wave,
    generate_sawtooth_wave,
    generate_square_wave,
    mod_generate_sine_wave,
    mod_generate_cosine_wave,
    mod_generate_triangle_wave,
    mod_generate_sawtooth_wave,
    mod_generate_square_wave,
    modulating,
    freq_modulating
)

wave_generators = {
    'sine': generate_sine_wave,
    'cosine': generate_cosine_wave,
    'triangle': generate_triangle_wave,
    'sawtooth': generate_sawtooth_wave,
    'square': generate_square_wave,
}

mod_wave_generators = {
    'sine': mod_generate_sine_wave,
    'cosine': mod_generate_cosine_wave,
    'triangle': mod_generate_triangle_wave,
    'sawtooth': mod_generate_sawtooth_wave,
    'square': mod_generate_square_wave,
}


class SignalPlotWidget(PlotWidget):
    def __init__(self, animation_flag = 1, parent=None):
        super().__init__(parent)

        self.arrays = []
        self.animation_flag = animation_flag

        self.axes.set_xlabel('Time, s')
        self.axes.set_ylabel('U, V')
        self.axes.grid(True)

    def plot(self, signal_name, frequency, amplitude=1, x_scale_value = 1, 
    y_scale_value = 1, flag = 1, animation_flag = 1):
        self.clear()
        self.animation_flag = animation_flag
        if flag == 1:
            self.axes.set_title(self.generate_formula(signal_name, amplitude, frequency))
        if signal_name == '-':
            return

        x_scale_type, y_scale_type = getScaleType(frequency, amplitude)
        frequency,amplitude = getScaledParams(frequency, amplitude, x_scale_type, y_scale_type)
        x_label, y_label = getAxisNames(x_scale_type, y_scale_type)
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
               
        x, y = wave_generators[signal_name](amplitude, frequency, x_scale_value)     

        x_points = []
        y_points = []
        if flag == 1:
            self.axes.set_xlim(-x_scale_value, x_scale_value)
            self.axes.set_ylim(-y_scale_value, y_scale_value)
        
        if self.animation_flag == 1 and flag == 0:
            i = 0
            checkvalue = len(x) / 20 
            for point in x:
                x_points.append(point)
                y_points.append(y[i])
                
                i += 1

                if i % (checkvalue) == 0:
                    self.axes.plot(x_points, y_points, color='#1f77b4')
                    self.view.draw()
                    self.view.flush_events()      
        else:
            self.axes.plot(x, y, color='#1f77b4')
            self.view.draw()
            self.view.flush_events()

    def generate_formula(self, fs_form_name, fs_amplitude=1, fs_frequency=1, ss_form_name = '-', ss_amplitude =1, ss_frequency=1):
        form = 'Formula: '

        if (fs_form_name == 'sine'):
            form += str(fs_amplitude) + r'$\cdot$' + 'sin(' + str(fs_frequency) + r'$\cdot$' + 't)'
        elif (fs_form_name == 'cosine'):
            form += str(fs_amplitude) + r'$\cdot$' +'cos(' + str(fs_frequency) + r'$\cdot$' + 't)'
        elif (fs_form_name == 'square'):
            form += r'$\frac{4\cdot'+ str(fs_amplitude) + r'}{\pi}\sum_{k=1}^\infty \frac{sin(k\cdot' + str(fs_frequency) +  r'\cdot t)}{k}$'   
        elif (fs_form_name == 'triangle'):
            form += r'$\frac{8\cdot'+ str(fs_amplitude) + r'}{\pi^{2}}\sum_{k=1}^\infty (-1)^{\frac{k-1}{2}} \cdot \frac{  sin(k\cdot'+ str(fs_frequency) + r'\cdot t)}{k^{2}}$'
        else:
            form += r'$\frac{' + str(fs_amplitude) + r'}{2} - \frac{'+ str(fs_amplitude) + r'}{\pi}\sum_{k=1}^\infty \frac{1}{k} \cdot sin(k\cdot' + str(fs_frequency) +  r'\cdot t)$'
        
        if (ss_form_name != '-'):
            form += ' + '
            if (ss_form_name == 'sine'):
                form += str(ss_amplitude) + 'sin(' + str(ss_frequency) + 't)'
            elif (ss_form_name == 'cosine'):
                form += str(ss_amplitude) +'cos(' + str(ss_frequency) + 't)'
            elif (ss_form_name == 'square'):
                form += r'$\frac{4\cdot'+ str(ss_amplitude) + r'}{\pi}\sum_{k=1}^\infty \frac{sin(k\cdot' + str(ss_frequency) +  r'\cdot t)}{k}$'   
            elif (ss_form_name == 'triangle'):
                form += r'$\frac{8\cdot'+ str(ss_amplitude) + r'}{\pi^{2}}\sum_{k=1}^\infty (-1)^{\frac{k-1}{2}} \cdot \frac{  sin(k\cdot'+ str(ss_frequency) + r'\cdot t)}{k^{2}}$'
            else:
                form += r'$\frac{' + str(ss_amplitude) + r'}{2} - \frac{'+ str(ss_amplitude) + r'}{\pi}\sum_{k=1}^\infty \frac{1}{k} \cdot sin(k\cdot' + str(ss_frequency) +  r'\cdot t)$'            
        
        return form

    def generate_formula_arr(self, signalArray):
        form = 'Formula: '
        ind = 0
        for signal in signalArray:
            curSigData = signalArray.getSignalByIndex(ind).getData()
        if (curSigData[0] == 'sine'):
            form += str(curSigData[1]) + r'$\cdot$' + 'sin(' + str(curSigData[2]) + r'$\cdot$' + 't)'
        elif (curSigData[0] == 'cosine'):
            form += str(curSigData[1]) + r'$\cdot$' +'cos(' + str(fs_frequency) + r'$\cdot$' + 't)'
        elif (curSigData[0] == 'square'):
            form += r'$\frac{4\cdot'+ str(curSigData[1]) + r'}{\pi}\sum_{k=1}^\infty \frac{sin(k\cdot' + str(fs_frequency) +  r'\cdot t)}{k}$'   
        elif (curSigData[0] == 'triangle'):
            form += r'$\frac{8\cdot'+ str(curSigData[1]) + r'}{\pi^{2}}\sum_{k=1}^\infty (-1)^{\frac{k-1}{2}} \cdot \frac{  sin(k\cdot'+ str(fs_frequency) + r'\cdot t)}{k^{2}}$'
        else:
            form += r'$\frac{' + str(curSigData[1]) + r'}{2} - \frac{'+ str(curSigData[1]) + r'}{\pi}\sum_{k=1}^\infty \frac{1}{k} \cdot sin(k\cdot' + str(fs_frequency) +  r'\cdot t)$'
        
        
        return form


    def polyharmonic(self, fs_signal_name, fs_frequency, fs_amplitude=1,  fs_duration=1,
                     ss_signal_name='', ss_amplitude=1, ss_frequency=1, ss_duration=1, animation_flag = 1):
        self.clear()
        self.animation_flag = animation_flag
        if fs_signal_name == '-' or ss_signal_name == '-':
            return

        fs_x_scale_type, fs_y_scale_type = getScaleType(fs_frequency, fs_amplitude)
        ss_x_scale_type, ss_y_scale_type = getScaleType(ss_frequency, ss_amplitude)
        x_type_mas = [fs_x_scale_type, ss_x_scale_type]
        y_type_mas = [fs_y_scale_type, ss_y_scale_type]
        freq_mas = [fs_frequency, ss_frequency]
        ampl_mas = [fs_amplitude, ss_amplitude]
        freq_mas, ampl_mas = getScaledParamsInMas(freq_mas, ampl_mas, x_type_mas, y_type_mas)
        self.axes.set_title(self.generate_formula(fs_signal_name, fs_amplitude, fs_frequency,
                     ss_signal_name, ss_amplitude, ss_frequency))
        #fx, fy = wave_generators[fs_signal_name](fs_amplitude, fs_frequency, fs_sample_rate, fs_duration)
        fx, fy = wave_generators[fs_signal_name](ampl_mas[0], freq_mas[0], fs_duration)
        
        if len(self.arrays) == 0:
            sx, sy = wave_generators[ss_signal_name](ampl_mas[1], freq_mas[1], ss_duration)
            py = fy + sy
            self.arrays.append([sx, sy])
            self.arrays.append([fx, py])
        else:
            py = fy + self.arrays[len(self.arrays) - 1][1]

            self.arrays.append([fx, py])

        if self.animation_flag:
            x_points = []
            y_points = []
            i = 0

            for point in fx:
                x_points.append(point)
                y_points.append(py[i])

                i += 1

                if i % (len(fx) / 20) == 0:
                    self.axes.plot(x_points, y_points, color='#1f77b4')
                    self.view.draw()
                    self.view.flush_events()
        else:
            self.axes.plot(self.arrays[len(self.arrays) - 1][0], self.arrays[len(self.arrays) - 1][1], color='#1f77b4')
            self.view.draw()

    def modulate(self, fs_frequency, fs_duration, ss_amplitude, ss_frequency, fs_amplitude, 
    y_scale = 1, fs_x_scale_type = 0, fs_y_scale_type = 0, ss_x_scale_type = 0, ss_y_scale_type = 0,
    animation_flag = 1, flag = 1):
        self.clear()
        self.animation_flag = animation_flag

         # x scale
         # ?????????? ???? flag?
        if flag == 1:
            
            x_scale_type = max(fs_x_scale_type, ss_x_scale_type)
            y_scale_type = max(fs_y_scale_type, ss_y_scale_type)
            if x_scale_type == 2:
                fs_frequency /= 1000000
                ss_frequency /= 1000000
                self.axes.set_xlabel('Time, ??s')
            elif x_scale_type == 1:
                fs_frequency /= 1000
                ss_frequency /= 1000
                self.axes.set_xlabel('Time, ms')
       
            # y scale
            if y_scale_type == 2:
                fs_amplitude /= 1000000
                ss_amplitude /= 1000000
                self.axes.set_ylabel('U, ??V')
            elif y_scale_type == 1:
                fs_amplitude /= 1000
                ss_amplitude /= 1000
                self.axes.set_ylabel('U, mV')

        x, y = modulating(fs_frequency, fs_duration, ss_amplitude, ss_frequency, fs_amplitude)
        
        if flag == 1:
            self.axes.set_xlim(-fs_duration, fs_duration)
            self.axes.set_ylim(-y_scale, y_scale)

        if self.animation_flag:
            i = 0
            for point in x:
                i += 1
                if i % 40 == 0:
                    self.axes.plot(x[0:i], y[0:i], color='#1f77b4')
                    self.view.draw()
                    self.view.flush_events()
        else:
            self.axes.plot(x, y, color='#1f77b4')
            self.view.draw()

    def freq_modulate(self, fs_frequency, fs_duration, ss_amplitude, ss_frequency, 
    fs_amplitude, y_scale= 1, animation_flag = 1, freq_dev = 10):
        self.clear()
        self.animation_flag = animation_flag        
        fs_x_scale_type, fs_y_scale_type = getScaleType(fs_frequency, fs_amplitude)
        ss_x_scale_type, ss_y_scale_type = getScaleType(ss_frequency, ss_amplitude)
        x_type_mas = [fs_x_scale_type, ss_x_scale_type]
        y_type_mas = [fs_y_scale_type, ss_y_scale_type]
        freq_mas = [fs_frequency, ss_frequency]
        ampl_mas = [fs_amplitude, ss_amplitude]
        freq_mas, ampl_mas = getScaledParamsInMas(freq_mas, ampl_mas, x_type_mas, y_type_mas)
        x, y = freq_modulating(fs_frequency, fs_duration, ss_amplitude, ss_frequency, freq_dev)
        # TODO make a scale in frequency window
        #x, y = freq_modulating(freq_mas[0], fs_duration, ampl_mas[1], freq_mas[1], freq_dev)

        self.axes.set_xlim(-fs_duration, fs_duration )
        self.axes.set_ylim(-y_scale , y_scale)
        x_label, y_label = getAxisNames(min(x_type_mas), min(y_type_mas))
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)

        if self.animation_flag:
            i = 0
            for point in x:
                i += 1
                if i % 40 == 0:
                    self.axes.plot(x[0:i], y[0:i], color='#1f77b4')
                    self.view.draw()
                    self.view.flush_events()
        else:
            self.axes.plot(x, y, color='#1f77b4')
            self.view.draw()                

    def remove_last_points(self, x_scale = 0, y_scale = 0):
        self.clear(x_scale, y_scale) 
        self.arrays.pop()

        if len(self.arrays) != 0:
            if(len(self.arrays) != 0):
                xy = self.arrays[-1]
                x = xy[0] 
                y = xy[1] 

                i = 0
                for point in x:

                    i += 1

                    if i % 40 == 0:
                        self.axes.plot(x[0:i], y[0:i], color='#1f77b4')
                        self.view.draw()
                        self.view.flush_events()

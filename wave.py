import numpy as np
from scipy import signal

def generate_sine_wave(amplitude, freq, duration):
    x = np.linspace(-duration, duration, 440 * int(10 / duration) if 10 / duration > 1 else int(440 * duration), endpoint=False)
    frequencies = x * freq
    y = amplitude * np.sin(frequencies * (2 * np.pi))
    return x, y


def generate_cosine_wave(amplitude, freq, duration):
    x = np.linspace(-duration, duration, 440 * int(10 / duration) if 10 / duration > 1 else int(440 * duration), endpoint=False)
    frequencies = x * freq
    y = amplitude * np.cos(frequencies * (2 * np.pi))
    return x, y


def generate_triangle_wave(amplitude, freq, duration):
    x = np.linspace(-duration, duration, 440 * int(10 / duration) if 10 / duration > 1 else int(440 * duration), endpoint=False)
    frequencies = x * freq
    y = amplitude * signal.sawtooth(frequencies * (2 * np.pi), 0.5)
    return x, y


def generate_sawtooth_wave(amplitude, freq, duration):
    x = np.linspace(-duration, duration, 440 * int(10 / duration) if 10 / duration > 1 else int(440 * duration), endpoint=False)
    frequencies = x * freq
    y = amplitude * signal.sawtooth(frequencies * (2 * np.pi), 1)
    return x, y


def generate_square_wave(amplitude, freq, duration):
    x = np.linspace(-duration, duration, 440 * int(10 / duration) if 10 / duration > 1 else int(440 * duration), endpoint=False)
    frequencies = x * freq
    y = amplitude * signal.square(frequencies * (2 * np.pi))
    return x, y

def generate_spectr_sine(ampl, freq, duration):
    num_of_points = 440 * int(10 / duration) if 10 / duration > 1 else int(440 * duration)
    x = np.linspace(-duration, duration, num_of_points, endpoint=False)
    y = [0] * num_of_points#y = np.empty(num_of_points, dtype=np.int32) #[]
    #for i in range(num_of_points):
    #    y[i] = 0
    #y = np.linspace(0, 0, num_of_points, endpoint=False)
    y[int(freq * (num_of_points / 2 * duration))] = ampl
    return x, y


def mod_generate_sine_wave(freq, duration, ampl):
    num_of_points = 440 * max((int(10 / duration) if 10 / duration > 1 else int(duration)), freq)
    x = np.linspace(0, 10, num_of_points, endpoint=False)
    y = [0] * len(x)
    y[int(freq * num_of_points / max(x))] = ampl
    #y[int(num_of_points / freq / 10 - 1)] = ampl
    return x, y


def mod_generate_cosine_wave(freq, duration):
    x = np.linspace(-duration, duration, 440 * int(10 / duration) if 10 / duration > 1 else int(440 * duration), endpoint=False)
    frequencies = x * freq
    y = np.cos(frequencies * (2 * np.pi))
    return x, y


def mod_generate_triangle_wave(freq, duration):
    x = np.linspace(-duration, duration, 440 * int(10 / duration) if 10 / duration > 1 else int(440 * duration), endpoint=False)
    frequencies = x * freq
    y = signal.sawtooth(frequencies * (2 * np.pi), 0.5)
    return x, y


def mod_generate_sawtooth_wave(freq, duration):
    x = np.linspace(-duration, duration, 440 * int(10 / duration) if 10 / duration > 1 else int(440 * duration), endpoint=False)
    frequencies = x * freq
    y = signal.sawtooth(frequencies * (2 * np.pi), 1)
    return x, y


def mod_generate_square_wave(freq, duration):
    x = np.linspace(-duration, duration, 440 * int(10 / duration) if 10 / duration > 1 else int(440 * duration), endpoint=False)
    frequencies = x * freq
    y = signal.square(frequencies * (2 * np.pi))
    return x, y


def modulating (fs_frequency, fs_duration, ss_amplitude, ss_frequency, fs_amplitude):
    x = np.linspace(-fs_duration, fs_duration, 440 * int(10 / fs_duration) if 10 / fs_duration > 1 else int(fs_sample_rate * 440), endpoint=False)
    y = []

    t1 = (2 * np.pi) / (1 / ss_frequency)
    t2 = (2 * np.pi) / (1 / fs_frequency)

    for point in x:
        y.append((fs_amplitude + ss_amplitude * np.cos(t1 * point)) * np.cos(t2 * point))

    return x, y

def specter_modulating(fs_frequency, fs_duration, ss_amplitude, ss_frequency, fs_amplitude):
    x = np.linspace(0, fs_duration, 440 * fs_duration, endpoint=False)
    y = []

    t1 = (2 * np.pi) / (1 / ss_frequency)
    t2 = (2 * np.pi) / (1 / fs_frequency)

    for point in x:
       y.append(0)
    index = len(x) // 2

    y[index] = fs_amplitude * np.cos(t2 * point)
    y[index + len(x) // 6] = (fs_amplitude * (ss_amplitude / fs_amplitude) / 2) * np.cos((t2 + t1) * point)
    y[index - len(x) // 6] = (fs_amplitude * (ss_amplitude / fs_amplitude) / 2) * np.cos((t2 - t1) * point)
    return x, y

def freq_modulating(fs_frequency, fs_duration, ss_amplitude, ss_frequency, freq_dev):
    # enough points?
    x = np.linspace(-fs_duration, fs_duration, int(fs_duration * 40 * int((ss_frequency + fs_frequency))), endpoint=False)
    y = []
    
    twopi = 2 * np.pi
    for point in x:
        y.append(ss_amplitude * np.cos(ss_frequency * twopi * point + freq_dev * np.sin(fs_frequency * point * twopi)))
    return x, y

def freq_modulating_specter(fs_frequency, ss_frequency, freq_dev):
    beta = freq_dev / fs_frequency
    left = ss_frequency -  (beta + 1) * fs_frequency
    right = ss_frequency +  (beta + 1) * fs_frequency
    x = np.linspace(left, right, int((right - left) * (ss_frequency + fs_frequency) / 4), endpoint=False)
    y = []
    for point in x:
       y.append(0)
    index = len(x) // 2
    i = 0.5
    n = 1
    y[index] = 1
    ind1 = fs_frequency * n * (ss_frequency + fs_frequency) / 4
    while (int(index - ind1) >= 0 and int(index + ind1) < len(x)):
        y[int(index - ind1)] = i
        y[int(index + ind1)] = i
        i /= 2
        n += 1
        ind1 = fs_frequency * n * (ss_frequency + fs_frequency) / 4
    return x, y

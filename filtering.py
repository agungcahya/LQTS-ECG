from numpy import diff
import matplotlib.pyplot as plt
import bwr
#====================================== DERIVATIVE AND ADAPTIVE FILTERING ==============================================
# Formula : H(z) = 0.1*(2+z^-1 - z^-2 - z^-3) #Five point derivative
def derivative(raw_signal):
    der = diff(raw_signal)
    return der

def five_point_derivative(raw_signal):
    ecg_der = []
    for i in xrange(len(raw_signal)):
        der = 0.1 * 2 * (raw_signal[i] + raw_signal[i-1] - raw_signal[i-3] - raw_signal[i-4])
        ecg_der.append(der)

    return ecg_der

def adaptive_filter(ecg_der):
    ecg_adp = []; a = 0.95;
    ecg_adp.append(0.01);
    for i in xrange(len(ecg_der)):
            adp = ( a * ecg_adp[i-1] ) + ( (1 - a) * ecg_der[i])
            ecg_adp.append(adp)
    return ecg_adp

def squaring(data):
    squared = []
    for i in range(len(data)):
        data[i] = data[i] ** 2
        squared.append(data[i])
    return squared


def main_filter(lines, signal_type):
    raw_signal = [0] * (len(lines) - 2)
    for i in xrange(len(raw_signal)):
        raw_signal[i] = float(lines[i + 2].split(',')[signal_type])

    # plt.figure(1)
    # plt.subplot(311);
    # plt.tight_layout()
    # plt.title('Raw signal ')
    # plt.plot(raw_signal)
    # plt.xlim(0, len(raw_signal[1000:2000]) - 1)
    #plt.plot(range(len(raw_signal)), raw_signal)
    len_sample = len(raw_signal)
    # print len_sample
    # ___________________________________________2.1 ECG FILTERING___________________________________________________________
    #(baseline, raw_signal) = bwr.bwr(raw_signal)
    ecg_der = five_point_derivative(raw_signal)
    ecg_adp = adaptive_filter(ecg_der)

    sampled_window = len_sample
    sample = []
    for i in range(len_sample):
        sample.append(ecg_adp[i-1])
    # print ecg_adp
    # print "Derivative result : ", ecg_der
    # plt.subplot(312);
    # plt.tight_layout()
    # plt.plot(ecg_adp)
    # plt.xlim(0, len(ecg_adp[1000:2000]) - 1)
    # #plt.plot(range(len(ecg_adp)), ecg_adp)
    # plt.title('Filtering')
    # print(len(sample))
    return sample
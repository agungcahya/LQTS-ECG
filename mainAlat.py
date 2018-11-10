import time
import filtering as filt
import features as feat
import features2 as feat2
import matplotlib.pyplot as plt
import dwt

#path = 'data/'


def main(data):
        signal_type = 0
        fs = 250
        qtcN = 470;
        f = open(data, 'r')
        lines = f.readlines()
        f.close()
        datafil = filt.main_filter(lines,signal_type)
        rec35, rec58, rec15, rec48 = dwt.wavelet(datafil, 'db6', 8)
        result = feat.main_test(datafil, fs, qtcN)
        #result = feat2.main_test(rec35, rec58, rec15, rec48, fs, qtcN)

        plt.show()
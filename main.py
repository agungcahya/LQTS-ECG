import time
import filtering as filt
import features as feat
import features2 as feat2
import matplotlib.pyplot as plt
import dwt

path = 'data/'
#path = 'data_alat/'
data = ['sel1','sel2','sel3','sel4','sel5','sel6','sel7','sel8','sel9','sel10']
data2 = ['sel11','sel12','sel13','sel14','sel15','sel16','sel17','sel18','sel19','sel20']
data3 = ['sel21','sel22','sel23','sel24','sel25','sel26','sel27','sel28','sel29','sel30',]
signal_type = 1
fs = 250
qtcN = 470;

for i in range(len(data)):
        print "========= DATA : ", data3[i] ,"============"
        read_data       = path + data3[i] + '.csv'
        #read_anotasi    = path + data[i] + '_an.csv'
        f = open(read_data, 'r')
        lines = f.readlines()
        f.close()
        datafil = filt.main_filter(lines,signal_type)

        feat.main_test(datafil, fs, qtcN)
        rec35, rec58, rec15, rec48 = dwt.wavelet(datafil, 'db4', 8)
        feat2.main_test(rec35, rec58, rec15, rec48, fs, qtcN)
        # rec35, rec58, rec15, rec48 = dwt.wavelet(datafil, 'db5', 8)
        # feat2.main_test(rec35, rec58, rec15, rec48, fs, qtcN)
        rec35, rec58, rec15, rec48 = dwt.wavelet(datafil, 'db6', 8)
        feat2.main_test(rec35, rec58, rec15, rec48, fs, qtcN)

#plt.show()
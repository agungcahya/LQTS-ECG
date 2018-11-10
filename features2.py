import time
import matplotlib.pyplot as plt
import filtering as filt
import math
import classification as clas
import bwr
import pywt
import dwt

def main_test(rec35, rec58, rec15, rec48, fs, qtcN):
    #___________________________________________2.1 FEATURE EXTRACTION__________________________________________________
    rec35 = rec35.tolist()
    rec58 = rec58.tolist()
    rec15 = rec15.tolist()
    rec48 = rec48.tolist()

    # plt.figure(1)
    # plt.subplot(313);
    # plt.plot(rec35)
    # #plt.plot(range(len(rec35)),rec35)
    # plt.xlim(0, len(rec35[1000:2000]) - 1)
    # plt.title('Sample Data')
    sample = rec35

    # 1. IDENTIFY R PEAKS
    MAX = max(sample);

    # 2. Obtain a threshold such that: Threshold t = (0.4) * MAX
    R = 0.4 * MAX
    list_upper = []; r_peaks = []
    for i in range(len(sample) - 1):
        if(sample[i] > R):
            #first upper
            if(len(list_upper) == 0):
                list_upper.append(sample[i])
            else:
                list_upper.append(sample[i])
                if(sample[i+1] < R):
                    find_r = max(list_upper)
                    find_r_in = sample.index(find_r)
                    r_plot = plt.plot(find_r_in, find_r, 'r.', markersize=8) #Plot the maximum peak
                    r_detect = [find_r_in, find_r]
                    r_peaks.append(r_detect)
                    list_upper = []

# 3. Calculate RR Interval & SET P Q S T peak
#     print "Total R peaks : ", len(r_peaks)

    # print r_peaks
    sample = rec48
    qtc = []
    rr_list = []
    pr_list = []
    qrs_list = []
    qt_list = []
    bpm_list = []
    for i in range(len(r_peaks) - 1):
        r1 = r_peaks[i][0]
        r2 = r_peaks[i + 1][0]
        rr = r2 - r1
        rr_list.append(rr)
        qtcB = [0, 0]
        qtcFri = [0, 0]
        qtcFra = [0, 0]
        qtcH = [0, 0]
        qtcR = [0, 0]

        # print "======= Beat ", i + 1, " to Beat ",i+2, " ========="
        # print "R1 : ", r1
        # print "R2 : ", r2
        # print "RR Interval : ", rr
        # SET T
        t_on  = (15 * rr)/100
        t_on  = t_on + r1
        t_off = (55 * rr)/100
        t_off = t_off + r1
        #plt.axvspan(t_on, t_off, facecolor='#f9ff4f', alpha=0.5)

        t = t_on; t_list = []
        while(t <= t_off):
            t_list.append(sample[t])
            t += 1
        t_peak = max(t_list)
        t_in   = sample.index(t_peak)
        t_plot = plt.plot(t_in, t_peak, 'g.', markersize=8) #Plot the T peak

        t = t_in; tend_list = []
        while (t <= t_off):
            if (sample[t] >= 0.0):
                tend_list.append(sample[t])
            # print(sample[t])
            t += 1
            # print(len(tend_list))
        if (len(tend_list) == 0):
            t_end = t_in
        else:
            t_min = min(tend_list)
            t_end = sample.index(t_min)
        t_plot = plt.plot(t_end, t_min, 'g.', markersize=8)  # Plot the T peak

        # SET P
        p_on  = (35 * rr)/100
        p_on  = r1 - p_on
        p_off = (5 * rr)/100
        p_off = r1 - p_off
        #plt.axvspan(p_on, p_off, facecolor='#ff9999', alpha=0.5)

        t = p_on; t_list = []
        while(t <= p_off):
            t_list.append(sample[t])
            t += 1
        p_peak = max(t_list)
        p_in   = sample.index(p_peak)
        p_plot = plt.plot(p_in, p_peak, 'b.', markersize=8) #Plot the P peak
        #print "P Peak   : ", p_in

        # SET S
        s_on  = r1
        s_off = (35 * rr) / 100
        s_off = r1 + s_off
        # plt.axvspan(s_on, s_off, facecolor='#beff9b', alpha=0.5)

        t = s_on; t_list = []
        while(t <= s_off):
            t_list.append(sample[t])
            t += 1
        s_peak = min(t_list)
        s_in   = sample.index(s_peak)
        s_plot = plt.plot(s_in, s_peak, 'y.', markersize=8) #Plot the S peak
        #print "S Peak   : ", s_in

        # SET Q
        x = (6.65 / 100) * rr
        q_on  = (5 * rr)/100
        q_on  = r1 - q_on
        q_off = r1

        t = q_on; t_list = []
        while(t <= q_off):
            t_list.append(sample[t])
            t += 1
        q_peak = min(t_list)
        q_in   = sample.index(q_peak)
        q_plot = plt.plot(q_in, q_peak, 'r.', markersize=8) #Plot the Q peak
        plt.axhline(0, color='#42f486')

# 4. ECG Timing Intervals Calculations
        # PR Interval
        t_pr = r1 - p_in
        pr_list.append(t_pr)
        #print "PR Interval : ", t_pr

        # QRS Duration
        x = (6.65/100)*rr
        t_qrs = (s_in + x)-(q_in - x)
        qrs_list.append(t_qrs)
        #print "QRS Duration : ", t_qrs

        #QT Interval
        t_qt = t_end - (q_in-x)
        qt_list.append(t_qt)
        #print "QT Interval : ", t_qt
        plt.axvspan(q_in - x, t_in + (rr * 0.13), facecolor='#beff9b', alpha=0.5)

        #QT Corrected
        k=0.006
        t_qt2 = float(t_qt) / fs
        rr2 = float(rr) / fs
        t_qtcB = (t_qt2 / math.sqrt(rr2)) * 1000
        t_qtcFri = (t_qt2 / math.pow(rr2, 1.0 / 3.0)) * 1000
        t_qtcFra = (t_qt2 + (0.154 * (1 - rr2))) * 1000
        t_qtcH = (t_qt2 + (0.00175*(60/rr2-60))) * 1000
        t_qtcR = (t_qt2 - (0.185 * (rr2-1))+k) * 1000
        qtcB[0] = t_qtcB
        qtcFri[0] = (t_qtcFri)
        qtcFra[0] = (t_qtcFra)
        qtcH[0] = (t_qtcH)
        qtcR[0] = (t_qtcR)
        # print "QT Corrected : ", qtcB[0]

        if (qtcB[0] > qtcN):
            qtcB[1] = 1
            # print "LQTS"
        else:
            qtcB[1] = 0
            # print "Normal"

        if (qtcFri[0] > qtcN):
            qtcFri[1] = 1
        else:
            qtcFri[1] = 0

        if (qtcFra[0] > qtcN):
            qtcFra[1] = 1
        else:
            qtcFra[1] = 0

        if (qtcH[0] > qtcN):
            qtcH[1] = 1
        else:
            qtcH[1] = 0

        if (qtcR[0] > qtcN):
            qtcR[1] = 1
        else:
            qtcR[1] = 0

        qtc.append([qtcB, qtcFri, qtcFra, qtcH, qtcR])
        #Vent Rate
        bpm = fs*60/rr
        bpm_list.append(bpm)
    #     print "BPM : ", bpm
    #     print t_end
    # print "======= INTERVALS ==========="
    # print rr_list, len(rr_list)

    rr_temp = 0; pr_temp = 0 ; qrs_temp = 0; qt_temp = 0; qtcorr_temp = 0; bpm_temp = 0
    for k in range(len(rr_list)):
        rr_temp     = rr_temp + rr_list[k]
        pr_temp     = pr_temp + pr_list[k]
        qrs_temp    = qrs_temp + qrs_list[k]
        qt_temp     = qt_temp + qt_list[k]
        qtcorr_temp = qtcorr_temp + qtc[k][0][0]
        bpm_temp    = bpm_temp + bpm_list[k]

    try:
        pr_mean     = pr_temp/len(pr_list)
        qrs_mean    = qrs_temp/len(qrs_list)
        qt_mean     = qt_temp/len(qt_list)
        qtcorr_mean = qtcorr_temp/len(rr_list)
        bpm_mean    = bpm_temp/len(bpm_list)
    except ZeroDivisionError:
        pr_mean     = 0
        qrs_mean    = 0
        qt_mean     = 0
        qtcorr_mean = 0
        bpm_mean    = 0

    #print "PR Mean  : ", pr_mean
    #print "QRS Mean : ", qrs_mean
    #print "QT Mean  : ", qt_mean
    print "QT Corr Mean : ", qtcorr_mean
    print "BPM Mean : ", bpm_mean

    #for j in range(len(rr_list)):
        #print qtc[j][0][1],qtc[j][1][1],qtc[j][2][1],qtc[j][3][1],qtc[j][4][1]

    TP,TN,FP,FN = clas.classification(qtc, 0, rr_list)
    print  TP,TN,FP,FN
    print "QTc B   : acc(", accuracy(TP,TN,FP,FN),"%) | spc (", specificity(TN,FP),"%) | sns(", sensitivity(TP,FN),"%)"
    TP,TN,FP,FN = clas.classification(qtc, 1, rr_list)
    print  TP,TN,FP,FN
    print "QTc Fri : acc(", accuracy(TP,TN,FP,FN),"%) | spc (", specificity(TN,FP),"%) | sns(", sensitivity(TP,FN),"%)"
    TP,TN,FP,FN = clas.classification(qtc, 2, rr_list)
    print  TP,TN,FP,FN
    print "QTc Fra : acc(", accuracy(TP,TN,FP,FN),"%) | spc (", specificity(TN,FP),"%) | sns(", sensitivity(TP,FN),"%)"
    TP,TN,FP,FN = clas.classification(qtc, 3, rr_list)
    print  TP,TN,FP,FN
    print "QTc H   : acc(", accuracy(TP,TN,FP,FN),"%) | spc (", specificity(TN,FP),"%) | sns(", sensitivity(TP,FN),"%)"


def accuracy(tp,tn,fp,fn):
    a = tp + tn
    b = tp + tn + fp + fn
    try:
        return float(a)/float(b) * 100
    except ZeroDivisionError:
        return 0

def specificity(tn,fp):
    a = tn
    b = tn + fp
    try:
        return float(a)/float(b) * 100
    except ZeroDivisionError:
        return 0

def sensitivity(tp,fn):
    a = tp
    b = tp + fn
    try:
        return float(a)/float(b) * 100
    except ZeroDivisionError:
        return 0

#================ MAIN ====================

# data_location = 'C:/xampp/htdocs/Telemedicine Innovation Challenge/api/python/data/';
#data = 'data/real_ecg.csv'
# read_data = data_location + data
# print "==================================="
# print "Read file : ", data
#f = open(data, 'r')
#line = f.readlines()
#f.close()

#lines = [486,483,483,481,480,479,482,484,487,487,488,488,492,491,494,495,498,497,502,504,506,506,511,514,517,520,523,525,530,533,537,538,541,541,543,544,544,544,542,537,530,521,513,505,500,493,489,485,485,483,482,482,484,483,482,482,487,486,487,484,488,488,490,489,490,491,494,491,491,490,494,493,494,496,499,500,509,510,513,516,528,535,542,541,540,529,520,508,500,492,489,486,483,481,479,478,483,483,483,481,481,480,478,475,489,538,617,687,712,685,617,559,542,549,543,519,499,484,479,478,480,478,476,475,476,478,480,481,484,486,488,489,491,490,492,495,497,496,499,500,504,505,508,511,515,518,521,521,525,528,531,532,534,533,537,537,536,531,526,519,512,503,497,490,486,482,482,482,480,478,479,479,482,481,481,480,482,482,483,482,484,483,485,483,484,484,485,483,484,484,485,483,485,488,494,498,501,500,506,515,523,530,530,524,515,502,494,487,479,473,472,467,465,462,462,461,463,462,464,464,464,460,459,474,539,637,717,724,677,588,529,519,532,522,500,480,466,463,464,463,463,462,464,463,465,465,467,470,473,473,476,478,479,481,484,487,490,490,494,497,501,503,507,509,514,516,522,523,526,527,530,531,534,531,531,529,529,522,515,505,497,490,485,479,477,474,473,472,473,473,474,473,474,474,476,476,478,477,476,477,479,481,480,481,483,482,483,483,485,484,485,484,486,488,496,501,510,512,513,518,525,531,537,536,531,520,508,501,496,489,487,482,482,478,478,478,480,481,483,482,482,480,480,481,520,609,717,763,752,678,598,551,550,549,531,506,487,480,479,476,476,475,475,475,476,477,480,481,483,484,487,486,489,490,493,495,499,501,505,505,507,509,514,518,522,524,530,531,534,537,540,540,542,540,541,540,539,532,525,515,508,499,494,488,483,479,479,477,478,478,476,475,477,476,477,477,479,478,479,479,480,479,481,481,483,482,484,484,485,484,485,484,487,486,489,490,498,505,510,508,510,518,530,535,534,531,522,512,502,493,490,486,482,478,479,478,480,479,480,479,480,481,482,478,475,492,565,673,754,761,708,627,572,555,556,538,510,495,482,475,474,472,473,472,474,474,477,478,480,480,483,483,486,487,490,493,496,496,500,501,505,506
#]
#result = main_test(line)

#plt.show()
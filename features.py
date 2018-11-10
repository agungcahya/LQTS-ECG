import time
import matplotlib.pyplot as plt
import filtering as filt
import math
import classification as clas
import bwr
import pywt
import dwt

def main_test(sample, fs, qtcN):

    #___________________________________________2.1 FEATURE EXTRACTION__________________________________________________
    #sample = sample.tolist()
    # plt.figure(1)
    # plt.subplot(313);
    # plt.plot(sample)
    # #plt.plot(range(len(sample)),sample)
    # plt.xlim(0, len(sample[1000:2000]) - 1)
    # plt.title('Features Extraction')

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
    print "Total R peaks : ", len(r_peaks)

    #print r_peaks
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
            if (sample[t]>=0.0):
                tend_list.append(sample[t])
            # print(sample[t])
            t += 1
            # print(len(tend_list))
        if (len(tend_list)==0):
            t_end = t_in
        else:
            t_min = min(tend_list)
            t_end = sample.index(t_min)
        # print(t_min)

        #t_plot = plt.plot(t_end, t_min, 'y.', markersize=8)  # Plot the T peak

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

        # SET S
        s_on  = r1
        s_off = (35 * rr)/100
        s_off = r1 + s_off
        # plt.axvspan(s_on, s_off, facecolor='#beff9b', alpha=0.5)
        t = s_on; t_list = []
        while(t <= s_off):
            t_list.append(sample[t])
            t += 1
        s_peak = min(t_list)
        s_in   = sample.index(s_peak)
        s_plot = plt.plot(s_in, s_peak, 'r.', markersize=8) #Plot the S peak
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
        #plt.axhline(0, color='#42f486')

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
        # print "QT Interval : ", t_qt
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
        qtcB[0] = (t_qtcB)
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
        # print "BPM : ", bpm
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
    print "QTc B : acc(", accuracy(TP,TN,FP,FN),"%) | spc (", specificity(TN,FP),"%) | sns(", sensitivity(TP,FN),"%)"
    TP,TN,FP,FN = clas.classification(qtc, 1, rr_list)
    print  TP,TN,FP,FN
    print "QTc Fri : acc(", accuracy(TP,TN,FP,FN),"%) | spc (", specificity(TN,FP),"%) | sns(", sensitivity(TP,FN),"%)"
    TP,TN,FP,FN = clas.classification(qtc, 2, rr_list)
    print  TP,TN,FP,FN
    print "QTc Fra   : acc(", accuracy(TP,TN,FP,FN),"%) | spc (", specificity(TN,FP),"%) | sns(", sensitivity(TP,FN),"%)"
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

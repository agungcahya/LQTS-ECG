import pywt
import pylab
def wavelet (signal, w, lv):
    a=signal
    ca=[]
    cd=[]
    for i in xrange(lv):
        (a, d) = pywt.dwt(a, w)
        ca.append(a)
        cd.append(d)

    coeff35 = [None, cd[4], cd[3], cd[2], None, None]
    rec35 = pywt.waverec(coeff35, w)
    coeff58 = [None, cd[7], cd[6], cd[5], None, None, None, None, None]
    rec58 = pywt.waverec(coeff58, w)
    coeff15 = [None, cd[4], cd[3], cd[2], cd[1], cd[0]]
    rec15 = pywt.waverec(coeff15, w)
    coeff48 = [None, cd[7], cd[6], cd[5], cd[4], cd[3], None, None, None]
    rec48 = pywt.waverec(coeff48, w)
    # print(len(signal))
    # print(len(rec35))
    # print(len(rec58))
    #rec35=filt.squaring(rec35)
    pylab.figure(2)
    ax_main = pylab.subplot(4, 1, 1)
    ax_main.plot(signal)
    pylab.title("Raw")
    ax_main.axhline(0, color='#42f486')
    pylab.xlim(0, len(signal[1000:2000]) - 1)
    ax_main = pylab.subplot(4, 1, 2)
    ax_main.plot(rec35)
    pylab.title("R Detection")
    ax_main.axhline(0, color='#42f486')
    pylab.xlim(0, len(rec35[1000:2000]) - 1)
    ax_main = pylab.subplot(4, 1, 3)
    ax_main.plot(rec48)
    pylab.title("QRS Detection")
    ax_main.axhline(0, color='#42f486')
    pylab.xlim(0, len(rec48[1000:2000]) - 1)
    ax_main = pylab.subplot(4, 1, 4)
    ax_main.plot(rec58)
    pylab.title("T Detection")
    ax_main.axhline(0, color='#42f486')
    pylab.xlim(0, len(rec58[1000:2000]) - 1)
    # ax_main = pylab.subplot(5, 1, 5)
    # ax_main.plot(rec15)
    # plt.axhline(0, color='#42f486')
    # pylab.xlim(0, len(rec15[1000:2000]) - 1)

    return rec35, rec58, rec15, rec48


def classification(qtc, fr, rr_list):
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i in range(len(rr_list)):
        if (qtc[i][4][1]==1):
            if (qtc[i][fr][1]==1):
                TP += 1
            else:
                FN += 1
        else:
            if (qtc[i][fr][1]==1):
                FP +=1
            else:
                TN += 1

    return TP, TN, FP, FN

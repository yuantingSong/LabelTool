import cv2,os
import numpy as np


## count the shot of detect and real

def analyse(test_path, cmp_path):
    # extra
    extraNum = 0
    # miss the right
    misNum = 0
    rightNum = 0
    realNum = 0
    i=0
    a,b,c,d=0,0,0,0
    ft = open(test_path, 'r')
    fc = open(cmp_path, 'r')
    linet = ft.readline()
    linec = fc.readline()
    j=0
    while linec and linet:
        # linec nc the standard
        nt = int(linet.split()[0])
        nc = int(linec.split()[0])
#        print(nc)
        if int(nc/1440)>=j:
            j+=1
            print( extraNum-a, misNum-b, rightNum-c, realNum-d)
            a,b,c,d=extraNum, misNum, rightNum, realNum

        if nt < nc:
            # extra
            extraNum += 1
            linet = ft.readline()

        else:
            # move c
            if nt == nc:
                # right
                rightNum += 1

                linet = ft.readline()
            else:
                misNum += 1

            linec = fc.readline()
            realNum += 1
    while linec:
        misNum += 1
        realNum += 1
        linec = fc.readline()

    nt=int(linet.split()[0])
    while linet and nt<=nc:
        nt=int(linet.split()[0])
        extraNum+=1
        linet=ft.readline()

    fc.close()
    ft.close()
    print(extraNum - a, misNum - b, rightNum - c, realNum - d)
    return extraNum, misNum, rightNum, realNum

test_path='hist.txt'
cmp_path='shotFirst.txt'
print(analyse(test_path,cmp_path))
import cv2,os,time

def prep(im):
    width = 9
    height = 8
    sIm = cv2.resize(im,(width, height))
    gIm = cv2.cvtColor(sIm, cv2.COLOR_BGR2GRAY)
    print(gIm.shape)
    diff=[]
    for row in range(height):
        for col in range(width-1):
            diff.append(gIm[row][col]>gIm[row][col+1])
    return diff

def haming(diff1,diff2):
    diff=0
    for i in range(len(diff1)):
        if(diff1[i]!=diff2[i]):
            diff+=1
    return diff

def similar(im1,im2, t=6):
    # True means similar   the same shot

    d1=prep(im1)
    d2=prep(im2)
    diff = haming(d1,d2)
    if(diff<6):
        return True
    return False



saveNum=0
im=cv2.imread(os.path.join('data', str(saveNum) + '.jpg'))
nim=prep(im)
print(nim[0:10])
print(similar(im,im))
#cv2.imwrite(os.path.join('test', str(saveNum) + '.jpg'), nim)
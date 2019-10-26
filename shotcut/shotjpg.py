
import cv2, os,copy
import numpy as np

def prepr(img1):
    ##################################
    # parameter resize
    ##################################
    sI=cv2.resize(img1,(8,9)).astype(np.float32)
    gIm=cv2.cvtColor(sI,cv2.COLOR_BGR2GRAY)
    diffrow=[]
    diffcol=[]
    height,width=gIm.shape
    for row in range(height-1):
        for col in range(width-1):
            diffrow.append(gIm[row][col]>gIm[row][col+1])
            diffcol.append(gIm[row][col]>gIm[row+1][col])
    return diffrow,diffcol

def hamingrc(img1,img2):
    # haming distance in two directions
    dr1,dc1=prepr(img1)
    dr2,dc2=prepr(img2)
    diffr=0
    diffc=0
    for i in range(len(dr1)):
        if(dr1[i]!=dr2[i]):
            diffr+=1
    for i in range(len(dr2)):
        if(dc1[i]!=dc2[i]):
            diffc+=1
    return diffr,diffc

def isdiff(img1,img2):
    # parameters
    t_row=5
    t_col=5
    ###############################
    diffr,diffc=hamingrc(img1,img2)
    if(diffr>t_row and diffc>t_col):
        return True
    else:
        return False

def img_rsz(img):
    max_size = 160
    imgH = img.shape[0]
    imgW = img.shape[1]
    if imgH <=max_size and imgW <= max_size:
        return img
    if imgW > imgH:
        newW = max_size
        newH = imgH*max_size//imgW
    else:
        newH = max_size
        newW = imgW*max_size//imgH
    return cv2.resize(img, (newW, newH))

def hist_rgb(img):
    img = img_rsz(img)
    bin_size = 16
    bin_len_r, bin_len_g, bin_len_b = [256/bin_size] * 3
    img_size = img.shape[0] * img.shape[1]
    img_b = np.reshape(img[:, :, 0] / bin_size, (img_size,))
    img_g = np.reshape(img[:, :, 1] / bin_size, (img_size,))
    img_r = np.reshape(img[:, :, 2] / bin_size, (img_size,))
    img_bgr = np.transpose(np.asarray([img_b, img_g, img_r]))
    hist, edges = np.histogramdd(img_bgr, bins = (bin_len_b, bin_len_g, bin_len_r), range=([0,bin_len_b], [0,bin_len_g], [0,bin_len_r]))
    norm = np.linalg.norm(hist) + 1e-9
    return hist/norm

def calc_chi_dist(hist1, hist2):
    gamma = 0.5
    hist_sum = hist1 + hist2 + 1e-9
    hist_sub = np.abs(hist1 - hist2)
    hist_mul = np.multiply(hist_sub, hist_sub)
    chi_dist = np.sum(np.divide(hist_mul, hist_sum))
    chi_dist = np.exp(gamma * chi_dist)
    return chi_dist

def isChanged(img1, img2, thresh=1.4):
    #####################################
    #parameter thresh
    hist1 = hist_rgb(img1)
    hist2 = hist_rgb(img2)
    chi_dist = calc_chi_dist(hist1, hist2)
    if chi_dist > thresh:
        return True
    else:
        return False

def flag(im,type):
    height,width,depth=im.shape
    value=255
    if(type):
        value=0
    for i in range(int(height/2-100),int(height/2+100)):
        for j in range(int(width/2-100),int(width/2+100)):

            im[i][j][:]=value
    return im

def shotes(video_path,out_path,savedir):

    cap = cv2.VideoCapture(video_path)
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    if int(major_ver) < 3:
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    else:
        fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
          int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    lastImg = np.ones((sz[0], sz[1], 3))
    frameNum = 0
    saveNum = 0
    curNum = 1
    txtid = 0
    txtName = os.path.join(out_path, str('hist') + str(txtid) + '.txt')
    f=open(txtName,'w+')
    hist=[]
    type=True
    fallpath= os.path.join(out_path, str('hist')  + '.txt')
    fall=open(fallpath,'w+')
    sign = np.ones((sz[0], sz[1], 3))

    while (cap.isOpened()):
        ret, im = cap.read()

        if curNum>=2880 :
            # new txt
            f.close()
            txtid+=1
            curNum=1
            txtName = os.path.join(out_path,str('hist')+str(txtid) + '.txt')
            f = open(txtName, 'a+')

        if im is None :
            print('finished')
            cap.release()
            f.close()
            fall.close()
            return hist

        if isChanged(lastImg,im):
            if isdiff(lastImg,im):
                cv2.imwrite(os.path.join(savedir,'all', str(frameNum) + '.jpg'), sign)
                frameNum+=1

                f.write(str(frameNum)+str(' ')+str(saveNum)+str(' ')+str(frameNum-saveNum))
                f.write('\n')
                fall.write(str(frameNum)+str(' ')+str(saveNum)+str(' ')+str(frameNum-saveNum))
                fall.write('\n')

                saveNum=saveNum+1
                print('%d  %d'%(frameNum,saveNum))
                hist.append(frameNum)
                lastType=type
                type=not type
            else:
                print('%d skip'%frameNum)

        cv2.imwrite(os.path.join(savedir,'all', str(frameNum) + '.jpg'), im)
        frameNum += 1
        curNum += 1
        lastImg = im


    cap.release()
    f.close()
    return hist




'''
main
'''
# set id
if __name__ == '__main__':
    id='third'
    videoPath='video/'+id+'.mkv'
    savedir='data/'+id
    txtdir=savedir+'/hist'
    history = shotes(videoPath,txtdir,savedir)
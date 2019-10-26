import cv2, os, time
import numpy as np

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

def getValue(img1,img2):

    hist1 = hist_rgb(img1)
    hist2 = hist_rgb(img2)
    chi_dist = calc_chi_dist(hist1, hist2)
    return chi_dist

def isChanged(img1, img2, thresh=1.5):
    hist1 = hist_rgb(img1)
    hist2 = hist_rgb(img2)
    chi_dist = calc_chi_dist(hist1, hist2)
    if chi_dist > thresh:
        return True
    else:
        return False

def shotes(video_path):
    cap = cv2.VideoCapture(video_path)
    lastImg = np.zeros((160, 160, 3))

    frameNum = 0
    saveNum=0
    while (cap.isOpened()):
        ret, im = cap.read()
        #test break
        if (frameNum > 10000):
            return

        if im is None:
            return
        if isChanged(lastImg, im):
            print(frameNum)
            cv2.imwrite(os.path.join('data', str(saveNum)+'.jpg'), im)
            saveNum=saveNum+1
        frameNum += 1
        lastImg = im
    cap.release()









'''
main
'''
shotes('first.mkv')
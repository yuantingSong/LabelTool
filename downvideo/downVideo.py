import urllib
import json
import time
import socket
import urllib.request
import re
import os
import io,time

timeout = 20

def getHtml(url):
    html = ''
    socket.setdefaulttimeout(timeout)
    try:
        time.sleep(0.03)
        page = urllib.request.urlopen(url)
        html = page.read()
        page.close()
    except Exception as e:
        print('ERRO:GET URL %s' % url)

    return html

def judge_type(qipuid):
    url_prefix = "http://qipu.qiyi.domain/fusion/getEntity?entity_id="
    url = url_prefix + str(qipuid)
    html = getHtml(url)
    if html == '':
        print('get html failed', qipuid)
        return -1, -1
    try:
        html = html.decode('UTF-8')
        html_json = json.loads(html)
        ch_id = ((html_json['base']['channel_id']))
        pyear = ((html_json['base']['page_publish_time']['year']))

        if qipuid.endswith('09'):
            # metadata = html_json["metadata"]
            # ch_id = metadata
            ch_id = -1
            print('***********************ERRO : 09 ', qipuid)
            return -1, -1
        return ch_id, pyear
    except:
        print('ERRO: get channel id ', qipuid)
        return -1, -2

def canAdd_old(qipuid, match, year):
    type, pyear, size = njudge_type(qipuid)
    flag = False
    rtindex = 0
    ryindex = 0
    for i in range(len(match)):
        if type == match[i]:
            rtindex = i
            for j in range(len(year)):
                if pyear == year[j]:
                    ryindex = j
                    flag = True
                    break
            break
    return flag, rtindex, ryindex

def njudge_type(qipuid):
    url_prefix = "http://qipu.qiyi.domain/fusion/getEntity?entity_id="
    url = url_prefix + str(qipuid)
    html = getHtml(url)
    if html == '':
        print('get html failed', qipuid)
        return -1, -1
    html = html.decode('UTF-8')
    html_json = json.loads(html)
    ch_id = -1
    pyear = -1
    duration  = -1
    if 'base' in html_json:
        ch_id = ((html_json['base']['channel_id']))
        pyear = ((html_json['base']['page_publish_time']['year']))
    if 'format' in html_json:
        duration = (html_json['format'][0]['duration'])
    print(duration)
    return ch_id, pyear,duration

def canAdd(qipuid,match,year,threshold):
    type, pyear,duration = njudge_type(qipuid)
    if duration >= threshold and type in match and pyear in year:
        return True,match.index(type),year.index(pyear)
    return False,-1,-1




def initial(match, year):
    idlist = []
    hist = []
    for i in match:
        a = []
        b = []
        for j in year:
            a.append(0)
            b.append('')
        hist.append(a)
        idlist.append(b)
    return idlist, hist

def downVideo(type, pyear,num,curid, urlList):
    videoPath = str(type)+'_'+str(pyear)+'_'+str(num)+'_'+str(curid)
    count=-1
    for url in urlList:
        count=count+1
        urlDown(url,videoPath+'_'+str(count))
        videoname=videoPath+'_'+str(count)+'.f4v'
        cmd="ffmpeg -i "+videoname+' -c copy -bsf:v h264_mp4toannexb -f mpegts '+videoPath+'_'+str(count)+'.ts'
        execute_cmd(cmd)

    cmd='ffmpeg -i "concat:'+videoPath+'_'+str(0)+'.ts'
    i=1
    while i<= count:
        cmd=cmd+'|'+videoPath+'_'+str(i)+'.ts'
        i=i+1
    print(cmd)
    cmd=cmd+'" -c copy -bsf:a aac_adtstoasc -movflags +faststart '+videoPath+'.f4v'
    execute_cmd(cmd)

    return count


def deltmp(count,type, pyear,num,curid):
    #del part
    videoPath = str(type)+'_'+str(pyear)+'_'+str(num)+'_'+str(curid)
    i=0
    print('Del cmd')
    while i<=count:
        tmp=videoPath+'_'+str(i)
        cmd = 'del '+tmp+'.f4v'+' and '+tmp+'.ts'
        execute_cmd(cmd)
        i=i+1

def execute_cmd(cmd):
    print(cmd)
    os.system(cmd)

def urlDown(urlPath,savePath):
    def handleUrl(urlPath):
        return re.sub(r'data.video.qiyi.com', '10.15.60.128',urlPath)

    print('downloading')
    urlPath=(handleUrl(urlPath))
    urllib.request.urlretrieve(urlPath,savePath+'.f4v')
    print('finish')




def findVideo(filepath,match,year,duration,startpoint):

    idlist, hist = initial(match, year)
    haveDone=0
	
    f = io.open(filepath + '.dat', 'r', encoding='utf-8')
    line = f.readline()
    count = 0
    while line :
        print(count)
        line_json = json.loads(line)
        curid = line_json['id']
        flag, tindex, yindex = canAdd(curid, match, year,duration)
        if flag == True:
            # update
            if haveDone<startpoint:
                haveDone+=1
                continue
            print('The  No.',haveDone,'  Video')
            haveDone=haveDone+1

            num=hist[tindex][yindex]
            num=num+1
            hist[tindex][yindex]=num

            lsCnt=downVideo(match[tindex],year[yindex],num,curid,line_json['video_url_list'])
            deltmp(lsCnt,match[tindex],year[yindex],num,curid)

        count = count + 1
        line = f.readline()
    print(idlist)
    print(hist)
    f.close()


if __name__ == '__main__':
    #parameters
    filepath = 'vv_star2018032615'
    startpoint=61
    match = [1, 2, 6]
    year = [2016, 2017, 2018]
    duration_threshold=1800
    findVideo(filepath,match,year,duration_threshold,startpoint)
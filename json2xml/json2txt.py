import io,os
import json

def convert(line_json):
    #json line to txt line
    # return name and txt content
    content=''
    name=line_json['id']
    name=os.path.basename(name)
    name=name.replace('image','')
    name=name.replace('.jpg','')

    boxes=line_json['det_res']
    for i in range(len(boxes)):
        content=content+str(boxes[i])
    content=content.replace(',','     ')

    return name, content

def newTxt(txtPath,name,content):
    path=txtPath+'/'+str(name)+'.txt'
    f=open(path,'w')
    f.write(content)
    f.close()

def json2txt(jsonPath,txtPath):
    f=io.open(jsonPath,'r',encoding='utf-8')
    line = f.readline()
    count =1
    while line:
        print(count)
        count=count+1
        line_json=json.loads(line)
        name,content=convert(line_json)
        newTxt(txtPath,name,content)

        line=f.readline()
        line=f.readline()

if __name__ == '__main__':
    jsonPath='2_2016.json'
    txtPath='2_2016txt'
    json2txt(jsonPath,txtPath)
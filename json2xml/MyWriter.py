#coding:utf-8
import os
import sys
import re
from PIL import ImageDraw, Image
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree
import codecs

XML_EXT = '.xml'
ENCODE_METHOD = 'utf-8'
# def compound_picture(path)
def get_pic_information(pic_path, dets_path):
    #dir = 'C:\\Users\\zhangxiaoyu02_sx\\DeskTop'
    if sys.platform in ['win32', 'win64']:
        fields = pic_path.split("\\")
    else:
        fields = pic_path.split("/")
    regex = re.compile(r'\s|\[|\]')
    coordinates = []
    with open(dets_path,) as f:
        coordinate = []
        elements = regex.split(f.read())
        for ele in elements:
            if not ele:
                continue
            if len(coordinate) < 5:
                coordinate.append(float(ele))
            if len(coordinate) == 5:
                coordinates.append(coordinate)
                coordinate = []
    im = Image.open(pic_path)
    imgSize = im.size
    localImgPath = "/".join(fields)
    foldername = fields[-2]
    filename = fields[-1]
   # print(foldername)
   # print(filename)
   # print(imgSize)
   # print(localImgPath)
    return foldername, filename, imgSize, localImgPath, coordinates

class PascalVocWriter:

    def __init__(self, foldername, filename, imgSize, databaseSrc='Unknown', localImgPath=None):
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.boxlist = []
        self.localImgPath = localImgPath
        self.verified = False
    def prettify(self, elem):
        """
            Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem, 'utf8')
        root = etree.fromstring(rough_string)
        return etree.tostring(root, pretty_print=True, encoding=ENCODE_METHOD).replace("  ".encode(), "\t".encode())
        # minidom does not support UTF-8
        '''reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t", encoding=ENCODE_METHOD)'''

    def genXML(self):
        """
            Return XML root
        """
        # Check conditions
        if self.filename is None or \
                self.foldername is None or \
                self.imgSize is None:
            return None

        top = Element('annotation')
        if self.verified:
            top.set('verified', 'yes')

        folder = SubElement(top, 'folder')
        folder.text = self.foldername

        filename = SubElement(top, 'filename')
        filename.text = self.filename

        if self.localImgPath is not None:
            localImgPath = SubElement(top, 'path')
            localImgPath.text = self.localImgPath

        source = SubElement(top, 'source')
        database = SubElement(source, 'database')
        database.text = self.databaseSrc

        size_part = SubElement(top, 'size')
        width = SubElement(size_part, 'width')
        height = SubElement(size_part, 'height')
        depth = SubElement(size_part, 'depth')
        #changed
        width.text = str(self.imgSize[0])
        height.text = str(self.imgSize[1])
        if len(self.imgSize) == 3:
            depth.text = str(self.imgSize[2])
        else:
            depth.text = '1'

        segmented = SubElement(top, 'segmented')
        segmented.text = '0'
        return top

    def addBndBox(self, xmin, ymin, xmax, ymax, score, name, difficult):
        bndbox = {'xmin': int(xmin), 'ymin': int(ymin), 'xmax': int(xmax), 'ymax': int(ymax)}
        bndbox['name'] = name
        bndbox['score'] = score
        bndbox['difficult'] = difficult
        self.boxlist.append(bndbox)

    def appendObjects(self, top):
        for each_object in self.boxlist:
            object_item = SubElement(top, 'object')
            name = SubElement(object_item, 'name')
            try:
                name.text = unicode(each_object['name'])
            except NameError:
                # Py3: NameError: name 'unicode' is not defined
                name.text = each_object['name']
            score = SubElement(object_item, 'score')
            score.text = str(each_object['score'])
            pose = SubElement(object_item, 'pose')
            pose.text = "Unspecified"
            truncated = SubElement(object_item, 'truncated')
            if int(each_object['ymax']) == int(self.imgSize[0]) or (int(each_object['ymin'])== 1):
                truncated.text = "1" # max == height or min
            elif (int(each_object['xmax'])==int(self.imgSize[1])) or (int(each_object['xmin'])== 1):
                truncated.text = "1" # max == width or min
            else:
                truncated.text = "0"
            difficult = SubElement(object_item, 'difficult')
            difficult.text = str( bool(each_object['difficult']) & 1 )
            bndbox = SubElement(object_item, 'bndbox')
            xmin = SubElement(bndbox, 'xmin')
            xmin.text = str(each_object['xmin'])
            ymin = SubElement(bndbox, 'ymin')
            ymin.text = str(each_object['ymin'])
            xmax = SubElement(bndbox, 'xmax')
            xmax.text = str(each_object['xmax'])
            ymax = SubElement(bndbox, 'ymax')
            ymax.text = str(each_object['ymax'])

    def save(self, targetFile=None):
        root = self.genXML()
        self.appendObjects(root)
        out_file = None
        if targetFile is None:
            out_file = codecs.open(self.filename + XML_EXT, 'w', encoding=ENCODE_METHOD)
        else:
            out_file = codecs.open(targetFile, 'w', encoding=ENCODE_METHOD)

        prettifyResult = self.prettify(root)
        out_file.write(prettifyResult.decode('utf8'))
        out_file.close()

def ge_xml(pic_path, dets_path):
    # 'C:\\Users\\zhangxiaoyu02_sx\\DeskTop\\002324.jpg',
    # 'C:\\Users\\zhangxiaoyu02_sx\\DeskTop\\002324.txt'
    foldername, filename, imgSize, localImgPath, coordinates = get_pic_information(pic_path, dets_path)
    print(foldername,filename)
    pascalVocWriter = PascalVocWriter(foldername, filename, imgSize, localImgPath = localImgPath)
    if len(coordinates) == 0:
        return
    for coordinate in coordinates:
        pascalVocWriter.addBndBox(*coordinate, 'person' + ": " + str(round(coordinate[4],2)),0)
    destnation = pic_path[:-4] + ".xml"
    pascalVocWriter.save(destnation)

def check_file_exists(fig_path,relative_dets_path):
    formats= ['.jpg', '.png',]
    for format in formats:
        relate_absolute_pic_path = os.path.join(fig_path, relative_dets_path[:-4] + format)
        print(relate_absolute_pic_path)
        if os.path.isfile(relate_absolute_pic_path):
            return relate_absolute_pic_path
    return


dets_path = "D:\\data\\2_2016txt"
fig_path =  "D:\\data\\2_2016"
#fig_path = "C:\\Users\\renmengyuan01_sx\\Downloads\\video_liu\\frames\\png_1e4bfa6a4dd1dfad6d4358e9c46ccfbb"
#dets_path = "C:\\Users\\renmengyuan01_sx\\Downloads\\video_liu\\frames_txt\\1e4bfa6a4dd1dfad6d4358e9c46ccfbb"\
for relative_dets_path in os.listdir(dets_path):

    if relative_dets_path.endswith('.txt',):
        absolute_dets_path = os.path.join(dets_path, relative_dets_path)
        relate_absolute_pic_path = check_file_exists(fig_path, relative_dets_path)
        if relate_absolute_pic_path:
            ge_xml( relate_absolute_pic_path, absolute_dets_path )


# ------------------------------------------
# SSH: Single Stage Headless Face Detector
# Demo
# by Mahyar Najibi
from __future__ import print_function
from SSH.test import qiyiStarsDetect
from argparse import ArgumentParser
import os
from utils.get_config import cfg_from_file, cfg, cfg_print
import caffe

def parser():
    parser = ArgumentParser('SSH Demo!')
    parser.add_argument('--imPath',dest='listPath',help='Path to the image',
                        default='/home/syt/input2/',type=str)
    parser.add_argument('--savePath',dest='savePath',help='Path to the image',
                        default= '/home/syt/yxl_detections',type=str)
    parser.add_argument('--saveTxt',dest='saveTxt',help='Path to the image',
                        default='/home/syt/yxl_json',type=str)
    parser.add_argument('--gpu',dest='gpu_id',help='The GPU ide to be used',
                        default=0,type=int)
    parser.add_argument('--proto',dest='prototxt',help='SSH caffe test prototxt',
                        default='SSH/models/test_ssh.prototxt',type=str)
    parser.add_argument('--model',dest='model',help='SSH trained caffemodel',
                        default='data/SSH_models/SSH.caffemodel',type=str)
    parser.add_argument('--cfg',dest='cfg',help='Config file to overwrite the default configs',
                        default='SSH/configs/wider_pyramid.yml',type=str)
    return parser.parse_args()

if __name__ == "__main__":

    # Parse arguments
    args = parser()
    root='/home/syt/input2'
	
    i=0

	
    for cur_root in os.listdir(root):
        # Load the external config
        i=i+1
        print(cur_root)
    if args.cfg is not None:
        cfg_from_file(args.cfg)
        # Print config file
        cfg_print(cfg)

    # Loading the network
    cfg.GPU_ID = args.gpu_id
    caffe.set_mode_gpu()
    caffe.set_device(args.gpu_id)
    assert os.path.isfile(args.prototxt),'Please provide a valid path for the prototxt!'
    assert os.path.isfile(args.model),'Please provide a valid path for the caffemodel!'

    print('Loading the network...', end="")
    net = caffe.Net(args.prototxt, args.model, caffe.TEST)
    net.name = 'SSH'
    print('Done!')

    # Read image
    assert not os.path.isfile(args.listPath),'Please provide a path to an existing image!'
    pyramid = True if len(cfg.TEST.SCALES)>1 else False
    # Perform detection
   # listDetect(net, args.listPath, args.savePath, args.saveTxt)
    if not os.path.exists(args.savePath):
        os.mkdir(args.savePath)
    if not os.path.exists(args.saveTxt):
	    os.mkdir(args.saveTxt)
		
    print(args.listPath)
    qiyiStarsDetect(net, args.listPath, args.savePath, args.saveTxt)


# -- coding: utf-8 --
import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, '..')))

import argparse
import cv2
import  random
from PIL import Image

from tools.interface.utils import get_device, model_import
from tools.interface.bch import BCHHelper
from tools.interface.predict import decode


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_path', help='path of the image file (.png or .jpg)',
                        default="out/encoded.jpg")
    parser.add_argument('--model_path', help='path of the model file (.pth)',
                        default="weight/latest-0.pth")
    parser.add_argument('--device', help='the model loaded in cpu(cpu) or gpu(cuda)',
                        default='cuda')
    return parser.parse_args()

def getuid1(video_path,device,model_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    random_frame_index = random.randint(0, frame_count - 1)
    cap.set(cv2.CAP_PROP_POS_FRAMES, random_frame_index)
    ret, frame = cap.read()

    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    bch = BCHHelper()
    device = get_device(device)
    decoder = model_import(model_path, "Decoder", device=device)

    # 调用 api
    
    uid, time, content, msg_pred, score, bf = decode(img=img,
                                                     bch=bch,
                                                     device=device,
                                                     model=decoder,
                                                     use_stn=True)

    print("水印指向用户: ", uid)
    print("水印指向时间: ", time)
    print("水印原生内容: ", content)
    # print("水印正确率: ", )
    print("水印置信度: ", score)
    print("校验码纠正位数: ", bf)
    cap.release()
    return uid


def getuid(video_path, device, model_path):
    cap = cv2.VideoCapture(video_path)
    frame_indices = [10, 11,12,13,14,15,16,17,18,19,20]  # 可以根据视频长度灵活选择多帧
    results = []

    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()

        if not ret:
            print(f"Failed to read frame {idx}")
            continue

        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        bch = BCHHelper()
        device = get_device(device)
        decoder = model_import(model_path, "Decoder", device=device)

        # 调用解码函数
        uid, time, content, msg_pred, score, bf = decode(img=img, bch=bch, device=device, model=decoder, use_stn=True)

        # 如果纠错位数不为 -1，说明解码成功，保存结果
        if bf != -1:
            # 打印结果
            print("水印指向用户: ", uid)
            print("水印指向时间: ", time)
            print("水印原生内容: ", content)
            print("水印置信度: ", score)
            print("校验码纠正位数: ", bf)
            cap.release()
            return uid
    cap.release()

    
    print("Failed to decode any frame.")
    return None

    # 如果需要，可以根据需要选择最好的结果或统计出现次数
    # 这里你可以根据需要添加进一步的处理逻辑




def decoderapi(image_path, model_path, device):
    img = cv2.imread(image_path)
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    bch = BCHHelper() 
    device = get_device(device)  
    decoder = model_import(model_path, "Decoder", device=device)  

    # 调用解码函数
    uid, time, content, msg_pred, score, bf = decode(img=img,
                                                     bch=bch,
                                                     device=device,
                                                     model=decoder,
                                                     use_stn=True)

    return uid


if __name__ == '__main__':
    getuid(video_path="out/encoded_video.avi",device='cpu',model_path="weight/latest-0.pth")


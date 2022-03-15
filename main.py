import cv2
import numpy as np
import random
from time import time
from matplotlib import pyplot as plt
import os

file_codesourse = open('code_soures2.txt', 'r', encoding='utf-8')
file_result = open('result.txt', 'w')
codes_string = file_codesourse.readline()
codes = np.array(list(codes_string))
#字符集数组 codes

codes_average_color = cv2.imread('codes_average2.png')
codes_average_color = cv2.resize(codes_average_color, (26, 23), interpolation=cv2.INTER_NEAREST)
codes_average_color = np.array(codes_average_color)[:, :, 0].reshape((598,))
#字符平均亮度数组 codes_average_color

codes = codes[np.argsort(codes_average_color)]
codes_average_color = np.sort(codes_average_color)
codes_average_color_counts = np.bincount(codes_average_color)
#统计数组 codes_average_color_counts
#两数组排序

start_list = list()
for i in range(codes_average_color_counts.shape[0]):
    start = np.sum(codes_average_color_counts[0:i])
    start_list.append(start)
codes_average_color_pix = np.vstack((start_list, codes_average_color_counts)).T
#pix 查找数组 codes_average_color_pix

#print(codes)
#print(codes_average_color_counts)
#print(codes_average_color)
#a = plt.plot(range(codes_average_color_counts.shape[0]) ,codes_average_color_counts)
#plt.show()

sourse_video = cv2.VideoCapture('aya.mp4')
sourse_video_w = sourse_video.get(3)
sourse_video_h = sourse_video.get(4)
sourse_video_fps = sourse_video.get(5)
sourse_video_frame = sourse_video.get(7)
sourse_wh = (int(sourse_video_w), int(sourse_video_h))
out_wh = (int(sourse_video_w / 16), int(sourse_video_h / 16))

file_result.write(str(out_wh[0]*2)+'\n'+str(out_wh[1]+1)+'\n')
file_result.write(str(int(sourse_video_frame))+'\n'+str(int(sourse_video_frame / sourse_video_fps))+'\n')

for f in range(int(sourse_video_frame) - 1):
    rat, single_frame = sourse_video.read()
    single_frame = np.array(single_frame / 2)
    single_frame = np.average(single_frame, axis=2).astype(np.uint8)
    single_frame = np.array(cv2.resize(single_frame, out_wh, interpolation=cv2.INTER_AREA))
    for i in single_frame:
        for pix in i:
            if pix in codes_average_color:
                pass
            else:
                d = 0
                while True:
                    if (pix-d) in codes_average_color:
                        pix = pix - d; break
                    if (pix+d) in codes_average_color:
                        pix = pix + d; break
                    d = d + 1
            pix_char_ind = codes_average_color_pix[pix][0] + random.randint(0, codes_average_color_pix[pix][1]-1)
            pix_char = codes[pix_char_ind]
            file_result.write(pix_char)
        file_result.write('\n')
    single_frame = np.array(cv2.resize(single_frame, sourse_wh, interpolation=cv2.INTER_NEAREST))
    cv2.imshow('result_priview', single_frame)
    cv2.waitKey(1)




#cv2.imshow('1', codes_average_color)
sourse_video.release()
file_codesourse.close()
file_result.close()


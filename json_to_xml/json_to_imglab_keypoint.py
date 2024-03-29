import os
import numpy as np
import copy
import codecs
import json
from glob import glob
import cv2
import shutil

# labelme_path = '/home/walt/Downloads/dataset/已标注-11/dev/shm/1672670153410605_bea9298c-3371-4f99-98f7-b271859acf11/1591039045110456321/'
labelme_path = '/mnt/sdb2/dataset/20230208/dev/shm/1675072906072340_9e716794-a2b2-49f0-a5fa-0965fbd86ecd/1608343461408632833/'
saved_path = '/mnt/sdb2/dataset/20230208/dev/xml'


# 文件计数器
counter = 0


with codecs.open(labelme_path + "xml" + ".xml", "w", "utf-8") as xml:
    # 3.获取待处理文件
    files = glob(labelme_path + "*.json")
    print(files)
    # 4.读取标注信息并写入 xml
    xml.write('<dataset>\n')
    xml.write('<images>\n')
    for json_file_ in files:
        # json_filename = labelme_path + json_file_ + ".json"
        # print(json_filename)
        json_file = json.load(open(json_file_, "r", encoding="utf-8"))

        # 获取文件名
        fileName = json_file["image_name"]
        if "-" in fileName:
            fileName = fileName.split(' ')[0]

        xml.write('\t<image' + " file ='" + str(fileName)  + "'>\n")

        # cubePoints是一个数组，数组每一项是一个字典{x:  ,y:  }

        top, left, width, height = 0, 0, 0, 0
        if "cubePoints" in json_file:
            for pointInLists in json_file['cubePoints']:
                point_x_list = []
                point_y_list = []
                point_list = []
                '''
                int()函数是可以将字符串转换为整形，但是这个字符串如果是带小数得,就会转换报错
                '''
                for pointInList in pointInLists:
                    pointX = int(float(pointInList["x"]))
                    pointY = int(float(pointInList["y"]))
                    point_list.append([pointX, pointY])

                point_x_list = np.array(point_list)[:, 0].tolist()
                point_y_list = np.array(point_list)[:, 1].tolist()
                point_x_list2 = point_x_list.copy()
                point_y_list2 = point_y_list.copy()
                point_x_list.sort()
                point_y_list.sort()

                point_list = np.array(point_list)
                point_list_desk = point_list[point_list[:,1].argsort()][-4:]


                point_0 = point_list_desk[point_list_desk[:,0].argsort()][0:2]
                point_0 = point_0[point_0[:,1].argsort()][1]
                point_list_desk = point_list_desk.tolist()
                point_list_desk.remove(point_0.tolist())
                point_list_desk = np.array(point_list_desk)

                point_1 = point_list_desk[point_list_desk[:,0].argsort()][-2:]
                point_1 = point_1[point_1[:,1].argsort()][1]
                point_list_desk = point_list_desk.tolist()
                point_list_desk.remove(point_1.tolist())
                point_list_desk = np.array(point_list_desk)

                point_2 = point_list_desk[point_list_desk[:,0].argsort()][-1]
                point_list_desk = point_list_desk.tolist()
                point_list_desk.remove(point_2.tolist())
                point_list_desk = np.array(point_list_desk)
                # point_list.sort()

                point_3 = point_list_desk[-1]

                point_desk_leg = [point_0.tolist(), point_1.tolist(), point_2.tolist(), point_3.tolist()]

                top = point_y_list[0]
                left = point_x_list[0]
                width = point_x_list[-1] - left
                height = point_y_list[-1] - top

                # <box top='100' left='5' width='387' height='296'>
                xml.write('\t\t<box' + " top='" + str(top) + "' left='" + str(left) + "' width='" + str(width) + "' height='" + str(height) + "'>\n")
                # <label>unlabelled</label>
                xml.write('\t\t\t<label>unlabelled</label>\n')

                # <part name='0' x='114' y='16'/>
                for index in range(len(point_desk_leg)):
                    xml.write('\t\t\t<part ' + "name='" + str(index) + "' x='" + str(point_desk_leg[index][0]) + "' y='" + str(point_desk_leg[index][1]) + "'/>\n")
                    index += 1

                xml.write('\t\t</box>\n')
            xml.write('\t</image>\n')
    xml.write('</images>\n')
    xml.write('</dataset>\n')

print("counter:", counter)
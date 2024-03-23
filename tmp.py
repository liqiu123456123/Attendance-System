# 导入必要的库
import os  # 导入os库，用于操作文件
import cv2  # 导入cv2库，用于图像处理，例如绘制矩形框
from PIL import Image  # 导入PIL库中的Image模块，用于图像处理，例如绘制图片
import face_recognition  # 导入face_recognition库，用于人脸识别


# 下面三个函数是自定义的，不是库内直接提供的。

# 将识别到的人脸绘制出来
def print_image(face, image):
    # 遍历所有识别到的人脸位置
    for face_location in face:
        # 获取人脸的坐标，face_location的顺序是top, right, bottom, left
        top, right, bottom, left = face_location
        # 根据坐标裁剪出人脸部分
        face_image = image[top:bottom, left:right]
        # 将裁剪出的人脸部分转换为PIL Image对象
        pil_image = Image.fromarray(face_image)
        # 显示转换后的图片
        pil_image.show()

    # 根据坐标在图片中画出框框


def print_image_tru(images, image_list):
    # 读取图片
    image = cv2.imread(images)
    # 遍历所有提供的坐标
    for one in image_list:
        # 根据提供的坐标顺序调整，以匹配OpenCV的矩形框绘制函数
        y1 = one[0]
        x1 = one[3]
        y2 = one[2]
        x2 = one[1]
        # 在图片上绘制矩形框，颜色为红色，线宽为2
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        # 显示带有矩形框的图片
    cv2.imshow("fff", image)
    # 等待用户按键，之后关闭窗口
    cv2.waitKey()


# 将目录中的图片加载到已知人脸库中
def get_face_data():
    # 设置图片所在的目录路径
    base_path = 'image/'
    # 获取该目录下的所有文件名
    name_content = os.listdir(base_path)
    # 初始化一个列表，用于存储人脸编码
    image_encoding_content = []
    # 遍历目录下的所有文件
    for one in name_content:
        # 拼接文件路径
        img = base_path + "/" + str(one)
        # 加载图片
        load = face_recognition.load_image_file(img)
        # 获取图片中的人脸编码，这里假设每张图片只有一个人脸
        encodings = face_recognition.face_encodings(load)[0]
        print(type(encodings))
        print(encodings)
        # 将人脸编码添加到列表中
        image_encoding_content.append(encodings)
        # 打印人脸编码的数量
    print(len(image_encoding_content))
    # 返回文件名列表和人脸编码列表
    return name_content, image_encoding_content


# 1、查找人脸的个数
def count_face(images):
    # 加载图片文件
    image = face_recognition.load_image_file(images)
    # 查找图片中所有的人脸位置
    face_locations = face_recognition.face_locations(image)
    # 打印出识别到的人脸数量
    print(f"该照片中识别出了{len(face_locations)}张人脸")
    # 使用矩形框标出人脸位置并显示图片
    print_image_tru(images, face_locations)


# 2、人脸识别
def face_recognitions(data_base_image, tmp_image):
    # 1、将传入的临时图片转化为人脸编码
    picture_of_tmp = face_recognition.load_image_file(tmp_image)
    # 2、尝试识别临时图片中的人脸编码
    try:
        # 获取临时图片中人脸的编码，假设只有一个人脸，所以取第一个元素
        tmp_encoding = face_recognition.face_encodings(picture_of_tmp)[0]
    except IndexError:
        # 如果未能识别出人脸，则打印提示信息并返回
        print('未识别出人脸')
        return

        # 使用数据库中的人脸编码与临时图片的人脸编码进行比较
    # compare_faces 返回一个布尔值列表，表示是否与数据库中的人脸匹配
    results = face_recognition.compare_faces(data_base_image[1], tmp_encoding)
    print(results)
    # 如果结果列表中有 True，说明匹配成功
    if True in results:
        # 获取匹配成功的人脸在数据库中的索引
        index = results.index(True)
        # 从数据库中获取匹配成功的人脸对应的姓名（假设姓名与文件名相关）
        names = data_base_image[0][index].split('.')[0]
        # 打印出验证成功的信息及姓名
        print(f"人脸验证成功,身份是{names}")
    else:
        # 如果列表中没有 True，说明匹配失败
        print("验证失败")

    # 临时图片的路径


tmp_image = r'liu2.jpeg'
# 调用之前定义的 get_face_data 函数获取数据库中的图片文件名和人脸编码
tuple_data = get_face_data()

# 调用人脸识别函数进行人脸识别
face_recognitions(tuple_data, tmp_image)
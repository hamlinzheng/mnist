#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os
import numpy as np
from dataset.mnist import load_mnist
from PIL import Image, ImageQt


from qt.layout import Ui_MainWindow
from qt.paintboard import PaintBoard

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication
from PyQt5.QtWidgets import QLabel, QMessageBox, QPushButton, QFrame
from PyQt5.QtGui import QPainter, QPen, QPixmap, QColor, QImage
from PyQt5.QtCore import Qt, QPoint, QSize

from simple_convnet import SimpleConvNet
from common.functions import softmax
from deep_convnet import DeepConvNet



MODE_MNIST = 1    # MNIST随机抽取
MODE_WRITE = 2    # 手写输入

Thresh = 0.5      # 识别结果置信度阈值



# 读取MNIST数据集
(_, _), (x_test, _) = load_mnist(normalize=True, flatten=False, one_hot_label=False)


# 初始化网络

# 网络1：简单CNN
"""
conv - relu - pool - affine - relu - affine - softmax
"""
network = SimpleConvNet(input_dim=(1,28,28), 
                        conv_param = {'filter_num': 30, 'filter_size': 5, 'pad': 0, 'stride': 1},
                        hidden_size=100, output_size=10, weight_init_std=0.01)
network.load_params("params.pkl")

# 网络2：深度CNN
# network = DeepConvNet()
# network.load_params("deep_convnet_params.pkl")


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
    
        # 初始化参数
        self.mode = MODE_MNIST
        self.result = [0, 0]

        # 初始化UI
        self.setupUi(self)
        self.center()

        # 初始化画板
        self.paintBoard = PaintBoard(self, Size = QSize(224, 224), Fill = QColor(0,0,0,0))
        self.paintBoard.setPenColor(QColor(0,0,0,0))
        self.dArea_Layout.addWidget(self.paintBoard)

        self.clearDataArea()

    # 窗口居中
    def center(self):
        # 获得窗口
        framePos = self.frameGeometry()
        # 获得屏幕中心点
        scPos = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        framePos.moveCenter(scPos)
        self.move(framePos.topLeft())
    
    
    # 窗口关闭事件
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()   
    
    # 清除数据待输入区
    def clearDataArea(self):
        self.paintBoard.Clear()
        self.lbDataArea.clear()
        self.lbResult.clear()
        self.lbCofidence.clear()
        self.result = [0, 0]

    """
    回调函数
    """
    # 模式下拉列表回调
    def cbBox_Mode_Callback(self, text):
        if text == '1：MINIST随机抽取':
            self.mode = MODE_MNIST
            self.clearDataArea()
            self.pbtGetMnist.setEnabled(True)

            self.paintBoard.setBoardFill(QColor(0,0,0,0))
            self.paintBoard.setPenColor(QColor(0,0,0,0))

        elif text == '2：鼠标手写输入':
            self.mode = MODE_WRITE
            self.clearDataArea()
            self.pbtGetMnist.setEnabled(False)

            # 更改背景
            self.paintBoard.setBoardFill(QColor(0,0,0,255))
            self.paintBoard.setPenColor(QColor(255,255,255,255))


    # 数据清除
    def pbtClear_Callback(self):
        self.clearDataArea()
 

    # 识别
    def pbtPredict_Callback(self):
        __img, img_array =[],[]      # 将图像统一从qimage->pil image -> np.array [1, 1, 28, 28]
        
        # 获取qimage格式图像
        if self.mode == MODE_MNIST:
            __img = self.lbDataArea.pixmap()  # label内若无图像返回None
            if __img == None:   # 无图像则用纯黑代替
                # __img = QImage(224, 224, QImage.Format_Grayscale8)
                __img = ImageQt.ImageQt(Image.fromarray(np.uint8(np.zeros([224,224]))))
            else: __img = __img.toImage()
        elif self.mode == MODE_WRITE:
            __img = self.paintBoard.getContentAsQImage()

        # 转换成pil image类型处理
        pil_img = ImageQt.fromqimage(__img)
        pil_img = pil_img.resize((28, 28), Image.ANTIALIAS)
        
        # pil_img.save('test.png')

        img_array = np.array(pil_img.convert('L')).reshape(1,1,28, 28) / 255.0
        # img_array = np.where(img_array>0.5, 1, 0)
    
        # reshape成网络输入类型 
        __result = network.predict(img_array)      # shape:[1, 10]

        # print (__result)

        # 将预测结果使用softmax输出
        __result = softmax(__result)
       
        self.result[0] = np.argmax(__result)          # 预测的数字
        self.result[1] = __result[0, self.result[0]]     # 置信度

        self.lbResult.setText("%d" % (self.result[0]))
        self.lbCofidence.setText("%.8f" % (self.result[1]))


    # 随机抽取
    def pbtGetMnist_Callback(self):
        self.clearDataArea()
        
        # 随机抽取一张测试集图片，放大后显示
        img = x_test[np.random.randint(0, 9999)]    # shape:[1,28,28] 
        img = img.reshape(28, 28)                   # shape:[28,28]  

        img = img * 0xff      # 恢复灰度值大小 
        pil_img = Image.fromarray(np.uint8(img))
        pil_img = pil_img.resize((224, 224))        # 图像放大显示

        # 将pil图像转换成qimage类型
        qimage = ImageQt.ImageQt(pil_img)
        
        # 将qimage类型图像显示在label
        pix = QPixmap.fromImage(qimage)
        self.lbDataArea.setPixmap(pix)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    Gui = MainWindow()
    Gui.show()

    sys.exit(app.exec_())
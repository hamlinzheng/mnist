# 纯Python实现CNN识别手写体数字+GUI

![](https://img.hamlinzheng.com/i/2020/02/07/psh0gw.png)


---

> 由于把数据集也传上来了，导致下载时间比较长，我打包了一份放在服务器，点击[这里](https://dl.hamlinzheng.com/Python/MNIST.zip)进行下载


项目文件结构如下所示

```
.
├── common
│   ├── functions.py
│   ├── gradient.py
│   ├── layers.py
│   ├── optimizer.py
│   ├── trainer.py
│   └── util.py
├── dataset
│   ├── mnist.pkl
│   ├── mnist.py
│   ├── t10k-images-idx3-ubyte.gz
│   ├── t10k-labels-idx1-ubyte.gz
│   ├── train-images-idx3-ubyte.gz
│   └── train-labels-idx1-ubyte.gz
├── deep_convnet_params.pkl
├── deep_convnet.py
├── mnist_cnn_gui_main.py
├── params.pkl
├── qt
│   ├── layout.py
│   ├── layout.ui
│   ├── paintboard.py
│   └── ui2py.sh
├── simple_convnet.py
├── train_convnet.py
└── train_deepnet.py
```

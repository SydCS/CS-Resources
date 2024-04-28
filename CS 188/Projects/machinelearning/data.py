import numpy as np

# 加载MNIST数据集
mnist_data = np.load("./data/mnist.npz")

# 查看数据集中的键
print("Keys in MNIST dataset:", mnist_data.files)

# 提取训练集、测试集、验证集数据和标签
x_train, y_train = mnist_data["train_images"], mnist_data["train_labels"]
x_test, y_test = mnist_data["test_images"], mnist_data["test_labels"]

# 查看数据形状
print("Shape of training images:", x_train.shape)
print("Shape of training labels:", y_train.shape)
print("Shape of test images:", x_test.shape)
print("Shape of test labels:", y_test.shape)

# 关闭文件
mnist_data.close()

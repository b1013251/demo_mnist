#coding: utf-8
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from PIL import Image
from PIL import ImageOps
import numpy as np


# 画像を読み込む
img = Image.open( 'seven.png' )
# グレースケールに変換
one = np.ones(784)
gray_img = ImageOps.grayscale(img) 
array = np.asarray(gray_img)
array2 = array.astype(np.float64) / 255.0
a =  one - np.reshape(array2, (1,np.product(array2.shape)))
print a
print a.size

# mnistデータ読み込み
print "****MNISTデータ読み込み****"
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

x = tf.placeholder("float", [None, 784])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
y = tf.nn.softmax(tf.matmul(x, W) + b)
y_ = tf.placeholder("float", [None, 10])
cross_entropy = -tf.reduce_sum(y_ * tf.log(y))

# 結果をロード
saver = tf.train.Saver()
sess = tf.Session()
saver.restore(sess, "model_ex.ckpt")

# 結果表示
answer = tf.argmax(y,1)
results =  sess.run(answer, feed_dict={x: a})

for result in results :
	print result

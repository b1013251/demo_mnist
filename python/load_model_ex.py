#coding: utf-8
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from PIL import Image
from PIL import ImageOps
import numpy as np
import sys
import math as math

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')

# 引数読み込み
param = sys.argv

# 画像を読み込む
img = Image.open( "./images/" + param[1] )
# グレースケールに変換
one = np.ones(784)
gray_img = ImageOps.grayscale(img)
array = np.asarray(gray_img)
array2 = array.astype(np.float64) / 255.0
a =  one - np.reshape(array2, (1,np.product(array2.shape)))

x = tf.placeholder("float", shape=[None, 784])
y_ = tf.placeholder("float", shape=[None, 10])

W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])
x_image = tf.reshape(x, [-1,28,28,1])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)
W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)
W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)



# 結果をロード
saver = tf.train.Saver()
sess = tf.Session()
saver.restore(sess, "./python/model_ex.ckpt")

answer = y_conv

# 結果表示
results =  sess.run(answer, feed_dict={x: a, keep_prob:1.0})
result = [round(results[0][0], 4),round(results[0][1], 4),round(results[0][2], 4),round(results[0][3], 4),round(results[0][4], 4),round(results[0][5], 4),round(results[0][6], 4),round(results[0][7], 4),round(results[0][8], 4),round(results[0][9], 4),results[0].argmax()]
print(result)

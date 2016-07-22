# -*- coding: utf-8 -*-
# Author: takami.sato

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

def weight_variable(shape):
    """適度にノイズを含んだ（対称性の除去と勾配ゼロ防止のため）重み行列作成関数
    """

    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    """バイアス行列作成関数
    """
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    """2次元畳み込み関数
    """
    return tf.nn.conv2d(x,
                        W,
                        strides=[1, 1, 1, 1], # 真ん中2つが縦横のストライド
                        padding='SAME')

def max_pool_2x2(x):
    """2x2マックスプーリング関数
    """
    return tf.nn.max_pool(x,
                          ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1],# 真ん中2つが縦横のストライド
                          padding='SAME')

def main():
    # mnistのダウンロード
    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

    sess = tf.InteractiveSession()
    with tf.device("/cpu:0"):
        # データ用可変2階テンソルを用意
        x = tf.placeholder("float", shape=[None, 784])
        # 正解用可変2階テンソルを用意
        y_ = tf.placeholder("float", shape=[None, 10])

        # 画像をリシェイプ 第2引数は画像数(-1は元サイズを保存するように自動計算)、縦x横、チャネル
        x_image = tf.reshape(x, [-1, 28, 28, 1])

        ### 1層目 畳み込み層

        # 畳み込み層のフィルタ重み、引数はパッチサイズ縦、パッチサイズ横、入力チャネル数、出力チャネル数
        # 5x5フィルタで32チャネルを出力（入力は白黒画像なので1チャンネル）
        W_conv1 = weight_variable([5, 5, 1, 32])
        # 畳み込み層のバイアス
        b_conv1 = bias_variable([32])
        # 活性化関数ReLUでの畳み込み層を構築
        h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

        ### 2層目 プーリング層

        # 2x2のマックスプーリング層を構築
        h_pool1 = max_pool_2x2(h_conv1)

        ### 3層目 畳み込み層

        # パッチサイズ縦、パッチサイズ横、入力チャネル、出力チャネル
        # 5x5フィルタで64チャネルを出力
        W_conv2 = weight_variable([5, 5, 32, 64])
        b_conv2 = bias_variable([64])
        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

        ### 4層目 プーリング層
        h_pool2 = max_pool_2x2(h_conv2)

        ### 5層目 全結合層

        # オリジナル画像が28x28で、今回畳み込みでpadding='SAME'を指定しているため
        # プーリングでのみ画像サイズが変わる。2x2プーリングで2x2でストライドも2x2なので
        # 縦横ともに各層で半減する。そのため、28 / 2 / 2 = 7が現在の画像サイズ

        # 全結合層にするために、1階テンソルに変形。画像サイズ縦と画像サイズ横とチャネル数の積の次元
        # 出力は1024（この辺は決めです）　あとはSoftmax Regressionと同じ
        W_fc1 = weight_variable([7 * 7 * 64, 1024])
        b_fc1 = bias_variable([1024])

        h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

        # ドロップアウトを指定
        keep_prob = tf.placeholder("float")
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

        ### 6層目 Softmax Regression層

        W_fc2 = weight_variable([1024, 10])
        b_fc2 = bias_variable([10])

        y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

    # 評価系の関数を用意
    cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    sess.run(tf.initialize_all_variables())

    for i in range(1000):
        batch = mnist.train.next_batch(50)
        if i%100 == 0:
            train_accuracy = accuracy.eval(feed_dict={x:batch[0],
                                                      y_: batch[1],
                                                      keep_prob: 1.0})
            print("step %d, training accuracy %g"%(i, train_accuracy))
        train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

    print("test accuracy %g"%accuracy.eval(feed_dict={
        x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))

    # 結果を保存
    saver = tf.train.Saver()
    saver.save(sess, "model_ex.ckpt")
    print "Model Saved."

if __name__ == "__main__":
    main()

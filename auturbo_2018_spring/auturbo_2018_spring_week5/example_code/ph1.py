import tensorflow as tf

val1 = 5

ph1 = tf.placeholder(dtype=tf.float32)

feed_dict = {ph1: val1}

sess=tf.Session()
result = sess.run(ph1, feed_dict=feed_dict)
print result
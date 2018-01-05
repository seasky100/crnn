"""
this is an implement to load img from mjsyth.tar
"""
from __future__ import print_function
import tensorflow as tf
import os
import glob
import sys
from utils import int64_feature,bytes_feature,load_label_from_imglist,load_image,encode_labels
import numpy as np

tf_filename = os.path.join("/mnt/sdb/mark/ch4/","ch4_train.tfrecords")
data_prefix = "/home/mark/Downloads/ch4_training_word_images_gt/"


imgLists = []

# Dirs = glob.glob(img_dir)
# imgDirs = []
# for imgDir in Dirs:
#     if os.path.isdir(imgDir):
#         imgDirs.extend(glob.glob(os.path.join(imgDir,"*")))

# for imgDir in imgDirs:
#     path = os.path.join(imgDir,"*.jpg")
#     imgList = glob.glob(os.path.join(imgDir,"*.jpg"))
#     imgLists.extend(imgList)


split_file = "/home/mark/Downloads/ch4_training_word_images_gt/gt.txt"


with open(split_file, 'r') as f:
    # i = 0
    labels = []
    for line in f:
        # if np.random.uniform(0, 1) < 0.3:
        #     continue
        # if i > 10:
        #     break

        # i+=1
        print(line)
        line = line.replace('\xef\xbb\xbf','')
        line = line.replace('\r\n','')
        # parse each line
        img_file = line.split(', ')[0]
        label = line.split(', ')[1][1:-1]

        labels.append(label)
        print(img_file, label)
        imgLists.append(os.path.join(data_prefix, img_file))



# labels = load_label_from_imglist(imgLists)
labels_encode,lengths = encode_labels(labels)



with tf.python_io.TFRecordWriter(tf_filename) as tfrecord_writer:
    for i, filename in enumerate(imgLists):
        sys.stdout.write('\r>> Converting image %d/%d' % (i + 1, len(imgLists)))
        sys.stdout.flush()
        try:
            image_data = load_image(filename)
            example = tf.train.Example(features=tf.train.Features(feature={"label/value": int64_feature(labels_encode[i]),
                                                                           "image/encoded": bytes_feature(image_data),
                                                                           "label/length":int64_feature(lengths[i]),
                                                                           'image/format': bytes_feature("jpeg")}))
            tfrecord_writer.write(example.SerializeToString())
        except Exception as e:
            print("Error: ",e)

print('\nFinished converting the dataset!')
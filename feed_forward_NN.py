from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Imports
import numpy as np
import tensorflow as tf
import pandas as pd
from scipy import ndimage as ndim
import scipy
import sys
import os
import imghdr


def cnn_model_fn(features, labels, mode):

  # Input layer
  input_layer = tf.reshape(features["x"], [-1,28,28,3])

  # Convolutional Layer #1
  conv1 = tf.layers.conv2d(
      inputs=input_layer,
      filters=32,
      kernel_size=[5, 5],
      padding="same",
      activation=tf.nn.relu)

  # Pooling Layer #1
  pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)

  # Convolutional Layer #2 and Pooling Layer #2
  conv2 = tf.layers.conv2d(
      inputs=pool1,
      filters=64,
      kernel_size=[5, 5],
      padding="same",
      activation=tf.nn.relu)
  pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)

  # Dense Layer
  pool2_flat = tf.reshape(pool2, [-1, 7 * 7 * 64])
  dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)
  dropout = tf.layers.dropout(
      inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

  # Logits Layer
  # Units is number of games
  logits = tf.layers.dense(inputs=dropout, units=5)

  predictions = {
      # Generate predictions (for PREDICT and EVAL mode)
      "classes": tf.argmax(input=logits, axis=1),
      # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
      # `logging_hook`.
      "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
  }

  if mode == tf.estimator.ModeKeys.PREDICT:
    return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

  # Calculate Loss (for both TRAIN and EVAL modes)
  # Depth is number of games
  onehot_labels = tf.one_hot(indices=tf.cast(labels, tf.int32), depth=5)
  loss = tf.losses.softmax_cross_entropy(
      onehot_labels=onehot_labels, logits=logits)

  # Configure the Training Op (for TRAIN mode)
  if mode == tf.estimator.ModeKeys.TRAIN:
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
    train_op = optimizer.minimize(
        loss=loss,
        global_step=tf.train.get_global_step())
    return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

  # Add evaluation metrics (for EVAL mode)
  eval_metric_ops = {
      "accuracy": tf.metrics.accuracy(
          labels=labels, predictions=predictions["classes"])}
  return tf.estimator.EstimatorSpec(
      mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)



def main(unused_argv):

    os.environ["PATH"] += os.pathsep + os.getcwd()

    data_dir = os.getcwd() + '/game_images/processed_images'

    sub_folders = next(os.walk(data_dir))[1]
    #print(len(sub_folders))

    img_df = pd.DataFrame( columns = ['Image Data','Game ID', 'Game Name'])

    for ii in range(len(sub_folders)):
        game_img_dir = data_dir +'/' +sub_folders[ii]
        #print(game_img_dir)
        for root, dirs, files in os.walk(game_img_dir):
            for item in files:
                img = ndim.imread(os.path.join(root, item))
                temp = pd.DataFrame([[img,ii,sub_folders[ii]]], columns = ['Image Data','Game ID', 'Game Name'])
                #print(temp.head)
                img_df = img_df.append(temp)
                #print(temp.head())
                #print(img_df.head())




    # Check to see if the data was imported correctl
    #print(img_df.head())
    #print(img_df.shape[0])

    #print(list(img_df['Image Data'].iloc[0].shape))
    features_shape = list(img_df['Image Data'].iloc[0].shape)

    img_df = img_df.sample(frac=1)

    # make variable of the labels
    label_names = ['Game ID']
    num_variables = list(img_df['Image Data'].iloc[0].shape)
    num_labels = img_df['Game ID'].iloc[-1]
    #NN_design = [num_variables,num_variables]
    n_data_variables = img_df.shape[0]
    n_training_variables = int(n_data_variables*.8)
    #print(n_training_variables)

    #print(img_df['Image Data'])

    img_data_df = []
    for element in img_df['Image Data']:
        img_data_df.append(element)
    #print(img_data_df[-1])
    img_data_df = np.array(img_data_df)
    #print(img_data_df)

    #print(img_data_df.shape())

    img_labels = []
    for element in img_df['Game ID']:
        img_labels.append(element)
    img_labels = np.array(img_labels)
    #print(img_labels)

    img_data_train = img_data_df[0:n_training_variables]
    img_data_validate = img_data_df[n_training_variables:]


    img_labels_train = img_labels[0:n_training_variables]
    img_labels_validate = img_labels[n_training_variables:]


    #features = [tf.feature_column.numeric_column("", shape=img_df['Image Data'].iloc[0].shape)]

    #classifier = tf.contrib.learn.DNNClassifier(feature_columns=features,
     #                                           hidden_units=NN_design,
     #                                           n_classes=num_labels)

    x_train = np.array(img_data_train.astype(np.float32))
    y_train = np.array(img_labels_train)
    x_eval = np.array(img_data_validate.astype(np.float32))
    y_eval = np.array(img_labels_validate)

    #train_data = mnist.train.images  # Returns np.array
    #train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
    #eval_data = mnist.test.images  # Returns np.array
    #eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)

  # Create the Estimator
    img_classifier = tf.estimator.Estimator(
        model_fn=cnn_model_fn, model_dir="/tmp/game_img_convnet_model")

    # Set up logging for predictions
    # Log the values in the "Softmax" tensor with label "probabilities"
    tensors_to_log = {"probabilities": "softmax_tensor"}
    logging_hook = tf.train.LoggingTensorHook(
        tensors=tensors_to_log, every_n_iter=50)

    # Train the model
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": x_train},
        y=y_train,
        batch_size=5,
        num_epochs=None,
        shuffle=True)
    img_classifier.train(
        input_fn=train_input_fn,
        steps=2000,
        hooks=[logging_hook])

    # Evaluate the model and print results
    eval_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": x_eval},
        y=y_eval,
        num_epochs=1,
        shuffle=False)
    eval_results = img_classifier.evaluate(input_fn=eval_input_fn)
    print(eval_results)


if __name__ == "__main__":
  tf.app.run()
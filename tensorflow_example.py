import tensorflow as tf
import os
import numpy as np
from tensorflow.contrib import learn

graph = None
sess = None
feed_dict = {}
type_dict = {}
vocab_processor = None

#TODO: more input values, mapping to columns or constants
def apply_model(value, tf_checkpoint_dir:str, vocab_file:str=""):
    global graph
    global sess
    global feed_dict
    global type_dict
    global vocab_processor

    if graph is None:
        checkpoint_file = tf.train.latest_checkpoint(checkpoint_dir)
        graph = tf.Graph()
        with graph.as_default():
            sess = tf.Session()
            # Load the saved meta graph and restore variables
            saver = tf.train.import_meta_graph(f"{checkpoint_file}.meta")
            saver.restore(sess, checkpoint_file)

            # Get the placeholders from the graph by name
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]
            output_function = graph.get_operation_by_name("output/predictions").outputs[0]

            type_dict[0] = input_x
            type_dict[1] = dropout_keep_prob
            type_dict["output"] = output_function

            if vocab_file != "":
                vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_file)

    with sess.as_default() and graph.as_default():
        # Map data into vocabulary
        raw = [value] #should be a list...
        if vocab_processor is not None:
            x = np.array(list(vocab_processor.transform(raw)))
        else:
            x = raw
        feed_dict[type_dict[0]] = x
        feed_dict[type_dict[1]] = 1.0
        return sess.run(type_dict["output"], feed_dict)

vocab_file = "/home/sklaebe/workspace/cnn-text-classification-tf/runs/1596453054/vocab"
checkpoint_dir = "/home/sklaebe/workspace/cnn-text-classification-tf/runs/1596453054/checkpoints"

print(apply_model("The movie is great", checkpoint_dir, vocab_file))
print(apply_model("The movie is bad", checkpoint_dir, vocab_file))
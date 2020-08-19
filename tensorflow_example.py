import tensorflow as tf
import numpy as np
from tensorflow.contrib import learn

graph = None
sess = None
feed_dict = {}
type_dict = {}
vocab_processor = None

#TODO: more input values, mapping to columns or constants
def apply_model(values, tf_checkpoint_dir:str, network_input_names, constants = [], vocab_file:str=""):
    global graph
    global sess
    global feed_dict
    global type_dict
    global vocab_processor

    if graph is None:
        checkpoint_file = tf.train.latest_checkpoint(tf_checkpoint_dir)
        graph = tf.Graph()
        with graph.as_default():
            sess = tf.Session()
            # Load the saved meta graph and restore variables
            saver = tf.train.import_meta_graph(f"{checkpoint_file}.meta")
            saver.restore(sess, checkpoint_file)

            # Get the placeholders from the graph by name
            for i in range(len(network_input_names)):
                type_dict[i] = graph.get_operation_by_name(network_input_names[i]).outputs[0]
            type_dict["output"] = graph.get_operation_by_name("output/predictions").outputs[0]

            if vocab_file != "":
                vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_file)

    with sess.as_default() and graph.as_default():
        # Map data into vocabulary
        for i in range(len(values)):
            if constants == [] or constants[i] is None:
                raw = [values[i]] #should be a list...
                if vocab_processor is not None:
                    x = np.array(list(vocab_processor.transform(raw)))
                else:
                    x = raw
            else:
                x = [constants[i]]
            feed_dict[type_dict[i]] = x
        return sess.run(type_dict["output"], feed_dict)[0]

vocab_file = "/home/sklaebe/workspace/cnn-text-classification-tf/runs/1596453054/vocab"
checkpoint_dir = "/home/sklaebe/workspace/cnn-text-classification-tf/runs/1596453054/checkpoints"

print(apply_model(["the movie is awesome", None], checkpoint_dir, ["input_x", "dropout_keep_prob"], [None, 1.0], vocab_file))
print(apply_model(["the movie is bad", None], checkpoint_dir, ["input_x", "dropout_keep_prob"], [None, 1.0], vocab_file))

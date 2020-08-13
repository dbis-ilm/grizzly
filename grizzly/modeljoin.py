def build_tensorflow_apply_from_checkpoint(tf_checkpoint_file: str, network_input_names, constants=[], vocab_file: str = ""):
    code = """
import tensorflow as tf
import numpy as np
from tensorflow.contrib import learn
import random
import os
def apply(a: str) -> int:
"""+f"""
    checkpoint_file = "{tf_checkpoint_file}"
    network_input_names = [{', '.join(['"%s"' % n for n in network_input_names])}]
    constants = {constants}
    vocab_file = "{vocab_file}"
"""+"""
    def vocab_needs_reload():
        ts = os.path.getmtime(vocab_file)
        return (not hasattr(random, "vocab_timestamp") or (ts != random.vocab_timestamp))

    def model_needs_reload():
        ts = os.path.getmtime(checkpoint_file + ".meta")
        return (not hasattr(random, "model_timestamp") or (ts != random.model_timestamp))

    def vocab_load():
        ts = os.path.getmtime(vocab_file)
        random.vocab_timestamp = ts
        random.vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_file)

    def model_load():
        ts = os.path.getmtime(checkpoint_file + ".meta")
        random.graph = tf.Graph()
        random.model_timestamo = ts
        with random.graph.as_default():
            random.sess=tf.Session()
            saver = tf.train.import_meta_graph(checkpoint_file + ".meta")
            saver.restore(random.sess, checkpoint_file)
            random.type_dict = {}
            for i in range(len(network_input_names)):
                random.type_dict[i] = random.graph.get_operation_by_name(network_input_names[i]).outputs[0]
            random.type_dict["output"] = random.graph.get_operation_by_name("output/predictions").outputs[0]

    def apply_model(values):
        #if (vocab_needs_reload()): vocab_load()
        #if (model_needs_reload()): model_load()
        vocab_load()
        model_load()
        with random.graph.as_default() and random.sess.as_default():
            x = np.array(list(random.vocab_processor.transform([values[0]])))
            feed_dict = {}
            feed_dict[random.type_dict[0]] = x
            feed_dict[random.type_dict[1]] = [constants[1]]
            return random.sess.run(random.type_dict["output"], feed_dict)[0].item()
    return apply_model([a.lower(), None])
"""
    #TODO: list must be compatible with constants
    return code

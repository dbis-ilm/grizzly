def build_tensorflow_apply_from_checkpoint(tf_checkpoint_dir: str, network_input_names, constants=[], vocab_file: str = ""):
    code = """
import tensorflow as tf
import numpy as np
from tensorflow.contrib import learn
def apply(a: str) -> int:
   
    graph = None
    sess = None
    feed_dict = {}
    type_dict = {}
    vocab_processor = None
"""+f"""
    def apply_model(values):
        global graph
        global sess
        global feed_dict
        global type_dict
        global vocab_processor
    
        tf_checkpoint_dir = "{tf_checkpoint_dir}"
        network_input_names = [{', '.join(['"%s"' % n for n in network_input_names])}]
        constants = {constants}
        vocab_file = "{vocab_file}"
"""+"""
        if graph is None:
            checkpoint_file = tf.train.latest_checkpoint(checkpoint_dir)
            graph = tf.Graph()
            with graph.as_default():
                sess = tf.Session()
                saver = tf.train.import_meta_graph(checkpoint_file + ".meta")
                saver.restore(sess, checkpoint_file)
    
                for i in range(len(network_input_names)):
                    type_dict[i] = graph.get_operation_by_name(network_input_names[i]).outputs[0]
                type_dict["output"] = graph.get_operation_by_name("output/predictions").outputs[0]
    
                if vocab_file != "":
                    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_file)
    
        with sess.as_default() and graph.as_default():
            for i in range(len(values)):
                if constants == [] or constants[i] is None:
                    raw = [values[i]]
                    if vocab_processor is not None:
                        x = np.array(list(vocab_processor.transform(raw)))
                    else:
                        x = raw
                else:
                    x = [constants[i]]
                feed_dict[type_dict[i]] = x
    
            return sess.run(type_dict["output"], feed_dict)[0]
    return apply([a, None])
        """
    #TODO: list must be compatible with constants
    return code

#! /usr/bin/env python

import tensorflow as tf
import numpy as np
import os
from neural_network import data_reader
from tensorflow.contrib import learn


class Get_Tweet_Label():
    def __init__(self):
        tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
        tf.flags.DEFINE_string("checkpoint_dir", "runs/1525531309/checkpoints",
                               "Checkpoint directory from training run")
        tf.flags.DEFINE_boolean("eval_train", False, "Evaluate on all training data")

        tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
        tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")

        self.FLAGS = tf.flags.FLAGS
        self.FLAGS._parse_flags()


    def check_words_using_network(self, sentence):
        print("\nParameters:")
        for attr, value in sorted(self.FLAGS.__flags.items()):
            print("{}={}".format(attr.upper(), value))

        vocab_path = os.path.join(self.FLAGS.checkpoint_dir, "..", "vocab")
        vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
        x_test = np.array(list(vocab_processor.transform([sentence])))

        checkpoint_file = tf.train.latest_checkpoint(self.FLAGS.checkpoint_dir)
        graph = tf.Graph()
        with graph.as_default():
            session_conf = tf.ConfigProto(
                allow_soft_placement=self.FLAGS.allow_soft_placement,
                log_device_placement=self.FLAGS.log_device_placement)
            sess = tf.Session(config=session_conf)
            with sess.as_default():
                saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
                saver.restore(sess, checkpoint_file)

                input_x = graph.get_operation_by_name("input_x").outputs[0]
                dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

                predictions = graph.get_operation_by_name("output/predictions").outputs[0]
                batches = data_reader.batch_iter(list(x_test), self.FLAGS.batch_size, 1, shuffle=False)

                for x_test_batch in batches:
                    batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
                    if batch_predictions[0] == 1:
                        return False
                return True


if __name__ == '__main__':
    labels = Get_Tweet_Label()
    labels.check_words_using_network("it is working")

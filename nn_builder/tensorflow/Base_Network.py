from tensorflow.python.keras.layers import BatchNormalization
from nn_builder.Overall_Base_Network import Overall_Base_Network
import tensorflow.keras.activations as activations
import tensorflow.keras.initializers as initializers
import tensorflow as tf
import numpy as np
import random
from abc import ABC, abstractmethod

class Base_Network(Overall_Base_Network, ABC):
    """Base class for TensorFlow neural network classes"""
    def __init__(self, layers, output_activation, hidden_activations, dropout, initialiser, batch_norm, y_range,
                 random_seed, print_model_summary):
        super().__init__(None, layers, output_activation,
                 hidden_activations, dropout, initialiser, batch_norm, y_range, random_seed, print_model_summary)

    @abstractmethod
    def call(self, x, training):
        """Runs a forward pass of the tensorflow model"""
        raise NotImplementedError

    @abstractmethod
    def create_and_append_layer(self, layer, list_to_append_layer_to, activation=None, output_layer=False):
        """Creates a layer and appends it to the provided list"""
        raise NotImplementedError

    def set_all_random_seeds(self, random_seed):
        """Sets all possible random seeds so results can be reproduced"""
        np.random.seed(random_seed)
        tf.random.set_seed(random_seed)
        random.seed(random_seed)

    def create_str_to_activations_converter(self):
        """Creates a dictionary which converts strings to activations"""
        str_to_activations_converter = {"elu": activations.elu, "exponential": activations.exponential,
                                        "hard_sigmoid": activations.hard_sigmoid, "linear": activations.linear,
                                        "relu": activations.relu, "selu": activations.selu, "sigmoid": activations.sigmoid,
                                        "softmax": activations.softmax, "softplus": activations.softplus,
                                        "softsign": activations.softsign, "tanh": activations.tanh, "none": activations.linear}
        return str_to_activations_converter

    def create_str_to_initialiser_converter(self):
        """Creates a dictionary which converts strings to initialiser"""
        str_to_initialiser_converter = {"glorot_normal": initializers.glorot_normal, "glorot_uniform": initializers.glorot_uniform,
                                        "xavier_normal": initializers.glorot_normal, "xavier_uniform": initializers.glorot_uniform,
                                        "xavier": initializers.glorot_uniform,
                                        "he_normal": initializers.he_normal, "he_uniform": initializers.he_uniform,
                                        "identity": initializers.identity, "lecun_normal": initializers.lecun_normal,
                                        "lecun_uniform": initializers.lecun_uniform, "truncated_normal": initializers.TruncatedNormal,
                                        "variance_scaling": initializers.VarianceScaling, "default": initializers.glorot_uniform}
        return str_to_initialiser_converter

    def create_dropout_layer(self):
        """Creates a dropout layer"""
        return tf.keras.layers.Dropout(rate=self.dropout)

    def create_hidden_layers(self):
        """Creates the hidden layers in the network"""
        hidden_layers = []
        for layer_ix, layer in enumerate(self.layers_info[:-1]):
            activation = self.get_activation(self.hidden_activations, layer_ix)
            self.create_and_append_layer(layer, hidden_layers, activation, output_layer=False)
        return hidden_layers

    def create_output_layers(self):
        """Creates the output layers in the network"""
        output_layers = []
        if isinstance(self.layers_info[-1], int) or not isinstance(self.layers_info[-1][0], list):
            self.layers_info[-1] = [self.layers_info[-1]]
        for output_layer_ix, output_layer in enumerate(self.layers_info[-1]):
            activation = self.get_activation(self.output_activation, output_layer_ix)
            self.create_and_append_layer(output_layer, output_layers, activation, output_layer=True)
        return output_layers

    def create_embedding_layers(self):
        """Creates the embedding layers in the network"""
        embedding_layers = []
        for embedding_dimension in self.embedding_dimensions:
            input_dim, output_dim = embedding_dimension
            embedding_layers.extend([tf.keras.layers.Embedding(input_dim, output_dim)])
        return embedding_layers

    def create_batch_norm_layers(self):
        """Creates the batch norm layers in the network"""
        batch_norm_layers = []
        for layer in self.layers_info[:-1]:
            batch_norm_layers.extend([BatchNormalization()])
        return batch_norm_layers

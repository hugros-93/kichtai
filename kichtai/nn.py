import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.losses import sparse_categorical_crossentropy
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow_addons.layers import WeightNormalization

import plotly.graph_objects as go


def rnn_seq_loss(labels, logits):
    '''Adapted loss function'''
    return sparse_categorical_crossentropy(labels, logits, from_logits=True)


def get_rnn_seq_model(vocab_size, embedding_dim, rnn_units, batch_size):
    '''Create a sequential RNN model adapted for text generation
    
    vocab_size: number of characters in the corpus
    embedding_dim: dimension of the embedding layer
    rnn_units: number of units in the LSTM
    batch_size: batch size, use `batch_size=1` for text generation, but not for training
    output: tensorflow model
    '''
    model = Sequential([
        Embedding(vocab_size, embedding_dim,
                  batch_input_shape=[batch_size, None]),
        LSTM(rnn_units, return_sequences=True, stateful=True,
             recurrent_initializer='glorot_uniform'),
        Dense(vocab_size)
    ])
    model.summary()
    return model


def talk_from_text(text_input, model, char2idx, idx2char, nb_steps=100, temperature=1.0):
    '''
    Talk from a trained model

    text_input: first characters used to start text generation
    model: trained model
    char2idx: dict. character -> corresponding id
    idx2char: dict. id -> corresponding character
    nb_steps: number of characters to generate
    temperature: the higher the temperature, the higher the creativity of the model.
    '''
    text_predict = text_input

    len_seq = model.get_config()['layers'][1]['config']['input_dim']
    x = [char2idx[x] for x in text_predict[-len_seq:]]

    model.reset_states()

    for _ in range(nb_steps):
        x = tf.expand_dims(x, 0)

        y_predicted = model(x)
        y_predicted = tf.squeeze(y_predicted, 0)
        y_predicted /= temperature
        y_predicted = tf.random.categorical(
            y_predicted, num_samples=1)[-1, 0].numpy()

        x = tf.expand_dims([y_predicted], 0)
        text_predict += idx2char[y_predicted]

    return text_predict

def plot_history(history):
    '''Plot the train and test loss function for each epoch'''
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=history.history['loss'], name='training loss'))
    fig.add_trace(go.Scatter(y=history.history['val_loss'], name='validation loss'))

    fig.update_layout(
        xaxis_title="Epochs",
        yaxis_title="Loss",
        title="Training history"
    )
    return fig
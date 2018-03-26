from keras.models import Sequential
from keras.layers import Dense, Convolution2D, MaxPooling2D, Dropout, Flatten
from keras.layers import Embedding, GRU, Input, Bidirectional, Merge, RepeatVector
from keras.regularizers import l2


def get_mlnn_model(input_shape, nb_classes):
    model = Sequential()
    model.add(Dense(1000, activation="relu", W_regularizer=l2(0.0001), input_shape=input_shape))
    model.add(Dense(1000, activation="relu", W_regularizer=l2(0.0001)))
    model.add(Dense(nb_classes, activation="softmax", W_regularizer=l2(0.0001)))
    return model


def get_cnn_model(input_shape, nb_classes):
    model = Sequential()
    model.add(Convolution2D(32, 3, 3, activation="relu", border_mode="same", input_shape=input_shape))
    model.add(Convolution2D(32, 3, 3, activation="relu", border_mode="same"))
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.25))

    model.add(Convolution2D(64, 3, 3, activation="relu", border_mode="same"))
    model.add(Convolution2D(64, 3, 3, activation="relu", border_mode="same"))
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes, activation="softmax"))
    return model


def get_big_cnn_model(input_shape, nb_classes):
    model = Sequential()
    model.add(Convolution2D(64, 3, 3, activation="relu", border_mode="same", input_shape=input_shape))
    model.add(Convolution2D(64, 3, 3, activation="relu", border_mode="same"))
    model.add(Convolution2D(64, 3, 3, activation="relu", border_mode="same"))
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.5))

    model.add(Convolution2D(128, 3, 3, activation="relu", border_mode="same"))
    model.add(Convolution2D(128, 3, 3, activation="relu", border_mode="same"))
    model.add(Convolution2D(128, 3, 3, activation="relu", border_mode="same"))
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.5))

    model.add(Convolution2D(256, 3, 3, activation="relu", border_mode="same"))
    model.add(Convolution2D(256, 3, 3, activation="relu", border_mode="same"))
    model.add(Convolution2D(256, 3, 3, activation="relu", border_mode="same"))
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(512, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(512, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes, activation="softmax"))
    return model


def get_fixed_cnn_model(input_shape, nb_classes):
    model = Sequential()
    model.add(Convolution2D(32, 3, 3, activation="relu", border_mode="same", input_shape=input_shape))
    model.add(Convolution2D(32, 3, 3, activation="relu", border_mode="same"))
    model.add(MaxPooling2D((2, 2)))

    model.add(Convolution2D(64, 3, 3, activation="relu", border_mode="same"))
    model.add(Convolution2D(64, 3, 3, activation="relu", border_mode="same"))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512, activation="relu"))
    model.add(Dense(nb_classes, activation="softmax"))
    return model


def get_logistic_model(input_shape, nb_classes):
    model = Sequential()
    model.add(Dense(nb_classes, activation="softmax", input_shape=input_shape))
    return model


def get_bigru_model(args):
    model = Sequential()
    model.add(Embedding(args.n_vocab, args.embed_dim, input_length=args.max_len))
    model.add(Bidirectional(GRU(args.hidden_dim, return_sequences=True, input_shape=(args.max_len, args.hidden_dim))))
    model.add(Bidirectional(GRU(args.hidden_dim)))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    return model


def get_babi_rnn(EMBED_HIDDEN_SIZE, vocab_size, story_maxlen, query_maxlen):
    sentrnn = Sequential()
    sentrnn.add(Embedding(vocab_size, EMBED_HIDDEN_SIZE,
                          input_length=story_maxlen))
    sentrnn.add(Dropout(0.3))

    qrnn = Sequential()
    qrnn.add(Embedding(vocab_size, EMBED_HIDDEN_SIZE,
                       input_length=query_maxlen))
    qrnn.add(Dropout(0.3))
    qrnn.add(GRU(EMBED_HIDDEN_SIZE, return_sequences=False))
    qrnn.add(RepeatVector(story_maxlen))

    model = Sequential()
    model.add(Merge([sentrnn, qrnn], mode='sum'))
    model.add(GRU(EMBED_HIDDEN_SIZE, return_sequences=False))
    model.add(Dropout(0.3))
    model.add(Dense(vocab_size, activation='softmax'))
    return model

MODEL_FACTORIES = {
    "mlnn": get_mlnn_model,
    "cnn": get_cnn_model,
    "big_cnn": get_big_cnn_model,
    "fixed_cnn": get_fixed_cnn_model,
    "logistic": get_logistic_model,
    "bigru": get_bigru_model,
    "babi_gru": get_babi_rnn
}

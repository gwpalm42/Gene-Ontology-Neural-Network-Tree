import tensorflow as tf
'''
basic training algorithm for a neural network
'''
def train_NN(data, labels, unique_labels: int, epoch_num=30):
    x, y = data.shape
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(units=128, input_shape=(y,), activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dropout(0.05, input_shape=(256,)))
    model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(unique_labels, activation=tf.nn.softmax))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(x=data, y=labels, batch_size=10, epochs=epoch_num, shuffle=True, verbose=2)
    return model

           
                    
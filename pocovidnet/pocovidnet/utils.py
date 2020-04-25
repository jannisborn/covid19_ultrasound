from tensorflow.keras.callbacks import Callback
import numpy as np
from sklearn.metrics import balanced_accuracy_score


# A class to show balanced accuracy.
class Metrics(Callback):

    def __init__(self, valid_data, model):
        super(Metrics, self).__init__()
        self.valid_data = valid_data
        self._data = []
        self.model = model

    def on_epoch_end(self, epoch, logs=None):
        # if epoch:
        #     for i in range(1):  # len(self.valid_data)):
        x_test_batch, y_test_batch = self.valid_data

        y_predict = np.asarray(self.model.predict(x_test_batch))

        y_val = np.argmax(y_test_batch, axis=1)
        y_predict = np.argmax(y_predict, axis=1)
        self._data.append(
            {
                'val_balanced': balanced_accuracy_score(y_val, y_predict),
            }
        )
        print(f'Balanced accuracy is: {self._data[-1]}')
        return

    def get_data(self):
        return self._data
import numpy as np
import neural_network as NN
'''
finds the optimal threshold for multiprediction model
'''
def threshold_descent(model, test_features, predicted_count: float) -> float:
    predictions = model.predict(test_features)
    threshold = np.average(predictions)
    count = threshhold_count(threshold, predictions)
    while not (count >= (predicted_count * 0.95) and count <= (predicted_count * 1.05)):
        if count > (predicted_count * 0.95):
            threshold = threshold * 1.05
        else:
            threshold = threshold * 0.95
        count = threshhold_count(threshold, predictions)
    return threshold
'''
returns the number of labels predicted with the current threshold.
'''
def threshhold_count(threshold, predictions) -> int:
    bin_scores = (predictions>threshold)
    return np.sum(bin_scores)
'''
class that holds the model and the threshold

train: uses the keras NN train and then learns the threshold

predict: uses the learning threshold to predict multiple labels. 
if there are no labels that are above the threshld, assign the highest
scoring label. 
'''
class ThresholdNetwork:
   def __init__(self):
      self.model = None
      self.threshold = None
   
   def train(self, data, test_data, labels, unique_labels: int, predicted_count: float):
       self.model = NN.train_NN(data, labels, unique_labels)
       self.threshold = threshold_descent(self.model, test_data, predicted_count)
   
   def predict(self, features):
        predictions = []
        all_scores = self.model.predict(features)
        for feature_scores in all_scores: 
            labels = np.where(feature_scores >= self.threshold)
            if len(labels[0]) == 0:
                labels = np.argmax(feature_scores)
                if type(labels) is not np.int64:
                   labels = labels[0]
            else: 
                labels = labels[0]
            predictions.append(labels)
        return np.asarray(predictions)
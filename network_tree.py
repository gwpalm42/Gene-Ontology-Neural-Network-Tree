import neural_network as nn
import numpy as np
'''
node that holds a neural network and can hold other neural networks 
'''
class neural_node:
    def __init__(self):
        self.children = []
        self.neural_network = None
        self.GO_term = None
        self.is_leaf = False
        self.GO_stdlabels = None
'''
Caller for the recursive method
'''
def neural_tree_train(features, labels):
    root = recursive_tree_train(features, labels, "0003674")
    return root
'''
recursively train on each hierarchy tier in the data
'''
def recursive_tree_train(features, labels, term):
    node = neural_node()
    node.GO_term = term
    # base case: The node is passed empty data
    if (len(labels) == 0): 
        node.is_leaf = True
        return node
    # recursive case: the node is passed data.
    # learn tier one labels
    # store model
    # create nodes based on tier one labels 
    # pass down correct data to nodes and recur
    # if there is only one type of class left, make a leaf
    else:
        learn_labels, stdlabels = std_tier_ones(labels)
        node.GO_stdlabels = stdlabels
        if len(np.unique(stdlabels)) == 1:
            node.is_leaf = True
            return node
        node.neural_network = nn.train_NN(features, learn_labels, len(np.unique(learn_labels)))
        labels, learn_labels = trim_first_terms(labels, learn_labels)
        index_dict = get_index_dict(learn_labels, stdlabels)
        for term in stdlabels:
            node.children.append(recursive_tree_train(features[index_dict[term]], labels[index_dict[term]], term))
    return node

'''
helper method that makes the data learnable for the neural network. 
'''
def std_tier_ones(labels) -> np.ndarray:
    GO_to_stdlabels = []
    new_labels = []
    unique_labels = 0
    for i in range(len(labels)):
        if labels[i][0] in GO_to_stdlabels:
            new_labels.append(GO_to_stdlabels.index(labels[i][0]))
        else: 
            GO_to_stdlabels.append(labels[i][0])
            new_labels.append(unique_labels)
            unique_labels = unique_labels + 1
    return np.asarray(new_labels), np.asarray(GO_to_stdlabels)
'''
returns a dictionary that corresponds np.where indices to the terms
'''
def get_index_dict(learn_labels, stdlabels):
    index_dict = dict()
    for i in range(len(stdlabels)): 
        index_dict[stdlabels[i]] = np.where(learn_labels == i)[0]
    return index_dict
'''
pops the first term off of each label
'''
def trim_first_terms(labels, learn_labels):
    deletions = []
    for i in range(len(labels)):
        labels[i].pop(0)
        if len(labels[i]) == 0:
            deletions.append(i)
    if(len(deletions) > 0):
        labels = np.delete(labels, np.asarray(deletions), 0)
        learn_labels = np.delete(learn_labels, np.asarray(deletions), 0)
    return labels, learn_labels

####################### PREDICTION ##############################################
''' 
prediction method for the neural tree.
'''
def neural_tree_predict(feature, root) -> str:
    final_prediction = '0003674  '
    return recursive_prediction(feature, root, final_prediction)
'''
Recursive prediction helper method
'''
def recursive_prediction(feature, root:neural_node, final_prediction: str) -> str: 
    if root.is_leaf:
        final_prediction = final_prediction + root.GO_term
        return final_prediction
    else:
        prediction = np.argmax(root.neural_network.predict(np.array([feature,])))
        GO_term = root.GO_stdlabels[prediction]
        final_prediction = final_prediction + GO_term + '  '
        for node in root.children:
            if node.GO_term == GO_term:
                return recursive_prediction(feature, node, final_prediction)


import numpy as np
import kmer_counter as kc

'''
convert text dictionary to python dict.
'''
def txt_to_dict(file_name: str) -> dict:
    with open(file_name,'r') as inf:
        return eval(inf.read())
'''
creates a dictionary of kmer counts from a text file where the labels are seperated from the sequence by a comma.
'''
def create_kmer_dict(file_name: str, k=3) -> dict:
    kmer_dict = {}
    with open(file_name, 'r') as file:
        for line in file.readlines():
            comma_index = line.find(',')
            kmer_dict[line[0:comma_index]] = get_kmer_count(line[comma_index+1:], k)
    return kmer_dict
'''
takes a string and returns an ndarray where each element represents a kmer count.
'''
def get_kmer_count(sequence: str, k) -> np.ndarray:
    return kc.kmer_count(sequence, k)
'''
combine two dictionaries that use proteins as keys into one dictionary with:
key "labels" = applicable GO terms.
key "features" = kmer array counts.
the index indicates corrolation. ie, labels[4] is the label for features[4]
'''
def combine_protein_dicts(features: dict, labels: dict) -> dict: 
    output = {}
    output['features'] = []
    output['labels'] = []
    for key in labels:
        if key in features:
            output['features'].append(features[key])
            output['labels'].append(labels)
    output['features'] = np.asarray(output['features'])
    output['labels'] = np.asarray(output['labels'])
    return output
'''
This code takes the kmer to GO dict and returns a dictionary that has 
the features and a single standardized class label.
'''
def create_class_label_dict(kmer_go_dict: dict) -> dict:
    labels = kmer_go_dict['labels']
    unique_labels = []
    unique_classes = 0
    for i in range(0,len(labels)):
        label_found = False
        for j in range(0, len(labels[i])):   
            if labels[i][j] in unique_labels:
                labels[i] = unique_labels.index(labels[i][j]) 
                label_found = True
                break
        if not label_found:
            unique_labels.append(labels[i][0])
            labels[i] = unique_classes
            unique_classes = unique_classes + 1
    
    kmer_go_dict['GO_terms'] = np.asarray(unique_labels)
    return kmer_go_dict
'''
shuffles and normalizes a dictionary containing 'features' and 'labels'
'''
def shuffle_and_normalize(fl_dict: dict) -> dict:
    import tensorflow as tf
    import sklearn
    
    features = fl_dict['features']
    labels = fl_dict['labels']
    features = tf.keras.utils.normalize(features, axis=1)
    features, labels = sklearn.utils.shuffle(features, labels)
    fl_dict['features']  = features   
    fl_dict['labels'] = labels
    return fl_dict
'''
returns the data sectioned into test and train based on section size.
'''
def split_data(data: np.ndarray, section_size: int):
      test = []
      train =[]
      for i in range(len(data)): 
            if ((i + 1) % section_size == 0):
                  test.append(data[i])
            else:
                  train.append(data[i])
      return np.asarray(train), np.asarray(test)
'''
takes the kmer_to_GO dictionary and splits each list label into n distinct points,
where n is the number of labels. Also standardizes the GO terms.
'''
def std_and_split_list_labels(kmer_to_GO_dict: dict) -> dict:
    labels = kmer_to_GO_dict['labels']
    features = kmer_to_GO_dict['features']
    unique_labels = []
    unique_classes = 0
    new_features = []
    new_labels = []
    for i in range(len(labels)):
        for j in range(0, len(labels[i])):   
            if labels[i][j] in unique_labels:
                new_labels.append(unique_labels.index(labels[i][j]))
                new_features.append(features[i])
            else: 
                unique_labels.append(labels[i][j])
                new_labels.append(unique_classes)
                new_features.append(features[i])
                unique_classes = unique_classes + 1
    kmer_to_GO_dict['labels'] = np.asarray(new_labels)
    kmer_to_GO_dict['features'] = np.asarray(new_features)
    kmer_to_GO_dict['GO_terms'] = np.asarray(unique_labels)
    return kmer_to_GO_dict
'''
takes an array of lists and returns the average length
'''
def label_count(labels) -> float:
    count = 0
    for label in labels:
        if type(label) is np.int64 or type(label) is np.int32:
            count = count + 1
        else: 
            count = count + len(label)
    return float(count)
'''
I don't know to score multiclass labels yet so here is this. 
'''
def score_multiclass(predictions, labels, GO_dict): 
    with open('predictions.txt', 'w') as file:
        for i in range(len(predictions)):
            file.write('Expected:  ')
            for label in labels[i]:
                file.write(label)
                file.write(' ')
            file.write('\n')
            file.write('Predicted: ')
            if type(predictions[i]) is np.int64: 
                    file.write(GO_dict[predictions[i]])
                    file.write(' ')
            else: 
                for j in range(len(predictions[i])):
                    file.write(GO_dict[predictions[i][j]])
                    file.write(' ')
            file.write('\n')
            file.write('\n')
'''
Score single output against multiclass
'''
def score_1output_against_multiclass(predictions, labels, GO_dict):
    scores = np.zeros(len(predictions))
    for i in range(len(scores)):
        if (labels[i].count(GO_dict[predictions[i]]) > 0):
            scores[i] = 1
    return np.mean(scores == 1)
'''
splits the multilabelled points and assign a hierarchy path to them
'''
def split_labels_and_get_hierarchy(kmer_to_GO_dict: dict):
    import hierarchy_dictionary as hd
    hd.get_go_dictionary()
    labels = kmer_to_GO_dict['labels']
    features = kmer_to_GO_dict['features']
    new_features = []
    new_labels = []
    for i in range(len(labels)):
        for j in range(0, len(labels[i])):   
            new_features.append(features[i])
            new_labels.append(hd.get_one_go_path("GO:" + labels[i][j]))
    new_dict = dict()
    new_dict['labels'] = np.asarray(new_labels)
    new_dict['features'] = np.asarray(new_features)
    return new_dict
'''
trims the -1 and the redundant labels
'''
def trim_hierarchy(hier_dict: dict): 
    labels = hier_dict['labels']
    features = hier_dict['features']
    new_features = []
    new_labels = []
    for i in range(len(labels)):
        if labels[i] != -1:
            new_features.append(features[i])
            labels[i].pop(0) # get rid of the first term
            new_labels.append(labels[i])
    new_dict = dict()
    new_dict['labels'] = new_labels
    new_dict['features'] = np.asarray(new_features)
    return new_dict
'''
prints out the predicted path and the potential correct paths per point
'''
def make_prediction_file(kmer_to_GO_dict, neural_tree): 
    import hierarchy_dictionary as hd
    import network_tree as nt
    hd.get_go_dictionary()
    with open('predictions.txt', 'w') as file:
        for i in range(len(kmer_to_GO_dict['labels'])):
            file.write('predicted hierarchy: ')
            file.write('\n')
            nt.neural_tree_predict_tofile(kmer_to_GO_dict['features'][i], neural_tree, file)
            file.write('\n')
            file.write('correct hierarchies: ')
            file.write('\n')
            for j in range(len(kmer_to_GO_dict['labels'][i])):
                if hd.get_one_go_path("GO:" + kmer_to_GO_dict['labels'][i][j]) != -1:
                    for term in hd.get_one_go_path("GO:" + kmer_to_GO_dict['labels'][i][j]):
                        file.write(term + ' ')
                    file.write('\n')
                else:
                    file.write("this term is obsolete, ignore prediction")
                    file.write('\n')
            file.write('\n')
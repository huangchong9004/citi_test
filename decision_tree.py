from datetime import datetime
from math import log, floor, ceil
import random
import numpy as np

#### This is a simple random forest classification method #######

class Utility(object):
    
    # This method computes entropy for information gain
    def entropy(self, class_y):
        # Input:            
        #   class_y         : list of class labels (0's and 1's)
        entropy = 0
        size, count = len(class_y), sum(class_y)
        if (count == 0 or count == size):
            entropy = 0
        else:
            m = (count * 1.0) /size
            n = 1 - m
            entropy = -m * log(m, 2) - n * log(n, 2)
        return entropy

    def partition_classes(self, X, y, split_attribute, split_val):
        # Inputs:
        #   X               : data containing all attributes
        #   y               : labels
        #   split_attribute : column index of the attribute to split on
        #   split_val       : a numerical value to divide the split_attribute
        X_left = [i for i in X if i[split_attribute] <= split_val ]
        X_right = [i for i in X if i[split_attribute] > split_val]
        y_left = [y[i] for i in range(len(y)) if X[i][split_attribute] <= split_val]
        y_right = [y[i] for i in range(len(y)) if X[i][split_attribute] > split_val]
        return (X_left, X_right, y_left, y_right)

    def information_gain(self, previous_y, current_y):
        # Inputs:
        #   previous_y: the distribution of original labels (0's and 1's)
        #   current_y:  the distribution of labels after splitting based on a particular
        #               split attribute and split value
        prev = self.entropy(previous_y)
        ratio = len(current_y[0])/len(previous_y)
        left = self.entropy(current_y[0])
        right = self.entropy(current_y[1])
        info_gain = np.float64((prev * len(previous_y) - (len(current_y[0]) * left + (len(current_y[1])) * right))/len(previous_y))
        
        return info_gain
    def best_split(self, X, y):
        split_attribute, split_val = 0, 0
        max_gain, num = -10, 3
        rand_idx = np.random.randint(0, len(X[0]), num)
        for i in rand_idx:
            temp = set([list[i] for list in X])
            left = []
            right =[]
            for value in temp:
                for j in range(len(X)):
                    if (X[j][i] <= value):
                        left.append(y[j])
                    else:
                        right.append(y[j])
                split = [left, right]
                info_gain = self.information_gain(y, split);
                if (info_gain > max_gain):
                    max_gain = info_gain
                    split_val = value
                    split_attribute = i
        X_left, X_right, y_left, y_right = self.partition_classes(X, y, split_attribute, split_val)
        result = {}
        result["split_attribute"] = split_attribute
        result["split_val"] = split_val
        result["X_left"] = X_left
        result["X_right"] = X_right
        result["y_left"] = y_left
        result["y_right"] = y_right
        return result

class DecisionTree(object):
    def __init__(self, max_depth):
        self.tree = {}
        self.max_depth = max_depth
    	
    def learn(self, X, y, par_node = {}, depth=0):
        if (len(X) == 0):
            val = np.mean(y)
            return  1 if val >= 0.5 else 0
        if (depth > self.max_depth):
            val = np.mean(y)
            return  1 if val >= 0.5 else 0
        u = Utility()
        result = u.best_split(X, y)
        node = {}
        node["split_attribute"] = result["split_attribute"]
        node["split_val"] = result["split_val"]
        node["left"] = self.learn(result["X_left"], result["y_left"], depth = depth + 1)
        node["right"] = self.learn(result["X_right"], result["y_right"], depth = depth + 1)
        if depth == 0:
            self.tree = node
        return node
    
    def classify(self, record):
        node = self.tree
        while isinstance(node, dict):
            split_attribute = node["split_attribute"]
            split_val = node["split_val"]
            if record[split_attribute] <= split_val:
                node = node["left"]
            else :
                node = node["right"]
        return node
        
class RandomForest(object):
    num_trees = 0
    decision_trees = []
    bootstraps_datasets = []
    bootstraps_labels = []

    def __init__(self, num_trees):
        self.num_trees = num_trees
        self.decision_trees = [DecisionTree(max_depth=10) for i in range(num_trees)]
        self.bootstraps_datasets = []
        self.bootstraps_labels = []
        
    def _bootstrapping(self, XX, n):
        sample = [] 
        labels = []  
        idx = [i for i in range(len(XX))]
        selection = random.choices(idx, k = len(idx))
        values= [XX[i] for i in selection]
        sample = [data[:-1] for data in values]
        labels = [data[-1] for data in values]
        return (sample, labels)

    def bootstrapping(self, XX):
        for i in range(self.num_trees):
            data_sample, data_label = self._bootstrapping(XX, len(XX))
            self.bootstraps_datasets.append(data_sample)
            self.bootstraps_labels.append(data_label)

    def fitting(self):
        for i in range(self.num_trees):
            self.decision_trees[i].learn(self.bootstraps_datasets[i], self.bootstraps_labels[i])

    def voting(self, X):
        y = []
        for record in X:
            votes = []
            
            for i in range(len(self.bootstraps_datasets)):
                dataset = self.bootstraps_datasets[i]
                
                if record not in dataset:
                    OOB_tree = self.decision_trees[i]
                    effective_vote = OOB_tree.classify(record)
                    votes.append(effective_vote)

            counts = np.bincount(votes)

            if len(counts) == 0:
                y  = np.append(y, np.random.randint(0, 2, 1))
            else:
                y = np.append(y, np.argmax(counts))
                
        return y

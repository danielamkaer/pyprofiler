import numpy as np

class Model:
    def __init__(self):
        self.features = []
#        self.profiles = []
        self.data = np.empty(shape=(0,0))

    def feature(self, name):
        if name not in self.features:
            self.features.append(name)
            self.data = np.concatenate((self.data, np.zeros(shape=(self.data.shape[0], 1))), axis=1)
            print(f"added feature {name}")
        return self.features.index(name)

    def addProfile(self, featureRow):
        self.data = np.concatenate((self.data, featureRow), axis=0)

#    def profile(self, name):
#        if name not in self.profiles:
#            self.profiles.append(name)
#            self.data = np.concatenate((self.data, np.zeros(shape=(1, self.data.shape[1]))), axis=0)
#            print(f"added profile {name}")
#        return self.profiles.index(name)

    def fromFeatures(self, features):
        ls = np.array([self.feature(name) for name in features])
        row = np.zeros(shape=(1, len(self.features)))
        row[0,ls] = 1
        return row

    def crossProduct(self, featureRow):
        if featureRow.shape[1] != self.data.shape[1]:
            featureRow = np.concatenate((featureRow, np.zeros(shape=(1, self.data.shape[1] - featureRow.shape[1]))), axis=1)

        return np.array([np.dot(featureRow, row)/featureRow.sum() for row in self.data])
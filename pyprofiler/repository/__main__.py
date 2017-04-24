import numpy as np
from pyprofiler.repository.model import Model
from pyprofiler.repository.util import features_from_profile
import pickle
import json
import sys

try:
    with open('model.bin','rb') as file:
        m = pickle.load(file)

except IOError:
    m = Model()

profile = json.load(sys.stdin)
features = features_from_profile(profile)
model_features = m.fromFeatures(features)
cross = m.crossProduct(model_features)
if cross.shape[0] > 0:
    print(f"cross: {cross}")
    i = np.argmax(cross)
    print(f"i: {i}")
    if cross[i] != 1:
        m.addProfile(model_features)
else:
    m.addProfile(model_features)

with open('model.bin','wb') as file:
    pickle.dump(m, file)

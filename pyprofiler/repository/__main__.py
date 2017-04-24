import numpy as np
from pyprofiler.repository.model import Model
from pyprofiler.repository.util import features_from_profile

m = Model()
#
#a = m.fromFeatures(['tcp:google.dk:443', 'tcp:facebook.com:443'])
#m.data = np.concatenate((m.data, a), axis=0)
#b = m.fromFeatures(['tcp:bt.dk:443', 'tcp:jp.com:443'])
#m.data = np.concatenate((m.data, b), axis=0)
#c = m.fromFeatures(['tcp:tado.com:443', 'tcp:danalock.com:443'])
#p1 = m.crossProduct(a)
#p2 = m.crossProduct(b)
#p3 = m.crossProduct(c)
#print(p1)
#print(p2)
#print(p3)

tado = {
    "clients": [
        {"proto": "tcp", "dest": "i.my.tado.com", "port": 443}
    ],
    "servers": []
}

hue = {
    "clients": [
        {"proto": "tcp", "dest": "bridge.meethue.com", "port": 443}
    ],
    "servers": [
        { "proto": "tcp", "port": 8080 }
    ]
}

tado_features = m.fromFeatures(features_from_profile(tado))
m.addProfile(tado_features)
hue_features = m.fromFeatures(features_from_profile(hue))
m.addProfile(hue_features)
print(m.data)

tado_features = m.fromFeatures(features_from_profile(tado))
hue_features = m.fromFeatures(features_from_profile(hue))

print(m.crossProduct(tado_features))
print(m.crossProduct(hue_features))
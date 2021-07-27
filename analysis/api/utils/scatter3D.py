import logging
import numpy as np
import pandas as pd

# PCA
from sklearn import decomposition


# THIS IS WHAT WE NEED TO LOOK AT!
from sklearn import preprocessing as preproc
# from sklearn.preprocessing import StandardScaler


logger = logging.getLogger(__name__)

def get_scatter3D(data):

    if(data['view']['settings']['method'] == "PCA"):
        feature_columns = data['view']['settings']['featureColumns']
        target_column = data['view']['settings']['targetColumn']

        df = pd.DataFrame(data['data'])
        df_train = df[feature_columns]
        X = df_train.values
        df_target = df[target_column]
        y = df_target.values

        if "preprocessingEnabled" in data['view']['settings'].keys():
            if "preprocMethod" in data['view']['settings'].keys():
                if(data['view']['settings']['preprocessingEnabled'] == True):
                    if(data['view']['settings']['preprocMethod'] == "StandardScaling"):
                        scaler = preproc.StandardScaler()
                        scaler.fit(X)
                        X = scaler.transform(X)
                    elif(data['view']['settings']['preprocMethod'] == "Normalization"):
                        normalizer = preproc.Normalizer().fit(X)
                        X = normalizer.transform(X)

        pca = decomposition.PCA(n_components=3)
        pca.fit(X)
        X = pca.transform(X)
        evr = pca.explained_variance_ratio_

        pca_x = []; pca_y = []; pca_z = []
        for pcaSet in X:
            pca_x.append(pcaSet[0])
            pca_y.append(pcaSet[1])
            pca_z.append(pcaSet[2])

        data['data']['x'] = pca_x
        data['data']['y'] = pca_y
        data['data']['z'] = pca_z
        data['data']['evr'] = evr

    return data['data']

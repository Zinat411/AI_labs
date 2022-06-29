
import pandas as pd
from keras.utils import to_categorical
from pandas import DataFrame
from sklearn.preprocessing import LabelEncoder, normalize, MinMaxScaler
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from sklearn import preprocessing

class readData:
    def __init__(self):
        self.path='glass.data'

    def readData(self):

        df = pd.read_csv(self.path)
        last_column,data = df.values[:, -1],df.values[:,1:-1]

        print(df)

        labels = LabelEncoder().fit_transform(last_column)
        print(labels)

        y =np.array(labels)
        plt.hist(y)
        plt.xlabel('glass types')
        plt.ylabel('num')
        # plt.show()

        # X=df.drop(data)
        X=preprocessing.normalize(data)
        normalized = DataFrame(MinMaxScaler().fit_transform(data))

        # X=normalize(X)



        # ros = RandomOverSampler(random_state=42)
        # x_ros, y_ros = ros.fit_resample(X, y)

        train_x, test_x, train_y, test_y = train_test_split(normalized,labels,stratify=labels,test_size=0.2,random_state=42)
        print('train_x :',train_x.shape)
        print('train_y :',train_y.shape)
        print('test_x :',test_x.shape)
        print('test_y :',test_y.shape)
        return train_x, train_y, test_x, test_y
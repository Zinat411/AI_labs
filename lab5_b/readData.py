
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from tensorflow.keras.utils import to_categorical, normalize
df = pd.read_csv('glass.data')
last_column = df.iloc[:, -1].values

#print(df)
labeencoder = LabelEncoder()
labels = labeencoder.fit_transform(last_column)
#print(labels)

y =np.array(labels)
plt.hist(y)
plt.xlabel('glass types')
plt.ylabel('num')
#plt.show()

X=df.drop(last_column)
X=normalize(X)
y= df.iloc[:, -1]


ros = RandomOverSampler(random_state=42)
x_ros, y_ros = ros.fit_resample(X, y)

X_train, X_test, y_train, y_test = train_test_split(x_ros,y_ros,test_size=0.2,random_state=42)
y_train=to_categorical(y_train)
y_test=to_categorical(y_test)
print('X_train :',X_train.shape)
print('y_train :',y_train.shape)
print('X_test :',X_test.shape)
print('y_test :',y_test.shape)
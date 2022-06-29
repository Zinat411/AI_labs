import numpy as np
from sklearn.neural_network import MLPClassifier
class NW:
    def __init__(self,train,train_y,test,test_y):
        self.train=train
        self.test=test
        self.train_y=train_y
        self.test_y=test_y
    def mlpFunc(self):
        results = [0, 0, 0, 0, 0, 0]
        correct = [0, 0, 0, 0, 0, 0]
        mlp = MLPClassifier(random_state=1, max_iter=30000)
        mlp= mlp.fit(self.train, self.train_y)
        predict_x = mlp.predict_proba(self.test)
        predict_y=self.softmax(predict_x)
        x = 0
        for p, t in zip(predict_y, self.test_y):
            results[p] += 1
            if p == t:
                correct[p] += 1
                x += 1
        print(f'Micro: {x / 43}')
        print(results)
        counter = 0
        for a, r in zip(results, correct):
            counter += (r / a)
        print(f'Macro: {counter / 6}')
    def softmax(self,predict_x):
        predict_y = []
        counter=0
        for i in predict_x:
            index = 0
            max = -1
            marr = np.exp(i) / np.sum(np.exp(i), axis=0)
            m = 0
            print(f'{counter}:   {marr}')
            for j in marr:
                temp=0
                if j > max:
                    max=j
                    m=index
                index += 1
            predict_y.append(m)
            counter += 1
        print(f'softmax:   {predict_y}')
        return predict_y
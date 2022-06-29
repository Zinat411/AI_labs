import numpy as np
from sklearn.neural_network import MLPClassifier


class NW:
    def __init__(self,train,trainvector,test,testvector):
        self.train=train
        self.test=test
        self.trainvector=trainvector
        self.testvector=testvector

    def mlpFunc(self):
        mlp = MLPClassifier(random_state=1, max_iter=3000)
        mlp= mlp.fit(self.train, self.trainvector)
        predictdata = mlp.predict_proba(self.test)
        predictedlabels=self.softmax(predictdata)


        results = [0, 0, 0, 0, 0, 0]
        correct = [0, 0, 0, 0, 0, 0]
        TP = 0
        for predection, test in zip(predictedlabels, self.testvector):
            results[predection] += 1
            if predection == test:
                correct[predection] += 1
                TP += 1
        print(f'Micro Result is: {TP / 43}')
        print(results)


        counter = 0
        for answer, result in zip(results, correct):
            counter += (result / answer)

        print(f'Macro result is : {counter / 6}')

    def softmax(self,predictions):
        predicted_labels = []
        counter=0
        for x in predictions:
            index = 0
            max_index = 0
            max = -1
            max_array = np.exp(x) / np.sum(np.exp(x), axis=0)

            print(f'{counter}:   {max_array}')
            for j in max_array:
                temp=0
                if j > max:
                    max=j
                    max_index=index
                index += 1

            predicted_labels.append(max_index)
            counter += 1
        print(f'softmax result is::   {predicted_labels}')
        return predicted_labels
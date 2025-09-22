import pickle

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

data_dict = pickle.load(open('./.pickle', 'rb'))

data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

model = RandomForestClassifier()

model.fit(x_train, y_train)
print('\033[91m'+'model: ' + '\033[92m', model)

y_predict = model.predict(x_test)
print('\033[91m'+'y_predict: ' + '\033[92m', y_predict)

score = accuracy_score(y_predict, y_test)
print('\033[91m'+'score: ' + '\033[92m', score)

print('{}% of samples were classified correctly !'.format(score * 100))

f = open('model.p', 'wb')
pickle.dump({'model': model}, f)
f.close()

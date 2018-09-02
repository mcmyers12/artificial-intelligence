#various approaches to Titanic data: SVM, random forests, naive model

import numpy as np
from sklearn import cross_validation
from sklearn.svm import SVC
#from sklearn.neural_network import BernoulliRBM
from sklearn.metrics import f1_score, accuracy_score
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from patsy import dmatrices

''' CSV Parsing based on Dumoulin's code '''
# read the training data
df = pd.read_csv("train.csv") 

df = df.drop(['Ticket','Cabin', 'Name'], axis=1)
# Remove NaN values
df = df.dropna() 

#print df.columns

df_target, df_data = dmatrices('Survived ~ C(Pclass) + C(Sex) + Age + \
                Parch + Fare + C(Embarked)', df, return_type="dataframe")

df_target = np.ravel(df_target)

x_train, x_test, y_train, y_test = cross_validation.train_test_split(
    df_data, df_target, test_size=0.4, random_state=0)

#print df_data.columns

''' Various approaches '''
#Support vector machine: this method has very poor F1
#Changing degree of kernel polynomial does not change results
model = SVC(verbose = True)
model.fit(x_train, y_train)
prediction = model.predict(x_test)

#print prediction

print "*** Support Vector Machine"
print 'Accuracy: %f' % model.score(x_test, y_test)
print 'F1 score: %f' % f1_score(y_test, prediction)
#Default degree = 3
# Accuracy: 0.631579
# F1 score: 0.450262

#Random forest - example from Kaggle
# Import the random forest package
from sklearn.ensemble import RandomForestClassifier 

# Create the random forest object which will include all the parameters
# for the fit
forest = RandomForestClassifier(n_estimators = 100)

# Fit the training data to the Survived labels and create the decision trees
#forest = forest.fit(train_data[0::,1::],train_data[0::,0])
forest = forest.fit(x_train, y_train)

# Take the same decision trees and run it on the test data
output = forest.predict(x_test)
print "*** Random Forest"
print 'Accuracy: %f' % forest.score(x_test, y_test)
print 'F1 score: %f' % f1_score(y_test, output)
#Tends towards ~.8 accuracy, ~.75 F1

#Super-Naive appraoch
#print x_train
naive_prediction = []
gender_model = []
for index, row in x_test.iterrows():
    if (row['C(Sex)[T.male]'] == 0 or row['Age'] < 18):
        gender_model.append(1)
    else:
        gender_model.append(0)

print "*** Very Simple Model: Assuming Women and Children Always Live"
print 'F1 score: %f' % f1_score(y_test, gender_model)
#F1 score ~ .72



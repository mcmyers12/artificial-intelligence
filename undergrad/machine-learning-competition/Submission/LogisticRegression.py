#!/usr/bin/env python
'''Authors: Miranda, Sarah, Chauncy
Version: Assignment 7
Date: April 22, 2015
Description: Feature inference, logistic regression for Titanic data modeling
'''

import numpy as np
import pandas as pd
from patsy import dmatrices, dmatrix
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation
from sklearn.metrics import f1_score

def infer_ages(frame):
    '''It stands to reason that maried people are older than unmarried people,
    so we infer people's ages based on title (Mr/Master/Mrs/Miss). idea from:
    kaggle.com/c/titanic/forums/t/10341/anyone-hit-80-with-scikit-learn
    '''
    ids = {'MarriedMaleAge':'Mr.', 'SingleMaleAge':'Master.',
        'MarriedFemaleAge':'Mrs.', 'SingleFemaleAge':'Miss.'}
    for key in ids.keys():
        #Create new column to find median age of marital status class
        frame[key] = frame['Age']
        #Fill in ages for each marital status class
        for index, row in frame.iterrows():
            if ids[key] not in row['Name']:
                frame.loc[index, key] = np.nan
        #Assign median age of marital status class to NANs
        for index, row in frame.iterrows():
            if ids[key] in row['Name'] and np.isnan(row['Age']):
                frame.loc[index, 'Age'] = frame[key].median()
        #No longer require this extra column
        frame.drop([key], axis=1)
    #'Ms.' not caught by the pattern, so just give them overall median
    frame.loc[(frame.Age.isnull()), 'Age'] = frame['Age'].median()
    return frame

def parse_test_set():
    '''Parse and process the test data set'''
    df_test = pd.read_csv("test.csv")
    df_test = infer_ages(df_test)
    df_test.drop(['Ticket', 'Cabin', 'Name'], axis=1)
    df_test.loc[(df_test.Parch.isnull()), 'Parch'] = 0
    df_test.loc[(df_test.Fare.isnull()), 'Fare'] = df_test['Fare'].median()
    dfin = dmatrix('C(Pclass) + C(Sex) + Age + \
                    Parch + Fare + C(Embarked)',
                    df_test, return_type="dataframe")
    return dfin

def parse_training_set():
    '''Parse and process the training data set'''
    df_train = pd.read_csv("train.csv")
    df_train = df_train.drop(['Ticket', 'Cabin', 'Name'], axis=1)
    df_train.loc[(df_train.Parch.isnull()), 'Parch'] = 0
    df_train.loc[(df_train.Fare.isnull()), 'Fare'] = df_train['Fare'].median()
    return df_train

def write_to_file(prediction, dfin):
    '''Write prediction associated with dfin to a CSV file'''
    fout = open('out.csv', 'w')
    fout.write("PassengerId,Survived\n")
    #Write to CSV
    for index, row in dfin.iterrows():
        #index + 892 == hacky way of writing PassengerId
        fout.write(str(index + 892) + "," + str(int(prediction[index])) + '\n')
    fout.close()

def main():
    '''Model and cross-validate training set, then make prediction for test'''
    #Parse CSVs into data frame
    dfin = parse_test_set()
    df_train = parse_training_set()

    #Partition the training set for cross-validation
    df_target, df_data = dmatrices('Survived ~ C(Pclass) + C(Sex) + Age + \
                    Parch + Fare + C(Embarked)',
                    df_train, return_type="dataframe")
    df_target = np.ravel(df_target)
    x_train, x_test, y_train, y_test = cross_validation.train_test_split(
        df_data, df_target, test_size=0.4, random_state=0)

    #Logistic regression with sklearn
    model = LogisticRegression().fit(x_train, y_train)
    y_predict = model.predict(x_test)
    print "Accuracy: %f" % model.score(x_test, y_test)
    print "F1 Score: %f" % f1_score(y_test, y_predict)

    #Now use the model to make a prediction
    prediction = model.predict(dfin)
    write_to_file(prediction, dfin)

if __name__ == '__main__':
    main()

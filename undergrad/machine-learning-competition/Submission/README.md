Here we describe some of the different models we looked at. Unless otherwise stated, F1 scores and accuracies are stated with respect to the training data set.

**Naive Model**  
As a benchmark for the machine learning algorithms we tested, we initially wrote a simple script in which all women and minors live, and everyone else dies. This approach yields an F1 score of ~0.72. We searched for more sophisticated models to improve upon this.

**Support Vector Machines**  
A support vector machine (SVC in sklearn.svm) creates a hyperplane in the parameter space in order to binarily classify data. For some reason, this model ended up being very poorly suited to the Titanic data; we obtained an accuracy of ~0.63 and an F1 score of about 0.45 by this method. We might have been able to improve upon this by modifying the SVM parameters, but we decided to move onto a different method.

**Neural Networks**  
We thought about using a neural network for this project, but sklearn only has a neural network for unsupervised learning (BernoulliRBM). This would be unsuitable for our purposes.

**Random Forests**  
A random forest (RandomForestClassifier in sklearn.ensemble) takes the average of a "forest" of decision trees in order to reduce the effects of overfitting in any single tree. Using a random forest, we managed to get an accuracy of ~0.78 and an F1 score of about 0.73: an improvement upon the naive model. However, this is non-deterministic: some runs of the random forest yielded higher accuracy/F1 scores and some yielded lower scores.

**Logistic Regression**  
Using logistic regression (LogisticRegression in sklearn.linear_model), we obtained an accuracy of ~0.81 and an F1 score of about 0.75. In the competition, this yielded an accuracy of 0.765 on the test data set. We ended up making a submission using this model, incorporating the age inference technique described below.

**Age Inference**  
To fill in the unknown ages of passengers, one could use the median age. However, we found a technique on the [forum](kaggle.com/c/titanic/forums/t/10341/anyone-hit-80-with-scikit-learn)  which incorporates name data to create a finer estimate of passenger age. Nearly every passenger name gives their title (Mr./Master./Mrs./Miss.) and these identifiers can be used to determine marital status. There is a positive correlation between marital status and age, so rather than fill in each unidentified age with the overall median, we filled it in with the median for one's marital status. The small remainder of people identified as Miss./Dr. or without titles are given the overall median age.

**Other Inferences**  
For missing fares, we used the median fare. For missing number of parents/children, we assigned 0, since if one doesn't know how many parents/children accompanied the passenger, then it's likely the passenger was unaccompanied.

**Notes on Pylint**  
Pylint gives a number of bugs of the form "No name X in Y" and "(Instance of)/(Module) X has no Y member". We believe this is a bug in pylint's static analysis with respect to imported modules (numpy, patsy, etc.). If you disable these messages, our code passes pylint.

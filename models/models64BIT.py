import pandas as pd
import pickle

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import train_test_split


data = pd.read_csv("bzData.csv", index_col=[0])

y = data['reliability']
X = data.drop(['reliability', 'product'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=26)


# Ada Boosting Classifier
model = AdaBoostClassifier(algorithm ='SAMME.R' , n_estimators=150, random_state=26)
model.fit(X_train,y_train)

filename = 'abc.sav'
pickle.dump(model, open(filename, 'wb'))

print("Finished ABC")

# Bagging Classifier
model = BaggingClassifier(n_estimators=10, max_features=4, random_state=26)
model.fit(X_train, y_train)

filename = 'bagging.sav'
pickle.dump(model, open(filename, 'wb'))

print("Finished Bagging")

# Extra Trees Classifier
model = ExtraTreesClassifier(n_estimators=10, criterion='gini', random_state=26, bootstrap=True)
model.fit(X_train,y_train)

filename = 'extratrees.sav'
pickle.dump(model, open(filename, 'wb'))

print("Finished Extra Trees")

# Gradient Boosting Classifer
model = GradientBoostingClassifier(random_state=26)
model.fit(X_train,y_train)

filename = 'gradientboosting.sav'
pickle.dump(model, open(filename, 'wb'))

print("Finished Gradient Boosting")

# KNN Classifier
model = KNeighborsClassifier(p=4, n_neighbors=30)
model.fit(X_train, y_train)

filename = 'knn.sav'
pickle.dump(model, open(filename, 'wb'))

print("Finished KNN")

# Random Forest Classifier
model = RandomForestClassifier(max_depth=5, random_state=26, criterion='gini', n_estimators=50, max_features=5, bootstrap=True)
model.fit(X_train, y_train)

filename = 'randomforest.sav'
pickle.dump(model, open(filename, 'wb'))

print("Finished Random Forest \n All models completed.")

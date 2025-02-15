# -*- coding: utf-8 -*-
"""CodSoft project 2 .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EXrgWeDQVcnFgd7Y2YHmJhSx9nGEwIiE#scrollTo=L5lKSzCcrEbl

#**CodSoft Project 2**

Use the Titanic dataset to build a model that predicts whether a
passenger on the Titanic survived or not.
We are using here logistic regresion and Decision Tree to classify.


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import GridSearchCV


# Dataset

data = pd.read_csv("titanic.csv")

"""#**Data Overview**"""

# to see the top rows

data.head()

data.info()

data.describe()

data.columns

data.isna().sum()

print("Shape of the titanic data:- ",data.shape)

"""#**Data Visualization**"""

def count_plot(feature):
    # This function takes a feature as input and creates a count plot
    sns.countplot(x=feature, data=data)
    plt.show()
    print("\n")

columns = ['Survived','Pclass','Sex','SibSp','Embarked', 'Parch']
for i in columns:
    count_plot(i)

data["Age"].plot(kind='hist', title = "Age", color = 'orange', edgecolor = 'black')

# pie chart showing rate of survival
survived_counts = data['Survived'].value_counts().reset_index()
survived_counts.columns = ['Survived', 'Count']
fig = px.pie(survived_counts, values='Count', names=['No', 'Yes'], title='Survived', labels={'Count': 'Count'}, color = ['No', 'Yes'])
fig.update_traces(textposition='inside',  textinfo='percent+label+value')
fig.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')
fig.show()

# Show histogram chart of survival counts by gender
fig1 = px.histogram(data, x='Sex', color='Survived', barmode='group', color_discrete_map={0: "yellow", 1: "red"})
fig1.update_layout(title='Sex: Survived vs Dead')
fig1.show()

# Show histogram chart of survival counts by Pclass
fig2 = px.histogram(data, x='Pclass', color='Survived', barmode='group', title='Pclass: Survived vs Dead', labels={'Pclass': 'Pclass'}, color_discrete_map={0: 'red', 1: 'blue'})
fig2.update_layout(title='PClass: Survived vs Dead')
fig2.show()

"""#**Data Preprocessing**"""

data.head()

#dropping unnecessay columns

data.drop(['PassengerId', 'Name', 'Cabin', 'Ticket'], axis=1, inplace=True)

#after dropping unnecessary column
data.head()

# Fill missing values in age column by imputing the mean
data['Age'].fillna(data['Age'].mean(), inplace=True)

# Fill missing values in embarked column by imputing the mode
data["Embarked"].fillna(data["Embarked"].mode()[0], inplace=True)

data.info()

# Transform categorical data into numerical data manually as there are only 2 to 3 values for each column
data['Sex'] = data['Sex'].map( {'female': 1, 'male': 2} ).astype(int)
data['Embarked'] = data['Embarked'].map( {'S': 1, 'C': 2, 'Q': 3} ).astype(int)

"""# **Exploring dataset**

Exploring dataset afer changes.
"""

#Understanding the relationship between all the features
sns.pairplot(data, hue='Survived')

# Checking corelation between Variables

plt.figure(figsize=(10,5))
sns.heatmap(data.corr(), annot=True, linewidths=.2)

# Calculate the correlation list
target_corr = data.corr()['Survived'].abs().sort_values(ascending=False)
# Create a bar chart to visualize the correlations
plt.figure(figsize=(10, 6))
sns.barplot(x=target_corr.index[1:], y=target_corr.values[1:])
plt.xticks(rotation=45, ha='right')
plt.xlabel('Features')
plt.ylabel('Correlation with diagnosis')
plt.title('Correlation between diagnosis and Features')
plt.tight_layout()
plt.show()

"""#**Modeling**"""

X = data.drop("Survived", axis=1)
Y = data["Survived"]

print(f"'X' shape: {X.shape}")
print(f"'y' shape: {Y.shape}")

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, shuffle = True, random_state=42)

#Feature Scaling (Standardization)
std = StandardScaler()
X_train = std.fit_transform(X_train)
X_test = std.transform(X_test )

pd.DataFrame(X_train,columns = X.columns ).describe(include = 'all')

def model_stats(Y_pred, Y_test):

    result = np.vstack((Y_pred, Y_test)).T
    #print(result)
    differences = np.count_nonzero(result.sum(axis = 1) == 1 )
    print('Wrong Predictions = ',differences)
    cm = confusion_matrix(Y_test, Y_pred)
    print(cm, '\n Accuracy Score = ',accuracy_score(Y_test, Y_pred))
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Reds')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title('Confusion Matrix')
    plt.show()

"""## ***Logistic Regression***"""

classifier = LogisticRegression(random_state = 0)
classifier.fit(X_train, Y_train)

"""Creating confussion matrix"""

Y_pred = classifier.predict(X_test)

model_stats(Y_test, Y_pred)

"""## ***Decision Tree***

Using decision tree we can classify survied persons and unsurvived one.
"""

# Create a grid of hyperparameter values
param_grid = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_depth': [3, 5, 7, None],
    "max_features": [i for i in range(1, 10, 1)],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [i for i in range(1, 5, 1)],
    'max_leaf_nodes': [None, 10, 20],
    'min_impurity_decrease': [1e-7, 1e-5, 1e-3]
}

# Create a decision tree classifier object
classifier = DecisionTreeClassifier(random_state = 0)

# Create a GridSearchCV object
grid_search = GridSearchCV(classifier, param_grid, cv=5)

# Fit the grid search object to the training data
grid_search.fit(X_train, Y_train)

# Get the best hyperparameters
best_params = grid_search.best_params_

# Create a decision tree classifier object with the best hyperparameters
classifier = DecisionTreeClassifier(**best_params)
classifier.fit(X_train,Y_train)

# Make predictions on the test data
Y_pred = classifier.predict(X_test)

# Evaluate the predictions
model_stats(Y_pred,Y_test)

F = ['Survived', 'Pclass', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
T = ['0', '1', '2', '3', '4', '5', '6']
fig = plt.figure(figsize = (25, 20))
plt = tree.plot_tree(classifier, feature_names = F, class_names = T, filled = True)
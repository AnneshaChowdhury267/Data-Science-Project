# -*- coding: utf-8 -*-
"""Group 10_CSE437_Living_Status_Prediction_of_Breast_Cancer_Patients.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eu9EgMVK4u6Rlxv58poWrGJSKupSSCtn
"""

#importing libraries here

import numpy as np
from google.colab import files
import pandas as pd
from sklearn.impute import SimpleImputer

from sklearn import preprocessing as process

from sklearn.model_selection import train_test_split

from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

import matplotlib.pyplot as plt

#for confusion matrix 
import numpy
from sklearn import metrics

#for PCA
from sklearn.decomposition import PCA


import seaborn as sb
import warnings

from google.colab import drive

drive.mount("/drive")

"""We load the dataset from our drive and see the first 5 instances of our dataset."""

import pandas as pd

df = pd.read_csv("/drive/MyDrive/Spring 2023 Semester/CSE437/Breast_Cancer.csv")

df.head()

"""We get a description of the dataset from all the columns, numerical as well as categorical variables."""

df.describe(include="all")

"""We printed the shape of the dataset here. We also drop the "differentiate" column because this column is completely similar with the "Grade" column. Here, 'Well Differentiated' is of Graded 01, 'Moderately Differentiated' is Graded 02, 'Poorly Differentiated' is Graded 03, and 'Undifferentiated' is Graded 04. We check the shape again after dropping the column."""

print(df.shape)
print("\n")

print(df['differentiate'].unique())
print(df['Grade'].unique())

df.drop(columns=["differentiate"], inplace=True)
print("\n")
print(df.shape)

"""We check the datatypes of the columns."""

df.dtypes

"""We check if there's any Null value in any of the columns in our dataframe."""

df.isnull().sum()

impute = SimpleImputer(missing_values=np.nan, strategy='mean')

impute.fit(df[['Age']])
df['Age'] = impute.transform(df[['Age']])

impute.fit(df[['Regional Node Examined']])
df['Regional Node Examined'] = impute.transform(df[['Regional Node Examined']])

df.isnull().sum() # Checking null values (not found any)

"""We check the if there's any duplicate values in the dataframe keeping the first duplicate occurances' as false."""

duplicate_values = df[df.duplicated(keep = "first")]
print(duplicate_values.shape)
print("\n")
duplicate_values.sort_values(by = list(df.columns))

"""As there's only one duplicate value, we drop it keeping the first row of it and change the source dataframe instead of returning a new instance, by keeping inplace value True."""

print(df.shape)
df.drop_duplicates(keep = "first", inplace = True)
print("\n")
print(df.shape)
print("\n")
df[df.duplicated(keep = "first")]

"""Renamed a column's name due to having a whitespace in the original name."""

df.rename(columns={"T Stage ": "T Stage"}, inplace=True)

"""Checking all the categorical variables' unique category names."""

for i in df.columns:
  print(f"{i} - {df[i].nunique()}")

"""Categorical Encoding to all the possible feature variables."""

temp1 = {'White': 1, 'Black': 2, 'Other': 3}
df["Race"] = df["Race"].replace(temp1)

temp2 = {'Married': 1, 'Divorced': 2, 'Single ' : 3, 'Widowed': 4, 'Separated': 5}
df["Marital Status"] = df["Marital Status"].replace(temp2)

temp3 = {'T1': 1, 'T2': 2, 'T3': 3, 'T4': 4}
df["T Stage"] = df["T Stage"].replace(temp3)

temp4 = {'N1': 1, 'N2': 2, 'N3': 3}
df["N Stage"] = df["N Stage"].replace(temp4)

temp5 = {'IIA': 1, 'IIIA': 2, 'IIIC': 3, 'IIB': 4, 'IIIB': 5}
df["6th Stage"] = df["6th Stage"].replace(temp5)

temp6 = {'1': 1, '2': 2, '3': 3, ' anaplastic; Grade IV': 4}
df["Grade"] = df["Grade"].replace(temp6)

temp7 = {'Regional': 1, 'Distant': 2}
df["A Stage"] = df["A Stage"].replace(temp7)

temp8 = {'Regional': 1, 'Distant': 2}
df["A Stage"] = df["A Stage"].replace(temp8)

temp9 = {'Positive': 0, 'Negative': 1}
df["Estrogen Status"] = df["Estrogen Status"].replace(temp9)
df["Progesterone Status"] = df["Progesterone Status"].replace(temp9)

"""Using Label Encoder to encode the Target Variable "Status". """

from sklearn import preprocessing as process

label_encoder = process.LabelEncoder()
df["Status"]= label_encoder.fit_transform(df["Status"]) #Level Alive = 0 and Dead = 1

"""We will be using Correlation Coefficient to select features. """

warnings.filterwarnings("ignore")

plt.figure(figsize=(12,6))
sb.heatmap(df.corr(),annot=True, fmt='.1g')

print(df.shape)
print("\n")
df.drop(columns=["Race"], inplace=True)
print(df.shape)

# Plotting frequency

for i in df:
    plt.figure(figsize = (5, 5))
    plt.hist(df[i])
    plt.xlabel(i)
    plt.ylabel("Frequency")
    plt.title(f"{i}")
    plt.show()

"""We drop the "Race" column as we can see that it has the least value in the Correlation Matrix, compared to the target variable "Status".

We make a copy of the dataframe. We use MinMax Scaler to scale the feature variables with int64 datatype and comparatively larger numerical values. Those variables/columns are: "Age", "Tumor Size", "Regional Node Examined", "Reginol Node Positive", "Survival Months". Also, the MinMax scaler works in the following way: 

x_std = (x – x.min(axis=0)) / (x.max(axis=0) – x.min(axis=0))

x_scaled = (x_std * (max – min)) + min

Here, 
x: Value of a feature instance.

x.min(axis=0) : Minimum feature value. 

x.max(axis=0): Maximum feature value 

min, max: feature_range (by default it is 0 and 1)
"""

df_scaled = df.copy()

scaler = process.MinMaxScaler()
df_scaled[["Age", "Tumor Size", "Regional Node Examined", "Reginol Node Positive", "Survival Months"]] = scaler.fit_transform(df_scaled[["Age", "Tumor Size", "Regional Node Examined", "Reginol Node Positive", "Survival Months"]])

"""We see the first 5 instances of our dataframe after scaling it."""

df_scaled.head(5)

"""We check the datatypes again after Categorical Encoding and Normalization/Scaling is completed."""

df_scaled.dtypes

"""As we can see, all the categorical feature variables and also the target variable here have become of type int64 after encoding. We have to make them of type category again and recheck."""

df_scaled["Marital Status"] = df_scaled["Marital Status"].astype("category")
assert df_scaled["Marital Status"].dtype == "category"

df_scaled["T Stage"] = df_scaled["T Stage"].astype("category")
assert df_scaled["T Stage"].dtype == "category"

df_scaled["N Stage"] = df_scaled["N Stage"].astype("category")
assert df_scaled["N Stage"].dtype == "category"

df_scaled["6th Stage"] = df_scaled["6th Stage"].astype("category")
assert df_scaled["6th Stage"].dtype == "category"

df_scaled["Grade"] = df_scaled["Grade"].astype("category")
assert df_scaled["Grade"].dtype == "category"

df_scaled["A Stage"] = df_scaled["A Stage"].astype("category")
assert df_scaled["A Stage"].dtype == "category"

df_scaled["Estrogen Status"] = df_scaled["Estrogen Status"].astype("category")
assert df_scaled["Estrogen Status"].dtype == "category"

df_scaled["Progesterone Status"] = df_scaled["Progesterone Status"].astype("category")
assert df_scaled["Progesterone Status"].dtype == "category"

df_scaled["Status"] = df_scaled["Status"].astype("category")
assert df_scaled["Status"].dtype == "category"

"""We recheck the datatype of all the variables again. It should be proper now."""

df_scaled.dtypes

plt.figure(figsize = (20, 15))

plt.subplot(3,2,1)
sb.countplot(x = 'Status', hue= 'Marital Status', palette='Set2', data = df_scaled)

plt.subplot(3,2,2)
sb.countplot(x = 'Status', hue= '6th Stage', palette='Set2', data = df_scaled)

plt.subplot(3,2,3)
sb.countplot(x = 'Status', hue= 'Grade', palette='Set2', data = df_scaled)

plt.subplot(3,2,4)
sb.countplot(x = 'Status', hue= 'T Stage', palette='Set2', data = df_scaled)

plt.subplot(3,2,5)
sb.countplot(x = 'Status', hue= 'N Stage', palette='Set2', data = df_scaled)

plt.subplot(3,2,6)
sb.countplot(x = 'Status', hue= 'A Stage', palette='Set2', data = df_scaled)

plt.figure(figsize = (20, 15))

plt.subplot(3,2,1)
sb.countplot(x = 'Status', hue= 'Estrogen Status', palette='Set2', data = df_scaled)

plt.subplot(3,2,2)
sb.countplot(x = 'Status', hue= 'Progesterone Status', palette='Set2', data = df_scaled)

plt.figure(figsize = (10,5))
sb.stripplot(x = 'Regional Node Examined', y ='Reginol Node Positive', data = df_scaled, hue='Status')

plt.figure(figsize=(15,8))
x=df_scaled['Tumor Size']
sb.displot(x,kde=True,color='#e74c3c')
plt.show()

from sklearn.model_selection import train_test_split

target = df_scaled[['Status']]
possible_features = df_scaled[['Age', 'Marital Status', 'T Stage', 'N Stage', '6th Stage', 'Grade', 'A Stage', 'Tumor Size', 'Estrogen Status', 'Progesterone Status', 'Regional Node Examined', 'Reginol Node Positive', 'Survival Months']]

x = possible_features
y = target

x_remain, x_test, y_remain, y_test = train_test_split(x, y, test_size = 0.20, random_state = 0, stratify = y)
x_train, x_dev, y_train, y_dev = train_test_split(x_remain, y_remain, test_size = 0.1, random_state = 0, stratify = y_remain)

print(x_train.shape)
print(y_train.shape)
print("\n")
print(x_dev.shape)
print(y_dev.shape)
print("\n")
print(x_test.shape)
print(y_test.shape)

target_labels = ['Alive', 'Dead']

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier

random_forest_model = RandomForestClassifier(criterion='entropy')
svc_model = SVC(kernel='poly', degree=5, gamma="auto")
knn_model = KNeighborsClassifier(metric = 'manhattan', weights = 'distance', n_neighbors = 7)
abc_model = AdaBoostClassifier(n_estimators = 15, estimator = random_forest_model, learning_rate = 0.01)

model_names = ["Random Forest Classifier", "Support Vector Classifier", "K Nearest Neighbours Classifier", "AdaBoost Classifier"]
models = [random_forest_model, svc_model, knn_model, abc_model]

from seaborn import heatmap
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

prediction_values_dev = []
prediction_values_test = []

accuracy_scores_dev = []
accuracy_scores_test = []

recall_scores_dev = []
recall_scores_test = []

precision_scores_dev = []
precision_scores_test = []

f1_scores_dev = []
f1_scores_test = []

for model in models:
  model.fit(x_train, y_train.values.ravel())

  prediction = model.predict(x_dev)
  accuracy = accuracy_score(y_dev, prediction)
  precision = precision_score(y_dev, prediction, average = "weighted")
  recall = recall_score(y_dev, prediction, average = "weighted")
  f1 = f1_score(y_dev, prediction, average = "weighted")

  prediction_values_dev.append(prediction)
  accuracy_scores_dev.append(accuracy)
  recall_scores_dev.append(recall)
  precision_scores_dev.append(precision)
  f1_scores_dev.append(f1)

  prediction = model.predict(x_test)
  accuracy = accuracy_score(y_test, prediction)
  precision = precision_score(y_test, prediction, average = "weighted")
  recall = recall_score(y_test, prediction, average = "weighted")
  f1 = f1_score(y_test, prediction, average = "weighted")

  prediction_values_test.append(prediction)
  accuracy_scores_test.append(accuracy)
  recall_scores_test.append(recall)
  precision_scores_test.append(precision)
  f1_scores_test.append(f1)

"""#Random Forest Classifier

"""

print(model_names[0],"\n---------------------------------------------------------------- \n")

print("Development Accuracy Store:",accuracy_scores_dev[0])
print("Development Precision Score:",precision_scores_dev[0])
print("Development Recall Score:",recall_scores_dev[0])
print("Development F1 Score:",f1_scores_dev[0])

print("\n")

print(classification_report(y_dev, prediction_values_dev[0], target_names = target_labels))

print("\n")

print("Test Accuracy Store:",accuracy_scores_test[0])
print("Test Precision Score:",precision_scores_test[0])
print("Test Recall Score:",recall_scores_test[0])
print("Test F1 Score:",f1_scores_test[0])

print("\n")

print(classification_report(y_test, prediction_values_test[0], target_names = target_labels))

conf_matrix = confusion_matrix(prediction_values_test[0], y_test)
heatmap(conf_matrix , cmap="Pastel1_r", xticklabels=['Positive(Actual)' ,'Negative(Actual)' ], yticklabels=['Positive(Predict)' ,'Negative(Predict)' ], annot=True)

"""#Support Vector Classifier"""

print(model_names[1],"\n---------------------------------------------------------------- \n")

print("Development Accuracy Store:",accuracy_scores_dev[1])
print("Development Precision Score:",precision_scores_dev[1])
print("Development Recall Score:",recall_scores_dev[1])
print("Development F1 Score:",f1_scores_dev[1])

print("\n")

print(classification_report(y_dev, prediction_values_dev[1], target_names = target_labels))

print("\n")

print("Test Accuracy Store:",accuracy_scores_test[1])
print("Test Precision Score:",precision_scores_test[1])
print("Test Recall Score:",recall_scores_test[1])
print("Test F1 Score:",f1_scores_test[1])

print("\n")

print(classification_report(y_test, prediction_values_test[1], target_names = target_labels))

conf_matrix = confusion_matrix(prediction_values_test[1], y_test)
heatmap(conf_matrix , cmap="Pastel1_r", xticklabels=['Positive(Actual)' ,'Negative(Actual)' ], yticklabels=['Positive(Predict)' ,'Negative(Predict)' ], annot=True)

"""#K Nearest Neighbours Classifier"""

print(model_names[2],"\n---------------------------------------------------------------- \n")

print("Development Accuracy Store:",accuracy_scores_dev[2])
print("Development Precision Score:",precision_scores_dev[2])
print("Development Recall Score:",recall_scores_dev[2])
print("Development F1 Score:",f1_scores_dev[2])

print("\n")

print(classification_report(y_dev, prediction_values_dev[2], target_names = target_labels))

print("\n")

print("Test Accuracy Store:",accuracy_scores_test[2])
print("Test Precision Score:",precision_scores_test[2])
print("Test Recall Score:",recall_scores_test[2])
print("Test F1 Score:",f1_scores_test[2])

print("\n")

print(classification_report(y_test, prediction_values_test[2], target_names = target_labels))

conf_matrix = confusion_matrix(prediction_values_test[2], y_test)
heatmap(conf_matrix , cmap="Pastel1_r", xticklabels=['Positive(Actual)' ,'Negative(Actual)' ], yticklabels=['Positive(Predict)' ,'Negative(Predict)' ], annot=True)

"""#AdaBoost Classifier"""

print(model_names[3],"\n---------------------------------------------------------------- \n")

print("Development Accuracy Store:",accuracy_scores_dev[3])
print("Development Precision Score:",precision_scores_dev[3])
print("Development Recall Score:",recall_scores_dev[3])
print("Development F1 Score:",f1_scores_dev[3])

print("\n")

print(classification_report(y_dev, prediction_values_dev[3], target_names = target_labels))

print("\n")

print("Test Accuracy Store:",accuracy_scores_test[3])
print("Test Precision Score:",precision_scores_test[3])
print("Test Recall Score:",recall_scores_test[3])
print("Test F1 Score:",f1_scores_test[3])

print("\n")

print(classification_report(y_test, prediction_values_test[3], target_names = target_labels))

conf_matrix = confusion_matrix(prediction_values_test[3], y_test)
heatmap(conf_matrix , cmap="Pastel1_r", xticklabels=['Positive(Actual)' ,'Negative(Actual)' ], yticklabels=['Positive(Predict)' ,'Negative(Predict)' ], annot=True)

from sklearn.decomposition import PCA

pca = PCA()
x_train_pca = pca.fit_transform(x_train)
x_dev_pca = pca.transform(x_dev)
x_test_pca = pca.transform(x_test)

explained_variance = pca.explained_variance_ratio_
print(explained_variance)

pca = PCA(n_components = 3)
x_train_pca = pca.fit_transform(x_train)
x_dev_pca = pca.transform(x_dev)
x_test_pca = pca.transform(x_test)

count = 0
while count < 4:
  print(model_names[count],"\n---------------------------------------------------------------- \n")
  models[count].fit(x_train_pca, y_train.values.ravel())

  prediction = models[count].predict(x_test_pca)
  print(classification_report(y_test, prediction, target_names = target_labels))

  count = count + 1

import matplotlib.pyplot as plt

# Create a list of tuples containing the model name and its accuracy scores
models_bar = [(model_names[0], accuracy_scores_dev[0]*100, accuracy_scores_test[0]*100),
          (model_names[1], accuracy_scores_dev[1]*100, accuracy_scores_test[1]*100),
          (model_names[2], accuracy_scores_dev[2]*100, accuracy_scores_test[2]*100),
          (model_names[3], accuracy_scores_dev[3]*100, accuracy_scores_test[3]*100)]

# Create lists for model names, training accuracies, and testing accuracies
model_names = [model[0] for model in models_bar]
training_accs = [model[1] for model in models_bar]
testing_accs = [model[2] for model in models_bar]

# Plot the accuracies
plt.figure(figsize=(10, 10))
plt.bar(model_names, training_accs, width=0.5, label='Development Accuracy')
plt.bar([name + ' (test)' for name in model_names], testing_accs, width=0.5, label='Testing Accuracy')
plt.xticks(rotation=45, ha='right')
plt.ylabel('Accuracy (%)')
plt.legend()
plt.show()
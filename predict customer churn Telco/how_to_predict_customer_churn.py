# -*- coding: utf-8 -*-
"""how to predict customer churn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QZIlfAL7Qc-a4SpQv6_NFFfIklhDbD90

# PREDIKSI CUSTOMER CHURN

## Problem Statment

Telecommunications companies face an increasing risk of customer churn due to increasingly fierce competition between providers. This can result in reduced company revenue.

Therefore an effective strategy is needed to reduce the churn rate and retain customers

## Solution

Predicting customer churn. This prediction is important for companies to know in order to be able to map a business strategy to retain customers.

## Goals

* Identify the factors that affect customer churn at telecommunications companies.
* Develop prediction models to estimate the probability of future customer churn.
* Identify potential churn customers and take action to retain them.

# Exploratory Data Analysis (EDA)

Upload Data Train and Data Test
"""

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

from google.colab import files
uploaded = files.upload()

import io
import pandas as pd
df= pd.read_csv(io.BytesIO(uploaded['Data Train Provider.csv']))

df.head()

"""* state: the state where the customer is located
* account_length: the number of days since the customer joined the service provider
* area_code: area code of the customer's phone
* international_plan: does the customer have an international service plan (yes/no)
* voice_mail_plan: does the customer have a voicemail service plan (yes/no)
* number_vmail_messages: the number of voicemail messages received by the subscriber
* total_day_minutes: number of minutes used by the customer during business hours (in minutes)
* total_day_calls: number of calls made by the customer during business hours
* total_day_charge: the fee charged to the customer for usage during business hours
* total_eve_minutes: the number of minutes the customer used during the night hours (in minutes)
* total_eve_calls: number of calls made by the customer during night hours
* total_eve_charge: the fee charged to the customer for use during night hours
* total_night_minutes: the number of minutes the customer spends sleeping hours (in minutes)
* total_night_calls: number of calls made by the customer during sleeping hours
* total_night_charge: the fee charged to the customer for usage during sleeping hours
* total_intl_minutes: number of minutes used by the customer for international calls (in minutes)
* total_intl_calls: number of calls made by the customer for international calls
* total_intl_charge: the fee charged to the customer for international calls
* number_customer_service_calls: the number of calls made by the customer to the customer service center
* churn: target variable indicating whether the customer switches services (yes/no)
"""

from google.colab import files
uploaded = files.upload()

import io
import pandas as pd
df_test= pd.read_csv(io.BytesIO(uploaded['Data Test.csv']))

df_test.head()

"""#### First we will take a look at the data"""

df.info()

df_test.info()

"""**No blank data**

**We divide the data into Categorical and Numerical data**
"""

Numericals = ['account_length', 'number_vmail_messages', 'total_day_minutes', 'total_day_calls', 'total_day_charge', 'total_eve_minutes', 'total_eve_calls',
              'total_eve_charge', 'total_night_minutes', 'total_night_calls', 'total_night_charge', 'total_intl_minutes', 'total_intl_calls', 'total_intl_charge', 
              'number_customer_service_calls']
Categoricals = ['state', 'area_code', 'international_plan', 'voice_mail_plan', 'churn']

df.describe()

# View summary descriptive statistics of columns with data type object (including strings)
df.describe(include='O')

df['churn'].value_counts()

"""Here is some initial information about the data we have:
1. There are 4250 data in each column in the dataframe.
2. The fields "international_plan" and "voice_mail_plan" each have 2 unique values, namely "yes" and "no", indicating whether the customer has an international service plan
3. The "churn" column also has 2 unique values, namely "yes" and "no", which indicate whether the customer has stopped subscribing to the service or is still actively using the company's services.
4. The value "area_code_415" in the "area_code" column appears 2108 times, which is the value that appears most frequently in that column.
5. The values ​​"no" in the columns "international_plan", "voice_mail_plan", and "churn" each appear with a higher frequency than the values ​​"yes".

## Univariate Anlysis
"""

plt.figure(figsize=(20,10))

for i in range(0, len(Numericals)):
    plt.subplot(2, 10, i+1)
    sns.boxplot(x=df[Numericals[i]], color='orange', orient='h')
    plt.tight_layout()

plt.show()

plt.figure(figsize=(20,10))
for i in range(len(Numericals)):
    plt.subplot(3, 5, i+1)
    sns.kdeplot(x=df[Numericals[i]], color='orange')

"""Among the Numerical Columns only Number_vmail_Messages, total_intl_class and number_customer_service call are Right or Positive Skew and the others are normally distributed"""

for i in range(len(Categoricals)):
    plt.figure(figsize=(15,5))
    sns.countplot(x=df[Categoricals[i]], data=df, color='green')

"""* The highest number of customers in the countries that have the WV country code
* Area code 415 is the area code of most customer telephones
* Customers have fewer international service plans than those who do not.
* It turns out that there are still many customers who do not have a voicemail service package
* From the existing Churn data, it turns out that there are more customers who do not churn. This indicates that the services provided allow customers to survive and not churn.

## Multivariate Analysis
"""

plt.subplots(figsize=(20,15))
sns.heatmap(df.corr(), annot=True)
plt.show()

"""In this case, the heatmap will show black on
entire heatmap box. However, if you pay more attention
Furthermore, the highest correlation value is found in the column
total day calls of 0.023 this means the number of calls that
carried out by customers during business hours
customers can churn or not.
The higher the value of the total day calls, the higher the churn rate that will occur.
otherwise for the smallest correlation value on Total night calls
equal to -0.0089 means the greater the total number
night it is likely that the customer will experience a slight churn

"""

fig, ax = plt.subplots(1, 1, figsize = (10,8))

sns.kdeplot(data = df, x = df['total_night_calls'], alpha = 0.7, multiple = 'stack', hue = 'churn')
ax.set_title('Distribution of total night calls dan churn', fontsize = 14)
ax.set_xlabel('Total Night Calls')

"""From the distribution it appears that the distribution is normal, the greater the total nights calls, the level of subscribers who do not churn or unsubscribe is more than those who do churn.

If you look further, services such as customer service or complaints can be an indication of customer satisfaction whether you can churn or not

# DATA PREPROCESSING

Split Data
"""

from sklearn.model_selection import train_test_split

X = df.drop(columns=['account_length', 'number_vmail_messages', 'total_day_minutes', 'total_day_calls', 'total_day_charge', 'total_eve_minutes', 'total_eve_calls',
              'total_eve_charge', 'total_night_minutes', 'total_night_calls', 'total_night_charge', 'total_intl_minutes', 'total_intl_calls', 'total_intl_charge', 
              'number_customer_service_calls', 'state', 'area_code', 'international_plan', 'voice_mail_plan', 'churn'])
y = df['churn']

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)

"""## Missing Value"""

df.isna().sum()

"""No Missing Value

## Duplicate Data
"""

print(df.duplicated().sum())

"""No Duplicate data

## Handle Outliers
"""

from scipy import stats

print(f'The number of rows before filtering out the outliers: {len(df)}')
filtered_entries = np.array([True] * len(df))
for col in ['account_length', 'number_vmail_messages', 'total_day_minutes', 'total_day_calls', 'total_day_charge', 'total_eve_minutes', 'total_eve_calls',
              'total_eve_charge', 'total_night_minutes', 'total_night_calls', 'total_night_charge', 'total_intl_minutes', 'total_intl_calls', 'total_intl_charge', 
              'number_customer_service_calls']:
    zscore=abs(stats.zscore(df[col]))
    filtered_entries = (zscore < 3) & filtered_entries


df = df[filtered_entries]
print(f'Number of rows after filtering outliers: {len(df)}')

df.info()

"""## Feature Encoding"""

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
categorical_cols = ['state', 'area_code', 'international_plan', 'voice_mail_plan', 'churn']

for col in categorical_cols:
    df[col] = le.fit_transform(df[col])

df.head()

"""# MODEL

## Logistic Regression
"""

from sklearn.model_selection import train_test_split

X = df.drop(['churn'], axis=1)
y = df['churn']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import cross_validate
from sklearn.linear_model import LogisticRegression

def eval_classification(model):
    y_pred = model.predict(X_test)
    y_pred_train = model.predict(X_train)
    y_pred_proba = model.predict_proba(X_test)
    y_pred_proba_train = model.predict_proba(X_train)
   

    print("Accuracy (Test Set): %.2f" % accuracy_score(y_test, y_pred))
    print("Precision (Test Set): %.2f" %precision_score(y_test, y_pred, zero_division=1))
    print("Recall (Test Set): %.2f" % recall_score(y_test, y_pred))
    print("F1-Score (Test Set): %.2f" % f1_score(y_test, y_pred))
  
    

    print("AUC (test-proba): %.2f" % roc_auc_score(y_test, y_pred_proba[:, 1]))
    print("AUC (train-proba): %.2f" % roc_auc_score(y_train, y_pred_proba_train[:, 1]))

    score = cross_validate(model, X, y, cv=5, scoring='roc_auc', return_train_score=True)
    print('roc_auc(crossval train): '+ str(score['train_score'].mean()))
    print('roc_auc(crossval test): '+ str(score['test_score'].mean()))

from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(max_iter=5000)
lr.fit(X_train, y_train)
eval_classification(lr)

"""* Accuracy (Test Set): 0.88
Accuracy measures how well the model predicts the correct label overall. In this case, the model has an accuracy of 0.88, meaning that your model is able to correctly predict 88% of all data samples in the dataset used for testing.

* Precision (Test Set): 0.61
Precision measures how well the model predicts absolutely positive positive data from all data that the model predicts positively. In this case, the model has a precision value of 0.61, which means that around 61% of the data predicted to be positive by the model are actually positive.

* Recall (Test Set): 0.19
Recall measures how well the model predicts truly positive positive data from all the positive data in the dataset. In this case, the model has a recall value of 0.19, which means that the model only succeeds in predicting about 19% of the positive data in the dataset.

* F1-Score (Test Set): 0.29
The F1-score is the harmonized average of precision and recall, which measures how well the model as a whole predicts the data. In this case, the model has an F1-score of 0.29, which indicates the overall model performance in predicting labels in the dataset.

* AUC (test-proba): 0.81
AUC (Area Under Curve) measures how well the model differentiates between positive and negative class data. In this case, the model has an AUC of 0.81 on the test data using the model's prediction probability. The higher the AUC value, the better the model's performance in discriminating between positive and negative classes.

* AUC (train-proba): 0.83
AUC on the training data using the probability prediction model shows the performance of the model on the training data. In this case, the AUC value is 0.83, which indicates that the model has a good performance in discriminating between positive and negative classes in the training data.

* roc_auc(crossval train): 0.8268933917687811
roc_auc(crossval train) is the AUC on the training data when the cross validation was performed. In this case, the AUC value is 0.826, which indicates that the model has good performance in discriminating between positive and negative classes in the training data during cross-validation.

* roc_auc(crossval test): 0.8195327615167786
roc_auc(crossval test) is the AUC on the test data when cross validation was performed. In this case, the AUC value is 0.819, which indicates that the model has good performance in distinguishing between positive and negative classes.

#### Tuning Hyperparameter
"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import classification_report, roc_auc_score


penalty = ['l2']
C =[float(x) for x in np.linspace(0.0001, 1, 100)]
hyperparameters = dict(penalty=penalty, C=C)

lr = LogisticRegression(max_iter=5000)
rs = RandomizedSearchCV(lr, hyperparameters, scoring='roc_auc', random_state=42, cv=5)
rs.fit(X_train, y_train)
eval_classification(rs)

import numpy as np
import pandas as pd
from sklearn.model_selection import learning_curve
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

# Create a Logistic Regression model
model = LogisticRegression(max_iter=5000)

# Calculating learning curves
train_sizes, train_scores, test_scores = learning_curve(model, X, y, cv=5)

# Make learning curve plots
plt.plot(train_sizes, np.mean(train_scores, axis=1), 'o-', color="r", label="Training error")
plt.plot(train_sizes, np.mean(test_scores, axis=1), 'o-', color="g", label="Cross-validation error")
plt.legend(loc="best")
plt.xlabel("Training examples")
plt.ylabel("Error")
plt.show()

def draw_learning_curve(param_values):
    train_scores= []
    test_scores= []

    for i in param_values:
      lr = LogisticRegression(penalty='l2', C=i, max_iter=5000)
      lr.fit(X_train, y_train)

      # eval on train
      y_pred_train_proba = lr.predict_proba(X_train)
      train_auc = roc_auc_score(y_train, y_pred_train_proba[:,1])
      train_scores.append(train_auc)

      #eval on test
      y_pred_proba = lr.predict_proba(X_test)
      test_auc = roc_auc_score(y_test, y_pred_proba[:,1])
      test_scores.append(test_auc)

      print('param value: ' +str(i) + '; train: ' +str(train_auc) + '; test: ' + str(test_auc))


    plt.plot(param_values, train_scores, label='Train')
    plt.plot(param_values, test_scores, label='Test')
    plt.xlabel('min_samples_leaf')
    plt.ylabel('AUC')
    plt.title('Learning Curve - Hypermeter C - Logistic Regression')
    plt.legend()
    plt.show()


param_values= [int(x) for x in np.linspace(1, 100, 100)]
draw_learning_curve(param_values)

"""## K-Nearst Neighboar (KNN)"""

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
eval_classification(knn)

"""#### Tuning Hyperparameter"""

from sklearn.utils.extmath import weighted_mode
from sklearn.model_selection import RandomizedSearchCV

n_neighbors = [int(x) for x in np.linspace(1, 100, 50)] 
weights = ['uniform', 'distance']
p = [1, 2, 3]
hyperparameters = dict(n_neighbors=n_neighbors, weights=weights, p=p)

knn.fit(X_train, y_train)
rs = RandomizedSearchCV(knn, hyperparameters, scoring='roc_auc', random_state=1, cv=5)
rs.fit(X_train, y_train)
eval_classification(rs)

from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
from sklearn.metrics import classification_report, roc_auc_score

# Dividing the data into train data and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply the undersampling technique to the train data
undersample = RandomUnderSampler(sampling_strategy='majority')
X_train_under, y_train_under = undersample.fit_resample(X_train, y_train)

# Applying oversampling technique to the data train
oversample = RandomOverSampler(sampling_strategy='minority')
X_train_over, y_train_over = oversample.fit_resample(X_train, y_train)

# Build models with undersample or oversample train data
knn = KNeighborsClassifier()
knn.fit(X_train_under, y_train_under)
# or
knn.fit(X_train_over, y_train_over)

# Evaluate the model on test data
y_pred = knn.predict(X_test)
y_pred_proba = knn.predict_proba(X_test)[:,1] # get the probability of a positive prediction
print(classification_report(y_test, y_pred))
print("ROC AUC (test-proba):", roc_auc_score(y_test, y_pred_proba))

# Evaluate the model on the train data
y_train_pred = knn.predict(X_train_under)
y_train_pred_proba = knn.predict_proba(X_train_under)[:,1] # get the probability of a positive prediction
print("ROC AUC (train-proba):", roc_auc_score(y_train_under, y_train_pred_proba))

def draw_learning_curve(param_values):
    train_scores= []
    test_scores= []

    for i in param_values:
      knn = KNeighborsClassifier(n_neighbors=i)
      knn.fit(X_train, y_train)

      # eval on train
      y_pred_train_proba = knn.predict_proba(X_train)
      train_auc = roc_auc_score(y_train, y_pred_train_proba[:,1])
      train_scores.append(train_auc)

      #eval on test
      y_pred_proba = knn.predict_proba(X_test)
      test_auc = roc_auc_score(y_test, y_pred_proba[:,1])
      test_scores.append(test_auc)

      print('param value: ' +str(i) + '; train: ' +str(train_auc) + '; test: ' + str(test_auc))


    plt.plot(param_values, train_scores, label='Train')
    plt.plot(param_values, test_scores, label='Test')
    plt.xlabel('n_neighbors')
    plt.ylabel('AUC')
    plt.title('Learning Curve - Hyperparameter Tuning - KNN')
    plt.legend()
    plt.show()


param_values= [int(x) for x in np.linspace(1, 100, 100)]
draw_learning_curve(param_values)

"""## Decisision Tree"""

from sklearn.tree import DecisionTreeClassifier

dtc = DecisionTreeClassifier()
dtc.fit(X_train, y_train)
eval_classification(dtc)

"""* Accuracy (Test Set): 0.90
Accuracy measures how well the model predicts the correct label overall. In this case, your model has an accuracy of 0.90, meaning that the model is able to correctly predict 90% of all data samples in the dataset used for testing.

* Precision (Test Set): 0.62
Precision measures how well the model predicts absolutely positive positive data from all data that the model predicts positively. In this case, the model has a precision value of 0.62, which means that around 62% of the data predicted to be positive by the model are actually positive.

* Recall (Test Set): 0.72
Recall measures how well the model predicts truly positive positive data from all the positive data in the dataset. In this case, the model has a recall value of 0.72, which means that your model successfully predicts around 72% of the positive data in the dataset.

* F1-Score (Test Set): 0.66
The F1-score is the harmonized average of precision and recall, which measures how well the model as a whole predicts the data. In this case, the model has an F1-score of 0.66, which indicates the overall model performance in predicting labels in the dataset.

* AUC (test-proba): 0.83
AUC (Area Under Curve) measures how well the model differentiates between positive and negative class data. In this case, your model has an AUC of 0.83 on the test data using the model's predicted probability. The higher the AUC value, the better the model's performance in discriminating between positive and negative classes.

* AUC (train-proba): 1.00
AUC on the training data using the probability prediction model shows the performance of the model on the training data. In this case, the AUC value is 1.00, which indicates that the model perfectly discriminates between the positive and negative classes in the training data.

* roc_auc(crossval train): 1.0
roc_auc(crossval train) is the AUC on the training data when the cross validation was performed. In this case, the AUC value is 1.0, which indicates that the model perfectly discriminates between positive and negative classes in the training data during cross-validation.

* roc_auc(crossval test): 0.8333880223976697
roc_auc(crossval test) is the AUC on the test data when cross validation was performed. In this case, the AUC value is 0.833, which indicates that your model has a good performance in discriminating between positive and negative classes in the test data during cross-validation.

### Tuning Hyperparamter
"""

from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from scipy.stats import uniform
import numpy as np

max_depth = [int(x) for x in np.linspace(1, 110, num= 10000)]
min_samples_split = [2, 5, 10, 100]
min_samples_leaf = [1, 2, 4, 10, 20, 50]
max_features = ['auto', 'sqrt']
criterion = ['gini', 'entropy']
splitter = ['best', 'random']

hyperparameters = dict(max_depth=max_depth,
                       min_samples_split=min_samples_split,
                       min_samples_leaf=min_samples_leaf,
                       max_features= max_features,
                       criterion=criterion,
                       splitter=splitter)

#model initialization

dtc = DecisionTreeClassifier()
dtc.fit(X_train, y_train)
eval_classification(dtc)

from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
from sklearn.metrics import classification_report, roc_auc_score

# Dividing the data into train data and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply the undersampling technique to the train data
undersample = RandomUnderSampler(sampling_strategy='majority')
X_train_under, y_train_under = undersample.fit_resample(X_train, y_train)

# Applying oversampling technique to the data train
oversample = RandomOverSampler(sampling_strategy='minority')
X_train_over, y_train_over = oversample.fit_resample(X_train, y_train)

# Build models with undersample or oversample train data
dtc = DecisionTreeClassifier(max_depth = 6)
dtc.fit(X_train_under, y_train_under)
# or
dtc.fit(X_train_over, y_train_over)

# Evaluate the model on test data
y_pred = dtc.predict(X_test)
y_pred_proba = dtc.predict_proba(X_test)[:,1] # get the probability of a positive prediction
print(classification_report(y_test, y_pred))
print("ROC AUC (test-proba):", roc_auc_score(y_test, y_pred_proba))

# Evaluate the model on the train data
y_train_pred = dtc.predict(X_train_under)
y_train_pred_proba = dtc.predict_proba(X_train_under)[:,1] # get the probability of a positive prediction
print("ROC AUC (train-proba):", roc_auc_score(y_train_under, y_train_pred_proba))

"""#### Learning Curve"""

def draw_learning_curve(param_values):
    train_scores= []
    test_scores= []

    for i in param_values:
      dtc = DecisionTreeClassifier(min_samples_leaf = i)
      dtc.fit(X_train, y_train)

      # eval on train
      y_pred_train_proba = dtc.predict_proba(X_train)
      train_auc = roc_auc_score(y_train, y_pred_train_proba[:,1])
      train_scores.append(train_auc)

      #eval on test
      y_pred_proba = dtc.predict_proba(X_test)
      test_auc = roc_auc_score(y_test, y_pred_proba[:,1])
      test_scores.append(test_auc)

      print('param value: ' +str(i) + '; train: ' +str(train_auc) + '; test: ' + str(test_auc))


    plt.plot(param_values, train_scores, label='Train')
    plt.plot(param_values, test_scores, label='Test')
    plt.xlabel('min_samples_leaf')
    plt.ylabel('AUC')
    plt.title('Learning Curve')
    plt.legend()
    plt.show()

param_values= [int(x) for x in np.linspace(1, 100, 100)]
draw_learning_curve(param_values)

"""## Feature Importance"""

def show_feature_importance(model):
    feat_importances = pd.Series(model.feature_importances_, index=X.columns)
    ax = feat_importances.nlargest(25).plot(kind= 'barh', figsize=(10, 8))
    ax.invert_yaxis()


    plt.xlabel('score')
    plt.ylabel('feature')
    plt.title('feature importance score')
    
show_feature_importance(dtc)

from google.colab import files
uploaded = files.upload()

import io
import pandas as pd
df= pd.read_csv(io.BytesIO(uploaded['Data Train Provider.csv']))

max_charge = df['total_day_charge'].max()
print("The highest value of total_day_charge is:", max_charge)

mean_total_day_charge = df['total_day_charge'].mean()
print("The highest value of total_day_charge is:", mean_total_day_charge)

night_calls = df['total_night_calls'].sum()
print("the total_night_calls total is:", night_calls)

"""From the histogram results below, the highest feature that has an effect on determining whether a customer can experience churn or not is total_day_charge.

Then in second place is the international_plan feature and in third place is the number_customer_service_calls feature

## Busines insight and rekomendasi

* Companies need to pay attention to the amount of fees charged to customers for using the service in one day. If the fees are too high, customers may become dissatisfied with the service and switch to another provider. Based on the data, the highest total_day_charge is 59.76 and the average total_day_charge is 30.64. Therefore, companies need to pay attention to pricing in order to remain competitive but not burdensome to customers.

* Customers with international activities may require more frequent international communications than regular customers. Based on the data, there are still many customers who do not have an international service package. Therefore, Companies need to ensure that they offer competitive international plans and provide good service to the customers who have them.

* Customers who frequently contact customer service are most likely to experience problems with service. This can be seen from total_night_calls, because the more calls that come in outside working hours, the more likely the service will experience problems. Based on the data held, the total_night_calls totaled 424318 calls. Therefore, companies need to ensure that their customer service is responsive and can help customers solve their problems quickly and effectively.
"""
# -*- coding: utf-8 -*-
"""ML assignment 1 Part 1

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Yit5K1Iy4TQ9mRKgXYkIZeQfAQBsZNxD

Data Preprocessing
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load the dataset
df = pd.read_csv('StudentsPerformance.csv')

# Check for missing values
print(df.isnull().sum())

# Encode categorical variables
label_encoders = {}
categorical_columns = ['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course']
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Standardize numerical features
scaler = StandardScaler()
df[['reading score', 'writing score']] = scaler.fit_transform(df[['reading score', 'writing score']])

""" Feature Engineering"""

from sklearn.preprocessing import PolynomialFeatures

# Features and target variable
X = df[['reading score', 'writing score']]
y = df['math score']

# Create polynomial features
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

"""Model Building"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_poly_train, X_poly_test, _, _ = train_test_split(X_poly, y, test_size=0.2, random_state=42)

# Train Multilinear Regression
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)

# Train Polynomial Regression
poly_reg = LinearRegression()
poly_reg.fit(X_poly_train, y_train)

"""Model Evaluation"""

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import matplotlib.pyplot as plt

# Predictions
y_pred_lin = lin_reg.predict(X_test)
y_pred_poly = poly_reg.predict(X_poly_test)

# Metrics
print("Multilinear Regression:")
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred_lin)))
print("MAE:", mean_absolute_error(y_test, y_pred_lin))
print("R² Score:", r2_score(y_test, y_pred_lin))

print("\nPolynomial Regression:")
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred_poly)))
print("MAE:", mean_absolute_error(y_test, y_pred_poly))
print("R² Score:", r2_score(y_test, y_pred_poly))

# Plotting
plt.scatter(y_test, y_pred_lin, label='Multilinear', alpha=0.5)
plt.scatter(y_test, y_pred_poly, label='Polynomial', alpha=0.5)
plt.xlabel('Actual Math Scores')
plt.ylabel('Predicted Math Scores')
plt.legend()
plt.title('Actual vs Predicted Math Scores')
plt.show()
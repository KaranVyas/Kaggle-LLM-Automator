import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

# Load the dataset
df = pd.read_csv('datasets/titanic/train.csv')

# Drop columns that are not needed for prediction
df = df.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1)

# Handle missing values
df['Age'].fillna(df['Age'].median(), inplace=True)
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

# One-hot encode categorical variables
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), ['Sex', 'Embarked'])], remainder='passthrough')
df_encoded = pd.get_dummies(df, columns=['Sex', 'Embarked'])

# Split dataset into features and target variable
X = df_encoded.drop('Survived', axis=1)
y = df_encoded['Survived']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
rf_classifier = RandomForestClassifier()
rf_classifier.fit(X_train, y_train)

# Predict the target variable for the test data
predictions = rf_classifier.predict(X_test)

# Save predictions to a CSV file
submission = pd.DataFrame({'PassengerId': X_test.index, 'Survived': predictions})
submission.to_csv('datasets/titanic/submission.csv', index=False)
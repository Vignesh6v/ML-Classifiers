# import the necessary packages
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix,accuracy_score
from sklearn.metrics import recall_score,precision_score
import numpy as np
import argparse

def sigmoid_activation(x):
	return 1.0 / (1 + np.exp(-x))

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--epochs", type=float, default=20,help="# of epochs")
ap.add_argument("-a", "--alpha", type=float, default=1, help="learning rate")
args = vars(ap.parse_args())

# Dataset
cancer = load_breast_cancer()
X= StandardScaler().fit_transform(cancer.data)
X_train, X_test, y_train, y_test = train_test_split(X, cancer.target, stratify=cancer.target, random_state=42)




X_train = np.c_[np.ones((X_train.shape[0])), X_train]
X_test = np.c_[np.ones((X_test.shape[0])), X_test]

print("[INFO] starting training...")
W = np.random.uniform(size=(X_train.shape[1],))


lossHistory = []
for epoch in np.arange(0, args["epochs"]):
	preds = sigmoid_activation(X_train.dot(W))
	error = preds - y_train
	loss = np.sum(error ** 2)
	lossHistory.append(loss)
	print("[INFO] epoch #{}, loss={:.7f}".format(epoch + 1, loss))
	gradient = X_train.T.dot(error) / X_train.shape[0]
	W += -args["alpha"] * gradient


y_pred = []
for i in range(X_test.shape[0]):
	activation = sigmoid_activation(X_test[i].dot(W))
	label = 0 if activation < 0.5 else 1
	y_pred.append(label)

print ("Confusiton Matrix")
print (confusion_matrix(y_test, y_pred))
print ("Accuracy")
print (accuracy_score(y_test,y_pred))
print ("Recall")
print (recall_score(y_test,y_pred))

print ("Precision")
print (precision_score(y_test,y_pred))

'''
# compute the line of best fit by setting the sigmoid function
# to 0 and solving for X2 in terms of X1
Y = (-W[0] - (W[1] * X)) / W[2]

# plot the original data along with our line of best fit
plt.figure()
plt.scatter(X[:, 1], X[:, 2], marker="o", c=y)
plt.plot(X, Y, "r-")
'''

# construct a figure that plots the loss over time
fig = plt.figure()
plt.plot(np.arange(0, args["epochs"]), lossHistory)
fig.suptitle("Training Loss")
plt.xlabel("Epoch #")
plt.ylabel("Loss")
plt.show()

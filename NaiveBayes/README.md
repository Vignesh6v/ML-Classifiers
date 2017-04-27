# NaiveBase Classifier

### nblearn

nblearn.py - is a program that trains on the training data to create the Naive Bayes model.

* It obtains the directory that contains all the training data from the command
line and reads all the files in the directory under the 4 categories "Positive", "Negative", "Deceptive" and "Truthful".
* It outputs the model's parameters into an output file(nbmodel.txt).

### nbclassify


nbclassify.py - is a program that reads the output file created by nblearn.py, and uses the model to classify the new unseen test data present in unknown categories. <br/>

The output is a labelling of each new .txt file into

1. "Positive" or "Negative"
2. "Truthful" or "Deceptive"

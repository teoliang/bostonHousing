"""Load the Boston dataset and examine its target (label) distribution."""

# TESTING GIT
# Again

# --Included:
# a loop for replicate runs
# hacky way to keep plots open
# suppression of warning messages
# -------------------------------#

# Load libraries
import numpy as np
import pylab as pl
from sklearn import datasets
from sklearn.tree import DecisionTreeRegressor
import matplotlib

################################
### ADD EXTRA LIBRARIES HERE ###
################################
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error, make_scorer
from sklearn import grid_search
import warnings
from sklearn.neighbors import NearestNeighbors

def load_data():
	"""Load the Boston dataset."""

	boston = datasets.load_boston()
	return boston


def explore_city_data(city_data):
	"""Calculate the Boston housing statistics."""

	# Get the labels and features from the housing data
	housing_prices = city_data.target
	housing_features = city_data.data

	###################################
	### Step 1. YOUR CODE GOES HERE ###
	###################################
	
	print "No. of houses: " + str(len(housing_prices))
	print "No. of housing features: " + str(housing_features.shape[1])
	print "Minimum price: " + str(np.min(housing_prices))
	print "Maximum price: " + str(np.max(housing_prices))
	print "Mean house price: " + str(np.mean(housing_prices))
	print "Median house price: " + str(np.median(housing_prices))
	print "Standard dev house price: " + str(np.std(housing_prices))
	# Please calculate the following values using the Numpy library
	# Size of data (number of houses)?
	# Number of features?
	# Minimum price?
	# Maximum price?
	# Calculate mean price?
	# Calculate median price?
	# Calculate standard deviation?


def split_data(city_data):
	"""Randomly shuffle the sample set. Divide it into 70 percent training and 30 percent testing data."""

	# Get the features and labels from the Boston housing data
	X, y = city_data.data, city_data.target
	# probably use http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.train_test_split.html for this
	###################################
	### Step 2. YOUR CODE GOES HERE ###
	###################################
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

	
	return X_train, y_train, X_test, y_test


def performance_metric(label, prediction):
	"""Calculate and return the appropriate error performance metric."""

	###################################
	### Step 3. YOUR CODE GOES HERE ###
	###################################
	return mean_squared_error(label, prediction)
	# The following page has a table of scoring functions in sklearn:
	# http://scikit-learn.org/stable/modules/classes.html#sklearn-metrics-metrics
	#pass


def learning_curve(depth, X_train, y_train, X_test, y_test, plots):
	"""Calculate the performance of the model after a set of training data."""

	# We will vary the training set size so that we have 50 different sizes
	sizes = np.round(np.linspace(1, len(X_train), 50))
	train_err = np.zeros(len(sizes))
	test_err = np.zeros(len(sizes))

	print "Decision Tree with Max Depth: "
	print depth

	for i, s in enumerate(sizes):

		# Create and fit the decision tree regressor model
		regressor = DecisionTreeRegressor(max_depth=depth)
		regressor.fit(X_train[:s], y_train[:s])

		# Find the performance on the training and testing set
		train_err[i] = performance_metric(y_train[:s], regressor.predict(X_train[:s]))
		test_err[i] = performance_metric(y_test, regressor.predict(X_test))

		# Plot learning curve graph
		
	if plots:
		learning_curve_graph(sizes, train_err, test_err, depth)


def learning_curve_graph(sizes, train_err, test_err, depth):
	"""Plot training and test error as a function of the training size."""

	pl.figure(depth)
	pl.title('Decision Trees: Performance vs Training Size')
	pl.plot(sizes, test_err, lw=2, label = 'test error')
	pl.plot(sizes, train_err, lw=2, label = 'training error')
	pl.legend()
	pl.xlabel('Training Size')
	pl.ylabel('Error')
	pl.show()


def model_complexity(X_train, y_train, X_test, y_test, plots):
	"""Calculate the performance of the model as model complexity increases."""

	#print "Model Complexity: "

	# We will vary the depth of decision trees from 2 to 25
	max_depth = np.arange(1, 25)
	train_err = np.zeros(len(max_depth))
	test_err = np.zeros(len(max_depth))

	for i, d in enumerate(max_depth):
		# Setup a Decision Tree Regressor so that it learns a tree with depth d
		regressor = DecisionTreeRegressor(max_depth=d)

		# Fit the learner to the training data
		regressor.fit(X_train, y_train)

		# Find the performance on the training set
		train_err[i] = performance_metric(y_train, regressor.predict(X_train))

		# Find the performance on the testing set
		test_err[i] = performance_metric(y_test, regressor.predict(X_test))

	# Plot the model complexity graph
	if plots:
		
		model_complexity_graph(max_depth, train_err, test_err)


def model_complexity_graph(max_depth, train_err, test_err):
	"""Plot training and test error as a function of the depth of the decision tree learn."""
	pl.ioff()
	pl.figure("Model Complexity")
	pl.title('Decision Trees: Performance vs Max Depth')
	pl.plot(max_depth, test_err, lw=2, label = 'test error')
	pl.plot(max_depth, train_err, lw=2, label = 'training error')
	pl.legend()
	pl.xlabel('Max Depth')
	pl.ylabel('Error')
	pl.show()
	
def fit_predict_model(city_data):
	"""Find and tune the optimal model. Make a prediction on housing data."""

	# Get the features and labels from the Boston housing data
	X, y = city_data.data, city_data.target

	# Setup a Decision Tree Regressor
	regressor = DecisionTreeRegressor()

	parameters = {'max_depth':(1,2,3,4,5,6,7,8,9,10)}

	###################################
	### Step 4. YOUR CODE GOES HERE ###
	###################################

	# 1. Find an appropriate performance metric. This should be the same as the
	# one used in your performance_metric procedure above:
	# http://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html
	score = make_scorer(mean_squared_error, greater_is_better=False)
	
	# 2. We will use grid search to fine tune the Decision Tree Regressor and
	# obtain the parameters that generate the best training performance. Set up
	# the grid search object here.
	# http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html#sklearn.grid_search.GridSearchCV
	reg = grid_search.GridSearchCV(regressor, parameters, scoring=score)
	# Fit the learner to the training data to obtain the best parameter set
	print "Final Model: " 
	reg.fit(X, y)
	print reg.best_params_
	
	# Use the model to predict the output of a particular sample
	
	# OJB sample to test boundaries of model - this sample might predict a price higher than original data's highest price. 
	# for non obvious features avrg of the highest price houses values was used
	#x = [0.00, 0.00, 11.00, 0, 0.00, 10.00, 100.00, 1.00, 24, 666.00, 16.00, 380.00, 1.00]
	
	# original sample
	x = [11.95, 0.00, 18.100, 0, 0.6590, 5.6090, 90.00, 1.385, 24, 680.0, 20.20, 332.09, 12.13]
	y = reg.predict(x)
	print "House: " + str(x)
	print "Prediction: " + str(y)
	
	# pro tip suggestion by the reviewer
	indexes = find_nearest_neighbor_indexes(x, X)
	sum_prices = []
	for i in indexes:
		sum_prices.append(city_data.target[i])
	
	
	neighbor_avg = np.mean(sum_prices)
	print "Nearest Neighbors average: " +str(neighbor_avg)
	
	
	
	return reg.best_params_
	
	# PRO TIP suggestion from the reviewer to check nearest neighbours
	
def find_nearest_neighbor_indexes(x, X):  # x is your vector and X is the data set.
	neigh = NearestNeighbors( n_neighbors = 10 )
	neigh.fit( X)
	distance, indexes = neigh.kneighbors( x )
	return indexes
	
	
#In the case of the documentation page for GridSearchCV, it might be the case that the example is just a demonstration of syntax for use of the function, rather than a statement about 
def main(plots):
	"""Analyze the Boston housing data. Evaluate and validate the
	performanance of a Decision Tree regressor on the housing data.
	Fine tune the model to make prediction on unseen data."""
	
	
	
	# Load data
	city_data = load_data()

	# Explore the data
	explore_city_data(city_data)
	
	# adds a loop for repeated runs (to find best median depth)
	# uncomment "best_avrg" if using loop
	# best_avrg = []
	
	for i in range(1):
		# # Training/Test dataset split
		X_train, y_train, X_test, y_test = split_data(city_data)

		# Learning Curve Graphs
		
		max_depths = [1,2,3,4,5,6,7,8,9,10]
		for max_depth in max_depths:
			learning_curve(max_depth, X_train, y_train, X_test, y_test, plots)

		# Model Complexity Graph
		model_complexity(X_train, y_train, X_test, y_test, plots)

		# Tune and predict Model
		fit_predict_model(city_data)
		
		# variables to use if running loop to find median (best depth)
		
		#----------------------------------------#
		# best_param = fit_predict_model(city_data)
		# best_avrg.append(best_param.values())
		
	# final_avrg = sum(best_avrg, [])
	# print np.median(final_avrg)
	#--------------------------------------------#

		
	print "Finished"
if __name__ == "__main__":
	
	pl.ion()
	
	plots = False
	# suppresses deprecation warning 
	warnings.filterwarnings('ignore')
	main(plots)
	
	



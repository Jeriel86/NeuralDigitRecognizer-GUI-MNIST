from scipy.io import loadmat
import numpy as np
from Model import neural_network
from RandInitialize import initialise
from Prediction import predict
from scipy.optimize import minimize




# Loading mat file
data = loadmat('dataset/mnist-original.mat')

# Extracting features from mat file
X = data['data']
X = X.transpose()

# Normalizing the data

X = X/255

# Extracting labels from mat file
y = data['label']
y = y.flatten()

# Splitting data into trining set with 40.000 examples
X_train = X[:40000, :]
y_train = y[:40000]

# Splitting data into testing set with 30.000 examples
X_test = X[40000:, :]
y_test = y[40000:]

m = X.shape[0]
input_layer_size = 784 # Images are of (28 X 28) px so there will be 784 features
hidden_layer_size = 100
num_labels = 10  # There are 10 classes [0, 9]

# Randomly initialising Thetas
initial_Theta1 = initialise(hidden_layer_size, input_layer_size)
initial_Theta2 = initialise(num_labels, hidden_layer_size)

# Unrolling parameters into a single column vector
initial_nn_params = np.concatenate([initial_Theta1.flatten(), initial_Theta2.flatten()])
maxiter = 100
lambda_reg = 0.1
myargs = (input_layer_size, hidden_layer_size, num_labels, X_train, y_train, lambda_reg)

# Calling minimize function to minimize cost function and to train weights
results = minimize(neural_network, x0=initial_nn_params, args=myargs, options={'disp': True,'maxiter':maxiter}, method="L-BFGS-B", jac=True)

nn_params = results["x"] # Trained Theta is extracted

# Weigths are split back to Theta1, Theta2
Theta1 = np.reshape(nn_params[:hidden_layer_size * (input_layer_size + 1)], (hidden_layer_size, input_layer_size + 1)) # shape = (100, 785)
Theta2 = np.reshape(nn_params[hidden_layer_size * (input_layer_size + 1):],(num_labels, hidden_layer_size + 1))   # shape = (10, 101)

# Checking test set accuracy to our model
pred = predict (Theta1, Theta2, X_test)
print('Training Set Accuracy: {:f}'.format((np.mean(pred==y_test) * 100)))

# Checking train set accuracy of our model
pred = predict(Theta1,Theta2, X_train)
print('Training Set Accuracy: {:f}'.format((np.mean(pred == y_train) * 100)))

# Evaluating precision of our model
true_positive = 0

for i in range(len(pred)):
    if pred[i] == y_train[i]:
        true_positive+=1
false_positive = len(y_train) - true_positive
print('precision =', true_positive/(true_positive+false_positive))

# Saving Thetas in .txt file 
np.savetxt('Thetas/Theta1.txt', Theta1, delimiter=' ')
np.savetxt('Thetas/Theta2.txt', Theta2, delimiter=' ')

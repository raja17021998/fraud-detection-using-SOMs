# -*- coding: utf-8 -*-
"""
Created on Wed May 29 08:44:57 2019

@author: Shashwat Bhardwaj
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# We are working on fraud detection. Lets say we are deep learning scientists, working in a bank, and we have a datset that contains information of customers, who are applying for advanced credit cards.So basically these are the informations that customers have to provide while filling the application form. Our mission is to detect potential fraud within these applications. By the end of the mission, we have to give the explicit list of customers, who potentially cheated.

dataset= pd.read_csv('Credit_Card_Applications.csv')
dataset.info()

# What our unsupervised model is going to to? 
# First af all all our customers are inputs to these networks. And then what happens is that these input points are going to be mapped to an output space, and between input space and output space, we have this neural network composed of neurons. Each neuron being initialized as a vector of weights, that is the same size as the vector of customers, i.e. we have a vector of 15 elements, because we have CustomerID + 14 attributes. And so for each observation point, i.e. for each customer the output of this customer, will be the neuron that is closest to the customer. So basically in the network we pick the neuron, that is closest to the customer. And this neuron is called the winning note for each customer. The winning node is the most similar neuron to the customer. Then we use a neighbourhood function like Gaussian Neighbourhood function, to update the weights of the neighbours of the node, to move them closer to the point. And we do this for all customers in the input space, and we repeat that again. We repeat this many times. And each time we repeat it, the output space decreases and loses dimensions. It reduces its dimensions little by little, and then it reaches the point, where the neighbourhood stops decreasing, where the ouput space starts decreasing. And that's the moment when we obtain our SOM in 2 dimensions, with all the winning nodes, that were eventually identified. 

# And so now we are getting closer to the frauds, because when we think about frauds, we think about outliers, because fraud is something, that far away from general rules, the rules that must be respected when applied to the credit card. So frauds are actually outliers, in this 2D SOM, simply because the outlier neurons are far from majority of neurons that follow the rules. So how to detect outliers in a SOM? for this we use MIT: Mean Interneuron Distance. That means, in our SOM, for each neuron, we rae going to compute the mean of the Eucledian Distance, between this neuron, and the neurons in the neighbourhood, which we have to define manually. So, we can compute the Eucledian distance between this neuron, and all the other neurons in the neighbourhood. That information on the SOM, will allow us to detect outliers i.e. frauds. Then we will be using an inverse mapping function, to identify which customers in the input space are associated with this winning node, that is an outlier. 

X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# Feature Scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
X = sc.fit_transform(X)

# Training the SOM
from minisom import MiniSom
som = MiniSom(x = 10, y = 10, input_len = 15, sigma = 1.0, learning_rate = 0.5)
som.random_weights_init(X)
som.train_random(data = X, num_iteration = 100)

# Higher the learning_rate, higher the convergence


# Visualizing the results
from pylab import bone, pcolor, colorbar, plot, show
bone()
pcolor(som.distance_map().T)
colorbar()
markers = ['o', 's']
colors = ['r', 'g']
for i, x in enumerate(X):
    w = som.winner(x)
    plot(w[0] + 0.5,
         w[1] + 0.5,
         markers[y[i]],
         markeredgecolor = colors[y[i]],
         markerfacecolor = 'None',
         markersize = 10,
         markeredgewidth = 2)
show()

# Finding the frauds
mappings = som.win_map(X)
frauds = np.concatenate((mappings[(8,1)], mappings[(6,8)]), axis = 0)
frauds = sc.inverse_transform(frauds)

























    

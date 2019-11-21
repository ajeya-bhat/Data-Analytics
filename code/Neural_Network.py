#Importing required libraries
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from keras.optimizers import SGD
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler,scale
from keras.layers.advanced_activations import LeakyReLU
import numpy as np

def combined_position(x):
    #Combining the similar Position Players under a single name for simplicity
    if x in ['ST','LW','RW','CF','RF','LF','RS','LS']: #All the forward positions.
        return 'Forward'
    elif x in ['CM','LM','LDM','RM','CDM','CAM','RDM','LAM','RAM','LCM','RCM']: #All midfield positions.
        return 'Midfielder'
    elif x in ['LCB','RCB','LWB','RWB','LB','CB','RB']: # All defending positions
        return 'Defender'
    elif x in ['GK']: #All goalkeepers
        return 'GoalKeeper'

#This function is used to aggregate the values of the columns which have the values improved or declined from the previous values
#denoted by value and + or - symbol with the change in the value.
def aggregate(x):
    if '+' in str(x):
        v1,v2 = x.split('+')
        if(len(v1) > 2):
            return 0
        if(len(v2) > 2):
            return v1
        v1 = int(v1)
        v2 = int(v2)
        return str(v1+v2)
    elif '-' in str(x):
        v1,v2 = x.split('-')
        if(len(v1) > 2):
            return 0
        if(len(v2) > 2):
            return v1
        v1 = int(v1) 
        v2 = int(v2)
        return str(v1+v2)
    return x

#This function is used to preprocess the data.
def preprocessing(data):
    
    removing_list = list(range(54,70))+list(range(75,104)) #list unwanted features from the data
    data.drop(data.columns[removing_list], axis = 1, inplace = True) #Removing the unwanted features.
    data.drop(['sofifa_id','short_name','nationality','player_url','dob','real_face','player_traits',
                'long_name','club','player_tags','body_type','wage_eur','team_jersey_number',
                'loaned_from','joined','contract_valid_until','nation_position','nation_jersey_number',
                'attacking_heading_accuracy','attacking_short_passing','work_rate','attacking_volleys','skill_fk_accuracy'
                ,'skill_curve','weak_foot','team_position'],inplace = True,axis = 1) 
    updating_list = ['attacking_crossing','attacking_finishing','skill_dribbling',
    'skill_long_passing','skill_ball_control','defending_marking','defending_sliding_tackle','defending_standing_tackle',
    'goalkeeping_handling','goalkeeping_diving']
    for i in updating_list:
        data[i] = data[i].map(aggregate)
    data[data['value_eur'] >= 0]
    data['player_positions'] = data['player_positions'].map(lambda x: x.split(',')[0] if ',' in x else x)
    data['player_positions'] = data['player_positions'].map(combined_position)
    data.fillna(0)

    data = pd.get_dummies(data, columns=['player_positions','preferred_foot'])
    return data


#Loading the year wise dataset
data_16 = pd.read_csv('fifa-20-complete-player-dataset/players_16.csv')
data_17 = pd.read_csv('fifa-20-complete-player-dataset/players_17.csv')
data_18 = pd.read_csv('fifa-20-complete-player-dataset/players_18.csv')
data_19 = pd.read_csv('fifa-20-complete-player-dataset/players_19.csv')
test_data = pd.read_csv('fifa-20-complete-player-dataset/players_20.csv')

#Considering the data from 2016-19 as traindata and 2020 as the test data
train_data = pd.concat([data_16,data_17,data_18,data_19], axis=0)
#Preprocessing both train and test data
train_data = preprocessing(train_data)
test_data = preprocessing(test_data)
#Removing the target variable from the training and testing feature values
X_train = train_data.drop('value_eur',axis = 1) # end index is exclusive
X_test = test_data.drop('value_eur',axis = 1)
#Factoring the target values in the order of million eur.
y_train = train_data['value_eur']/1000000
y_test = test_data['value_eur']/1000000
#Filling the NA values with 0s
X_train = pd.DataFrame(X_train).fillna(0)
X_test = pd.DataFrame(X_test).fillna(0)

#Defining a Neural Network Model with Various Hidden Layers
def model():
    model = Sequential()
    model.add(Dense(128,input_dim = 36,activation = 'relu'))
    model.add(Dense(256,activation = 'relu'))
    model.add(Dense(512,activation = 'relu'))
    model.add(Dense(256,activation = 'relu'))
    model.add(Dense(1,activation='linear'))
    model.compile(loss='mean_squared_error',optimizer='adam',metrics=['mse'])
    return model

#Creating the neural network model instance and training on the train dataset and validating it on test data for n number of epochs
neural_net = model()
neural_net.fit(X_train,y_train,validation_data = (X_test,y_test),epochs = 10,verbose = 2)
_, train_mse = neural_net.evaluate(X_train,y_train, verbose=0)
_, test_mse = neural_net.evaluate(X_test,y_test, verbose=0)
#Printing the train and test mean squared error.
print(train_mse,test_mse)


# Data-Analytics Project
## Football player market value predictor and fantasy team recommender
Football is the most popular sport in the world, and thus there is no surprise that footballers earn a lot of money. The market value of the ones at the pinnacle hold a huge market value.<br>
With all teams not having a big budget, the ones with a smaller budget have to manage the finances and also should ensure the best team possible with those finances.<br>
### The aim of this project is to:
* Predict the market value of footballers given various attributes of them like age, team, overall rating and their market value from the years
before.
* Given the money allotted to buy players, recommend the best possible team .

<br>
The data used is the fifa dataset from the years 2015 to 2020 , courtesy Kaggle.
<br>
The following data preprocessing has been doene:

* The numerous positions which a player might play in is changed to just his best position, for easier computation.
* The columns which have gk attributes have been set to NULL for players who are not goalkeepers, and the attributes which do not matter for a goalkeeper have been set to  NULL for players who are not goalkeepers.
* The data which initially has 104 columns is brought down to 65 columns, as the attributes of the players' weak positions would not be of any use to predict his market value . (This might change in the future, as while making the best team, some players 'might' fall out of their favourite position.).
* The players are grouped into continents based on the nationality , as the region in general, rather than nationality has a higher influence on a footballer.
* The players are grouped into 4 categories: forwards, midfielders, backs, and goalkeepers , based on their best position. <br>
Care is taken for the above changes to the dataset such that when a new column is created ,the actual data is not lost.<br><br>

OLS is used which gives a general idea as to what features are significant.<br>
Data transformation is done such that residuals do not follow any pattern.<br>
An adjusted R<sup>2</sup> of 0.97 is obtained, which leads to the initial belief that there is overfitting in this model.<br>

### What we plan to do in the future:

* Try other models which might provide a better result in predicting the market value, like, PCR,Ridge and Lasso Regression, ANN, etc.
* Recommend the best team with the funds available using techniques like collaborative filtering.



# NBA-Season-Data-Analysis
Exploring Scipy for NBA Analysis

# Project Overview 
This project analyzes NBA player statistics, focusing on three-point accuracy across multiple seasons. It utilizes data from the players_stats_by_season_full_details.csv file, and performs various analyses such as determining the player with the most regular seasons, calculating three-point accuracy for each season, performing linear regression, and more. The results are printed either to a file or displayed in the terminal, based on user preference. Important: Please note that if you choose to print to a file, the code will not finish running until you close the linear regression graph.

# Design 
1)  Data loading and Filtering 
- Data set is loaded into pandas dataframe
- Data is then filtered by NBA regular season statistics
2) Indentifiy player
- groups the data by player then counts numbers of unique seasons
- identifies player with the highest number of seasons 





# Methods and Attributes 
- DataFrame
- Linear Regression
- plot ()
- print_output()

# Limitations 
- Its dependent on the user
- The user is required to make a choice whether to print the results in the terminal or a file
- The script will keep promting the user to make a decision till its made vaild 

# Future Improvments 
- Perfomance enhancements:  Since the dataset is larger the code takes a long time to run
- More Analysis could be done to include multiple players instead of just one
- More Visualizations could be added to demonstrate the data more visuabily 

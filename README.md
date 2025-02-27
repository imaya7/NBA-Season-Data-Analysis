# NBA-Season-Data-Analysis
Exploring Scipy Python library for NBA Analysis

# Project Overview 
This project analyzes NBA player statistics, focusing on three-point accuracy across multiple seasons. It utilizes data from the players_stats_by_season_full_details.csv file and performs various analyses such as determining the player with the most regular seasons, calculating three-point accuracy for each season, performing linear regression, and more. The results are printed either to a file or displayed in the terminal, based on user preference. Important: Please note that if you choose to print to a file, the code will not finish running until you close the linear regression graph.


# Files 
- 3p_accuracy_plot.png example graph
- output.txt example output
- players_stats_by_season_full_details.csv file from Kaggle Here is the link to learn more about the CSV file https://www.kaggle.com/datasets/jacobbaruch/basketball-players-stats-per-season-49-leagues
- NBA Copilot chat - documented help from the copilot
- ScipyAssignment1 -python code contains analysis
- ScipyAssignment - empty file  

# Librarys
-pandas as pd 
-numpy as np
-os module 
-scipy import stats, integrate, optimize 
-matplotlib.pyplot as plt 


# Code Explanation
The code starts by importing necessary libraries and setting the file path for the dataset. It loads the dataset using pandas and filters it to include only NBA regular season data. The player who has played the most regular seasons is identified by grouping the data by Player and counting the number of unique seasons. The user is prompted to choose whether the output should be printed to a file or the terminal. The dataset is then filtered to include only the data for the identified player and three-point accuracy for each season is calculated. Linear regression is performed using Scipy's optimize.curve_fit to find the line of best fit for three-point accuracy over the years. The code calculates the average predicted three-point accuracy using numerical integration and compares it to the actual average accuracy. Statistical measures for the 'FGM' and 'FGA' columns are calculated, and t-tests are performed to compare these columns. Finally, a scatter plot with the line of best fit is created, saved as an image, and displayed. The code includes error handling for potential issues such as file not found, empty CSV file, malformed CSV file, and other unexpected errors.


# Class Attributes
- filePath: Stores the path to the CSV file containing player statistics.
- League: Column in the DataFrame representing the league (e.g., NBA).
- Stage: Column in the DataFrame representing the stage of the season (e.g., Regular_Season)
- Player: Column in the DataFrame representing player names.
- Season: Column in the DataFrame representing the season years.
  
# Methods 
- pd.read_csv: Load dataset
- os.path.join: Path concatenation
- os.path.dirname: Directory path
- df.groupby: Group data
- df.copy: Copy DataFrame
- df.sort_values: Sort data
- optimize.curve_fit: Linear regression
- integrate.trapz: Numerical integration
- stats.ttest_rel: Paired t-test
- plt.scatter: Scatter plot
- plt.plot: Line plot
- plt.savefig: Save plot
- plt.show: Display plot
- input: User input
- print: Output text

 

# Limitations 
- User Dependency: The script requires user input to decide whether to print the results in the terminal or a file
- Repeated Prompting: The script will continuously prompt the user until a valid choice is made

# Future Improvements 
- Optimize the code to handle larger datasets more efficiently to reduce runtime
- Add more visualizations to illustrate the data and findings better
- Add interactive plots to allow users to explore the data more 

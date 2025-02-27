import pandas as pd
import numpy as np
import os
from scipy import stats, integrate, optimize
import matplotlib.pyplot as plt

try:
    # Set file path using the current directory
    filePath = os.path.join(os.path.dirname(__file__), 'players_stats_by_season_full_details.csv')

    # Load the dataset
    df = pd.read_csv(filePath)

    # 0. Filter for NBA regular season data
    nbaRegularSeason = df[(df['League'] == 'NBA') & (df['Stage'] == 'Regular_Season')]

    # 1. Determine the player who has played the most regular seasons
    playerSeasons = nbaRegularSeason.groupby('Player')['Season'].nunique()
    mostSeasonsPlayer = playerSeasons.idxmax()

    # Ask the user if they want the output printed to a file or the terminal
    while True:
        outputChoice = input("Do you want the output printed to a file or the terminal? (file/terminal): ").strip().lower()
        if outputChoice in ['file', 'terminal']:
            break
        else:
            print("Error: Please enter 'file' or 'terminal' for output.")

    if outputChoice == 'file':
        outputFile = open('output.txt', 'w')
        def printOutput(*args, **kwargs):
            print(*args, **kwargs, file=outputFile)
    else:
        def printOutput(*args, **kwargs):
            print(*args, **kwargs)

    # Redirect print statements based on user choice
    printOutput(f"\n1. Player with most regular seasons: {mostSeasonsPlayer}")

    # Filter data for this player
    playerData = nbaRegularSeason[nbaRegularSeason['Player'] == mostSeasonsPlayer].copy()

    # 2. Calculate three-point accuracy for each season
    playerData.loc[:, '3pAccuracy'] = playerData['3PM'] / playerData['3PA']

    # Extract year from Season for proper ordering and analysis
    playerData.loc[:, 'year'] = playerData['Season'].apply(lambda x: int(x.split(' - ')[0]))

    # Sort data by year for proper analysis
    playerData = playerData.sort_values('year')

    # Display 3P accuracy for each season
    printOutput("\n2. 3-Point Accuracy by Season:")
    seasonAccuracy = playerData[['Season', 'year', '3pAccuracy']].sort_values('year')
    printOutput(seasonAccuracy.to_string(index=False))

    # 3. Perform linear regression for three-point accuracy across the years played
    X = playerData['year'].values
    y = playerData['3pAccuracy'].fillna(0).values

    # Use scipy's optimize.curve_fit for linear regression
    def linear_model(x, a, b):
        return a * x + b

    params, _ = optimize.curve_fit(linear_model, X, y)
    slope, intercept = params

    printOutput(f"\n3. Linear Regression Analysis:")
    printOutput(f"Line of Best Fit Equation: 3P Accuracy = {slope:.12f} × Year + {intercept:.12f}")

    # Calculate R-squared
    residuals = y - linear_model(X, slope, intercept)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r_squared = 1 - (ss_res / ss_tot)
    printOutput(f"R-squared: {r_squared:.12f}")

    # Add predicted values to dataframe
    playerData.loc[:, '3pAccuracyPred'] = linear_model(X, slope, intercept)

    # 4. Calculate the average three-point accuracy by integrating the fit line
    firstSeason = playerData['year'].min()
    lastSeason = playerData['year'].max()
    seasonsRange = np.arange(firstSeason, lastSeason + 1)
    predictedAccuracies = linear_model(seasonsRange, slope, intercept)

    # Integrate using the trapezoidal rule
    averagePredictedAccuracy = integrate.trapz(predictedAccuracies, seasonsRange) / (lastSeason - firstSeason)

    # Alternatively, calculate average directly using the regression equation (analytical integration)
    analyticalAverage = slope * (lastSeason + firstSeason) / 2 + intercept

    # Compare to actual average three-point accuracy
    actualAverageAccuracy = playerData['3pAccuracy'].mean()

    printOutput(f"\n4. Average 3P Accuracy Analysis:")
    printOutput(f"Average predicted 3P accuracy (from numerical integration): {averagePredictedAccuracy:.12f}")
    printOutput(f"Average predicted 3P accuracy (from analytical integration): {analyticalAverage:.12f}")
    printOutput(f"Actual average 3P accuracy: {actualAverageAccuracy:.12f}")
    printOutput(f"Difference (numerical vs actual): {abs(averagePredictedAccuracy - actualAverageAccuracy):.12f}")
    printOutput(f"Difference (analytical vs actual): {abs(analyticalAverage - actualAverageAccuracy):.12f}")

    # 5. Interpolate missing values for 2002-2003 and 2015-2016 seasons
    missingSeasons = [2002, 2015]
    interpolatedValues = linear_model(np.array(missingSeasons), slope, intercept)

    printOutput(f"\n5. Interpolated 3P accuracy for missing seasons:")
    for season, value in zip(missingSeasons, interpolatedValues):
        # Calculate interpolated value using the line equation directly
        directInterpolation = slope * season + intercept
        printOutput(f"Season {season}-{season+1}: {value:.12f} (Using model.predict)")
        printOutput(f"Season {season}-{season+1}: {directInterpolation:.12f} (Using line equation directly)")

    # 6. Statistical analysis
    printOutput("\n6. Statistical Analysis:")
    printOutput(" Statistical measures for FGM and FGA columns:")

    # Calculate statistical measures for FGM and FGA columns
    fgmStats = playerData['FGM'].agg(['mean', 'var', 'skew', 'kurtosis']).rename_axis('Statistic')
    fgaStats = playerData['FGA'].agg(['mean', 'var', 'skew', 'kurtosis']).rename_axis('Statistic')

    # Combine stats for comparison
    statsComparison = pd.DataFrame({
        'FGM': fgmStats,
        'FGA': fgaStats
    })

    # Print to file or terminal
    printOutput(statsComparison)

    # Compare the statistics from the FGM and FGA columns
    printOutput("\nComparison of FGM and FGA statistics:")
    printOutput(f"Mean difference: {fgmStats['mean'] - fgaStats['mean']:.12f}")
    printOutput(f"Variance difference: {fgmStats['var'] - fgaStats['var']:.12f}")
    printOutput(f"Skewness difference: {fgmStats['skew'] - fgaStats['skew']:.12f}")
    printOutput(f"Kurtosis difference: {fgmStats['kurtosis'] - fgaStats['kurtosis']:.12f}")

    # 7 Perform t-tests
    printOutput("\n7. T-test Analysis:")

    # Perform relational t-test on FGM and FGA columns
    relationalTTest = stats.ttest_rel(playerData['FGM'], playerData['FGA'])

    # Perform individual t-tests on FGM and FGA columns
    fgmTTest = stats.ttest_1samp(playerData['FGM'], 0)
    fgaTTest = stats.ttest_1samp(playerData['FGA'], 0)

    printOutput(f"Relational t-test (FGM vs FGA): t-statistic = {relationalTTest.statistic:.12f}, p-value = {relationalTTest.pvalue:.12f}")
    printOutput(f"FGM individual t-test: t-statistic = {fgmTTest.statistic:.12f}, p-value = {fgmTTest.pvalue:.12f}")
    printOutput(f"FGA individual t-test: t-statistic = {fgaTTest.statistic:.12f}, p-value = {fgaTTest.pvalue:.12f}")

    # In-depth comparison of t-test results
    printOutput("\nIn-depth Comparison of T-test Results:")
    printOutput("The relational t-test compares the means of the FGM and FGA columns directly, taking into account the paired nature of the data.")
    printOutput("The individual t-tests compare each column against a hypothesized mean of 0, without considering the relationship between the columns.")
    printOutput(f"Relational t-test p-value: {relationalTTest.pvalue:.12f}")
    printOutput(f"FGM individual t-test p-value: {fgmTTest.pvalue:.12f}")
    printOutput(f"FGA individual t-test p-value: {fgaTTest.pvalue:.12f}")
    printOutput("A lower p-value in the relational t-test indicates a significant difference between the FGM and FGA columns,")
    printOutput("while the individual t-tests indicate whether each column's mean is significantly different from 0.")

    # Create a scatter plot with line of best fit
    plt.figure(figsize=(10, 6))
    plt.scatter(playerData['year'], playerData['3pAccuracy'], color='blue', label='Actual Accuracy')

    # Generate evenly spaced years for a smoother line plot
    yearMin = playerData['year'].min()
    yearMax = playerData['year'].max()
    yearLine = np.linspace(yearMin, yearMax, 100)
    accuracyLine = linear_model(yearLine, slope, intercept)

    # Plot the line of best fit
    plt.plot(yearLine, accuracyLine, color='red', label=f'y = {slope:.12f}x + {intercept:.12f}')

    plt.xlabel('Season (Year)')
    plt.ylabel('3P Accuracy')
    plt.title(f'Three-Point Accuracy Over Seasons for {mostSeasonsPlayer}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('3p_accuracy_plot.png')  # Save the plot as an image
    plt.show()

    if outputChoice == 'file':
        outputFile.close()

except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure the file path is correct.")
except pd.errors.EmptyDataError:
    print("Error: The CSV file is empty.")
except pd.errors.ParserError:
    print("Error: The CSV file is malformed.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

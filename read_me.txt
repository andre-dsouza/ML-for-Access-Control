Prediction and Anomaly Detection for Enterprise Access Control

Credit to Benjamin Solecki for ensemble.py used for prediction
https://github.com/bensolucky/Amazon


STEPS TO RUN


DATA CLEANING

output.xml is raw MS Access Output

parser.py converts output.xml to a dataframe: cleaned.csv

counts_and_usage_generator.py converts cleaned.csv to newcounts.csv with value counts and resource usage percentages

output.xml -> cleaned.csv -> newcounts.csv



ANOMALY DETECTION

anomalies.ipynb can be used to reproduce graphs, detected outliers, and results


outlier score results go to csv in data_ouputs folder

All_Outputs contains all 7 classifiers tested, including unsuitable ones
Good_Outputs contains results from using Isolation Forest, CBLOF and HBOS
use the legend in these folders to match the outlier results to each classifier

graphs contains resource usage feature pairings for Isolation Forest, CBLOF and HBOS

unsuitable_graphs visualize four unsuitable models tested



ACTIONABLE REVIEW DATA

data_with_outlier_score.csv contains Outlier Score (out of 63) for each of 66.3k rows, along with same data from newcounts.csv

can sort and review by descending outlier score to check if outliers are valid

Filtering for scores greater than 16 corresponds to ~ 3k outliers for employee resource pairings (5% of dataset), composed of 144 employees for review (out of 956)

can filter newcounts.csv on dn value counts to find employees with excess access, average employee can access 68 resources but some up to 260

can filter newcounts.csv on manager value counts to find managers with high occurrences, check if overly lenient when approvang





PREDICTION FOLDER

synthetic_rows.ipynb uses newcounts.csv to synthesize 4k resource denial rows, and creates training and testing sets

counts_and_usage_generator.py should be rerun on training and testing data to produce value counts and resource usage percentages

can use ensemble.py to generate prediction results, but do not assume significance, must test on unsynthesized dataset and further develop

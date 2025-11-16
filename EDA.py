import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import KNNImputer, IterativeImputer


# ### TODO: College Results CSV.
# cr_csv = pd.read_csv('College Results View 2021 Data Dump for Export.xlsx - College Results View 2021 Data .csv')

# ### All rows have some null values.
# print(len(cr_csv), cr_csv.isna().any(axis=1).sum())

# ### Replace 'NA' with np.nan.
# cr_csv.replace('NA', np.nan, inplace=True)

# ### Count number of nulls. -> Remove columns with 65%+ total nulls & rows with 65%+ total nulls.
# print(cr_csv.isna().sum())
# cr_csv = cr_csv[cr_csv.columns[cr_csv.isna().mean() <= 0.65]]
# cr_csv = cr_csv[cr_csv.isna().mean(axis=1) <= 0.65]
# print(len(cr_csv.columns), len(cr_csv))


# ### Create tabulation file.
# writefile = 'college_results_table.txt'
# open(writefile, 'w').close()

# with open(writefile, 'a') as wf:
#     feature_table = [['Feature', '25th', 'Median', '75th', 'Mean', 'Std']]

#     for col in cr_csv.columns:
#         feature_row = [col]

#         cr_feature = cr_csv[col]
#         cr_feature = cr_feature.dropna().reset_index(drop=True)

#         if cr_feature.dtype == object: continue

#         feature_row.extend([np.percentile(cr_feature, 25), np.percentile(cr_feature, 50), np.percentile(cr_feature, 75),
#                            np.mean(cr_feature), np.std(cr_feature)])

#         feature_table.append(feature_row)

    
#     wf.write(tabulate(feature_table[1:], headers=feature_table[0], tablefmt='fancy_grid'))
#     wf.close()

# cr_csv.to_csv('college_results.csv', index=False)


# # WHEN RUNNING ML, ENSURE TRAIN/TEST SPLITS CREATED PRIOR TO ML, OTHERWISE DATA LEAKAGE. OR IGNORE.
# ### Create ML version of cr_csv w/ imputations. -> Remove columns of type STRING OBJECT.
# cr_ml_csv = cr_csv.select_dtypes(exclude=['object']).drop(columns=['UNIQUE_IDENTIFICATION_NUMBER_OF_THE_INSTITUTION'], axis=1)
# cr_ml_np = KNNImputer(missing_values=np.nan, n_neighbors=7).fit_transform(cr_ml_csv)
# cr_ml_csv.loc[:, :] = cr_ml_np.round(3)
# cr_ml_csv.to_csv('college_results_ml.csv', index=False)



# ### TODO: Affordability Gap CSV.
# ag_csv = pd.read_csv('Affordability Gap Data AY2022-23 2.17.25.xlsx - Affordability_latest_02-17-25 1.csv')

# ### Replace '.' with np.NaN.
# ag_csv.replace('.', np.nan, inplace=True)

# ### Most rows have some null values.
# print(len(ag_csv), ag_csv.isna().any(axis=1).sum())

# ### Filter out rows & columns with excess null values.
# print(ag_csv.isna().sum()[ag_csv.isna().sum() > 0])
# ag_csv = ag_csv.drop(columns=['MSI Type', 'HBCU', 'PBI', 'ANNHI', 'TRIBAL', 'AANAPII', 'HSI', 'NANTI'])

# ### Create tabulation file.
# writefile = 'affordability_gap.txt'
# open(writefile, 'w').close()

# with open(writefile, 'a') as wf:
#     feature_table = [['Feature', '25th', 'Median', '75th', 'Mean', 'Std']]

#     for col in ag_csv.columns:
#         feature_row = [col]

#         cr_feature = ag_csv[col]
#         cr_feature = cr_feature.dropna().reset_index(drop=True)

#         if cr_feature.dtype == object: continue

#         feature_row.extend([np.percentile(cr_feature, 25), np.percentile(cr_feature, 50), np.percentile(cr_feature, 75),
#                            np.mean(cr_feature), np.std(cr_feature)])

#         feature_table.append(feature_row)

    
#     wf.write(tabulate(feature_table[1:], headers=feature_table[0], tablefmt='fancy_grid'))
#     wf.close()

# ag_csv.to_csv('affordability_gap.csv', index=False)

# # WHEN RUNNING ML, ENSURE TRAIN/TEST SPLITS CREATED PRIOR TO ML, OTHERWISE DATA LEAKAGE. OR IGNORE.
# ### Create ML version of cr_csv w/ imputations. -> Remove columns of type STRING OBJECT.
# ag_ml_csv = ag_csv.select_dtypes(exclude=['object'])
# ag_ml_np = KNNImputer(missing_values=np.nan, n_neighbors=7).fit_transform(ag_ml_csv)
# ag_ml_csv.loc[:, :] = ag_ml_np.round(3)
# ag_ml_csv.to_csv('ag_results_ml.csv', index=False)



### Cross-match DataFrames to see how many colleges are found in both sets.
larger_df = pd.read_csv('affordability_gap.csv')
smaller_df = pd.read_csv('college_results.csv')

not_in = 0
for id in smaller_df['UNIQUE_IDENTIFICATION_NUMBER_OF_THE_INSTITUTION'].values:
    if id not in larger_df['Unit ID'].values: not_in += 1
# print(not_in)

### Aggregate the two DataFrames together while removing colleges not in larger_df.
combined = pd.merge(larger_df, smaller_df, left_on='Unit ID', right_on='UNIQUE_IDENTIFICATION_NUMBER_OF_THE_INSTITUTION', how='left')

### Extract critical features.
# Feature Engineering: Avg. Cost of Attendance (CoA In State + CoA OOS) / 2.

# print(combined['Cost of Attendance: Out of State'].isna().sum())
# exit()

# Remove county from recommendation algorithm.
### TODO: ENSURE ALL COLUMNS EXIST IN 'combined' -> adjust to make it exist.
crit_features = ['Institution Name', 'City', 'State Abbreviation', 'Sector Name', 'MSI Status', 'Avg Cost of Attendance', 'Income Earned from Working 10 Hours a Week at State\'s Minimum Wage',
                 'Affordability Gap (net price minus income earned working 10 hrs at min wage)', 'Adjusted Monthly Center-Based Child Care Cost', 'Institution Level', 'Institution Size Category', 
                 'County', 'State Code (FIPS)', 'Latitude', 'Longitude', 'Region #', 'Subregion #', 'Admissions Website', 'Institution Status']
crit_features.extend(['Number of Bachelors Degrees White Total', 'Number of Bachelors Degrees American Indian or Alaska Native Total', 'Number of Bachelor Degrees Asian Total', 'Number of Bachelors Degrees Black of African American Total', 'Number of Bachelors Degrees Latino Total', 'Number of Bachelors Degrees Native Hawaiian or Other Pacific Islander Total', 
                      'Number of Degrees Awarded in Science, Technology, Engineering, and Math', 'Number of Degrees Awarded in Arts and Humanities',
                      'Total Enrollment', 'Bachelor\'s Degree Graduation Rate Within 4 Years - Total', 'Transfer Out Rate', 'Median Earnings of Students Working and Not Enrolled 10 Years After Entry',
                      'Percent of Undergraduates Age 25 and Older'])
# crit_features.extend('Average Cost of Attendance')

combined = combined[crit_features]
print(combined.columns, len(combined.columns))

# combined.to_csv(, index=False)

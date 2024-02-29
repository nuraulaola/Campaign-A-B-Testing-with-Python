# 1. Import Libraries
"""

import pandas as pd # Data manipulation and analysis
import numpy as np # Numerical operations
import matplotlib.pyplot as plt # Data visualization
import seaborn as sns # Data visualization
import plotly.express as px # Data visualization
from plotly.subplots import make_subplots # Data visualization
import plotly.graph_objects as go # Data visualization
import cufflinks as cf # Create interactive plot directly from pandas DataFrames
from scipy import stats # Statistical test and analysis
from scipy.stats import ttest_ind # Statistical test and analysis
from statsmodels.stats.proportion import proportions_ztest # Statistical test and analysis
from sklearn.metrics import confusion_matrix, classification_report # Advanced analysis

"""# 2. Load Datasets

## 2.1 Control Dataset
"""

control_url = 'https://github.com/nuraulaola/Campaign-A-B-Testing-with-Python/raw/main/Datasets/control_group.csv'
control_df = pd.read_csv(control_url, sep = ";")
control_df.head()

control_df.columns

# Clean up column names
control_df.columns = ["campaign_name", "date", "spend_usd", "impressions", "reach", "website_clicks", "searches", "view_content", "add_to_cart", "purchase"]
control_df.head()

"""## 2.2 Test Dataset"""

test_url = 'https://github.com/nuraulaola/Campaign-A-B-Testing-with-Python/raw/main/Datasets/test_group.csv'
test_df = pd.read_csv(test_url, sep = ";")
test_df.head()

test_df.columns

# Clean up column names
test_df.columns = ["campaign_name", "date", "spend_usd", "impressions", "reach", "website_clicks", "searches", "view_content", "add_to_cart", "purchase"]
test_df.head()

"""# 3. Exploratory Data Analysis (EDA) of Each DF

## 3.1 Data Summary

### 3.1.1 Control DF Summary
"""

control_df.info()

# Convert 'date' column to datetime
control_df['date'] = pd.to_datetime(control_df['date'])
control_df.info()

"""### 3.1.2 Test DF Summary"""

test_df.info()

# Convert 'date' column to datetime
test_df['date'] = pd.to_datetime(test_df['date'])
test_df.info()

"""## 3.2 Descriptive Statistics

### 3.2.1 Control DF Descriptive Statistics
"""

control_df.describe()

"""### 3.2.2 Test DF Descriptive Statistics"""

test_df.describe()

"""## 3.3 Check for Missing Values

### 3.3.1 Check for Missing Values in Control DF
"""

control_df.isnull().sum()

# Fill missing values with the mean of column
control_df['impressions'] = control_df['impressions'].fillna(control_df['impressions'].mean())
control_df['reach'] = control_df['reach'].fillna(control_df['reach'].mean())
control_df['website_clicks'] = control_df['website_clicks'].fillna(control_df['website_clicks'].mean())
control_df['searches'] = control_df['searches'].fillna(control_df['searches'].mean())
control_df['view_content'] = control_df['view_content'].fillna(control_df['view_content'].mean())
control_df['add_to_cart'] = control_df['add_to_cart'].fillna(control_df['add_to_cart'].mean())
control_df['purchase'] = control_df['purchase'].fillna(control_df['purchase'].mean())

control_df.head()

"""### 3.3.2 Check for Missing Values in Test DF"""

test_df.isnull().sum()

"""## 3.4 Check for Duplicates

### 3.4.1 Check for Duplicates in Control DF
"""

# Check for duplicates in control_df
controldf_duplicate_rows = control_df[control_df.duplicated()]

# Display duplicate rows
print("Duplicate Rows:")
print(controldf_duplicate_rows)

"""### 3.4.2 Check for Duplicates in Test DF"""

# Check for duplicates in test_df
testdf_duplicate_rows = test_df[test_df.duplicated()]

# Display duplicate rows
print("Duplicate Rows:")
print(testdf_duplicate_rows)

"""# 4. Datasets Merge"""

ab_df = control_df.merge(test_df, how='outer').sort_values(['date']).reset_index(drop=True)
ab_df.head()

ab_df.info()

ab_df.describe()

"""# 5. A/B Testing

## 5.1 Comparison of Key Metrics
"""

campaign_metrics = ab_df.groupby('campaign_name').mean().reset_index()
melted_metrics = pd.melt(campaign_metrics, id_vars='campaign_name', var_name='Metric', value_name='Value')

fig = px.bar(melted_metrics, x='campaign_name', y='Value', color='Metric',
             labels={'Value': 'Mean Value'},
             title='Comparison of Metrics Between Control and Test Campaigns',
             barmode='group')
fig.show()

"""From the plot, it is evident that the test campaign has higher spending than the control campaign, indicating that more financial resources were allocated to the test. This might have resulted in increased website clicks and searches, signifying improved user engagement (despite lower impressions and reach). The differences between the view_content and
add_to_cart metrics suggest variations in user behavior between the campaigns. However, similar purchase metrics indicate that both campaigns had a comparable conversion rate.

## 5.2 Trendline Plots
"""

fig = px.scatter(data_frame=ab_df,
                 x='spend_usd',
                 y='reach',
                 size='impressions',
                 color='campaign_name',
                 trendline='ols')

fig.update_layout(xaxis_title='Spend (USD)',
                  yaxis_title='Reach',
                  title='Trendline of Spend (USD) vs. Reach by Campaign',
                  legend_title='Campaign Name')

fig.show()

"""As expected, allocating more budget to a campaign generally enables the campaign to reach a broader audience. The plot reveals a positive correlation between spending and reach. However, the size of the dots, representing the impressions metric, does not appear to exhibit a strong correlation with either spending or reach."""

fig = px.scatter(data_frame=ab_df,
                 x='reach',
                 y='website_clicks',
                 size='impressions',
                 color='campaign_name',
                 trendline='ols')

fig.update_layout(xaxis_title='Reach',
                  yaxis_title='Website Clicks',
                  title='Trendline of Reach vs. Website Clicks by Campaign',
                  legend_title='Campaign Name')

fig.show()

"""Some campaigns exhibit high reach but relatively low website clicks. Additionally, there is one campaign with an exceptionally high number of website clicks relative to its reach."""

fig = px.scatter(data_frame=ab_df,
                 x='website_clicks',
                 y='view_content',
                 color='campaign_name',
                 trendline='ols')

fig.update_layout(xaxis_title='Website Clicks',
                  yaxis_title='View Content',
                  title='Trendline of Website Clicks vs. View Content by Campaign',
                  legend_title='Campaign Name')

fig.show()

"""The Test Campaign has a higher number of website clicks than the Control Campaign. However, the Control Campaign has a higher number of content views. This suggests that the Test Campaign was better at attracting users to the website, but the Control Campaign was better at keeping them engaged once they arrived."""

fig = px.scatter(data_frame=ab_df,
                 x='add_to_cart',
                 y='purchase',
                 color='campaign_name',
                 trendline='ols')

fig.update_layout(xaxis_title='Add to Cart',
                  yaxis_title='Purchase',
                  title='Trendline of Add to Cart vs. Purchase by Campaign',
                  legend_title='Campaign Name')

fig.show()

"""The lines show that there is a positive correlation between adds to carts and purchases for both campaigns. This means that as the number of adds to carts increases, the number of purchases also increases. However, the slope of the line for the "Test Campaign" is steeper than the slope of the line for the "Control Campaign". This means that for every one add to cart in the "Test Campaign", there are more purchases than for every one add to cart in the "Control Campaign". In conclusion, the plot suggests that the "Test Campaign" is more effective at converting adds to carts into purchases than the "Control Campaign".

# 6. Conclusion

While the Test campaign garnered more initial engagement, the Control campaign might have fostered deeper user connection. Ultimately, the "better" campaign depends on the specific marketing goals and priorities. If immediate purchases were the main objective, the Test campaign might be considered more successful. However, if fostering long-term brand engagement and customer loyalty is equally important, the Control campaign might be seen as more valuable.
"""

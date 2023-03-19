# Serverless Bank Dashboard

https://7a2sgjfva5.execute-api.us-east-2.amazonaws.com/dev

<ul>
<li>This dashboard is a user interface that helps visualize the financial health and income of each bank through a myriad of indicators. The indicators consist of individual and combinations of measures for risk profiles,
capital, and assets.</li>
<li>The dashboard uses a Dash app embedded in a Flask server to display longitudinal Federal Financial Institutions Examination Council (FFIEC) data from their Call Reports, which include indicators of the financial health of each bank.</li>
<li>On the dashboard, there are two dropdowns that pass data into the Dash callback function.</li>
<ul><li>The first dropdown lists all of the Regulatory Capital Components and Ratios schedule (RCFA) codes that can be individually selected by the user.
<li>The RCFA codes are enriched with their meaning through correlating data from the data_dict table in the API.</li>
<li>The second dropdown displays the available bank IDs for the selected RCFA code. It is dependent on the first dropdown to avoid errors when a certain bank ID did not report on the specified criteria.</li>
</ul>
<li>The data is reported quarterly, and information for the quarter and year is converted into the date used in the graph through the Python function named update_year.</li>
<li>The Plotly graph illustrates the trends based on the RCFA and bank code chosen.</li>
</ul>

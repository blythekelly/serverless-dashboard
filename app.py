"""
Blythe Kelly
Bank Dashboard for the Data Science for Economics Research Group
https://stackoverflow.com/questions/66845303/deploying-a-plotly-dash-app-to-aws-using-serverless-framework
https://medium.com/swlh/developing-a-serverless-backend-api-using-flask-39398d0eb95d
https://stackoverflow.com/questions/45342990/aws-lambda-error-unzipped-size-must-be-smaller-than-262144000-bytes
https://github.com/serverless/serverless-python-requirements/issues/663
https://github.com/99x/serverless-dynamodb-local/issues/135
https://stackoverflow.com/questions/66845303/deploying-a-plotly-dash-app-to-aws-using-serverless-framework
https://stackoverflow.com/questions/53220719/importerror-no-module-named-dash
https://www.serverless.com/blog/flask-serverless-api-in-aws-lambda-the-easy-way
https://github.com/plotly/dash/issues/22 
"""

from collections import namedtuple
import dash
from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import requests
from dash.dependencies import Input, Output
from flask import Flask
import pkg_resources

_true_get_distribution = pkg_resources.get_distribution
_Dist = namedtuple('_Dist', ['version'])

def _get_distribution(dist):
    if dist == 'flask-compress':
        return _Dist('1.9.0') 
    else:
        return _true_get_distribution(dist)

pkg_resources.get_distribution = _get_distribution

server = Flask(__name__)

app = dash.Dash(__name__,
                server=server,
                routes_pathname_prefix='/',
                requests_pathname_prefix='/dev/'
                )

base_url = "https://4yjz4qhd61.execute-api.us-east-2.amazonaws.com/dev"
data_dict=requests.get("https://4yjz4qhd61.execute-api.us-east-2.amazonaws.com/dev/single/data_dict").json()

#Creating a list of the keys to use in dropdown options
key_list=[]
for i in range(len(data_dict)):
    if data_dict[i]["meaning"] not in key_list:
        key_list.append(data_dict[i]["meaning"].title()+" ("+data_dict[i]["item_code"]+")")

specific_key_bid_list=[]

#Dash app layout with some style formatting
app.layout = html.Div(id = 'parent', style={'color': '#FFFFFF', 'font-family':'Arial'}, children = [
        html.H1(id = 'H1', 
        children = 'Bank Dashboard', 
        style = {'textAlign':'center'}),

        dcc.Dropdown( id = 'dropdown_key',
        options = key_list,
        value = key_list[5]),

        dcc.Dropdown(id = 'dropdown_bank_id',
        options=specific_key_bid_list),

        dcc.Graph(id = 'line_graph',
        className='dcc_compon')
        

    ])

#First callback to output what bank IDs are included in the second dropdown.
@app.callback(Output(component_id='dropdown_bank_id', component_property= 'options'),
            Output(component_id='dropdown_bank_id', component_property= 'value'),
            [Input(component_id='dropdown_key', component_property= 'value')])

def set_bank_id(value):
    key_item_code=value[-9:-1]

    specific_key_list=requests.get(base_url+"/single/"+key_item_code).json()
    for record in specific_key_list:
        if not(record["bank_id"] in specific_key_bid_list):
            specific_key_bid_list.append(record["bank_id"])

    return specific_key_bid_list, specific_key_bid_list[0]
        
#Second callback to output the line graph of the bank's audit values
@app.callback(Output(component_id='line_graph', component_property= 'figure'),
              [Input(component_id='dropdown_key', component_property= 'value')],
              [Input(component_id='dropdown_bank_id', component_property= 'value')])

def new_line_graph(dropdown_value_key, dropdown_value_id):
    key_item_code=dropdown_value_key[-9:-1]
            
    specified_key = requests.get(base_url+"/single/"+key_item_code).json()

    #Creating function to have date included based of quarter system
    bank_data=[]
    def update_year(specified_key):
        for i in range(len(specified_key)):
            if specified_key[i]['bank_id'] == dropdown_value_id:
                if specified_key[i]['quarter']==1:
                    year=specified_key[i]['year']
                    specified_key[i]['year']="March 31, "+str(year)

                if specified_key[i]['quarter']==2:
                    year=specified_key[i]['year']
                    specified_key[i]['year']="June 3, "+str(year)

                if specified_key[i]['quarter']==3:
                    year=specified_key[i]['year']
                    specified_key[i]['year']="September 30, "+str(year)

                if specified_key[i]['quarter']==4:
                    year=specified_key[i]['year']
                    specified_key[i]['year']="December 31, "+str(year)

                bank_data.append(specified_key[i])
        return bank_data

    #Creating a graph with the data selected
    specified_key=update_year(specified_key)
    fig = px.line(specified_key, x='year', y=key_item_code, color='bank_id', 
    title="{} by Bank".format(dropdown_value_key.title()), markers= True, color_discrete_sequence=["#556b2f"])
    
    
    fig.update_layout(title = '{} by Bank'.format(dropdown_value_key.title()),
                    xaxis_title = 'Years',
                    yaxis_title = dropdown_value_key.title(),
                    font_color="white",
                    plot_bgcolor= 'rgba(0, 0, 0, 0)',
                    paper_bgcolor= 'rgba(0, 0, 0, 0)'
                    )
    fig.update_xaxes(showline=True, linewidth=2, linecolor='#556b2f', gridcolor='#1f2c56')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='#556b2f', gridcolor='#1f2c56')
    return fig

    

#Running the Dash app on the port 8052 because the default 8050 is in use. 

def __call__(self, *args, **kwargs):
    return self.server.__call__(*args, **kwargs)

if __name__ == '__main__': 
    server.run(debug=True, port = 8000)

import pandas as pd

# Load data
WORLD_CONFIRMED_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
WORLD_DEATHS_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
WORLD_RECOVERED_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

world_confirmed = pd.read_csv(WORLD_CONFIRMED_URL)
world_deaths = pd.read_csv(WORLD_DEATHS_URL)
world_recovered = pd.read_csv(WORLD_RECOVERED_URL)

sets = [world_confirmed, world_deaths, world_recovered]

# Rename Country/Region and Province/State, and replace NaN's for '' 
for i in range(3):
    sets[i].rename(columns={'Country/Region':'Country', 'Province/State':'State'}, inplace=True)
    sets[i][['State']] = sets[i][['State']].fillna('')
    sets[i].fillna(0, inplace=True)
   
# Group States and sum
sets_grouped = []
cases = ['confirmed cases', 'deaths', 'recovered cases']
for i in range(3):
    sets_grouped.append(sets[i].groupby('Country').sum())


import datetime
# yesterday's date
yesterday = world_confirmed.columns[-1]

def daily(n_top=10):

    # compute daily values for the n_top countries
    sets_grouped_daily = [df.sort_values(by=yesterday, ascending=False).iloc[:n_top, 2:].diff(axis=1).T 
                          for df in sets_grouped]
    
    return sets_grouped_daily

roll = 7

def rolling(n_since=100, roll=roll):

    # transform to rolling average
    dFs = daily()
    
    sets_grouped_daily_top_rolled = []
    for i in range (3): # Transform each dataset at a time
        dF = dFs[i] 
        top_countries = dF.columns
        # get the rolling mean
        dF = dF.rolling(roll).mean()
        # for each column in a DF, get rows >= n_since and reset index
        since = [pd.DataFrame( dF[i][dF[i] >= n_since].reset_index(drop=True) ) for i in top_countries]
        # concatenate the columns
        sets_grouped_daily_top_rolled.append(pd.concat(since, axis=1, join='outer'))

    return sets_grouped_daily_top_rolled
    
#visualization
def bokeh_plot(dataF, cat, n_since, tickers, n_top=10):

    ''' Customizations for the Bokeh plots '''
    # cat = {'confirmed', 'deaths', 'recoveries'}
    # n_since = number of cases since we start counting
    # n_top = number of top countries to show
    # tickers = customized tickers for the logy axis. It is simpler to manually define
        # them than to compute them for each case.
    
from bokeh.io import output_notebook, output_file, show, reset_output
from bokeh.plotting import figure, save
from bokeh.models import ColumnDataSource, NumeralTickFormatter, HoverTool
from bokeh.palettes import Category20

    #Specify the selection tools to be made available
    select_tools = ['box_zoom', 'pan', 'wheel_zoom', 'reset', 'crosshair', 'save']

    # Format the tooltip
    tooltips = [
        ('', '$name'),
        ('Days since', '$x{(0)}'), 
        ('{}'.format(cat), '$y{(0)}')
    ]

    # figure details
    p = figure(y_axis_type="log", plot_width=840, plot_height=600, 
               x_axis_label='Days since average daily {} passed {}'.format(cat, n_since),
               y_axis_label='',
               title=
               'Daily {} ({}-day rolling average) by number of days ' \
               'since {} cases - top {} countries ' \
               '(as of {})'.format(cat, roll, n_since, n_top, yesterday),
               toolbar_location='right',tools=select_tools)

    for i in range(n_top):
        p.line(dataF.index[:], dataF.iloc[:,i], line_width=2, color=Category20[20][i], alpha=0.8, 
               legend_label=dataF.columns[i], name=dataF.columns[i])
        p.circle(dataF.index[:], dataF.iloc[:,i], color=Category20[20][i], fill_color='white',
                 size=3, alpha=0.8, legend_label=dataF.columns[i], name=dataF.columns[i])

    p.yaxis.ticker = tickers

    p.legend.location = 'top_right'
    p.legend.click_policy='hide'

    p.add_tools(HoverTool(tooltips=tooltips))

    output_file('index.html'.format(cat))

    return save(p, 'index.html'.format(cat))
      
yticks = [5,10,20,50,100,200,500,1000,2000]
bokeh_plot(rolling(n_since=3)[1], 'deaths', n_since=3, tickers=yticks)  
import pandas as pd
import plotly.graph_objs as go
import requests
from collections import defaultdict


def sort_date(L):
    splitup = L.split('-')
    return splitup[0], splitup[1], splitup[2]


def return_figures():
    """Creates four plotly visualizations


    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    functions = ['TIME_SERIES_DAILY',
                 'TIME_SERIES_WEEKLY',
                 'TIME_SERIES_MONTHLY',
                 'STOCH',
                 'STOCH',
                 #  'STOCH'
                 ]
    company = 'MSFT'
    outputsize = 'compact'
    key = 'Y30E2S63RTWADYO4'

    return_type = ['Time Series (Daily)',
                   'Weekly Time Series',
                   'Monthly Time Series',
                   'Technical Analysis: STOCH',
                   'Technical Analysis: STOCH',
                   #    'Technical Analysis: STOCH'
                   ]

    data_frames = []
    urls = []

    for i, f in enumerate(functions):
        if i == 0:
            url = 'https://www.alphavantage.co/query?function=' + f +\
                '&symbol=' + company + '&outputsize=' + outputsize +\
                '&apikey=' + key
        elif i == 3:
            url = 'https://www.alphavantage.co/query?function=' + f +\
                '&symbol=' + company + '&interval=daily' +\
                '&apikey=' + key
        elif i == 4:
            url = 'https://www.alphavantage.co/query?function=' + f +\
                '&symbol=' + company + '&interval=weekly' +\
                '&apikey=' + key
        # elif i == 5:
        #     url = 'https://www.alphavantage.co/query?function=' + f +\
        #         '&symbol=' + company + '&interval=monthly' +\
        #         '&apikey=' + key
        else:
            url = 'https://www.alphavantage.co/query?function=' + f +\
                '&symbol=' + company + '&apikey=' + key

        urls.append(url)

        r = requests.get(url)

        data = defaultdict(list)
        if i < 3:
            data[company] = [[], []]
        else:
            data[company] = [[], [[], []]]

        dates = list(r.json()[return_type[i]].keys())[:100]
        dates.sort(key=sort_date)

        for date in dates:
            data[company][0].append(date)
            if i < 3:
                data[company][1].append(float(
                    r.json()[return_type[i]].get(date)['4. close']))
            else:
                data[company][1][0].append(float(
                    r.json()[return_type[i]].get(date)['SlowK']))
                data[company][1][1].append(float(
                    r.json()[return_type[i]].get(date)['SlowD']))

        data_frames.append(data)

    graph_one = []
    df_one = pd.DataFrame(data_frames[0])

    x_val = df_one.iloc[0][0]
    y_val = df_one.iloc[1][0]
    graph_one.append(
      go.Scatter(
          x=x_val,
          y=y_val,
          mode='lines'
      )
    )

    layout_one = dict(title=return_type[0],
                      yaxis=dict(title='Price'),
                      )

    graph_two = []
    df_two = pd.DataFrame(data_frames[1])

    x_val = df_two.iloc[0][0]
    y_val = df_two.iloc[1][0]
    graph_two.append(
      go.Scatter(
          x=x_val,
          y=y_val,
          mode='lines'
      )
    )

    layout_two = dict(title=return_type[1],
                      yaxis=dict(title='Price'),
                      )

    graph_three = []
    df_three = pd.DataFrame(data_frames[2])

    x_val = df_three.iloc[0][0]
    y_val = df_three.iloc[1][0]
    graph_three.append(
      go.Scatter(
          x=x_val,
          y=y_val,
          mode='lines'
      )
    )

    layout_three = dict(title=return_type[2])

    graph_four = []
    df_four = pd.DataFrame(data_frames[3])

    x_val = df_four.iloc[0][0]
    yk_val = df_four.iloc[1][0][0]
    yd_val = df_four.iloc[1][0][1]
    graph_four.append(
      go.Scatter(
          x=x_val,
          y=yk_val,
          mode='lines',
          name='K'
      )
    )
    graph_four.append(
      go.Scatter(
          x=x_val,
          y=yd_val,
          mode='lines',
          name='D'
      )
    )

    layout_four = dict(title='STOCH (daily)')

    graph_five = []
    df_five = pd.DataFrame(data_frames[4])

    x_val = df_five.iloc[0][0]
    yk_val = df_five.iloc[1][0][0]
    yd_val = df_five.iloc[1][0][1]
    graph_five.append(
      go.Scatter(
          x=x_val,
          y=yk_val,
          mode='lines',
          name='K'
      )
    )
    graph_five.append(
      go.Scatter(
          x=x_val,
          y=yd_val,
          mode='lines',
          name='D'
      )
    )

    layout_five = dict(title='STOCH (weekly)')

    # graph_six = []
    # df_six = pd.DataFrame(data_frames[5])

    # x_val = df_six.iloc[0][0]
    # yk_val = df_six.iloc[1][0][0]
    # yd_val = df_six.iloc[1][0][1]
    # graph_six.append(
    #   go.Scatter(
    #       x=x_val,
    #       y=yk_val,
    #       mode='lines',
    #       name='K'
    #   )
    # )
    # graph_six.append(
    #   go.Scatter(
    #       x=x_val,
    #       y=yd_val,
    #       mode='lines',
    #       name='D'
    #   )
    # )

    # layout_six = dict(title='STOCH (monthly)')

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    figures.append(dict(data=graph_five, layout=layout_five))
    # figures.append(dict(data=graph_six, layout=layout_six))

    return figures

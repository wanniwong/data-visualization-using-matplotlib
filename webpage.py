import pandas
import justpy as jp
import matplotlib.pyplot as plt
from pytz import utc
from datetime import datetime

# read data from reviews.csv
data = pandas.read_csv('reviews.csv', parse_dates=['Timestamp'])

# data engineering
total_review = data['Rating'].count()

data['Day'] = data['Timestamp'].dt.date
day_avg = data.groupby(['Day']).count()

data['Week'] = data['Timestamp'].dt.strftime('%Y-%U')
week_avg = data.groupby(['Week']).mean()

data['Month'] = data['Timestamp'].dt.strftime('%Y-%m')
mth_avg = data.groupby(['Month']).mean()

data['Month'] = data['Timestamp'].dt.strftime('%Y-%m')
mth_avg_crs = data.groupby(['Month', 'Course Name']).mean().unstack()

share = data.groupby(['Course Name'])['Rating'].count()

# graph chart definition
spline = """
{
    chart: {
        type: 'spline',
        inverted: false,
        width: 500,
        height: 400
    },
    xAxis: {
        reversed: false,
        title: {
            enabled: true,
            text: 'Date'
        },
        labels: {
            format: '{value}'
        },
        accessibility: {
            rangeDescription: ''
        },
        maxPadding: 0.05,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: 'Average Rating'
        },
        labels: {
            format: '{value}'
        },
        lineWidth: 2
    },
    legend: {
        enabled: false
    },
    tooltip: {
        headerFormat: '<b>{series.name}</b><br/>',
        pointFormat: '{point.x}: {point.y}'
    },
    plotOptions: {
        spline: {
            marker: {
                enable: false
            }
        }
    },
    series: [{
        name: '',
        data: []
    }]
}
"""

areaspline = """
{
    chart: {
        type: 'spline'
    },
    legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'top',
        x: 0,
        y: 120,
        floating: false,
        borderWidth: 1,
        backgroundColor: '#FFFFFF'
    },
    xAxis: {
        title: {
            text: 'Date'
        },
        plotBands: [{
            from: 4.5,
            to: 6.5,
            color: 'rgba(68, 170, 213, .2)'
        }]
    },
    yAxis: {
        title: {
            text: 'Average Rating'
        }
    },
    tooltip: {
        shared: true,
    },
    credits: {
        enabled: false
    },
    plotOptions: {
        areaspline: {
        fillOpacity: 0.5
        }
    },
    series: [{
        name: '',
        data: []
    }]
}
"""

pie = """
{
    chart: {
        type: 'pie'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
            }
        }
    },
    series: [{
        name: '',
        colorByPoint: true,
        data: [{
            name: '',
            y: 61.41,
            sliced: true,
            selected: true
        }]
    }]
}
"""

# create webpage using justpy
def app():
    wp = jp.QuasarPage()
    title = jp.QDiv(a=wp, text='Analysis of Course Review', 
        classes='text-h3 text-weight-bolder text-center q-pa-md')
    title = jp.QDiv(a=wp, text=f'Total number of records: {total_review} reviews', 
        classes='text-h6 text-weight-bold text-italic text-center q-pb-xl')

    # average rating by day
    g1 = jp.HighCharts(a=wp, options=spline, classes='inline-block')
    g1.options.title.text = 'Average Rating by Day'
    g1.options.xAxis.categories = list(day_avg.index)
    g1.options.series[0].data = list(day_avg['Rating'])

    # average rating by week
    g2 = jp.HighCharts(a=wp, options=spline, classes='inline-block')
    g2.options.title.text = 'Average Rating by Week'
    g2.options.xAxis.categories = list(week_avg.index)
    g2.options.series[0].data = list(week_avg['Rating'])

    # average rating by month
    g3 = jp.HighCharts(a=wp, options=spline, classes='inline-block ')
    g3.options.title.text = 'Average Rating by Month'
    g3.options.xAxis.categories = list(mth_avg.index)
    g3.options.series[0].data = list(mth_avg['Rating'])

    # average rating by month by course
    g4 = jp.HighCharts(a=wp, options=areaspline, classes='q-pa-lg')
    g4.options.title.text = 'Average Rating by Month by Course'
    g4.options.xAxis.categories = list(mth_avg_crs.index)
    g4_data = [{'name': v1, 'data': [v2 for v2 in mth_avg_crs[v1]]} for v1 in mth_avg_crs.columns]
    g4.options.series = g4_data

    # number of ratings by course
    c1 = jp.HighCharts(a=wp, options=pie, classes='q-pa-lg')
    c1.options.title.text = 'Number of Ratings by Course'
    c1_data = [{'name':v1, 'y':v2} for v1, v2 in zip(share.index, share)]
    c1.options.series[0].data = c1_data
    
    return wp

jp.justpy(app)
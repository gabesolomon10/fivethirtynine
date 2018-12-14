from __future__ import absolute_import, print_function
from flask import Flask, render_template, request, redirect, flash, url_for
from flaskext.mysql import MySQL

# caching imports
from flask_caching import Cache

# calendar stuff ...
from calendar import Calendar, day_abbr as day_abbrs, month_name as month_names

from bokeh.layouts import gridplot
from bokeh.models import Plot, ColumnDataSource, FactorRange, CategoricalAxis, HoverTool, CategoricalScale, LinearColorMapper
from bokeh.models.glyphs import Text, Rect
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.resources import INLINE
from bokeh.util.browser import view
from bokeh.sampledata.us_holidays import us_holidays

from bokeh.plotting import figure, output_file, show
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

from bokeh.sampledata.iris import flowers
#from bokeh.transform import factor_cmap, factor_mark
from bokeh.transform import linear_cmap
from bokeh.util.hex import hexbin
from bokeh.embed import components

import json
import requests
import pandas as pd
import numpy as np
import time

# word cloud import
from wordcloud import WordCloud

app = Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})
app.secret_key = b'?\x8c\x1eg#/|\x13\xe4\xc8;\xc3\x0e\x13\xe9$'
app.config['MYSQL_DATABASE_HOST'] = 'mysql-instance1.cyxrf7jrt6gm.us-east-2.rds.amazonaws.com'
app.config['MYSQL_DATABASE_USER'] = 'hindesn'
app.config['MYSQL_DATABASE_PASSWORD'] = 'minnie4us'
app.config['MYSQL_DATABASE_DB'] = 'cis550hpps'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql = MySQL()
mysql.init_app(app)

def make_calendar(sp500_data_lst, djia_data_lst, nasdaq_data_lst, twitter_data_lst, holiday_lst, nyt_data_lst, approval_data_lst, generic_dem_lst, generic_rep_lst, plot_wid, plot_ht, year, month, firstweekday="Sun"):
	firstweekday = list(day_abbrs).index(firstweekday)
	calendar = Calendar(firstweekday=firstweekday)

	month_days  = [ None if not day else str(day) for day in calendar.itermonthdays(year, month) ]
	month_weeks = len(month_days)//7

	workday = "linen"
	weekend = "lightsteelblue"

	def weekday(date):
	    return (date.weekday() - firstweekday) % 7

	def pick_weekdays(days):
	    return [ days[i % 7] for i in range(firstweekday, firstweekday+7) ]

	day_names = pick_weekdays(day_abbrs)
	week_days = pick_weekdays([workday]*5 + [weekend]*2)

	source = ColumnDataSource(data=dict(
	    days            = list(day_names)*month_weeks,
	    weeks           = sum([ [str(week)]*7 for week in range(month_weeks) ], []),
	    month_days      = month_days,
	    day_backgrounds = ['white']*len(month_days),
	))

	djia_data = [(dj_date, DJIA) for (dj_date, DJIA) in djia_data_lst if dj_date.year == year and dj_date.month == month]

	nasdaq_data = [(nas_date, NASDAQCOM) for (nas_date, NASDAQCOM) in nasdaq_data_lst if nas_date.year == year and nas_date.month == month]

	sp500_data = [(sp500_date, SP500) for (sp500_date, SP500) in sp500_data_lst if sp500_date.year == year and sp500_date.month == month]

	holidays = [(holiday_date, Holiday) for (holiday_date, Holiday) in holiday_lst if holiday_date.year == year and holiday_date.month == month]

	twitter_data = [(twitter_date, topics) for (twitter_date, topics) in twitter_data_lst if twitter_date.year == year and twitter_date.month == month]

	nyt_data = [(nyt_date, headlines) for (nyt_date, headlines) in nyt_data_lst if nyt_date.year == year and nyt_date.month == month]

	approval_data = [(approval_date, approve_estimate) for (approval_date, approve_estimate) in approval_data_lst if approval_date.year == year and approval_date.month == month]
	approval_data.sort()

	generic_dem = [(generic_date, dem_estimate) for (generic_date, dem_estimate) in generic_dem_lst if generic_date.year == year and generic_date.month == month]
	generic_dem.sort()

	generic_rep = [(generic_date, rep_estimate) for (generic_date, rep_estimate) in generic_rep_lst if generic_date.year == year and generic_date.month == month]
	generic_rep.sort()

	colors_djia = [ DJIA for _, DJIA in djia_data ]
	colors_sp500 = [ SP500 for _, SP500 in sp500_data ]
	colors_nasdaq = [ NASDAQCOM for _, NASDAQCOM in nasdaq_data ]

	for i in range(len(colors_djia)-1):
		avg = np.mean([colors_djia[i], colors_sp500[i], colors_nasdaq[i]])
		
		if 0 < avg <= 11000:
			colors_djia[i] = '#E52700'
		elif 11000 < avg <= 11100:
			colors_djia[i] = '#E33A00'
		elif 11100 < avg <= 11200:
			colors_djia[i] = '#E14C00'
		elif 11200 < avg <= 11300:
			colors_djia[i] = '#DF5E00'
		elif 11300 < avg <= 11400:
			colors_djia[i] = '#DD6F00'
		elif 11400 < avg <= 11500:
			colors_djia[i] = '#DB8000'
		elif 11500 < avg <= 11600:
			colors_djia[i] = '#D99100'
		elif 11600 < avg <= 11700:
			colors_djia[i] = '#D7A100'
		elif 11700 < avg <= 11800:
			colors_djia[i] = '#D5B100'
		elif 11800 < avg <= 11900:
			colors_djia[i] = '#D3C100'
		elif 11900 < avg <= 12000:
			colors_djia[i] = '#D1D000'
		elif 12000 < avg <= 12100:
			colors_djia[i] = '#BECF00'
		elif 12200 < avg <= 12300:
			colors_djia[i] = '#ABCD00'
		elif 12300 < avg <= 12400:
			colors_djia[i] = '#99CB00'
		elif 12400 < avg <= 12500:
			colors_djia[i] = '#87C900'
		elif 12500 < avg <= 12600:
			colors_djia[i] = '#75C700'
		elif 12500 < avg <= 12600:
			colors_djia[i] = '#64C500'
		else:
			colors_djia[i] = '#53C300'

	holiday_source = ColumnDataSource(data=dict(
	    month_djia = [ DJIA for _, DJIA in djia_data ],
	    month_nasdaq = [ NASDAQCOM for _, NASDAQCOM in nasdaq_data ],
	    month_sp500 = [ SP500 for _, SP500 in sp500_data ],
	    month_twitter = [ topics for _, topics in twitter_data ],
		month_holidays = [ Holiday for _, Holiday in holidays ],
		nyt_days  = [ day_names[weekday(nyt_date)] for nyt_date, _ in nyt_data ],
		nyt_weeks = ['0'] + [ str((weekday(nyt_date.replace(day=1)) + nyt_date.day) // 7) for nyt_date, _ in nyt_data ],
		month_nyt = [ headlines for _, headlines in nyt_data ],
		month_approval = [ approve_estimate for _, approve_estimate in approval_data ],
		month_generic_dem = [ dem_estimate for _, dem_estimate in generic_dem ],
		month_generic_rep = [ rep_estimate for _, rep_estimate in generic_rep ],
		day_backgrounds = colors_djia,
	))

	xdr = FactorRange(factors=list(day_names))
	ydr = FactorRange(factors=list(reversed([ str(week) for week in range(month_weeks) ])))
	x_scale, y_scale = CategoricalScale(), CategoricalScale()

	plot = Plot(x_range=xdr, y_range=ydr, x_scale=x_scale, y_scale=y_scale,
	            plot_width=plot_wid, plot_height=plot_ht)
	plot.title.text = month_names[month] + " " + str(year)
	plot.title.text_font_size = "14pt"
	plot.title.text_color = "black"
	plot.title.offset = 25
	plot.min_border_left = 5
	plot.min_border_top= 5
	plot.min_border_bottom= 190
	plot.border_fill_color = "white"
	plot.background_fill_alpha = 0.5
	plot.border_fill_alpha = 0.3

	rect = Rect(x="days", y="weeks", width=0.9, height=0.9, fill_color="day_backgrounds", line_color="silver")
	plot.add_glyph(source, rect)

	rect = Rect(x="nyt_days", y="nyt_weeks", width=0.9, fill_color="day_backgrounds",height=0.9)
	rect_renderer = plot.add_glyph(holiday_source, rect)

	text = Text(x="days", y="weeks", text="month_days", text_align="center", text_baseline="middle")
	plot.add_glyph(source, text)

	xaxis = CategoricalAxis()
	xaxis.major_label_text_font_size = "10pt"
	xaxis.major_label_standoff = 0
	xaxis.major_tick_line_color = None
	xaxis.axis_line_color = None
	plot.add_layout(xaxis, 'above')

	TOOLTIPS = """
	<div style="height:100%; max-width:300px; min-width:200px;background-color: aliceblue; position:relative;">
		<div>
			<span style="font-size: 17px; font-weight: bold;"> Holiday: @month_holidays</span><br>
			<span style="font-size: 15px; font-weight: bold; color: darkgrey;"> Trump Approval Rating: @month_approval{0,0.0}%</span><br>
			<span style="font-size: 15px; font-weight: bold; color: blue;"> Generic Democrat: @month_generic_dem{0,0.0}%</span><br>
			<span style="font-size: 15px; font-weight: bold; color: red;"> Generic Republican: @month_generic_rep{0,0.0}%</span><br>
			<span style="font-size: 17px; font-weight: bold;"> NASDAQ: @month_nasdaq{0,0.00}</span><br>
			<span style="font-size: 17px; font-weight: bold;"> DJIA: @month_djia{0,0.00}</span><br>
			<span style="font-size: 17px; font-weight: bold;">S&P500: @month_sp500{0,0.00}</span><br>
		</div>
		<div>
			<img
			src="/static/img/nyt_logo.png" height="15" width="15"
			style="float: left;"></img>
		</div>
		<div>
			<span style="font-size: 17px; font-weight: bold;">NYT Headlines:</span>
			<span style="font-size: 15px;">@month_nyt</span>
		</div>
		<div>
			<img
			src="/static/img/twitter_logo.png" height="15" width="15"
			style="float: left;"></img>
		</div>
		<div>
			<span style="font-size: 17px; color:blue; font-weight: bold;">Trending Tweets:</span>
			<span style="font-size: 15px; color:blue;">@month_twitter</span>
		</div>
	</div>
	"""

	hover_tool = HoverTool(renderers=[rect_renderer], tooltips=TOOLTIPS)
	# hover_tool = HoverTool(renderers=[rect_renderer], tooltips=[("Holiday", "@month_holidays"),("DJIA", "@month_djia{0,0.00}"),
	# 	("NASDAQ", "@month_nasdaq{0,0.00}"),("S&P500", "@month_sp500{0,0.00}"),("NYT Headlines", "@month_nyt"),("Trending Tweets","@month_twitter")])
	plot.tools.append(hover_tool)

	return plot

@app.route('/', methods=['GET'])
@cache.cached(timeout=50)
def index():
	# get top 5 news articles for the day
	url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'sortBy=popularity&'
       'apiKey=0a342b710f474a4cb3ce82b434f22749')
	articles = requests.get(url).json()["articles"]
	titles = []
	for i in range(10):
		titles.append(articles[i].get("title"))

	return render_template("index.html", response=titles)

@app.route('/about/')
@cache.cached()
def about():
    return render_template('about.html')

#Noah added 11/27; updated 12/5; updated 12/10
@app.route('/keywords/',methods=['GET', 'POST'])
def keywords():
	if request.method == 'POST':

		# user inputs
		search_src = request.form['search_source']
		user_keyword = request.form['user_keyword']

		# DJIA data
		if search_src == "nyt":


			# start query timer
			start_time = time.time()


			cur1 = mysql.get_db().cursor()

			cur1.execute("DROP TABLE IF EXISTS NYT_STUFF");

			cur1.execute("CREATE TEMPORARY TABLE NYT_STUFF as (SELECT date, headline, `sub-headline` FROM cis550hpps.nyt_headlinesv2 WHERE headline like '%s' ORDER BY date DESC LIMIT 20);" %("%" + user_keyword + "%"));

			cur1.execute("SELECT DATE(nyt.date), headline, `sub-headline`,round(t1.approve_estimate  - (SELECT t2.approve_estimate FROM cis550hpps.APPROVAL_TOPLINEv2 t2 WHERE t2.date < t1.date AND t2.subgroup = 'All polls' ORDER BY t2.date DESC LIMIT 1),3) AS DAY_CHANGE_IN_APPROVAL FROM NYT_STUFF nyt LEFT JOIN cis550hpps.APPROVAL_TOPLINEv2 t1 ON nyt.date = t1.date WHERE t1.subgroup = 'All polls' ORDER BY nyt.date desc;");

			rv1 = cur1.fetchall()
			rv_string1 = str(rv1)
			nyt_data = list(rv1)

			cur1.execute("DROP TEMPORARY TABLE NYT_STUFF;");


			cur1.execute("SELECT YEAR (nyt.date), MONTHNAME(nyt.date), count(headline) FROM cis550hpps.nyt_headlinesv2 nyt WHERE headline like '%s' GROUP BY YEAR (nyt.date), MONTH(nyt.date) ORDER BY YEAR (nyt.date) desc, MONTH(nyt.date) desc;"%("%" + user_keyword + "%"));
			rv3 = cur1.fetchall()
			rv_string3 = str(rv3)
			nyt_monthly = list(rv3)

			# end query timer
			query_time = str(round((time.time() - start_time),5))


			return render_template("keywords_result.html", nyt_data = nyt_data, nyt_monthly = nyt_monthly, user_keyword = user_keyword, query_time = query_time)





		if search_src == "twr":

			# start query timer
			start_time = time.time()

			cur1 = mysql.get_db().cursor()

			cur1.execute("DROP TABLE IF EXISTS TWITTER_STUFF");

			cur1.execute("CREATE TEMPORARY TABLE TWITTER_STUFF as(SELECT date, topic FROM cis550hpps.trending_tweetsv2 WHERE topic like '%s'ORDER BY date DESC LIMIT 20);" %("%" + user_keyword + "%"));

			cur1.execute("SELECT DATE(ts.date), ts.topic,round(t1.approve_estimate  - (SELECT t2.approve_estimate FROM cis550hpps.APPROVAL_TOPLINEv2 t2 WHERE t2.date < t1.date AND t2.subgroup = 'All polls'ORDER BY t2.date DESC LIMIT 1),3) AS DAY_CHANGE_IN_APPROVAL FROM TWITTER_STUFF ts LEFT JOIN cis550hpps.APPROVAL_TOPLINEv2 t1 ON ts.date = t1.date WHERE t1.subgroup = 'All polls';");

			rv2 = cur1.fetchall()
			rv_string2 = str(rv2)
			twitter_data = list(rv2)

			cur1.execute("DROP TEMPORARY TABLE TWITTER_STUFF;");

			cur1.execute("SELECT YEAR (twr.date), MONTHNAME(twr.date), count(topic) FROM cis550hpps.trending_tweetsv2 twr WHERE topic like '%s' GROUP BY YEAR (twr.date), MONTH(twr.date) ORDER BY YEAR (twr.date) desc, MONTH(twr.date) desc;"%("%" + user_keyword + "%"));
			rv4 = cur1.fetchall()
			rv_string4 = str(rv4)
			twr_monthly = list(rv4)

			# end query timer
			query_time = str(round((time.time() - start_time),5))


			return render_template("keywords_twitter_result.html", twitter_data = twitter_data, twr_monthly = twr_monthly, user_keyword = user_keyword, query_time = query_time)

	return render_template('keywords.html')


@app.route('/calendar/',methods=['GET'])
@cache.cached()
def calendar():
	if request.method == 'GET':
		# start query timer
		start_time = time.time()

		# djia data
		cur = mysql.get_db().cursor()
		cur.execute("SELECT date AS dj_date, DJIA FROM DJIAv2 WHERE date <> '0000-00-00 00:00:00'");
		rv = cur.fetchall()
		rv_string = str(rv)

		djia_data_lst = list(rv)

		# nasdaq data
		cur2 = mysql.get_db().cursor()
		cur2.execute("SELECT date AS nas_date, NASDAQCOM FROM NASDAQCOMv2 WHERE date <> '0000-00-00 00:00:00'");
		rv2 = cur2.fetchall()
		rv2_string = str(rv2)

		nasdaq_data_lst = list(rv2)

		# sp500 data
		cur3 = mysql.get_db().cursor()
		cur3.execute("SELECT date AS sp500_date, SP500 FROM SP500v2 WHERE date <> '0000-00-00 00:00:00'");
		rv3 = cur3.fetchall()
		rv_string3 = str(rv3)

		sp500_data_lst = list(rv3)

		# twitter data
		cur4 = mysql.get_db().cursor()
		cur4.execute("SELECT date AS twitter_date, JSON_ARRAYAGG(topic) AS topics FROM trending_tweetsv2 GROUP BY date")
		rv4 = cur4.fetchall()
		rv_string4 = str(rv4)

		twitter_data = list(rv4)

		twitter_data_lst = []

		for i in twitter_data:
			topics_lst = i[1]
			topics_lst = topics_lst.split(',')
			topics_lst = topics_lst[:15]
			topics_lst[0] = topics_lst[0][1:]
			twitter_data_lst.append((i[0], topics_lst))

		# holidays
		cur5 = mysql.get_db().cursor()
		cur5.execute("SELECT date AS holiday_date, Holiday FROM CalendarHolidays WHERE date <> '0000-00-00 00:00:00'");
		rv5 = cur5.fetchall()
		rv_string5 = str(rv5)

		holiday_lst = list(rv5)

		# nyt data
		cur6 = mysql.get_db().cursor()
		cur6.execute("SELECT date AS nyt_date, JSON_ARRAYAGG(headline) AS headlines FROM nyt_headlinesv2 GROUP BY date")
		rv6 = cur6.fetchall()
		rv_string6 = str(rv6)

		nyt_data = list(rv6)

		nyt_data_lst = []

		for i in nyt_data:
			headlines = i[1]
			headlines = headlines.split('","')
			headlines[0] = headlines[0][1:]
			headlines[-1] = headlines[-1][:-1]
			nyt_data_lst.append((i[0], headlines))

		# presidential approval rating
		cur7 = mysql.get_db().cursor()
		cur7.execute("SELECT date AS approval_date, approve_estimate FROM APPROVAL_TOPLINEv2 WHERE subgroup='All polls'")
		rv7 = cur7.fetchall()
		rv_string7 = str(rv7)

		approval_data_lst = list(rv7)

		# generic ballot democrat
		cur8 = mysql.get_db().cursor()
		cur8.execute("SELECT date AS generic_date, dem_estimate FROM generic_toplinev2")
		rv8 = cur8.fetchall()
		rv_string8 = str(rv8)

		generic_dem_lst = list(rv8)

		# generic ballot republican
		cur9 = mysql.get_db().cursor()
		cur9.execute("SELECT date AS generic_date, rep_estimate FROM generic_toplinev2")
		rv9 = cur9.fetchall()
		rv_string9 = str(rv9)

		generic_rep_lst = list(rv9)

		# end query timer
		query_time = str(round((time.time() - start_time),5))

		# start page load timer
		start_time = time.time()

		months_2018 = [ [ make_calendar(sp500_data_lst, djia_data_lst, nasdaq_data_lst, twitter_data_lst, holiday_lst, nyt_data_lst, approval_data_lst, generic_dem_lst, generic_rep_lst, 425, 555, 2018, 3*i + j + 1) for j in range(3) ] for i in range(4) ]
		grid_2018 = gridplot(toolbar_location=None, children=months_2018)

		doc = Document()
		doc.add_root(grid_2018)

		script, div = components(grid_2018)

		# get load time 
		load_time = str(round((time.time() - start_time),5))

		return render_template('calendar.html', script=script, div=div, query_time=query_time, load_time=load_time)
	
@app.route('/calendar-month-home/',methods=['GET','POST'])
def dropdown():
	if request.method == 'GET':
		return render_template('calendar-month-home.html')
	elif request.method == 'POST':
		current_month = request.form.get('month-selector')
		return redirect(url_for('calendar_month', current_month=current_month))
	
@app.route('/calendar-month/<current_month>',methods=['GET'])
@cache.cached()
def calendar_month(current_month):
	if request.method == 'GET':
		# start query timer
		start_time = time.time()

		if current_month == 'jan':
			start_date = pd.to_datetime('1/1/2018')
			end_date = pd.to_datetime('1/31/2018')
			month = 1
			current_month = 'January'
		elif current_month == 'feb':
			start_date = pd.to_datetime('2/1/2018')
			end_date = pd.to_datetime('2/28/2018')
			month = 2
			current_month = 'February'
		elif current_month == 'mar':
			start_date = pd.to_datetime('3/1/2018')
			end_date = pd.to_datetime('3/31/2018')
			month = 3
			current_month = 'March'
		elif current_month == 'apr':
			start_date = pd.to_datetime('4/1/2018')
			end_date = pd.to_datetime('4/30/2018')
			month = 4
			current_month = 'April'
		elif current_month == 'may':
			start_date = pd.to_datetime('5/1/2018')
			end_date = pd.to_datetime('5/31/2018')
			month = 5
			current_month = 'May'
		elif current_month == 'jun':
			start_date = pd.to_datetime('6/1/2018')
			end_date = pd.to_datetime('6/30/2018')
			month = 6
			current_month = 'June'
		elif current_month == 'jul':
			start_date = pd.to_datetime('7/1/2018')
			end_date = pd.to_datetime('7/31/2018')
			month = 7
			current_month = 'July'
		elif current_month == 'aug':
			start_date = pd.to_datetime('8/1/2018')
			end_date = pd.to_datetime('8/31/2018')
			month = 8
			current_month = 'August'
		elif current_month == 'sep':
			start_date = pd.to_datetime('9/1/2018')
			end_date = pd.to_datetime('9/30/2018')
			month = 9
			current_month = 'September'
		elif current_month == 'oct':
			start_date = pd.to_datetime('10/1/2018')
			end_date = pd.to_datetime('10/31/2018')
			month = 10
			current_month = 'October'
		elif current_month == 'nov':
			start_date = pd.to_datetime('11/1/2018')
			end_date = pd.to_datetime('11/30/2018')
			month = 11
			current_month = 'November'
		elif current_month == 'dec':
			start_date = pd.to_datetime('12/1/2018')
			end_date = pd.to_datetime('12/31/2018')
			month = 12
			current_month = 'December'

		#DJIA data
		cur = mysql.get_db().cursor()
		cur.execute("SELECT date AS dj_date, DJIA FROM DJIAv2 WHERE date BETWEEN '%s' AND '%s'" %(start_date, end_date));
		rv = cur.fetchall()
		rv_string = str(rv)

		djia_data_lst = list(rv)

		#nasdaq data

		cur2 = mysql.get_db().cursor()
		cur2.execute("SELECT date AS nas_date, NASDAQCOM FROM NASDAQCOMv2 WHERE date BETWEEN '%s' AND '%s'" %(start_date, end_date));
		rv2 = cur2.fetchall()
		rv2_string = str(rv2)

		nasdaq_data_lst = list(rv2)

		#sp500 data

		cur3 = mysql.get_db().cursor()
		cur3.execute("SELECT date AS sp500_date, SP500 FROM SP500v2 WHERE date BETWEEN '%s' AND '%s'" %(start_date, end_date));
		rv3 = cur3.fetchall()
		rv_string3 = str(rv3)

		sp500_data_lst = list(rv3)

		# twitter data

		cur4 = mysql.get_db().cursor()
		cur4.execute("SELECT date AS twitter_date, JSON_ARRAYAGG(topic) AS topics FROM trending_tweetsv2 WHERE date BETWEEN '%s' AND '%s' GROUP BY date" %(start_date, end_date))
		rv4 = cur4.fetchall()
		rv_string4 = str(rv4)

		twitter_data = list(rv4)

		twitter_data_lst = []

		for i in twitter_data:
			topics_lst = i[1]
			topics_lst = topics_lst.split(',')
			topics_lst = topics_lst[:15]
			topics_lst[0] = topics_lst[0][1:]
			twitter_data_lst.append((i[0], topics_lst))

		# holidays
		cur5 = mysql.get_db().cursor()
		cur5.execute("SELECT date AS holiday_date, Holiday FROM CalendarHolidays WHERE date <> '0000-00-00 00:00:00' AND date BETWEEN '%s' AND '%s'" %(start_date, end_date));
		rv5 = cur5.fetchall()
		rv_string5 = str(rv5)

		holiday_lst = list(rv5)

		# nyt data
		cur6 = mysql.get_db().cursor()
		cur6.execute("SELECT date AS nyt_date, JSON_ARRAYAGG(headline) AS headlines FROM nyt_headlinesv2 WHERE date BETWEEN '%s' AND '%s' GROUP BY date" %(start_date, end_date))
		rv6 = cur6.fetchall()
		rv_string6 = str(rv6)

		nyt_data = list(rv6)

		nyt_data_lst = []
		
		for i in nyt_data:
			headlines = i[1]
			headlines = headlines.split('","')
			headlines[0] = headlines[0][1:]
			headlines[-1] = headlines[-1][:-1]
			nyt_data_lst.append((i[0], headlines))

		# presidential approval rating
		cur7 = mysql.get_db().cursor()
		cur7.execute("SELECT date AS approval_date, approve_estimate FROM APPROVAL_TOPLINEv2 WHERE subgroup='All polls' AND date BETWEEN '%s' AND '%s'" %(start_date, end_date))
		rv7 = cur7.fetchall()
		rv_string7 = str(rv7)

		approval_data_lst = list(rv7)

		# generic ballot democrat
		cur8 = mysql.get_db().cursor()
		cur8.execute("SELECT date AS generic_date, dem_estimate FROM generic_toplinev2 WHERE date BETWEEN '%s' AND '%s'" %(start_date, end_date))
		rv8 = cur8.fetchall()
		rv_string8 = str(rv8)

		generic_dem_lst = list(rv8)

		# generic ballot republican
		cur9 = mysql.get_db().cursor()
		cur9.execute("SELECT date AS generic_date, rep_estimate FROM generic_toplinev2 WHERE date BETWEEN '%s' AND '%s'" %(start_date, end_date))
		rv9 = cur9.fetchall()
		rv_string9 = str(rv9)

		generic_rep_lst = list(rv9)

		# end query timer
		query_time = str(round((time.time() - start_time),5))

		# start page load timer
		start_time = time.time()

		months_2018 = make_calendar(sp500_data_lst, djia_data_lst, nasdaq_data_lst, twitter_data_lst, holiday_lst, nyt_data_lst, approval_data_lst, generic_dem_lst, generic_rep_lst, 555, 725, 2018, month)
		
		script, div = components(months_2018)

		# get load time
		load_time = str(round((time.time() - start_time),5))
		
		return render_template('calendar-month.html', script=script, div=div, load_time=load_time, query_time=query_time, current_month=current_month)
	
@app.route('/wordcloud',methods=['GET'])
@cache.cached()
def make_wordcloud():
	if request.method == 'GET':
		# nyt data
		cur = mysql.get_db().cursor()
		cur.execute("SELECT headline FROM nyt_headlines")
		nyt = cur.fetchall()

		# twitter data
		cur4 = mysql.get_db().cursor()
		cur4.execute("SELECT topic FROM trending_tweets")
		twitter = cur4.fetchall()

		text_str = ""
		for entry in nyt:
			text_str = text_str + entry[0] + ' '

		for entry in twitter:
			text_str = text_str + entry[0] + ' '

		# Generate a word cloud image
		wordcloud = WordCloud(width=1300, height=850, margin=10, background_color='white',min_font_size = 30, max_font_size = 120, colormap = 'gist_heat').generate(text_str)
		
		wordcloud.to_file('static/img/new_plot7.png')

		return render_template('test.html')
	
@app.route('/trends', methods=['GET', 'POST'])
def trends():

	if request.method == 'POST':

		# get the dates
		first_date = request.form['first_date']
		second_date = request.form['second_date']

		data_source = request.form['data_selector']

		# check for invalid date formatting
		#if is_invalid(the_date):
			#flash('Invalid date!')
			
			#return redirect(request.url)

		first_date_datetime = pd.to_datetime(first_date)
		second_date_datetime = pd.to_datetime(second_date)

		# month = date_datetime.month
		# day = date_datetime.day
		# year = date_datetime.year

		# start query timer
		start_time = time.time()

		cur = mysql.get_db().cursor()
		cur.execute("SELECT DJIAv2.date AS date, SP500, NASDAQCOM, DJIA, approve_estimate, dem_estimate, rep_estimate\
			FROM DJIAv2 JOIN SP500v2 ON DJIAv2.date = SP500v2.date JOIN NASDAQCOMv2 ON DJIAv2.date = NASDAQCOMv2.date JOIN APPROVAL_TOPLINEv2 ON\
			DJIAv2.date = APPROVAL_TOPLINEv2.date JOIN generic_toplinev2 ON generic_toplinev2.date = DJIAv2.date WHERE APPROVAL_TOPLINEv2.subgroup = 'All polls'\
			AND DJIAv2.date BETWEEN '%s' AND '%s' GROUP BY DJIAv2.date" %(first_date_datetime, second_date_datetime)); 
		rv = cur.fetchall()
		rv_string = str(rv)

		# end query timer
		query_time = str(round((time.time() - start_time),5))

		# start page load timer
		start_time = time.time()




		data = list(rv)

		dates = []
		djia = []
		sp500 = []
		nasdaq = []
		approval = []
		generic_dems = []
		generic_reps = []

		i=0

		while i < len(data):
			dates.append(data[i][0])
			sp500.append(data[i][1])
			nasdaq.append(data[i][2])
			djia.append(data[i][3])
			approval.append(data[i][4])
			generic_dems.append(data[i][5])
			generic_reps.append(data[i][6])
			i += 1

		#Graphing

		#SP500 Graph
		p1 = figure(plot_width=650, plot_height=400, x_axis_type='datetime',title = 'S&P 500 over Time', x_axis_label = 'Date', y_axis_label = 'S&P Points')
		p1.line(dates,sp500,color='blue', line_width=4)

		#NASDAQ Graph
		p2 = figure(plot_width=650, plot_height=400, x_axis_type='datetime',title = 'Nasdaq over Time', x_axis_label = 'Date', y_axis_label = 'Nasdaq Points')
		p2.line(dates,nasdaq,color='green', line_width=4)

		#Dow-Jones Graph
		p3 = figure(plot_width=650, plot_height=400, x_axis_type='datetime',title = 'Dow-Jones over Time', x_axis_label = 'Date', y_axis_label = 'Dow-Jones Points')
		p3.line(dates,djia,color='magenta', line_width=4)

		#Approval Rating Graph
		p4= figure(plot_width=650, plot_height=400, x_axis_type='datetime',title = 'Approval Rating over Time', x_axis_label = 'Date', y_axis_label = 'Percent Approval')
		p4.line(dates,approval,color='orange', line_width=4)

		colors_list = ['blue', 'red']
		legends_list = ['Democrats', 'Republicans']
		xs=[dates, dates]
		ys=[generic_dems, generic_reps]


		p5= figure(plot_width=650, plot_height=400, x_axis_type='datetime',title = 'Generic Ballot over Time', x_axis_label = 'Date', y_axis_label = 'Percent Support')
		
		for (colr, leg, x, y ) in zip(colors_list, legends_list, xs, ys):
			p5.line(x, y, color= colr, legend= leg, line_width=4)
			p5.legend.location = "top_left"
			p5.legend.click_policy="hide"


		#get components
		script_sp, div_sp = components(p1)
		script_nasdaq, div_nasdaq= components(p2)
		script_djia, div_djia = components(p3)
		script_approval, div_approval= components(p4)
		script_generic, div_generic= components(p5)

		# get load time 
		load_time = str(round((time.time() - start_time),5))

		if data_source == "S&P 500":

				return render_template("trends_results.html", script = script_sp , div = div_sp, load_time = load_time, query_time = query_time)

		elif data_source == "Dow-Jones":

				return render_template("trends_results.html", script = script_djia , div = div_djia, load_time = load_time, query_time = query_time)

		elif data_source == "NASDAQ":

				return render_template("trends_results.html", script = script_nasdaq, div = div_nasdaq, load_time = load_time, query_time = query_time)

		elif data_source == "Presidential Approval Rating":

				return render_template("trends_results.html", script = script_approval, div = div_approval, load_time = load_time, query_time = query_time)

		elif data_source == "Generic Ballot":

				return render_template("trends_results.html", script = script_generic, div = div_generic, load_time = load_time, query_time = query_time)


	

	elif request.method == 'GET':

		return render_template("trends.html")


@app.route('/trends_results/',methods=['GET','POST'])
def trends_results():
	if request.method == 'GET':
		return render_template('trends_results.html')
	
@app.route('/presidential_factors', methods=['GET', 'POST'])
def extremes():

	if request.method == 'POST':

		# get the dates
		first_date = request.form['first_date']
		second_date = request.form['second_date']

		#get the type of query: approval or disapproval
		search_type = request.form['approval_or_disapproval']
		
		#adjusting date time formats
		first_date_datetime = pd.to_datetime(first_date)
		second_date_datetime = pd.to_datetime(second_date)

		#defining engine for sql query
		curP = mysql.get_db().cursor()

		#Query scenarios
		if search_type == "approval":
			
			# start query timer
			start_time = time.time()

			#Daily Tweets
			curP.execute("DROP TABLE IF EXISTS daily_tweets;");
			curP.execute("CREATE TEMPORARY TABLE daily_tweets AS (SELECT date, JSON_ARRAYAGG(topic) AS topics FROM trending_tweetsv2 WHERE date > '%s' AND date < '%s' GROUP BY date);" %(first_date_datetime, second_date_datetime));

			#New York Times Headlines
			curP.execute("DROP TABLE IF EXISTS nyt_grouped_headlines;");
			curP.execute("CREATE TEMPORARY TABLE nyt_grouped_headlines AS (SELECT date AS date, JSON_ARRAYAGG(headline) AS headlines FROM nyt_headlinesv2 WHERE date > '%s' AND date < '%s' GROUP BY date);"%(first_date_datetime, second_date_datetime));
		
			#SP500 Daily Changes
			curP.execute("DROP TABLE IF EXISTS SP500_Daily_Changes;");
			curP.execute("CREATE TEMPORARY TABLE SP500_Daily_Changes AS (SELECT sp1.date, sp1.SP500, TRUNCATE(((sp1.SP500 / (SELECT sp2.SP500 FROM cis550hpps.SP500v2 AS sp2 WHERE sp2.date < sp1.date ORDER BY sp2.date DESC LIMIT 1)) - 1)*100, 3) AS DAYLY_PERC_CHANGE_SP500 FROM cis550hpps.SP500v2 AS sp1 WHERE sp1.date > '%s' AND sp1.date < '%s');"%(first_date_datetime, second_date_datetime));
			
			#Query that joins all tables
			curP.execute("SELECT DATE(at.date), TRUNCATE(MAX(at.approve_estimate),2), TRUNCATE(spd.DAYLY_PERC_CHANGE_SP500,2) , dt.topics, nyt.headlines FROM APPROVAL_TOPLINEv2 AS at LEFT JOIN SP500_Daily_Changes AS spd ON at.date = spd.date LEFT JOIN daily_tweets AS dt ON at.date = dt.date LEFT JOIN nyt_grouped_headlines AS nyt ON at.date = nyt.date WHERE at.date > '%s' AND at.date < '%s';" %(first_date_datetime, second_date_datetime));
			rv = curP.fetchall()
			rv_string = str(rv)
			approval_extremes_data = list(rv)
			
			curP.execute("DROP TABLE IF EXISTS daily_tweets;");
			curP.execute("DROP TABLE IF EXISTS nyt_grouped_headlines;");
			curP.execute("DROP TABLE IF EXISTS PA_Changes;");
			curP.execute("DROP TABLE IF EXISTS SP500_Daily_Changes;");
			
			# end query timer
			query_time = str(round((time.time() - start_time),5))
			
			return render_template("approval_factors_result.html", approval_extremes_data = approval_extremes_data, query_time = query_time)

		if search_type == "disapproval":
			
			# start query timer
			start_time = time.time()

			#Daily Tweets
			curP.execute("DROP TABLE IF EXISTS daily_tweets;");
			curP.execute("CREATE TEMPORARY TABLE daily_tweets AS (SELECT date, JSON_ARRAYAGG(topic) AS topics FROM trending_tweetsv2 WHERE date > '%s' AND date < '%s' GROUP BY date);" %(first_date_datetime, second_date_datetime));

			#New York Times Headlines
			curP.execute("DROP TABLE IF EXISTS nyt_grouped_headlines;");
			curP.execute("CREATE TEMPORARY TABLE nyt_grouped_headlines AS (SELECT date AS date, JSON_ARRAYAGG(headline) AS headlines FROM nyt_headlinesv2 WHERE date > '%s' AND date < '%s' GROUP BY date);"%(first_date_datetime, second_date_datetime));
		
			#SP500 Daily Changes
			curP.execute("DROP TABLE IF EXISTS SP500_Daily_Changes;");
			curP.execute("CREATE TEMPORARY TABLE SP500_Daily_Changes AS (SELECT sp1.date, sp1.SP500, TRUNCATE(((sp1.SP500 / (SELECT sp2.SP500 FROM cis550hpps.SP500v2 AS sp2 WHERE sp2.date < sp1.date ORDER BY sp2.date DESC LIMIT 1)) - 1)*100, 3) AS DAYLY_PERC_CHANGE_SP500 FROM cis550hpps.SP500v2 AS sp1 WHERE sp1.date > '%s' AND sp1.date < '%s');"%(first_date_datetime, second_date_datetime));
			
			#Query that joins all tables
			curP.execute("SELECT DATE(at.date), TRUNCATE(MAX(at.disapprove_estimate),2), TRUNCATE(spd.DAYLY_PERC_CHANGE_SP500,2), dt.topics, nyt.headlines FROM APPROVAL_TOPLINEv2 AS at LEFT JOIN SP500_Daily_Changes AS spd ON at.date = spd.date LEFT JOIN daily_tweets AS dt ON at.date = dt.date LEFT JOIN nyt_grouped_headlines AS nyt ON at.date = nyt.date WHERE at.date > '%s' AND at.date < '%s';" %(first_date_datetime, second_date_datetime));
			rv = curP.fetchall()
			rv_string = str(rv)
			disapproval_extremes_data = list(rv)
			
			curP.execute("DROP TABLE IF EXISTS daily_tweets;");
			curP.execute("DROP TABLE IF EXISTS nyt_grouped_headlines;");
			curP.execute("DROP TABLE IF EXISTS PA_Changes;");
			curP.execute("DROP TABLE IF EXISTS SP500_Daily_Changes;");
			
			# end query timer
			query_time = str(round((time.time() - start_time),5))

			return render_template("disapproval_factors_result.html", disapproval_extremes_data = disapproval_extremes_data, query_time = query_time)
		
		if search_type == "top 5":

			# start query timer
			start_time = time.time()
			
			#Presidential Approval Rating Changes
			curP.execute("DROP TABLE IF EXISTS PA_Changes;");
			curP.execute("CREATE TEMPORARY TABLE PA_Changes AS (SELECT t1.date, (((t1.approve_estimate - (SELECT t2.approve_estimate FROM cis550hpps.APPROVAL_TOPLINEv2 AS t2 WHERE t2.date < t1.date AND t2.subgroup = 'All polls' ORDER BY t2.date DESC LIMIT 1)))) AS Day_Change_Approval FROM cis550hpps.APPROVAL_TOPLINEv2 AS t1 WHERE t1.subgroup = 'All polls');");
			
			#Daily Tweets
			curP.execute("DROP TABLE IF EXISTS daily_tweets;");
			curP.execute("CREATE TEMPORARY TABLE daily_tweets AS (SELECT date, JSON_ARRAYAGG(topic) AS topics FROM trending_tweetsv2 WHERE date > '%s' AND date < '%s' GROUP BY date);" %(first_date_datetime, second_date_datetime));

			#New York Times Headlines
			curP.execute("DROP TABLE IF EXISTS nyt_grouped_headlines;");
			curP.execute("CREATE TEMPORARY TABLE nyt_grouped_headlines AS (SELECT date AS date, JSON_ARRAYAGG(headline) AS headlines FROM nyt_headlinesv2 WHERE date > '%s' AND date < '%s' GROUP BY date);"%(first_date_datetime, second_date_datetime));
		
			#SP500 Daily Changes
			curP.execute("DROP TABLE IF EXISTS SP500_Daily_Changes;");
			curP.execute("CREATE TEMPORARY TABLE SP500_Daily_Changes AS (SELECT sp1.date, sp1.SP500, TRUNCATE(((sp1.SP500 / (SELECT sp2.SP500 FROM cis550hpps.SP500v2 AS sp2 WHERE sp2.date < sp1.date ORDER BY sp2.date DESC LIMIT 1)) - 1)*100, 3) AS DAYLY_PERC_CHANGE_SP500 FROM cis550hpps.SP500v2 AS sp1 WHERE sp1.date > '%s' AND sp1.date < '%s');"%(first_date_datetime, second_date_datetime));
			
			#Presidential Approval Rating Changes
			curP.execute("DROP TABLE IF EXISTS PA_Changes;");
			curP.execute("CREATE TEMPORARY TABLE PA_Changes AS (SELECT t1.date, (((t1.approve_estimate - (SELECT t2.approve_estimate FROM cis550hpps.APPROVAL_TOPLINEv2 AS t2 WHERE t2.date < t1.date AND t2.subgroup = 'All polls' ORDER BY t2.date DESC LIMIT 1)))) AS Day_Change_Approval FROM cis550hpps.APPROVAL_TOPLINEv2 AS t1 WHERE t1.subgroup = 'All polls' AND t1.date > '%s' AND t1.date < '%s');" %(first_date_datetime, second_date_datetime));
			
			#Query that joins all tables
			curP.execute("SELECT DATE(pa.date), TRUNCATE(pa.Day_Change_Approval,2), TRUNCATE(spd.DAYLY_PERC_CHANGE_SP500,2), dt.topics, nyt.headlines FROM PA_Changes AS pa LEFT JOIN SP500_Daily_Changes AS spd ON pa.date = spd.date LEFT JOIN daily_tweets AS dt ON pa.date = dt.date LEFT JOIN nyt_grouped_headlines AS nyt ON pa.date = nyt.date WHERE pa.date > '%s' AND pa.date < '%s' ORDER BY ABS(pa.Day_Change_Approval) DESC LIMIT 5;" %(first_date_datetime, second_date_datetime));
			rv = curP.fetchall()
			rv_string = str(rv)
			top5_extremes_data = list(rv)
			
			curP.execute("DROP TABLE IF EXISTS daily_tweets;");
			curP.execute("DROP TABLE IF EXISTS nyt_grouped_headlines;");
			curP.execute("DROP TABLE IF EXISTS PA_Changes;");
			curP.execute("DROP TABLE IF EXISTS SP500_Daily_Changes;");
			
			# end query timer
			query_time = str(round((time.time() - start_time),5))

			return render_template("top5_factors_result.html", top5_extremes_data = top5_extremes_data, query_time = query_time)


	if request.method == 'GET':

		return render_template("presidential_factors.html")

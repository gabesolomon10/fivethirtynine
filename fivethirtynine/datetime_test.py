import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host="mysql-instance1.cyxrf7jrt6gm.us-east-2.rds.amazonaws.com",
  user="hindesn",
  passwd="minnie4us",
  database="cis550hpps"
)

# set the start date
start = datetime.datetime.strptime("2018/10/01", '%Y/%m/%d')

# set the end date
end = datetime.datetime.strptime("2018/10/25", '%Y/%m/%d')

date_range = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

# for i in date_range:
# 	# if i.month < 10 and i.day < 10:
# 	# 	string_date = '0' + str(i.month) + '/0' + str(i.day) + '/' + str(i.year)
# 	# elif i.month < 10:
# 	# 	string_date = '0' + str(i.month) + '/' + str(i.day) + '/' + str(i.year)
# 	# elif i.day < 10:
# 	# 	string_date = str(i.month) + '/0' + str(i.day) + '/' + str(i.year)
# 	# else:
# 	string_date = str(i.month) + '/' + str(i.day) + '/' + str(i.year)
# 	print(string_date)
# 	print(i)

cur = mydb.cursor()

#cur.execute("SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'trending_tweets'");
#cur.execute("SELECT tt.date, SP500, topic FROM trending_tweets tt JOIN SP500 sp ON tt.date = sp.date LIMIT 100")
#cur.execute ("UPDATE APPROVAL_TOPLINE SET modeldate='%s' WHERE modeldate='%s'" %(i, string_date))
#cur.execute("ALTER TABLE APPROVAL_TOPLINE ADD COLUMN date_updated DATETIME NOT NULL;")
#mydb.commit()
#cur.execute("SELECT * FROM APPROVAL_TOPLINE")
cur.execute("DESCRIBE APPROVAL_TOPLINE")
#cur.execute("UPDATE APPROVAL_TOPLINE SET date_updated=modeldate");
#cur.execute("ALTER TABLE nyt_headlines DROP COLUMN \ufeffdate");
#mydb.commit()
#cur.execute("DESCRIBE nyt_headlines")
#cur.execute("ALTER TABLE APPROVAL_TOPLINE RENAME COLUMN date_updated TO date")
#mydb.commit()
rv = cur.fetchall()
rv_string = str(rv)
print(rv_string)
print(cur.rowcount, 'record(s) affected')





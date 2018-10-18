import tweet_database
import read_file
import sqlite3

def vine_mentioned(text):
	mention = 0
	if "vine" in text:
		mention = 1
	return mention

def hq_mentioned(text):
	mention = 0
	if "hqtrivia" in text:
		mention = 1
	return mention

def rt_mentioned(text):
	mention = 0
	if tweet.text[0:4] == "RT @":
		mention = 1
	return mention

def link_mentioned(text):
	mention = 0
	if "/t.co/" in text:
		mention = 1
	return mention

def get_sentiment(text):
	return TextBlob(text).sentiment.polarity

if __name__ == '__main__':
	conn = sqlite3.connect('tweets_info_no_dupes.db')
	c = conn.cursor()

	c.execute("""CREATE TABLE IF NOT EXISTS tweets_info_no_dupes(tweet text, username text,
	 created_at text, followers_count int, tweets_collected int, total_polarity real,
	  average_polarity real, vine_mentions real, hq_mentions real, vine_links_collected real,
	   retweets_collected real)""")
	conn.commit()

	tweets = read_file.collect_tweets(read_file.collect_data('tweets.json'))
	print ("table created")
	for tweet in tweets:
		try:
			c.execute("""SELECT * FROM tweets_info_no_dupes WHERE username = ? AND created_at = ?""",
				(tweet.screen_name, tweet.created_at))
			check_dupes = c.fetchone()

			c.execute("""SELECT * FROM tweets_info_no_dupes WHERE username = ?""",
				(tweet.screen_name))
			check_user = c.fetchone()

			"""
			3 cases: tweet is not a duplicate but the user is in the database
			"""
			if check_dupes != None:
			#case for tweet being a duplicate

			"""
			just move along, don't update any info in database 
			"""
				continue

			elif check_user == None:

				#Create entry for new user
				c.execute("""INSERT INTO tweets_info_no_dupes VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
					(tweet.text, tweet.screen_name, tweet.created_at, tweet.followers_count, 1,
						get_sentiment(tweet.text), get_sentiment(tweet.text), vine_mentioned(tweet.text),
						 hq_mentioned(tweet.text), link_mentioned(tweet.text), rt_mentioned(tweet.text)))
				conn.commit()

			else:
				#user is in database, but this tweet is not a duplicate

				c.execute("""SELECT * FROM tweets_info_no_dupes WHERE 
					username = ?""", (tweet.screen_name))
				data = c.fetchone()

				prev_tweets_collected = data[4]
				prev_total_polarity = data[5]
				prev_avg_polarity = data[6]
				prev_vine_mentions = data[7]
				prev_hq_mentions = data[8]
				prev_links_collected = data[9]
				prev_rts_collected = data[10]


				"""

				TODO: ADD FIELD FOR USER IN UPDATE COMMAND

				"""

				c.excecute("""UPDATE tweets_info_no_dupes SET tweets_collected = ?
				 WHERE tweets_collected = ? AND username = ?""", 
				 (prev_tweets_collected+1, prev_tweets_collected, tweet.screen_name))
				conn.commit()

				c.execute("""UPDATE tweets_info_no_dupes SET total_polarity = ? 
					WHERE total_polarity = ? AND username = ?""", (prev_total_polarity + 
						get_sentiment(tweet.text), prev_total_polarity, tweet.screen_name))
				conn.commit()

				c.execute("""UPDATE tweets_info_no_dupes SET average_polarity = ? 
					WHERE average_polarity = ? AND username = ?""", 
					((prev_average_polarity + get_sentiment(tweet.text))/
					 prev_tweets_collected + 1, prev_average_polarity, tweet.screen_name))
				conn.commit()

				c.execute("""UPDATE tweets_info_no_dupes SET vine_mentions = ? 
					WHERE vine_mentions = ? AND username = ?""", 
					(prev_vine_mentions + vine_mentioned(tweet.text), prev_vine_mentions, 
						tweet.screen_name))
				conn.commit()

				c.execute("""UPDATE tweets_info_no_dupes SET hq_mentions = ? 
					WHERE hq_mentions = ? AND username = ?""", 
					(prev_hq_mentions + hq_mentioned(tweet.text), prev_hq_mentions, 
						tweet.screen_name))
				conn.commit()

				c.execute("""UPDATE tweets_info_no_dupes SET vine_links_collected = ? 
					WHERE vine_links_collected = ? AND username = ?""", (prev_links_collected + 
						link_mentioned(tweet.text), prev_links_collected, tweet.screen_name))
				conn.commit()

				c.execute("""UPDATE tweets_info_no_dupes SET retweets_collected = ? 
					WHERE retweets_collected = ? AND username = ?""", (prev_rts_collected + 
						rt_mentioned(tweet.text), prev_rts_collected, tweet.screen_name))
				conn.commit()

		except:
			continue
			
	c.close()
	conn.close()

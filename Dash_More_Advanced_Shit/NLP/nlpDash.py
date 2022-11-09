from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import tweepy
from textblob import TextBlob
import re
import emoji


df = pd.read_csv("auth-data.csv")

# function to clearn tweets from emojis and links and line breaks and more
def clean_tweets(txt):
	txt = re.sub(r"RT[\s]+", "", txt)
	txt = txt.replace("\n", " ")
	txt = re.sub(" +", " ", txt)
	txt = re.sub(r"https?:\/\/\S+", "", txt)
	txt = re.sub(r"(@[A-Za-z0–9_]+)|[^\w\s]|#", "", txt)
	txt = emoji.replace_emoji(txt, replace='')
	txt.strip()
	return txt

# Connect to Twitter API:
consumerKey = df.iloc[0,0]
consumerSecret = df.iloc[0,1]
accessToken = df.iloc[0,2]
accessTokenSecret = df.iloc[0,3]

# Set authentication and access token
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)
authenticate.set_access_token(accessToken, accessTokenSecret)
# Create Twitter API using authentication information
api = tweepy.API(authenticate, wait_on_rate_limit=True)

# search tweets with a certain term and analyze them
tweets = api.search_tweets(q="love", lang="en", count=20)
for tweet in tweets:
	print(tweet.text)
	print(tweet.retweet_count)

	# Clean the tweet
	cleaned = clean_tweets(tweet.text)
	s = TextBlob(cleaned).sentiment.subjectivity
	p = TextBlob(cleaned).sentiment.polarity
	print(f'Subjectivity is: {s}')
	print(f'Polarity/Sentiment is: {p}')
	print("---------------------")
exit()



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
	html.H1("Natural Language Processing with Dash", style={'textAlign': 'center'}),
	html.H4("Search Term:", style={'textAlign': 'center'}),
	html.Center(
		user_search := dcc.Input(type='text', 
							 debounce=True, 
							 placeholder="Type search term for tweets", 
							 value='love'),
		className='mb-2'
	),
	
	dbc.Row([
		dbc.Col(subj_figure := dcc.Graph(figure={}), width=6),
		dbc.Col(polrt_figure := dcc.Graph(figure={}), width=6)
	]),
	
	output_table := html.Div(children=[])

], fluid=True)


@callback(
	Output(output_table,'children'),
	Output(subj_figure, 'figure'),
	Output(polrt_figure, 'figure'),
	Input(user_search, 'value')
)
def update_app(search_term):
	tweets = api.search_tweets(q=search_term, lang="en", count=20)

	cleaned_tweets, subjectivity_scores, polarity_scores = [], [], []
	for tweet in tweets:
		# Clean the tweet
		cleaned = clean_tweets(tweet.text)

		# Subjectivity analysis
		s = TextBlob(cleaned).sentiment.subjectivity
		subjectivity_scores.append(s)

		# Polarity analysis
		p = TextBlob(cleaned).sentiment.polarity
		polarity_scores.append(p)

		# Build list of all cleaned tweets
		cleaned_tweets.append(cleaned)

	# Calculate average of subjectivity and polarity scores
	average_subj = sum(subjectivity_scores) / len(subjectivity_scores)
	average_polrty = sum(polarity_scores) / len(polarity_scores)

	# Create Dash DataTable
	table_data = [{'tweet-column': t} for t in cleaned_tweets]
	the_table = dash_table.DataTable(table_data, style_cell={'textAlign': 'left'})
	
	# Create Bar chart of subjectivity scores
	fig_s = go.Figure(data=[go.Bar(y=subjectivity_scores)])
	fig_s.add_hline(y=average_subj, annotation_text="Mean:"+str(round(average_subj,2)), annotation_font_color="orange", annotation_position="top left", annotation_font_size=15)
	fig_s.update_traces(text=subjectivity_scores, textposition='outside', texttemplate='%{text:.2}')
	fig_s.update_xaxes(showticklabels=False)
	fig_s.update_layout(title="Subjectivity Scores")

	# Create Bar chart of Polarity (sentiment)
	fig_p = go.Figure(data=[go.Bar(y=polarity_scores)])
	fig_p.add_hline(y=average_polrty, annotation_text="Mean:"+str(round(average_polrty,2)), annotation_font_color="orange", annotation_position="top left", annotation_font_size=15)
	fig_p.update_traces(text=polarity_scores, textposition='outside', texttemplate='%{text:.2}')
	fig_p.update_xaxes(showticklabels=False)
	fig_p.update_layout(title="Polarity Scores")

	return the_table, fig_s, fig_p


if __name__ == "__main__":
	app.run()

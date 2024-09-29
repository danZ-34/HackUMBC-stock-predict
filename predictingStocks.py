import yfinance
import pandas
#from neuralprophet import NeuralProphet
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

#import streamlit as st


from flask import Flask, render_template
import altair
import io
import base64

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
	return 'Hi there, this is the home page'

@app.route('/stockhistory')
def stock_history():
	#get the company stock
	stock_for_company = "AAPL"
	start_date = "2019-05-14"
	end_date = "2021-04-23"	

	#raw data conversion
	stock_data = yfinance.download(stock_for_company, start_date, end_date, interval='1mo')
	stock_data_html = stock_data.to_html()


	#Plot the data
	plt.figure(figsize=(12, 7))
	plt.plot(stock_data['Open'], label='Stock open', color='green')
	plt.plot(stock_data['Close'], label='Stock Closed', color='red')

	#Moving average predictions
	stock_data['Opening_MA3'] = stock_data['Open'].rolling(window=3).mean()
	stock_data['Closing_MA3'] = stock_data['Close'].rolling(window=3).mean()

	plt.plot(stock_data['Opening_MA3'], label='3-Month Opening Move Average', color='blue')
	plt.plot(stock_data['Closing_MA3'], label='3-Month Closing Move Average', color='purple')


	plt.title('Stock Prices')
	plt.xlabel('Date and Time')
	plt.ylabel("Price in US Dollars")
	plt.legend()
	plt.grid()

	#Save the plot to buffer
	img_buffer = io.BytesIO()
	plt.savefig(img_buffer, format='png')
	plt.close()
	img_buffer.seek(0)

	#Image encode to base64
	plot_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')

	return render_template('raw_data.html', plot_base64=plot_base64, stock_data_html=stock_data_html)



if __name__ == "__main__":
	print("hi there")

	app.run()
	
	

	

	

	

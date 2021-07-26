#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User
from difflib import SequenceMatcher

config = configparser.ConfigParser()
config.read("config.ini")
app = Flask(__name__)
app.secret_key = config['Network']['app.secret_key']


# database connection function
def connect_to_db():
	engine = create_engine(config['Database']['URL_database'])
	session = sessionmaker(bind=engine)()
	return session


# retrieving all data from the database
def get_data_from_db():
	session = connect_to_db()
	users = session.query(User).order_by(User.user_id).all()
	return users


# calculation of the coefficient by SequenceMatcher
def get_ratio_sm(first_team, second_team):
	return SequenceMatcher(None, first_team, second_team).ratio()


# calculating the coefficient by Tanimoto
def get_ratio_tn(first_name, second_name):
	a, b, c = len(first_name), len(second_name), 0.0
	for sym in first_name:
		if sym in second_name:
			c += 1
	return c/(a+b-c)


# displaying the login page
@app.route('/login')
def login():
	return render_template('login.html')


# displaying the sign up page
@app.route('/signup')
def signup():
	return render_template('signup.html')


# displaying the main page
@app.route('/')
def main():
	return render_template('main.html')


# display of a page with a factor
@app.route('/ratio', methods=['POST'])
def ratio():
	first_team = request.form.get('first_team')
	second_team = request.form.get('second_team')
	ratio_value_sm = round(get_ratio_sm(first_team, second_team), 2)
	ratio_value_tn = round(get_ratio_tn(first_team, second_team), 2)
	return render_template('index.html', ratio_value_sm=ratio_value_sm, ratio_value_tn=ratio_value_tn)


# user sign up processing
@app.route('/signup', methods=['POST'])
def signup_post():
	username = request.form.get('username')
	password = request.form.get('password')
	confirm_password = request.form.get('confirm_password')
	if password != confirm_password:
		flash('Password mismatch')
		return redirect(url_for('signup'))
	session = connect_to_db()
	# receiving a user by mail
	user = session.query(User).filter_by(username=username).first()
	if user:  # if a user is found, we want to redirect back to signup page so user can try again
		flash('Email address already exists')
		return redirect(url_for('signup'))
	# adding a registered user to the database
	qry = config['Database']['insert_user_signup_qry'].format(username, password)
	session.execute(qry)
	session.commit()
	return redirect(url_for('login'))


# user login processing
@app.route('/login', methods=['POST'])
def login_post():
	session = connect_to_db()
	username = request.form.get('username')
	password = request.form.get('password')
	user = session.query(User).filter_by(username=username).first()
	# check if the user actually exists
	if not user or user.password != password:
		flash('Please check your login details and try again.')
		return redirect(url_for('login'))  # if the user doesn't exist or password is wrong, reload the page
	users = get_data_from_db()
	# user role check
	return render_template('index.html', userslist=users)


# updating the password for the user
@app.route('/update', methods=['POST'])
def update_post():
	old_password = request.form.get('old_password')
	new_password = request.form.get('new_password')
	session = connect_to_db()
	try:
		user_id = session.query(User).filter_by(password=old_password).first().user_id
	except Exception as e:
		flash('Wrong password')
		return render_template('index.html')
	qry = config['Database']['update_user_qry'].format('password', new_password, user_id)
	session.execute(qry)
	session.commit()
	return render_template('index.html')


# main application launch function
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8000)

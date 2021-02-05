# So what goes in the routes module? The routes are the different URLs that the 
# application implements. In Flask, handlers for the application routes are written 
# as Python functions, called view functions. View functions are mapped to one or 
# more route URLs so that Flask knows what logic to execute when a client requests 
# a given URL.

#The operation that converts a template into a complete HTML page is called rendering.
from flask import render_template, flash, redirect, url_for
from app import app
from app.models import *
from app.forms import GetToken, MyToken

#a token object
myTokenObj = MyToken()

#get the token
@app.route('/')
@app.route('/token', methods=['GET', 'POST'])
def token():
    form = GetToken()
    if form.validate_on_submit():
        #collect all data in a list
        theToken = form.token.data
        myTokenObj.set_token(theToken)
        return redirect(url_for('home'))
    else:
        flash(" ... hent token fra Postman ...")
    return render_template('token.html', title='Get token', form=form)

#read data
@app.route('/home')
def home():
    products, sapSystem = main_module(myTokenObj)
    system = sapSystem
    return render_template('home.html', title='oData received from SAP API', products=products, system=system)

#the list of wines that is to young to drink
@app.route('/about')
def about():
    aboutX = ' .. under construction ..'
    return render_template('about.html', title='About this app', aboutX=aboutX)



# So what goes in the routes module? The routes are the different URLs that the 
# application implements. In Flask, handlers for the application routes are written 
# as Python functions, called view functions. View functions are mapped to one or 
# more route URLs so that Flask knows what logic to execute when a client requests 
# a given URL.

#The operation that converts a template into a complete HTML page is called rendering.
from flask import render_template, flash, redirect, url_for
from app import app
from app.models import *

@app.route('/')
@app.route('/home')
def home():
    user = {'username': 'GeirOwe'}
    products, sapSystem = main_module()
    system = sapSystem
    return render_template('home.html', title='oData received from SAP API', user=user, products=products, system=system)

#the list of wines that is to young to drink
@app.route('/about')
def about():
    user = {'username': 'GeirOwe'}
    aboutX = ' .. under construction ..'
    return render_template('about.html', title='About this app', user=user, aboutX=aboutX)

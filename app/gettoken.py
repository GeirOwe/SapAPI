import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import msal
import config
from werkzeug.middleware.proxy_fix import ProxyFix

from flask import flash
from app import app
from app.models import *
from app.forms import GetToken, MyToken
from app.modelsPL import *
from app.modelsSCM import *

#start a session to manage the cache and tokens
Session(app)

# See also https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/#proxy-setups
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route("/index")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('index.html', user=session["user"], version=msal.__version__)

@app.route("/login")
def login():
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    session["flow"] = _build_auth_code_flow(scopes=config.SCOPE)
    return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)

@app.route(config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    try:
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        if "error" in result:
            return render_template("auth_error.html", result=result)

        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    except ValueError:  # Usually caused by CSRF
        pass  # Simply ignore them
    #check what scope - PL, SCM or ODATA API
    currentScope = result.get('scope')
    if currentScope == config.SCOPEPL:
        return redirect(url_for("pllogon"))
    elif currentScope == config.SCOPESCM:
        return redirect(url_for("scmlogon"))
    else:
        return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("about", _external=True))

#read data
@app.route('/home')
def home():
    #get token from cache
    tokenFromCache = _get_token_from_cache(config.SCOPE)
    theToken = tokenFromCache['access_token']
    #read the SAP API based on token
    products, sapSystem = main_module(theToken)
    system = sapSystem
    return render_template('home.html', title='oData received from SAP API', products=products, system=system)

#start / home for the app
@app.route("/")
@app.route('/about')
def about():
    aboutX = ''
    return render_template('about.html', title='About this app', aboutX=aboutX)

#test accessing the Basic PL api
@app.route("/plapi")
def plapi():
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    session["flow"] = _build_auth_code_flow(scopes=config.SCOPEPL)
    return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)

#access towards PL api ok?
@app.route("/pllogon")
def pllogon():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('employee.html', user=session["user"], version=msal.__version__)

#read PL data
@app.route('/pldata')
def pldata():
    #get token from cache
    tokenFromCache = _get_token_from_cache(config.SCOPEPL)
    theToken = tokenFromCache['access_token']
    #read the Basic PL API based on token
    emplNo = '686603'
    #theToken = '...'
    employee, sapSystem = pl_module(theToken, emplNo)
    system = sapSystem
    return render_template('empldata.html', title='oData received from Basic PL API', employee=employee, system=system)

######## request input
# get input from user - employee number ... and maybe a token to use.
#read PL data
@app.route('/getpldata')
def getpldata():
    # be om ansattnr og eventuelt token
    return render_template('empInput.html', title='Be om ansatt nr')

@app.route('/registerPL', methods=['POST'])
def registerPL():
    # get input data
    emplNo = request.form.get('emplno')
    theToken = request.form.get('intoken')
    if not theToken:
        #get token from cache
        tokenFromCache = _get_token_from_cache(config.SCOPEPL)
        theToken = tokenFromCache['access_token']
    #read the Basic PL API based on token
    employee, sapSystem = pl_module(theToken, emplNo)
    system = sapSystem
    return render_template('empldata.html', title='oData received from Basic PL API', employee=employee, system=system)
####### end request input

#test accessing the SCM api
@app.route("/scmapi")
def scmapi():
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    session["flow"] = _build_auth_code_flow(scopes=config.SCOPESCM)
    return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)

#access towards SCM api ok?
@app.route("/scmlogon")
def scmlogon():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('scm.html', user=session["user"], version=msal.__version__)

#read SCM data
@app.route('/scmdata')
def scmdata():
    #get token from cache
    tokenFromCache = _get_token_from_cache(config.SCOPESCM)
    theToken = tokenFromCache['access_token']
    #read the SCM Dev API based on token
    SCMdata, sapSystem = scm_module(theToken)
    system = sapSystem
    return render_template('SCMdata.html', title='oData received from SCM API', SCMdata=SCMdata, system=system)

###########
#MSAL below
###########

def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()
        #print(session["token_cache"])

def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        config.CLIENT_ID, authority=authority or config.AUTHORITY,
        client_credential=config.CLIENT_SECRET, token_cache=cache)

def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [],
        redirect_uri=url_for("authorized", _external=True))

def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result

app.jinja_env.globals.update(_build_auth_code_flow=_build_auth_code_flow)  # Used in template

if __name__ == "__main__":
    app.run()
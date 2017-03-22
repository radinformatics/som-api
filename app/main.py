from flask import (
    Flask, 
    url_for,
    session,
    render_template, 
    request,
    jsonify
)

from flask_basicauth import BasicAuth
from flask_wtf.csrf import CSRFProtect
from flask_restful import Resource, Api
from werkzeug import secure_filename
from som.api.google.dlp.client import DLPApiConnection

from random import choice
import webbrowser
import tempfile
import shutil
import random
import uuid
import os


# SERVER CONFIGURATION ##############################################
class SomServer(Flask):

    def __init__(self, *args, **kwargs):
        super(SomServer, self).__init__(*args, **kwargs)

        # Set up temporary directory on start of application
        self.tmpdir = tempfile.mkdtemp()
        self.dlp = DLPApiConnection()


app = SomServer(__name__)
app.secret_key = os.environ['HELLOKITTY']
app.config['SESSION_TYPE'] = 'filesystem'


# PW/csrf protect site ###############################################
csrf = CSRFProtect(app)

app.config['BASIC_AUTH_USERNAME'] = os.environ['MEATBALLS']
app.config['BASIC_AUTH_PASSWORD'] = os.environ['MARINARA']
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

'''
# SET UP SAML ########################################################

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/saml/login'

# setup python-saml-flask
from .auth import SamlManager
saml_manager = SamlManager()
saml_manager.init_app(app)

# setup acs response handler
@saml_manager.login_from_acs
def login_from_acs(acs):
  # define login logic here depending on idp response
  # must call login_user() and redirect as necessary
  print acs.get('attributes')
  pass


@saml_manager.login_from_acs
def acs_login(acs):
    if acs.get('errors'):
        return jsonify({'errors': acs.get('errors')})
    elif not acs.get('logged_in'):
        return jsonify({"error": 'login failed'})
    else:
        for attr in acs.get('attributes'):
            if attr[0] == 'emailAddress':
                login_user(User.find_or_create(attr[1])) #JustInTime user creation
        if not current_user.is_authenticated():
            return {'error': 'could not find email in idp authentication response'}
    return redirect('/home')
'''

# CONTAINER VIEWS ###################################################


@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')


@app.route('/clean', methods=['POST'])
@basic_auth.required
def remove_phi():
    '''POST view to try removing PHI'''  
    if request.method == 'POST':
        text = request.form.get('text')
        cleaned = app.dlp.remove_phi(texts=[text])
        return jsonify({'cleaned':cleaned,
                        'original':text})


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0')

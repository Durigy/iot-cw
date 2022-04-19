from main import app
from main import db
from flask import render_template, url_for, request, redirect, flash
# from main.forms import LoginForm

@app.errorhandler(404)
def page_not_found(e):
    return redirect('home')

@app.errorhandler(500)
def page_not_found(e):
    return redirect('home')

@app.route('/', methods=['GET', 'POST'])
def home():
    pass

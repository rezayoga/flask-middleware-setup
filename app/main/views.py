from . import main_blueprint
from flask import render_template, request, redirect, url_for, current_app, abort
from app.models import User, Movie

@main_blueprint.route('/')
def index():
    u = User.query.all()
    current_app.logger.info("Index page loading")
    return render_template('main/index.html', users=u)

@main_blueprint.route('/admin')
def admin():
    abort(500)
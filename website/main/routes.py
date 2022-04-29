from datetime import datetime
from . import app, db
import secrets
from flask import render_template, url_for, request, redirect, flash
# from flask_login import login_user, logout_user, login_required, current_user
# from .forms import LoginForm
from flask_restful import Api, Resource, abort, marshal_with, reqparse, fields
from .models import User, Device, DeviceData


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404, There's an error</h1>"

@app.errorhandler(500)
def page_not_found(e):
    return "<h1>500, There's an error</h1>"

# @app.route('/', methods=['GET', 'POST'])
# @login_required
# def home():
#     # return render_template('login.html', title='login')
#     return render_template(
#         'base_simple.html',
#         title='home'
#     )

@app.route('/')
def home():
    return '<h1>Hello There</h1>'


# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated: return redirect(url_for('home'))

#     form = LoginForm()

#     if form.validate_on_submit():
#         user = ''
#         if User.query.filter_by(email=form.email.data).first():
#             user = User.query.filter_by(email=form.email.data).first()

#         # user = User.query.filter_by(displayname=form.displayname.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user, remember=form.remember.data)
#         else:
#             flash('Login Unsuccessful. Check displayname/email and Password')

#     return render_template(
#         'user/login.html',
#         title='Login',
#         form=form
#     )

# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(request.referrer)




#### api ####

# Alram activated
# @app.route("/api/<api_key>/send_data", methods=['GET', 'POST'])
# def logout(api_key):
# @app.route("/api/send_data", methods=['GET', 'POST'])
# def api_send_data():
#     content = request.json
#     print(content)
#     return True

api = Api(app)

device_post_args = reqparse.RequestParser()
device_post_args.add_argument("api_key", type=str, help="API key not sent", required=True)
device_post_args.add_argument("name", type=str, help="Name not sent")
device_post_args.add_argument("hashed_password", type=str, help="Password not sent")
device_post_args.add_argument("is_armed", type=bool, help="Armed status not sent")

device_get_args = reqparse.RequestParser()
device_get_args.add_argument("device_id", type=str, help="Device ID not sent", required=True)
device_get_args.add_argument("api_key", type=str, help="API key not sent", required=True)

device_data_post_args = reqparse.RequestParser()
device_data_post_args.add_argument("api_key", type=str, help="API key not sent", required=True)
device_data_post_args.add_argument("light", type=bool, help="Light not sent")
device_data_post_args.add_argument("device_id", type=str, help="Device ID not sent", required=True)
device_data_post_args.add_argument("time", type=str, help="Time status not sent")
device_data_post_args.add_argument("is_intruder", type=bool, help="Is Intruder not sent")
device_data_post_args.add_argument("reset_counter", type=bool, help="Counter not sent")


resource_fields = {
    'id': fields.String,
    'name': fields.String,
    'hashed_password': fields.Integer,
    'is_armed': fields.Boolean,
    'user_id': fields.String
}

def generate_id():
    id = secrets.token_hex(10)
    return id

class DeviceAPI(Resource):
    @marshal_with(resource_fields)
    def get(self, device_id):
        args = device_get_args.parse_args()

        user = User.query.filter_by(api_key=args['api_key']).first()
        if not user: abort(404, message="no user")

        result = Device.query.filter_by(id=args['device_id']).first()
        if not result: abort(404, message="Couldn't find the result")
        return result


    # @marshal_with(resource_fields)
    def post(self): #, device_id):
        args = device_post_args.parse_args()

        user = User.query.filter_by(api_key=args['api_key']).first()
        if not user: abort(404, message="no user")

        gened_id = generate_id()

        device = Device(
            id = gened_id,
            name = args['name'],
            password = args['hashed_password'],
            is_armed = args['is_armed'],
            user_id = user.id
        )

        db.session.add(device)
        db.session.commit()
        return {'id': str(gened_id)}, 201        

    @marshal_with(resource_fields)
    def put(self):
        args = device_post_args.parse_args()

        if not User.query.filter_by(api_key=args['api_key']).first(): abort(404, message="no user")

        device = Device.query.filter_by(id=args['id']).first()
        if not device: abort(404, message="Couldn't find the result")
        
        
        if args['name']: device.name = args['name']
        if args['hashed_password']: device.hashed_password = args['hashed_password']
        if args['is_armed']: device.is_armed = args['is_armed']

        db.session.commit()
        return device, 201      

class DeviceGetAPI(Resource):
    @marshal_with(resource_fields)
    def post(self): #, device_id):
        args = device_get_args.parse_args()

        user = User.query.filter_by(api_key=args['api_key']).first()
        if not user: abort(404, message="no user")

        device = Device.query.filter_by(id=args['device_id']).first()
        if not device: abort(404, message="Couldn't find the result")

        return device, 201 

class DeviceSendDataAPI(Resource):
    # @marshal_with(resource_fields)
    def post(self): #, device_id):
        args = device_data_post_args.parse_args()

        user = User.query.filter_by(api_key=args['api_key']).first()
        if not user: abort(404, message="no user")

        # device = Device.query.filter_by(id=args['device']).first()
        # if not device: abort(404, message="no device")

        gened_id = generate_id()

        device_data = DeviceData(
            id = gened_id,
            light = args['light'],
            is_intruder = args['is_intruder'],
            time = args['time'],
            reset_counter = args['reset_counter'],
            device_id = args['device_id']
        )

        db.session.add(device_data)
        db.session.commit()
        return {'set':True}, 201

api.add_resource(DeviceAPI, "/api/device")
api.add_resource(DeviceGetAPI, "/api/device/get")
api.add_resource(DeviceSendDataAPI, "/api/device/send_data")
from datetime import datetime
from . import app, db, api
import secrets
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegistrationForm, ChangeDevicePasswordForm
from flask_restful import Resource, abort, marshal_with, reqparse, fields
from .models import User, Device, DeviceInfo
from .graph import intrusions_vs_time, intrusions_vs_light_night, vision_accuracy
import bcrypt

# # Reference: https://stackoverflow.com/questions/32237379/python-flask-redirect-to-https-from-http
# @app.before_request
# def before_request():
#     if not request.is_secure:
#         url = request.url.replace('http://', 'https://', 1)
#         code = 301
#         return redirect(url, code=code)


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        '404.html',
        title='404'
    )

@app.errorhandler(500)
def page_not_found(e):
    return "<h1>500, There's an error</h1>"

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    devices = Device.query.filter_by(user_id = current_user.id).all()

    graph_intrusions_vs_time = intrusions_vs_time()
    graph_intrusions_vs_light_night = intrusions_vs_light_night()

    return render_template(
        'index.html',
        title='Account',
        devices = devices,
        graph_intrusions_vs_time = graph_intrusions_vs_time,
        graph_intrusions_vs_light_night = graph_intrusions_vs_light_night
    )

@app.route('/account')
@login_required
def account():
    return render_template(
        'user/account.html',
        title='Account'
    )

@app.route('/device/<device_id>', methods=['GET', 'POST'])
@login_required
def device(device_id):
    device = Device.query.get_or_404(device_id)
    if device.user_id != current_user.id: 
        flash('device not found')
        return redirect('404')

    
    graph_vision_accuracy = vision_accuracy(device_id) if not vision_accuracy(device_id) == None else ''

    form = ChangeDevicePasswordForm()
    if form.validate_on_submit and request.method == "POST":
        hashed_password = bcrypt.hashpw(bytes(form.password.data,'UTF-8'), bcrypt.gensalt())
        device.password = hashed_password
        db.session.commit()
        flash('Device password updated')
        return redirect(url_for('index'))

    return render_template(
        'device/device.html',
        title='Update Device',
        form=form,
        device = device,
        graph_vision_accuracy = graph_vision_accuracy
    )


#################################
#                               #
#           User Stuff          #
#                               #
#################################

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit() and request.method == "POST":
        user_id = generate_id()
        api_key = generate_id()
        
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        hashed_password = bcrypt.hashpw(bytes(form.password.data,'UTF-8'), bcrypt.gensalt())

        user = User(
            id = user_id,
            email = form.email.data,
            password = hashed_password,
            api_key = api_key
        )

        db.session.add(user)
        db.session.commit()
        flash('Account Created - You can now Login in')
        return redirect(url_for('login'))
    return render_template(
        'user/register.html',
        title='Register',
        form=form
    )


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit() and request.method == "POST":
        user = User.query.filter_by(email = form.email.data).first()

        if user and bcrypt.checkpw(bytes(form.password.data,'UTF-8'), bytes(user.password,'UTF-8')):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("index"))
        else:
            flash('Login Unsuccessful. Check displayname/email and Password')

    return render_template(
        'user/login.html',
        title = 'Login',
        form = form
    )

@app.route("/logout")
def logout():
    logout_user()
    return redirect(request.referrer)



def generate_id():
    id = secrets.token_hex(10)
    return id


#################################
#                               #
#           API Stuff           #
#                               #
#################################

device_post_args = reqparse.RequestParser()
device_post_args.add_argument("api_key", type=str, help="API key not sent", required=True)
device_post_args.add_argument("name", type=str, help="Name not sent")
device_post_args.add_argument("hashed_password", type=str, help="Password not sent")
device_post_args.add_argument("is_armed", type=bool, help="Armed status not sent")

device_put_args = reqparse.RequestParser()
device_put_args.add_argument("api_key", type=str, help="API key not sent", required=True)
device_put_args.add_argument("device_id", type=str, help="Device ID not sent", required=True)
device_put_args.add_argument("name", type=str, help="Name not sent")
device_put_args.add_argument("hashed_password", type=str, help="Password not sent")
device_put_args.add_argument("is_armed", type=bool, help="Armed status not sent")

device_get_args = reqparse.RequestParser()
device_get_args.add_argument("device_id", type=str, help="Device ID not sent", required=True)
device_get_args.add_argument("api_key", type=str, help="API key not sent", required=True)

device_data_post_args = reqparse.RequestParser()
device_data_post_args.add_argument("api_key", type=str, help="API key not sent", required=True)
device_data_post_args.add_argument("light", type=bool, help="Light not sent")
device_data_post_args.add_argument("device_id", type=str, help="Device ID not sent", required=True)
device_data_post_args.add_argument("time", type=str, help="Time status not sent")
device_data_post_args.add_argument("is_intruder", type=bool, help="Is Intruder not sent")
device_data_post_args.add_argument("reset_counter", type=int, help="Counter not sent")


# resource_fields = {
#     'id': fields.String,
#     'name': fields.String,
#     'hashed_password': fields.String,
#     'is_armed': fields.Boolean,
#     'user_id': fields.String
# }

class DeviceAPI(Resource):
    # @marshal_with(resource_fields)
    # def get(self, device_id):
    #     args = device_get_args.parse_args()

    #     user = User.query.filter_by(api_key=args['api_key']).first()
    #     if not user: abort(404, message="no user")

    #     device = Device.query.filter_by(id=args['device_id']).first()
    #     if not device: abort(404, message="Couldn't find the result")
    #     return {
    #         'id': device.id,
    #         'name': device.name,
    #         'hashed_password': device.password,
    #         'is_armed': device.is_armed,
    #         'user_id': device.user_id
    #     }


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

    # @marshal_with(resource_fields)
    def put(self):
        args = device_put_args.parse_args()

        if not User.query.filter_by(api_key=args['api_key']).first(): abort(404, message="no user")

        device = Device.query.filter_by(id=args['device_id']).first()
        if not device: abort(404, message="Couldn't find the result")
        
        
        if args['name']: device.name = args['name']
        if args['hashed_password']: device.hashed_password = args['hashed_password']
        if args['is_armed'] == True: 
            device.is_armed = True
        elif args['is_armed'] == False: 
            device.is_armed = False

        db.session.commit()
        return {
            'id': device.id,
            'name': device.name,
            'hashed_password': device.password,
            'is_armed': device.is_armed,
            'user_id': device.user_id
        }, 201     

class DeviceGetAPI(Resource):
    # @marshal_with(resource_fields)
    def post(self): #, device_id):
        args = device_get_args.parse_args()

        user = User.query.filter_by(api_key=args['api_key']).first()
        if not user: abort(404, message="no user")

        device = Device.query.filter_by(id=args['device_id']).first()
        if not device: abort(404, message="Couldn't find the result")

        return {
            'id': device.id,
            'name': device.name,
            'hashed_password': device.password,
            'is_armed': device.is_armed,
            'user_id': device.user_id
        }, 201  

class DeviceSendDataAPI(Resource):
    # @marshal_with(resource_fields)
    def post(self): #, device_id):
        args = device_data_post_args.parse_args()

        user = User.query.filter_by(api_key=args['api_key']).first()
        if not user: abort(404, message="no user")

        # device = Device.query.filter_by(id=args['device']).first()
        # if not device: abort(404, message="no device")

        gened_id = generate_id()

        device_data = DeviceInfo(
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
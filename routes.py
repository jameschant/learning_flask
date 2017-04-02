from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, Place
from forms import SignupForm, LoginForm, AddressForm

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/learningflask'
db.init_app(app)


app.secret_key = "development-key"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))
    # Instantiate a new instance of the SignupForm class.
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            # If the form isn't validated, reload the page and a new form.
            return render_template('signup.html', form=form)
        else:
            # New usable instance of the User object called newuser each time POST is successful
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            return redirect(url_for('home'))
    elif request.method == "GET":
        return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if 'email' in session:
        return redirect(url_for('home'))
    form = LoginForm()
    # If the form has been posted and the validation check fails, reload the login form
    if request.method == "POST":
        if form.validate() == False:
            return render_template("login.html", form=form)
        else:
            # else fetch the data from the login form, so collect the email and password data
            email = form.email.data
            password = form.password.data

            # Then using this, check whether the user exists in the database
            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                # If the user does exist and the password check works out, login the user by
                # creating a new session and redirecting to the homepage.
                session['email'] = form.email.data
                return redirect(url_for('home'))
            else:
                # Else if the user doesn't exist in the database with that email and password, reload the form,
                # so this redirects to the login route that triggers a normal GET request
                return redirect(url_for('login'))

    # If a GET request ahas been received we simply render the form.
    elif request.method == "GET":
        return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route("/home", methods=["GET", "POST"])
def home():
    # An if statement so that if the user isn't logged in, they cannot reach the Home area, which should only be
    # accessible to logged in users. There we redirect them to the login page using url_for. Otherwise we render home.
    if 'email' not in session:
        return redirect(url_for('login'))

    form = AddressForm()

    places = []
    my_coordinates = (37.4221, -122.0844)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('home.html', form=form)
        else:
            # get the address
            address = form.address.data

            # query for places around it
            p = Place()
            my_coordinates = p.address_to_latlng(address)
            places = p.query(address)

            # return those results
            return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)

    elif request.method == 'GET':
        return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)

if __name__ == "__main__":
    app.run(debug=True)
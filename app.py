from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import LoginManager, login_required, UserMixin
from models import Voter, Address  # Assuming you have defined SQLAlchemy models

app = Flask(__name__)
app.secret_key = '2076'  # Replace with a secure secret key

# Create a SQLAlchemy database engine
# Replace the database URL with your actual database connection details
db_engine = create_engine('postgresql://voter:matchmaster7847@localhost:5432/voterblend')

# Create a SQLAlchemy session
Session = sessionmaker(bind=db_engine)
db_session = Session()

# Define SQLAlchemy models for the voters and addresses tables
Base = declarative_base()

class Voter(Base):
    __tablename__ = 'voters'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    mobile_no = Column(String)
    epic_id = Column(String)
    address = Column(String)
    # Add more columns as needed

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    mobile_no = Column(String)
    # Add more columns as needed

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)

# Sample User class for Flask-Login (you should replace this with your user model)
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    # Replace this with your actual user loading logic
    return User(user_id)

@app.route('/')
# @login_required  # Commented out for testing
def index():
    # Fetch data from the 'voters' and 'addresses' tables
    voters_data = db_session.query(Voter).all()
    addresses_data = db_session.query(Address).all()

    return render_template('index.html', username=request.user_id, voter_records=voters_data, address_records=addresses_data)

@app.route('/search', methods=['POST'])
# @login_required  # Commented out for testing
def search():
    selected_voter = request.form['selected_voter']
    voter_name = request.form['voter_name']

    # Use the selected_voter and voter_name to query matching addresses
    # Replace the following code with your actual query logic
    matching_addresses = get_matching_addresses(selected_voter, voter_name)

    return render_template('index.html', username=request.user_id, selected_voter=selected_voter, voter_name=voter_name, address_results=matching_addresses)

@app.route('/update', methods=['POST'])
# @login_required  # Commented out for testing
def update():
    selected_address = request.form['selected_address']
    
    # Query the database to get the selected address
    address = db_session.query(Address).filter_by(name=selected_address).first()

    if address:
        # Perform the update operation on the voter's information
        # Example: Update the voter's address in the voters table
        voter = db_session.query(Voter).filter_by(name=selected_address).first()
        if voter:
            voter.address = address.address
            db_session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

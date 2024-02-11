from flask import Flask, render_template, request, redirect, url_for, session,jsonify,send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO

app=Flask(__name__)
app.secret_key = 'that_is_top_sceret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:2104/postgres'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'


    position = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
    
class ClubRequest(db.Model):
    __tablename__ = 'club_requests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Make ID auto-generated
    club_name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.LargeBinary)
    money = db.Column(db.Float)
    approval_chain = db.Column(db.String(100))
    curent=db.Column(db.String(100))
    approval=db.Column(db.String(100), default='Pending')
    maker=db.Column(db.String(100))
    def __repr__(self):
        return f"<ClubRequest {self.id}>"
    


class Societ(db.Model):
    __tablename__ = 'societ'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    fa = db.Column(db.String(50), nullable=False)
    societi = db.Column(db.String(50), nullable=False)
    key = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<societi {self.id}>"
    
class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fa = db.Column(db.String(50) )
    sec=db.Column(db.String(50))
    club = db.Column(db.String(50), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    societi=db.Column(db.String(50), nullable=False)
    budget=db.Column(db.Float, nullable=False,default=15000)

    def __repr__(self):
        return f"<Club {self.id}>"
    

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sign_up', methods=['POST'])
def sign_up():
    return render_template("signup.html")




@app.route('/login', methods=['POST'])
def login():
    return render_template("login.html")



@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username, password=password).first()
    
    if user:
        session['position']=user.position
        session['user']=user.username
        return 'Login successful'
    else:
        return 'Invalid username or password'

    






@app.route('/create_account', methods=['POST'])
def create_account():
    try:
        position = request.form['pos']
        print(position)
        username = request.form['username']
        password = request.form['password']
        key = request.form['key']
        if 'society' in request.form:
            sc = request.form['society']


        session['position']=position
        session['user']=username
        
        
        
        
        new_user = User(position=position, username=username, password=password)
        
        # Add the new user to the database session
        db.session.add(new_user)

        if position == 'c_mem':
            societ = Societ.query.filter_by(key=key).first()
            if societ:
                new_club = Club(club=username,key=password,societi=societ.societi) ##########################
                db.session.add(new_club)
            else:
                raise Exception("Invalid key for society")
            
        elif position == 'c_sec' or position == 'c_fa':
            club = Club.query.filter_by(key=key).first()
            if club:
                if position == 'c_sec':
                    club.sec = username
                elif position == 'c_fa':

                    club.fa = username
            else:
                raise Exception("Invalid key for club")
            db.session.commit()
            
        elif position == 's_fa':

            new_request = Societ(
            fa=username,
            societi=sc,
            key=request.form['key'])

            # Add the new request to the database session
            db.session.add(new_request)



            



        
        

        db.session.commit()
        return "Success"
    except Exception as e:
        # If an error occurs during commit, rollback the session and return an error message
        db.session.rollback()
        return jsonify({'error': str(e)})
    

    


    

@app.route('/requestx', methods=['POST'])
def requestx():
    return render_template("request.html")





@app.route('/upload_request', methods=['POST'])
def upload_request():
    if (session.get('position',None)=='c_mem'):
            chain='c_sec'
        
    elif(session.get('position',None)=='c_sec'):
            chain='c_fa'
            
            

    else:
        return "Please Login"
    #try:
    subject = request.form['subject']
    description = request.form['description']
    attachment = request.files['attachment'].read()  # Read binary content of the uploaded file
    money=request.form['money']
    maker=session.get('user',None)
    # Create a new ClubRequest instance and store the PDF content as binary data
    if (session.get('position',None)=='c_mem'):
        chain='c_sec'
        club_record = Club.query.filter_by(club=session.get('user', None)).first()
        if club_record and club_record.sec is not None:
            user = club_record.sec
        else:
            raise Exception("No record found in Club table for the specified user")
    
    elif(session['postion']=='c_mem'):
        chain='c_fa'
        club_record = Club.query.filter_by(club=session.get('user', None)).first()
        if club_record and club_record.fa is not None:
            user = club_record.fa
        else:
            raise Exception("No record found in Club table for the specified user")
    
    new_request = ClubRequest(
        club_name=session.get('user',None),
        subject=subject,
        description=description,
        attachment=attachment,
        approval_chain=chain,
        curent=user,
        money=money,
        maker=maker

    )

    # Add the new request to the database session
    db.session.add(new_request)

    # Commit the transaction
    db.session.commit()

    return 'Request submitted successfully'
    # except Exception as e:
    #     # If any error occurs, rollback the transaction
    #     db.session.rollback()
    #     return f'Error occurred: {str(e)}'



@app.route('/print_club_requests', methods=['POST'])
def print_club_requests():
    user = session.get('user', None)
    if user:
        club_requests = ClubRequest.query.filter_by(curent=user).all()
        return render_template('club_requests.html', club_requests=club_requests)
    else:
        return "No user session found."
    









@app.route('/requests_list')
def requests_list():
    # Retrieve the list of requests from the database
    requests = ClubRequest.query.all()
    
    # Render the template and pass the list of requests to it
    return render_template('requests_list.html', requests=requests)
    


@app.route('/download_pdf/<int:request_id>')
def download_pdf(request_id):
    # Retrieve the ClubRequest instance from the database
    request_record = ClubRequest.query.get(request_id)
    
    # If the request record does not exist, return an error message
    if not request_record:
        return 'Request not found'
    
    # Read the binary data of the attachment
    attachment_data = request_record.attachment
    
    # Serve the binary data as a downloadable file
    return send_file(BytesIO(attachment_data), mimetype='application/pdf', as_attachment=True, download_name=f'request_{request_id}.pdf')
           

if __name__=="__main__":
    app.run(debug=True)
from cloudant import Cloudant
from flask import *
import atexit
import os
import json
import datetime
import random
import json
from twilio.rest import Client

app = Flask(__name__, static_url_path='')
app.secret_key = 'random string 123456789'

db_name = 'mydb_n1'
client = None
db = None
email_g=""
account_sid = "ACb8f2d52ff6645fac6db1212e3afa3494"
auth_token = "cf0cdcc501f8b8809958ed9fdcd64135"

timeSlotList=['06AM-08AM','08AM-10AM','10AM-12PM','12PM-02PM','02PM-04PM','04PM-06PM','06PM-08PM']

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif "CLOUDANT_URL" in os.environ:
    client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'],
                      url=os.environ['CLOUDANT_URL'], connect=True)
    db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))


@app.route('/')
def root():

     if 'email' not in session:
         return render_template('login.html', error='')
     else:
         loggedIn, userName = getLoginDetails()
         categoryData = db['catagory_data_item']['menuitem']
         
         # Returns the current local date
         today = datetime.date.today()
        
         datelist = []
         i=0
         
         for i in range(8):
           datelist.append(str(today + datetime.timedelta(days=1+i))) 
           
         return render_template('home.html', loggedIn=loggedIn, userName=userName,categoryData=categoryData,dateData=datelist,timeData=timeSlotList)         
         
@app.route('/savedb')
def savedb():
    for document in sampleData:
        # Retrieve the fields in each row.

        jsonDocument = {
            "_id": document[0],
            "password": document[1],
            "first_name": document[2],
            "last_name": document[3],
            "addr_line1": document[4],
            "addr_line2": document[5],
            "zipcode": document[6],
            "city": document[7],
            "state": document[8],
            "country": document[9],
            "phone_no": document[10]
        }
        newDocument = db.create_document(jsonDocument)

    return "0"

#To populate catagory
@app.route('/savecatagory')
def savecatagory():
    catagoryDocument ={
    "_id": "catagory_data_item",
    "menuitem": [
          {"name": "Toys", "image": "images/Toy_image.jpg", "points":"5"},
          {"name": "Clothes", "image": "images/Clothes_image.jpg", "points":"4"},
          {"name": "NewsPaper", "image": "images/NewsPaper_image.jpg", "points":"1"},
          {"name": "Electronics", "image": "images/Electronics_image.jpg", "points":"2"},
          {"name": "Utensils", "image": "images/Utensils_image.jpg", "points":"3"},
        ]
    }
    # First retrieve the catagory document
    #cur_catagory = db['catagory_data_item']
    
    # Delete the catagory document
    #cur_catagory.delete()

    newDocument = db.create_document(catagoryDocument)
    return "0"

@app.route('/showdb')
def showdb():
    return jsonify(list(db))

@app.route('/deletedb')
def deletedb():
    client.delete_database(db_name)
    return "0"

@app.route("/registrationForm")
def registrationForm():
    return render_template("register.html")

@app.route("/registrationFormAgent")
def registrationFormAgent():
    return render_template("registerAgent.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Parse form data
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']

 
        jsonDocument = {
            "_id": email,
            "password": password,
            "first_name": firstName,
            "last_name": lastName,
            "addr_line1": address1,
            "addr_line2": address2,
            "zipcode": zipcode,
            "city": city,
            "state": state,
            "country": country,
            "phone_no": phone,
            "type": "user",
            "bookings": []
        }
        newDocument = db.create_document(jsonDocument)

        msg = "Registered Successfully"
        return render_template("login.html", error=msg)

@app.route("/registerAgent", methods=['GET', 'POST'])
def registerAgent():
    if request.method == 'POST':
        # Parse form data
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']

        jsonDocument = {
            "_id": email,
            "password": password,
            "first_name": firstName,
            "last_name": lastName,
            "addr_line1": address1,
            "addr_line2": address2,
            "zipcode": zipcode,
            "city": city,
            "state": state,
            "country": country,
            "phone_no": phone,
            "type": "Agent",
        }
        newDocument = db.create_document(jsonDocument)

        msg = "Registered Successfully"
        return render_template("login.html", error=msg)
    
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
      
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('root'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)


@app.route("/loginAgent", methods=['POST', 'GET'])
def loginAgent():
    if request.method == 'POST':
        email = request.form['email']
      
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('pickup'))
        else:
            error = 'Invalid Agent ID / Password'
            return render_template('login.html', error=error)
        
@app.route("/loginForm")
def loginForm():
    # if 'email' in session:
    #      return redirect(url_for('root'))
    # else:
        return render_template('login.html', error='')



@app.route("/bookPickup", methods=['POST', 'GET'])
def bookPickup():
    if request.method == 'POST':
          if 'email' not in session:
                return render_template('login.html', error='')
          else:
                booking_num=''.join(random.sample('123456789', 5))
                email = session ['email']
                b_document = db[email]
                b_document['bookings'].append(booking_num)
                b_document.save()
                date_selected = request.form['dateSelector']
                time_selected = request.form['timeSelector']
                client = Client(account_sid, auth_token)
                # sending message
                phone = db[email]['phone_no']
                message_content = "Booking confirmed. Booking number "+ booking_num + ". Pick up scheduled for " + date_selected + " between " + time_selected
                message = client.messages.create(body=message_content, from_="+15855638648", to=phone)      #+15855638648
                message_content = "Pickup confirmed. Pickup number "+ booking_num + ". Pick up scheduled for " + date_selected + " between " + time_selected
                message = client.messages.create(body=message_content, from_="+15855638648", to="+917483103069")      #+15855638648
                return render_template('bookpickup.html', date=date_selected, time=time_selected,booking=booking_num)

@app.route("/orders")
def orders():
          if 'email' not in session:
                return render_template('login.html', error='')
          else:
                email = session ['email']
                bookings = db[email]['bookings']
                history=""
                i=0
                bookedData = []
                pickedData = []
                totalRewards=0
                
                for booking in bookings:
                    
                    if booking in db:
                         data = {
                        "Booking" : booking,
                         "Clothes" : db[booking]["Clothes"],
                         "Electronics" : db[booking]["Electronics"] ,
                         "NewsPaper" :  db[booking]["NewsPaper"] ,
                         "Others" :  db[booking]["Others"] ,
                         "Utensils" :  db[booking]["Utensils"] ,
                         "Toys" :  db[booking]["Toys"] ,
                         "Rewards" :  db[booking]["Rewards"] 
                          }
                         totalRewards += int ( db[booking]["Rewards"])
                         pickedData.append(data)
                    else:
                        data = {
                                "Booking" : booking,
                               }
                        bookedData.append(data)
                return render_template('history.html', bookedData=bookedData,pickedData=pickedData,totalRewards=totalRewards)


@app.route("/Pickup")
def pickup():
   categoryData = db['catagory_data_item']['menuitem']
   return render_template('pickup.html',categoryData=categoryData)


@app.route("/savePickup", methods=['POST', 'GET'])
def savePickup():
    if request.method == 'POST':

        categoryData = db['catagory_data_item']['menuitem']

        total_reward=0
        for data in categoryData:
           total_reward+= (int)(request.form[data['name']]) * 2
          
        total_reward+= (int)(request.form['others']) * 2
        
        jsonDocument =  {
            "_id"  : request.form["BookingNo"],
            "booking_ref_no": request.form["BookingNo"],
            "Toys": request.form["Toys"],
            "Clothes": request.form["Clothes"],
            "NewsPaper": request.form["NewsPaper"],
            "Electronics": request.form["Electronics"],
            "Utensils": request.form["Utensils"],
            "Others": request.form["others"],
            "Rewards": str(total_reward)
            
        }
    newDocument = db.create_document(jsonDocument)    
    #msg = json.dumps(jsonDocument)
    #return render_template('login.html', error=msg)
    return render_template('pickupconfirm.html', doc = jsonDocument)

    



@app.route("/logout")
def logout():
    session.pop('email', None)
    return render_template('login.html', error='Logged Out Successfully.')



@atexit.register
def shutdown():
    if client:
        client.disconnect()


#To check if user email and password match 
def is_valid(email, password):
    if db[email]['password'] == password :
        return True
    return False

def getLoginDetails():
    if 'email' not in session:
         loggedIn = False
         firstName = ''
    else:
        loggedIn = True
        email = session['email']
        if email in db:
            firstName = db[email]['first_name'] + " " + db[email]['last_name']
        else:
            firstName = ''
    return (loggedIn, firstName)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

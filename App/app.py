import flask as fk
from flask import Flask, url_for, redirect, request, render_template, session
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from utils.user import User
from utils.admin import Admin
from utils.product import Product
from utils.weather import Weather
from utils.prediction import Prediction
from utils.firbase import Firebase
from werkzeug.utils import secure_filename


app=Flask(__name__, static_folder="static", template_folder="templates")
user=User(app=app)
admin=Admin(app=app)
product=Product()
weather=Weather()
prediction=Prediction()
firebase=Firebase()

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
os.environ['TF_ENABLE_ONEDNN_OPTS']='0'

load_dotenv('.env')
app.secret_key=os.getenv('APP_SECRET_KEY')


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if not session['loggedIn']:
            if request.method=='POST':
                uName=request.form['username']
                password=request.form['password']
                
                status,loggedUser = user.logInUser(userName=uName, password=password)
                
                if loggedUser is None:
                    session['loggedIn']=False
                    return render_template('login.html', errorMassage=status)
                else:
                    session['loggedIn']=True
                    session['username']=loggedUser['userName']
                    
                    
                    if loggedUser['adminUserFlag'] == "True":
                        session['adminUserFlag'] = True
                        return redirect(url_for('adminDashboard'))
                    else:
                        session['adminUserFlag'] = False
                        return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', errorMassage=" ")
        else:
            return redirect(url_for('dashboard'))
    except:
        session['loggedIn']=False
        return redirect(url_for('login'))
    
 
@app.route('/register', methods=['GET', 'POST'])
def register(errorMassage=" "):
    try:
        if not session['loggedIn']:
            if request.method=='POST':
                name=request.form['name']
                phoneNumber=request.form['phoneNumber']
                uName=request.form['username']
                password=request.form['password']
                
                status=user.addUser(name=name, phoneNumber=phoneNumber, userName=uName, password=password)
                
                if status: 
                    session['loggedIn']=True
                    session['registered']=True
                    session['username']=uName
                    session['phoneNumber']=phoneNumber
                    session['adminUserFlag']=False
                                        
                    return redirect(url_for('setup')) 
                else:
                    errorMassage="Registration Failed"
                    return render_template('register.html', errorMassage=errorMassage)
            else:
                return render_template('register.html', errorMassage=errorMassage)
        else:
            return redirect(url_for('dashboard'))
    except:
        session['loggedIn']=False
        return redirect(url_for('register'))
    
    
    
@app.route('/setup', methods=['GET', 'POST'])
def setup(errorMassage=" "):
    #try:
        if session['loggedIn']:
            if session['registered']:
                if request.method=='POST':
                    location=request.form['location']
                    country=request.form['country']
                    code=request.form['code']
                    uName=session['username']
                    status=user.setupIoT(userName=uName, location=location, country=country, code=code)
                    if status:
                        session['registered']=False
                        return redirect(url_for('dashboard'))
                    else:
                        errorMassage='IoT device setup failed'
                        return render_template('setupIoT.html', errorMassage=errorMassage)
                else:
                    return render_template('setupIoT.html', errorMassage=errorMassage)
            else:
                return redirect(url_for('register'))
        else:
            return redirect(url_for('login')) 
    #except:
        session['loggedIn']=False
        session['registered']=False
        return redirect(url_for('login'))
                
    
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    try:
        if not session['loggedIn']:
            return redirect(url_for('login'))
        else:
            if session['adminUserFlag']:
                return redirect(url_for('adminDashboard'))
            else:
                _, loggedUser=user.getUserByUserName(userName=session['username'])
                currentDate=datetime.now().date()
                currentTime=datetime.now().time().strftime('%H:%M:%S')
                iotDevices=loggedUser['code']
                return render_template('dashboard.html', currentDate=currentDate, currentTime=currentTime, iotDevices=iotDevices)
    except:
        session['loggedIn']=False
        return redirect(url_for('login'))
    
@app.route('/addIoT', methods=['GET', 'POST'])
def addIoT(errorMassage = " "):
    try:
        if not session['loggedIn']:
            return redirect(url_for('login'))
        else:
            if request.method =='POST':
                ioTCode=request.form['IoTCode']
                uName=session['username']
                status=user.addIoT(userName=uName, code=ioTCode)
                
                if status:
                    errorMassage='IoT device added successfully'
                    return render_template('addIoT.html', errorMassage=errorMassage)
                else:
                    errorMassage='IoT device setup failed'
                    return render_template('addIoT.html', errorMassage=errorMassage)
            else:
                return render_template('addIoT.html', errorMassage=errorMassage) 
    except:
        session['loggedIn']=False
        return redirect(url_for('login'))

@app.route('/IoTDevice/<deviceID>', methods=['GET', 'POST'])
def IoT(deviceID):
    try:
        if not session['loggedIn']:
            return redirect(url_for('login'))
        else:
            if request.method =="POST":
                threshold=request.form['range']
                print(threshold)
            else:
                iotData=firebase.getValues(key=deviceID)
            return render_template('IoTDevice.html', deviceID=deviceID, iotData=iotData)
    except:
        session['loggedIn']=False
        return redirect(url_for('login'))
    
@app.route('/deleteIoTDevice/<deviceID>', methods=['GET', 'POST'])
def deleteIoTDevice(deviceID):
    try:
        if not session['loggedIn']:
            return redirect(url_for('login'))
        else:
            uName=session['username']
            status=user.deleteIoT(userName=uName, code=deviceID)
            if status:
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('IoT', deviceID=deviceID))
    except:
        session['loggedIn']=False
        return redirect(url_for('login'))
    
    
@app.route('/editIoTDevice/<deviceID>', methods=['GET', 'POST'])
def editIoTDevice(deviceID, errorMassage = " "):
    try:
        if not session['loggedIn']:
            return redirect(url_for('login'))
        else:
            _, loggedUser=user.getUserByUserName(userName=session['username'])
            
            location=loggedUser['location']
            
            if request.method =='POST':
                uName=session['username']
                newDeviceID=request.form['IoTCode']
                
                if deviceID != newDeviceID:
                    status=user.editIoT(userName=uName, code=deviceID, newCode=newDeviceID)
                    if status:
                        return redirect(url_for('IoT', deviceID=newDeviceID))
                    else:
                        errorMassage="couldn't not change IoT device"
                        return render_template('editIoT.html', deviceID=deviceID, location=location, errorMassage=errorMassage)
                else:
                    errorMassage="Your new device ID is too similar to one of your device ID"
                    return render_template('editIoT.html', deviceID=deviceID, location=location, errorMassage=errorMassage)
            else:
                return render_template('editIoT.html', deviceID=deviceID, location=location, errorMassage=errorMassage)
    except:
        session['loggedIn']=False
        return redirect(url_for('login'))
    
    
@app.route('/adminDashboard', methods=['GET', 'POST'])
def adminDashboard():
    try:
        if not session['loggedIn']:
            return redirect(url_for('login'))
        else:
            if session['adminUserFlag']:
                nonAdminUserCount=admin.getDocumentCount(collectionName='Users', adminUserFlag='False')
                adminCount=admin.getDocumentCount(collectionName='Users', adminUserFlag='True')
                productCount=admin.getDocumentCount(collectionName='Products')
                
                return render_template('adminDashboard.html', nonAdminUserCount=nonAdminUserCount, productCount=productCount, adminCount=adminCount)
                
            elif not session['adminUserFlag']:
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('login'))
    except:
        session['loggedIn']=False
        return redirect(url_for('login'))
            
    
@app.route('/addUser', methods=['GET', 'POST'])
def addUser(errorMassage=" "):
    try:
        if not session['loggedIn']:
            return redirect(url_for('login'))
        else:
            if session['adminUserFlag']:
                if request.method=='POST':
                    name=request.form['name']
                    phoneNumber=request.form['phoneNumber']
                    uName=request.form['username']
                    password=request.form['password']
                    adminUserFlag=request.form['gridRadios']
                    
                    status=user.addUser(name=name, phoneNumber=phoneNumber,userName=uName, password=password,adminUserFlag=adminUserFlag)
                    if status:
                        errorMassage="User added successfully."
                    else:
                        errorMassage="Failed adding user."
                return render_template('addUser.html', errorMassage=errorMassage)
            else:
                return redirect(url_for('login'))
    except:
       session['loggedIn']=False
       return redirect(url_for('login'))


@app.route('/addProduct', methods=['GET', 'POST'])
def addProduct(errorMassage=" "):
    try:
        if not session['loggedIn']:
            return redirect(url_for('login'))
        else:
            if session['adminUserFlag']:
                if request.method=='POST':
                    fertilizerName=request.form['fertilizerName']
                    useFor=request.form['useFor']
                    fertilizerType=request.form['fertilizerType']
                    manufacturer=request.form['manufacturer']
                    status=product.addProduct(fertilizerName=fertilizerName, useFor=useFor, fertilizerType=fertilizerType, manufacturer=manufacturer)
                    if status:
                        errorMassage="Product successfully added."
                    else:
                        errorMassage="Failed adding product."
                        
                    return render_template('addProduct.html', errorMassage=errorMassage)   
                else: 
                    return render_template('addProduct.html', errorMassage=errorMassage)
            else:
                return redirect(url_for('login'))
    except:
       session['loggedIn']=False
       return redirect(url_for('login'))



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    try:
        if session['loggedIn']:
            session.clear()
            session['loggedIn']=False
            return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    except:
        session['loggedIn']=False
        return redirect(url_for('login'))
        


@app.errorhandler(404)
def pageNotFound(e):
    return render_template('pageNotFound.html'), 404

@app.errorhandler(400)
def badRequest(e):
    return render_template('badRequest.html'), 400

@app.route('/youAreOffline')
def youAreOffline():
    return render_template('youAreOffline.html'), 503 


@app.route('/profile', methods=['GET', 'POST'])
def profile(status=" "):
    try:
        if session['loggedIn']:
            _, loggedUser=user.getUserByUserName(userName=session['username'])
            name=loggedUser['name']
            phoneNumber=loggedUser['phoneNumber'] 
            location=loggedUser['location']
            country=loggedUser['country']
                        
            return render_template('profile.html', status=status, name=name, country=country, location=location, phoneNumber=phoneNumber)
        else:
            return redirect(url_for('login'))
    except:
        session['loggedIn']=False
        return redirect(url_for('login'))
    
    
    
@app.route('/changeProfile', methods=['GET', 'POST'])
def changeProfile(status=" "):
    try:
        if session['loggedIn']:
            if request.method == 'POST':
                uName=session['username']
                name=request.form['name']
                userNameEdited=request.form['username']
                country=request.form['country']
                location=request.form['location']
                phoneNumber=request.form['phoneNumber']
                
                status=user.updateUser(userName=uName, name=name, userNameEdited=userNameEdited, country=country, location=location, phoneNumber=phoneNumber)
                
                session['username']=userNameEdited
                
                _, loggedUser=user.getUserByUserName(userName=session['username'])
                name=loggedUser['name']
                phoneNumber=loggedUser['phoneNumber'] 
                location=loggedUser['location']
                country=loggedUser['country']
                
                return render_template('profile.html', status=status, name=name, country=country, location=location, phoneNumber=phoneNumber) 
            else:
                
                _, loggedUser=user.getUserByUserName(userName=session['username'])
                name=loggedUser['name']
                phoneNumber=loggedUser['phoneNumber'] 
                location=loggedUser['location']
                country=loggedUser['country']
                
                return render_template('profile.html', status=status, name=name, country=country, location=location, phoneNumber=phoneNumber) 
        else:
            _, loggedUser=user.getUserByUserName(userName=session['username'])
            name=loggedUser['name']
            phoneNumber=loggedUser['phoneNumber'] 
            location=loggedUser['location']
            country=loggedUser['country']
            
            return render_template('profile.html', status=status, name=name, country=country, location=location, phoneNumber=phoneNumber) 
    except:
        session['loggedIn']=False
        return redirect(url_for('login'))
    
    
     
@app.route('/changePassword', methods=['POST'])
def changePassword(status=" "):
    try:
        if session['loggedIn']:
            if request.method == 'POST':
                uName=session['username']
                password=request.form['password']
                newpassword=request.form['newpassword']
                renewpassword=request.form['renewpassword']
                
                _, loggedUser=user.getUserByUserName(userName=session['username'])
                name=loggedUser['name']
                phoneNumber=loggedUser['phoneNumber'] 
                location=loggedUser['location']
                country=loggedUser['country']
                
                if newpassword == renewpassword:
                    if newpassword != password:
                        status=user.changePassword(userName=uName, oldPassword=password, newPassword=newpassword)
                        return render_template('profile.html', status=status, name=name, country=country, location=location, phoneNumber=phoneNumber)
                    else:
                        status="Your new password is too similar to one of your new password."
                        return render_template('profile.html', status=status, name=name, country=country, location=location, phoneNumber=phoneNumber) 
                else:
                    status="Can not change password."
                    return render_template('profile.html', status=status, name=name, country=country, location=location, phoneNumber=phoneNumber) 
            else:
                return render_template('profile.html', status=status, name=name, country=country, location=location, phoneNumber=phoneNumber)
        else:
            return redirect(url_for('login'))
    except:
        session['loggedIn']=False
        return redirect(url_for('login'))
    
@app.route('/deleteUser', methods=['GET', 'POST'])
def deleteUser(status=" "):
    try:
        if session['loggedIn']:
            if request.method == 'POST':
                password=request.form['password']
                rePassword=request.form['rePassword']
                                
                if password == rePassword:
                    status=user.deleteUser(userName=session['username'], password=password)
                    return redirect(url_for('logout'))
                else:
                    status='Can not delete account'
                    return render_template('profile.html', status=status) 
            else:
                return render_template('profile.html', status=status)
        else:
            return redirect(url_for('login'))
    except:
        session['loggedIn']=False
        return redirect(url_for('login'))
    
@app.route('/needHelp', methods=['GET', 'POST'])
def needHelp():
    try:
        if not session['loggedIn']:
            return redirect(url_for('login'))
        else:
            return render_template('needHelp.html')
    except:
        session['loggedIn']=False
        return redirect(url_for('login'))
    
    
@app.route('/weatherForecast', methods =['GET', 'POST'])
def weatherForecast():
    try:
        if session['loggedIn']:
            _, loggedUser=user.getUserByUserName(userName=session['username'])
            
            location=loggedUser['location']
            
            weatherDataJson, weatherForecastJson, airPollutionDataJson=weather.getAllWeatherData(location=location)
            
            currentDate=datetime.now().date()
            currentTime=datetime.now().time().strftime('%H:%M:%S')
            
            if weatherDataJson or weatherForecastJson or airPollutionDataJson:
                return render_template('weatherForecast.html', weatherDataJson=weatherDataJson, currentDate=currentDate, currentTime=currentTime, location=location, airPollutionDataJson=airPollutionDataJson, weatherForecastJson=weatherForecastJson)
            else:
                return redirect(url_for('youAreOffline'))
        else:
            return redirect(url_for('login'))
    except:
        session['loggedIn']=False
        return redirect(url_for('login'))
     
     
@app.route('/diseasePrediction', methods =['GET', 'POST'])
def diseasePrediction(pred=" ", confidence=0, recommendedProducts=None):
    try:
        if session['loggedIn']:
            if request.method == 'POST':
                imageFile=request.files['file']
                filePath=imageFile.name
                imageFile.save(secure_filename(filePath))
                pred, confidence=prediction.makePrediction(imagePath=filePath)
                recommendedProducts=product.recommendProducts(useFor=pred)
                return render_template('prediction.html', pred=pred, confidence=confidence, recommendedProducts=recommendedProducts)
            else:
                return render_template('prediction.html', pred=pred, confidence=confidence, recommendedProducts=recommendedProducts)
        else:
            return redirect(url_for('login'))
    except:
        session['loggedIn']=False
        return redirect(url_for('login'))
     
@app.route('/fertilizers', methods =['GET', 'POST'])
def fertilizers():
    try:
        if session['loggedIn']:
            fertilizers =product.showAllProducts()
            return render_template('fertilizers.html', fertilizers=fertilizers)
        else:
            return redirect(url_for('login'))
    except:
        session['loggedIn']=False
        return redirect(url_for('login'))
     
            
if __name__=="__main__":
    app.run(debug=True, port=8080)
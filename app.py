from flask import Flask, render_template, request
import pickle


# loadng models
##########################################################################################################################
file = open("model.pkl","rb")
model = pickle.load(file)
file.close()


file = open("le.pkl","rb")
le = pickle.load(file)
file.close()

##########################################################################################################################
app = Flask(__name__, template_folder='./templates',static_folder='./static')


@app.route("/")
def hello():
    return render_template("home.html")


@app.route("/", methods = ['post'])
def submit():
    year = int(request.form["Year"])
    driven = float(request.form["Driven"])
    brand = request.form["brand"]
    le_brand = le.transform([brand])[0]
    
    if request.form["Fuel_Type"] == "Petrol":
        fuel_Diesel=0
        fuel_Petrol=1
    elif request.form["Fuel_Type"] == "Diesel":
        fuel_Diesel=1
        fuel_Petrol=0
    else:
        fuel_Diesel=0
        fuel_Petrol=0
        
    if request.form["Seller_Type_Individual"]=="Dealer":
        seller_type_Individual=0
    else:
        seller_type_Individual=1
        
    
    if request.form["Transmission_Mannual"]=="Mannual":
        transmission_Manual = 1
    else:
        transmission_Manual = 0
        
    
    owner = int(request.form["Owner"])
    if owner == 1:
        o2 = 0
        o3 = 0 
        o4 = 0
    elif owner == 2:
        o2 = 1
        o3 = 0 
        o4 = 0
    elif owner == 3:
        o2 = 0
        o3 = 1
        o4 = 0
    else:
        o2 = 0
        o3 = 0
        o4 = 1
    old = 2020-year
    text = model.predict([[le_brand,year,driven,fuel_Diesel,fuel_Petrol,seller_type_Individual,transmission_Manual,o2,o3,o4,old]])
    text = round(text[0],2)
    return render_template("home.html", result = text)


if __name__=="__main__":
    app.run()
from flask import Flask, request, render_template
import pickle
import pandas as pd
import sqlite3

app = Flask(__name__)
f=open("Model//model.pkl",'rb')
model=pickle.load(f)

con=sqlite3.connect("new_schema")
cur=con.cursor()
cur.execute("DROP TABLE IF EXISTS login;")
cur.execute("CREATE TABLE login(`username` char(20), `password` char(20));")
cur.execute('''INSERT INTO login VALUES("Rohan","abc"),("Parthiv","123"),("xyz","xyz"),("abc","xyz");''')
con.commit()

df=pd.read_sql("SELECT * FROM login",con)

@app.route("/")
def main():
    return render_template("Login.html")

@app.route("/verify", methods=['Post'])
def Verify():
    uname,pwd=list(request.form.values())
    if (df[df['username']==uname].password==pwd).all():
        return render_template("index.html")
    return render_template("LoginFailure.html")
    

@app.route("/predict", methods=['Post'])
def pred():
    print("clicked")
    formvalues=request.form.values()
    features=[float(i) for i in formvalues]
    return render_template("success.html",val=int(model.predict([features])))

if __name__=='__main__':
    app.run(host='localhost',port=5000)

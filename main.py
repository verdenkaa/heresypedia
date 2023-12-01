from flask import * 
from database_setup import *


app = Flask(__name__) 

engine = create_engine("sqlite:///data.db")
session = Session(bind=engine)

@app.route('/') 
@app.route('/index/<persons>') 
def index(): 
      return render_template('index.html', persons=["LEGION PRAETOR", "LEGION CATAPHRACTII PRAETOR"]) 

@app.route('/solider') 
def solider():
      name = request.args.get('warrior')
      spec = session.query(Solider).filter(Solider.name == name).first()
      wargear=spec.wargear.replace("\n", " ").split(" • ")
      print(wargear)
      wargear_names = [session.query(Weapons).filter(Weapons.name == x).first() for x in wargear]
      print(wargear_names)
      return render_template('solider.html', warrior=spec.name, type=spec.type, points=spec.points, wargear=wargear, wargear_names=wargear_names)

if __name__ == '__main__': 
   app.run(debug = True)
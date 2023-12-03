from flask import * 
from database_setup import *


app = Flask(__name__) 

engine = create_engine("sqlite:///data.db")
session = Session(bind=engine)

@app.route('/') 
@app.route('/index/<persons>') 
def index(): 
      li = [i[0] for i in session.query(Solider.name).all()]
      return render_template('index.html', persons=li) 

@app.route('/solider') 
def solider():
      name = request.args.get('warrior')
      spec = session.query(Solider).filter(Solider.name == name).first()
      wargear=spec.wargear.replace("\n", " ").split(" • ")
      #print(wargear)
      wargear_names = [session.query(Weapons).filter(Weapons.name == x).first() for x in wargear]
      #print(wargear_names)

      #  ДОБАВИТЬ СЮДА ЗАПРОС ПО ТАБЛИЦЕ СПОСОБНОСТЕЙ

      options = [i.split("- ") for i in spec.Options.split("\n")]
      print(options[1])
      print(len(options))
      return render_template('solider.html', warrior=spec.name, type=spec.type, points=spec.points, wargear=wargear_names, param=spec.Parameters.split(),
                             srules=spec.Srules.replace("\n", " ").split(" • "), options=options)

if __name__ == '__main__': 
   app.run(debug = True)
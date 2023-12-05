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

@app.route('/solider', methods=['GET', 'POST']) 
def solider():
      added_wargear = ["Please choose wargear"]
      

      name = request.args.get('warrior')
      spec = session.query(Solider).filter(Solider.name == name).first()
      wargear=spec.wargear.replace("\n", " ").split(" • ")
      #print(wargear)
      #wargear_names = [session.query(Weapons).filter(Weapons.name == x).first() for x in wargear if str(x) is None]
      #print(wargear_names)
      added_wargear = wargear
      if request.method == 'POST':
            added_wargear = request.form.getlist('s_wargear')
            added_wargear += request.form.getlist('o_wargear')
      #added_wargear = tuple(frozenset(added_wargear))
           
      #print(wargear_names)

      #  ДОБАВИТЬ СЮДА ЗАПРОС ПО ТАБЛИЦЕ СПОСОБНОСТЕЙ

      options = [i.split("- ") for i in spec.Options.split("• ")]
      #print(options[1])
      #print(len(options))
      #print(options[1])
      return render_template('solider.html', spec = spec, wargear=wargear, param=spec.Parameters.split(),
                             srules=spec.Srules.replace("\n", " ").split(" • "), options=options, added_wargear=added_wargear)

if __name__ == '__main__': 
   app.run(debug = True)
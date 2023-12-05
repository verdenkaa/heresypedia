from flask import * 
from objects import *
import re


def replacer_number_X(a):
      return a.replace("1", "X").replace("2", "X").replace("3", "X").replace("4", "X").replace("5", "X").replace("6", "X").replace("7", "X").replace("8", "X").replace("9", "X").replace("+", "")

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

      added_wargear = wargear
      if request.method == 'POST':
            added_wargear = request.form.getlist('s_wargear')
            added_wargear += request.form.getlist('o_wargear')


      #  ДОБАВИТЬ СЮДА ЗАПРОС ПО ТАБЛИЦЕ СПОСОБНОСТЕЙ

      options = [i.split("- ") for i in spec.Options.split("• ")]

      weapon_spec = []
      wargear_spec = {}
      for i in added_wargear:
           moment_i = session.query(Weapons).filter(Weapons.name == replacer_number_X(i)).first()
           if moment_i is not None:
                  if moment_i.Class == "w":
                        weapon_spec.append(moment_i)
                  else:
                        wargear_spec[moment_i.name] = moment_i.Type
      weapon_abil = {}
      for i in weapon_spec:
           for j in i.Type.split(", "):
                  #j = re.sub(r'[^\w\s]+|[\d]+', r'',j).strip().rstrip()
                  #print(session.query(W_abilites).first())
                  moment_i = session.query(W_abilites).filter(W_abilites.name == replacer_number_X(j)).first()
                  if moment_i is not None:
                        weapon_abil[moment_i.name] = moment_i.ability

      srules_spec = {}
      for i in spec.Srules.replace("\n", " ").split(" • "):
            print(i)
            moment_i = session.query(Srules).filter(Srules.name == replacer_number_X(i)).first()
            if moment_i is not None:
                        srules_spec[replacer_number_X(i)] = moment_i.ability


      return render_template('solider.html', spec = spec, wargear=wargear, param=spec.Parameters.split(),
                             srules=spec.Srules.replace("\n", " ").split(" • "), options=options, added_wargear=added_wargear,
                               compos=spec.compos.split("• "), unit_type=spec.unit_type, weapon_spec=weapon_spec, wargear_spec=wargear_spec,
                               weapon_abil=weapon_abil, srules_spec=srules_spec)

#if __name__ == '__main__': 
   #app.run(debug = True)
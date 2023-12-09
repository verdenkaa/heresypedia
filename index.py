from flask import * 
from objects import *
import re


def replacer_number_X(a):
      return a.replace("1", "").replace("2", "").replace("3", "").replace("4", "").replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "").replace("+", "").replace("(", "").replace(")", "").replace(" ", "").replace('"', "")

def replacer_number(a):
      return a.replace("1", "").replace("2", "").replace("3", "").replace("4", "").replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "").replace("+", "").replace("(", "").replace(")", "")

COMBI_WEAPON = {"Magna combi-weapon": ["Bolter (Primary)/Meltagun (Secondary)", "Bolter (Primary)/Plasma gun (Secondary)", "Bolter (Primary)/Disintegrator (Secondary)"],
                "Minor combi-weapon": ["Bolter (Primary)/Flamer (Secondary)", "Bolter (Primary)/Volkite charger (Secondary)", "Bolter (Primary)/Grenade launcher (Secondary)"],
                "Power weapon": ["Power sword", "Power axe", "Power maul", "Power lance"]} #  Список компи вооружения

app = Flask(__name__) 

engine = create_engine("sqlite:///data.db")
session = Session(bind=engine)


@app.route('/') 
@app.route('/index/<persons>') 
def index(): 
      persons = [i for i in session.query(Solider).all()]
      persons_list = {"HQ": [], "ELITES": [], "TROOPS": [], "DEDICATED TRANSPORT": [], "FAST ATTACK": [], "HEAVY SUPPORT": [], "LORDS OF WAR": []}
      for i in persons:
            persons_list[i.type].append(i.name)
      print(persons_list)
      return render_template('index.html', persons=persons_list) 

@app.route('/solider', methods=['GET', 'POST']) 
def solider():
      
      name = request.args.get('warrior')
      spec = session.query(Solider).filter(Solider.name == name).first()
      wargear=spec.wargear.replace("\n", " ").split(" • ") #  первичное вооружение

      added_wargear = wargear
      if request.method == 'POST': #  получение списка взятого вооружения
            added_wargear = request.form.getlist('s_wargear')
            added_wargear += request.form.getlist('o_wargear')

      added_wargear_rework = []
      for i in range(len(added_wargear)):
            if "/" in added_wargear[i]:
                added_wargear_rework += added_wargear[i].split("/")
            else:
                  added_wargear_rework.append(added_wargear[i])
      



      options = [i.split("- ") for i in spec.Options.split("• ")] #  вариативные закачки

      weapon_spec = [] #  характеристики оружия
      wargear_spec = {} #  характеристики снаряжения
      for i in added_wargear_rework:
           moment_i = session.query(Weapons).filter(Weapons.name.like(f"{i.split(' (')[0]}%")).first()

           if moment_i is not None:
                  if moment_i.Class == "w": #  если класс оружия
                        weapon_spec.append(moment_i) #  добавляем оружие в виду класса
                  else:
                        wargear_spec[re.sub(r'[^\w\s]+|[\d]+', r'', moment_i.name).strip()] = moment_i.Type #  иначе добавляем в снаряжение в виде строки
      print(wargear_spec)
      weapon_abil = {} #  словарь правил на оружие
      for i in weapon_spec:
            for j in i.Type.split(", "):
                  j2 = re.sub(r'[^\w\s]+|[\d]+', r'', j).strip() #  очищаем все кроме букв
                  moment_i = session.query(Srules).filter(Srules.name.like(f"{j2}%")).first()
                  if moment_i is not None:
                        weapon_abil[j] = moment_i.ability #  добавляем значение способности

      srules_spec = {} #  словарь специальных правил
      for i in spec.Srules.replace("\n", " ").split(" • "):
            moment_i = session.query(Srules).filter(Srules.name.like(f"%{i.split(" (")[0]}%")).first()
            if moment_i is not None:
                        srules_spec[replacer_number(i)] = moment_i.ability #  добавляем значение способности


      return render_template('solider.html', spec = spec, wargear=wargear, param=[ i.split() for i in spec.Parameters.split("<>")],
                             srules=spec.Srules.replace("\n", " ").split(" • "), options=options, added_wargear=added_wargear,
                               compos=spec.compos.split("• "), unit_type=spec.unit_type.split("• "), weapon_spec=weapon_spec, wargear_spec=wargear_spec,
                               weapon_abil=weapon_abil, srules_spec=srules_spec, d_transp=spec.d_transp, COMBI_WEAPON=COMBI_WEAPON)

if __name__ == '__main__': 
   app.run()

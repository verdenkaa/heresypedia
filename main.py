from flask import * 
app = Flask(__name__) 

@app.route('/') 
@app.route('/index/<persons>') 
def index(): 
      return render_template('index.html', persons=["LEGION PRAETO", "LEGION CATAPHRACTII PRAETOR"]) 

@app.route('/solider') 
def solider(): 
      return render_template('solider.html', warrior=request.args.get('warrior'))

if __name__ == '__main__': 
   app.run(debug = True)


from flask import Flask, render_template

from com.kimdonghee.models.seoul.seoul_controller import SeoulController


app = Flask(__name__) 
@app.route('/')
def intro():

    return render_template("/index.html")

@app.route("/seoul") 
def titanic():

    controller = SeoulController()
    controller.modelling("cctv_in_seoul.csv", "crime_in_seoul.csv", "pop_in_seoul.xls")

    return render_template("/seoul.html")


if __name__ == '__main__':  
   app.run(debug=True)

app.config['TEMPLATES_AUTO_RELOAD'] = True

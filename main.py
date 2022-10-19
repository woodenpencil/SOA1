# SEE: https://stackoverflow.com/questions/25978879/how-to-create-chained-selectfield-in-flask-without-refreshing-the-page/49969686#49969686

# flask sqlalchemy

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

# app.py

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import json

# Initialize the Flask application
app = Flask(__name__)

app.config['SECRET_KEY'] = "caircocoders-ednalan"

# sqlite config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\Win10\\source\\flask\\cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind the instance to the 'app.py' Flask application
db = SQLAlchemy(app)


class Regions(db.Model):
    __tablename__ = 'regions'
    region_id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String(250))

    def __repr__(self):
        return '\n region_id: {0} region_name: {1}'.format(self.region_id, self.region_name)

    def __str__(self):
        return '\n region_id: {0} region_name: {1}'.format(self.region_id, self.region_name)


class Districts(db.Model):
    __tablename__ = 'districts'
    district_id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer)
    region_name = db.Column(db.String(250))

    def __repr__(self):
        return '\n district_id: {0} region_id: {1} region_name: {2}'.format(self.district_id, self.region_id, self.region_name)

    def __str__(self):
        return '\n district_id: {0} region_id: {1} region_name: {2}'.format(self.district_id, self.region_id, self.region_name)

class Towns(db.Model):
    __tablename__ = 'town'
    town_id = db.Column(db.Integer, primary_key=True)
    town_name= db.Column(db.String(250))
    district_id = db.Column(db.Integer)
    town_type = db.Column(db.String(250))
    population = db.Column(db.Integer)

    def __init__(self, district_id, town_name, town_type, population):
        self.town_name=town_name
        self.district_id=district_id
        self.town_type = town_type
        self.population = population


def get_dropdown_values():
    """
    dummy function, replace with e.g. database call. If data not change, this function is not needed but dictionary
could be defined globally
    """

    # Create a dictionary (myDict) where the key is
    # the name of the brand, and the list includes the names of the car models
    #
    # Read from the database the list of cars and the list of models.
    # With this information, build a dictionary that includes the list of models by brand.
    # This dictionary is used to feed the drop down boxes of car brands and car models that belong to a car brand.
    #
    # Example:
    #
    # {'Toyota': ['Tercel', 'Prius'],
    #  'Honda': ['Accord', 'Brio']}

    regions = Regions.query.all()
    # Create an empty dictionary
    myDict = {}
    for p in regions:

        key = p.region_name
        region_id = p.region_id

        # Select all car models that belong to a car brand
        q = Districts.query.filter_by(region_id=region_id).all()

        # build the structure (lst_c) that includes the names of the car models that belong to the car brand
        lst_c = []
        for c in q:
            lst_c.append(c.region_name)
        myDict[key] = lst_c

    class_entry_relations = myDict

    return class_entry_relations


@app.route('/_update_dropdown')
def update_dropdown():
    # the value of the first dropdown (selected by the user)
    selected_class = request.args.get('selected_class', type=str)
    updated_values = get_dropdown_values()[selected_class]

    # create the value sin the dropdown as a html string
    html_string_selected = ''
    for entry in updated_values:
        html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

    return jsonify(html_string_selected=html_string_selected)
'''
@app.route('/_update_towns')
def update_towns():
    # the value of the second dropdown (selected by the user)
    selected_entry = request.args.get('selected_entry', type=str)
    print(selected_entry)
    # get values for the second dropdown
    #updated_values = get_dropdown_values()[selected_class]

    # create the value sin the dropdown as a html string
    #html_string_selected = ''
    #for entry in updated_values:
    #    html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

    return jsonify(html_string_towns="")
'''

@app.route('/_process_data')
def process_data():
    selected_class = request.args.get('selected_class', type=str)
    selected_entry = request.args.get('selected_entry', type=str)
    selected_towns = request.args.get('selected_town', type=str)
    #print(selected_class)
    #print(selected_entry)
    sel = Districts.query.filter_by(region_name=selected_entry).first().district_id
    selected_towns = Towns.query.with_entities(Towns.town_name, Towns.district_id, Towns.town_type, Towns.population).filter_by(district_id=sel)
    #print(selected_towns.all())
    res = selected_towns.all()
    #print(res)
    for i in range(len(res)):
        t = res[i]
        t = list(t)
        t[1] = selected_entry
        res[i] = t
    #dis_id = map(lambda x: x[1]=selected_entry, res)
    #res = list(res)
    print(res)
    #if len(res)>1:
    #    res = ';'.join(res)
    # process the two selected values here and return the response; here we just create a dummy string

    return jsonify(
        random_text="Вы выбрали {} область {} район.{}".format(selected_class, selected_entry, res))


@app.route('/')
def index():
    """
    initialize drop down menus
    """

    class_entry_relations = get_dropdown_values()

    default_classes = sorted(class_entry_relations.keys())
    default_values = class_entry_relations[default_classes[0]]

    return render_template('index.html',
                           all_classes=default_classes,
                           all_entries=default_values)



@app.route('/addtown', methods=('GET', 'POST'))
def addtown():
    """
    add data to db from form
    """
    if request.method == 'POST':
        district = request.form['district']
        town = request.form['town']
        sel = Districts.query.filter_by(region_name=district)

        if not district:
            flash('Введите название района!')
        elif sel.all()==[]:
            flash('Не найдено районов')
        elif not town:
            flash('Введите название населенного пункта')
        else:
            newtown = Towns(sel.first().district_id, town)
            db.session.add(newtown)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('addtown.html')


@app.route('/deletetown', methods=('GET', 'POST'))
def deletetown():
    """
    delete data from db from form
    """
    if request.method == 'POST':
        district = request.form['district']
        town = request.form['town']
        sel = Districts.query.filter_by(region_name=district)
        if not district:
            flash('Введите название района!')
        elif sel.first()==None:
            flash('Не найдено районов')
        elif not town:
            flash('Введите название населенного пункта')
        else:
            Towns.query.filter_by(town_name=town).delete()
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('deletetown.html')

@app.route('/edittown', methods=('GET', 'POST'))
def edittown():
    """
    edit data at db from form
    """
    if request.method == 'POST':
        district = request.form['district']
        town = request.form['town']
        newtown = request.form['newtown']
        population = request.form['population']
        newtype = request.form['type']
        population = int(population)
        #print(newtown)
        #print(population)
        #print(newtype)

        sel = Districts.query.filter_by(region_name=district)
        newtown = newtown[1:]
        newtype = newtype[1:]
        if not district:
            flash('Введите название района!')
        elif sel.first()==None:
            flash('Не найдено районов')
        elif not town:
            flash('Введите название населенного пункта')
        else:
            town = town[1:]
            sel = Towns.query.filter_by(town_name=town).first().town_id
            sel_dis = Towns.query.filter_by(town_name=town).first().district_id
            selected_towns = Towns.query.with_entities(Towns.town_name, Towns.district_id).filter_by(town_id=sel).first()
            Towns.query.filter_by(town_name=town).delete()
            print(selected_towns)
            #print(newtown)
            newt = Towns(selected_towns[1], newtown, newtype, population)
            db.session.add(newt)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('edittown.html')

if __name__ == '__main__':
    app.run(debug=True)
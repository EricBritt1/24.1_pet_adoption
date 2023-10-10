from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.app_context().push()


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "GOTEMLOLOLOLOLXX"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
db.create_all()



@app.route("/")
def show_list():
    """
    Generates lists of all pets in database regardless of availability!
    """
    pets = Pet.query.all()

    return render_template("pet_list.html", pets=pets)

@app.route('/add', methods=["GET", "POST"])
def add_pet_form():
    """Importing AddPetForm() from logic py (Uses WTForms). Generates form that allows us to add pets to our database using our Pet model found in models.py"""
    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        pet=Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(pet)
        db.session.commit()
        
        return redirect('/')
    else:
        return render_template('pet_form.html', form=form)

@app.route('/pet_information/<int:pet_id>')
def pet_information(pet_id):
    """After clicking link on '/' by animal photo will generate this page full of facts about them"""
    pet = Pet.query.get_or_404(pet_id)
    return render_template('pet_information.html', pet=pet)

@app.route('/pet_information/<int:pet_id>/edit', methods=["GET", "POST"])
def edit_pet_information(pet_id):
    """Using imported EditPetForm from forms.py. Generates a form that allows us to edit SOME pet information stored in database object."""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.available = form.available.data
        pet.notes = form.notes.data
        db.session.commit()
        return redirect(f'/pet_information/{pet_id}')

    else: 
        return render_template('edit_pet_information.html', form=form, pet=pet)


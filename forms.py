from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, URLField, BooleanField
from wtforms.validators import InputRequired, Optional, ValidationError

def field_age(form, field):
    if field.data < 1 or field.data > 29:
        raise ValidationError(f'Field {field.label.text} must be between 0 to 30')

def field_species(form,field):
    if field.data != "dog" and field.data != "cat" and field.data != "porcupine":
        raise ValidationError(f'Field {field.label.text} must be either cat, dog, or porcupine')

class AddPetForm(FlaskForm):

    name  = StringField("Name", validators=[InputRequired()])
    species = StringField("Species", validators=[InputRequired(), field_species])
    photo_url = URLField("Photo URL", validators=[Optional()])
    age = IntegerField("Age", validators=[Optional(), field_age])
    notes = TextAreaField("Notes", [Optional()])

class EditPetForm(FlaskForm):
    photo_url = URLField("Photo URL", validators=[Optional()])
    notes = TextAreaField("Notes", [Optional()])
    available = BooleanField("Available?")
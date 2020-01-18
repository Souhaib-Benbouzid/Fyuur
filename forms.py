from datetime import datetime
from flask_wtf import Form, FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField,BooleanField
from wtforms.validators import DataRequired, AnyOf, URL,ValidationError
from enum import Enum
from app import Genre

def validate_genre(form, field):
    genres_entered = field.data
    exists = False

    for genre in genres:
        genre_object = Genre.query.filter_by(genre=genre).first()
        if genre_object:
            exists = True
    if not exists:
        raise ValidationError("pick a genre")



class VenueForm(FlaskForm):
    """ New Venue """

    name = StringField(
        'name', validators=[DataRequired('Please Enter Your Name!')]
    )
    city = StringField(
        'city', validators=[DataRequired('Please Enter Your City!')]
    )
    state = SelectField(
        'state', validators=[DataRequired('Please Enter Your State')],
        choices=[]
    )
    address = StringField(
        'address', validators=[DataRequired('Please Enter Your Address')]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link', validators=[DataRequired('Please Enter an Image link'), URL()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction [done]
        'genres', 
        validators=[DataRequired(),validate_genre],
        choices=[]
    )
    facebook_link = StringField(
        'facebook_link', validators=[DataRequired('Please Enter Your Facebook link!'),URL()]
    )
    website_link = StringField(
        'website_link', validators=[DataRequired('Please Enter Your Website link!'),URL()]
    )
    seeking_talent = BooleanField(
        'seeking_talent', 
    )
    seeking_description = StringField('seeking_description', validators=[DataRequired('Describe The Talent You are looking For')])

    # enum restriction on genre


# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM

# NEW SHOW
class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

# NEW ARTIST
class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[]
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[]
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
    )
    

""" 
# add states to the database

states =[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]

for choice in states:
    state = State(state=choice[0])
    db.session.add(state)

# add genres to the database

  geners=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]


for choice in geners:
    state = State(state=choice[0])
    db.session.add(state)

"""
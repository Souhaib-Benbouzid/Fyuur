#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from logging import Formatter, FileHandler
import logging
from forms import *
from config import SQLALCHEMY_DATABASE_URI
import pytz
import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')  
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database [Done]
app.config['SQLALCHEMY_DATABASE_URI'] =  SQLALCHEMY_DATABASE_URI
app.config['WHOOSH_BASE'] = 'whoosh/base'
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



class VenueGenre(db.Model):
    __tablename__ = 'venue_genre'
    __table_args__ = (db.UniqueConstraint('name','venue'),)
  
    id = db.Column(db.Integer, primary_key = True, )
    name = db.Column(db.String(50),nullable = False)
    venue = db.Column(db.Integer, db.ForeignKey('venue.id'))
    
    def __repr__(self):
      return '<id: {}, name: {},venue: {},>'.format( self.id, self.name, self.venue)
  
class ArtistGenre(db.Model):
    __tablename__ = 'artist_genre'
    __table_args__ = (db.UniqueConstraint('name','artist'),)
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key = True, )
    name = db.Column(db.String(50),nullable = False)
    artist = db.Column(db.Integer, db.ForeignKey('artist.id'))
   

    def __repr__(self):
      return '<id: {}, name: {},artist: {},>'.format( self.id, self.name, self.artist)
  
class Venue(db.Model):
    __tablename__ = 'venue'
    __table_args__ = (db.UniqueConstraint('name','city','state','address'),)


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    address = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120), nullable = False)
    image_link = db.Column(db.String(500), nullable = False)
    facebook_link = db.Column(db.String(120), nullable = False)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate [done]
    
    website_link = db.Column(db.String(120), nullable = False)  
    seeking_talent = db.Column(db.Boolean, nullable = False , default = False)
    seeking_description = db.Column(db.String(1200), nullable = True )

    shows = db.relationship('Show', backref = 'venue')
    genres = db.relationship('VenueGenre', backref='venues')

    def __repr__(self):
      return '<id: {}, name: {}, city: {}, state: {}, address: {},genres: {}, phone: {}, image: {}, facebook: {}, website: {}, seeking_talent: {}, seeking_description: {}>'.format( self.id, self.name, self.city, self.state, self.address, self.genres, self.phone, self.image_link, self.facebook_link, self.website_link, self.seeking_talent, self.seeking_description)


class Artist(db.Model):
    __tablename__ = 'artist'
    __table_args__ = (db.UniqueConstraint('name','city','state','phone'),)


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120), nullable = False)
    image_link = db.Column(db.String(500), nullable = False)
    facebook_link = db.Column(db.String(120), nullable = True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate [done]
    website_link = db.Column(db.String(120), nullable = True)
    seeking_venues = db.Column(db.Boolean(), nullable = False, default= False)
    seeking_description = db.Column(db.String(120), nullable = True)
    

    # on to many relationship with show (artist is parent table) 
    shows = db.relationship('Show', backref = 'artist')
    genres = db.relationship('ArtistGenre', backref = 'artists')

    def __repr__(self):
      return '<id: {}, name: {}, city: {}, state: {}, genres: {}, phone: {}, image: {}, facebook: {}, website: {}, seeking_venues: {}, seeking_description: {}>'.format( self.id, self.name, self.city, self.state,
      self.genres,self.phone, self.image_link, self.facebook_link, self.website_link, self.seeking_venues, self.seeking_description)
     
       
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. [done]

class Show(db.Model):
    __tablename__ = 'show'
    __table_args__ = (db.UniqueConstraint('artist_id', 'date'),)

    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime(timezone=True), default = datetime.datetime.utcnow, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))

    def __repr__(self):
      return '<id: {}, date: {}, artist_id: {}, venue_id: {}>'.format( self.id, self.date, self.artist_id, self.venue_id,)
  

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#----------------------------------------------------------------------------#

@app.route('/venues')
def venues():
  # TODO: replace with real venues data. [done]
  # num_shows should be aggregated based on number of upcoming shows per venue.
  data= []
  try:   
    # returns all the unique areas in the db
    areas = db.session.query(Venue.city,Venue.state).group_by(Venue.state,Venue.city).all()
    for a in areas:
      area = {
          "city": a[0],
          "state": a[1],
          "venues": []
          }
      # returns all the venues for each unique area in the db
      venues = Venue.query.filter(Venue.state == a[1], Venue.city == a[0]).all()
      
      #create a venue dictionary for each venue in the area
      for v in venues:
        venue_in_the_area = {
            "id": v.id,
            "name": v.name,
            "num_upcoming_shows": Show.query.filter(Show.date > datetime.datetime.now(tz=pytz.UTC), Show.venue_id == v.id).count(),
          }
        area['venues'].append(venue_in_the_area)

      # add the area to the data
      data.append(area)
      
    ''' data=[{
      "city": "San Francisco",
      "state": "CA",
      "venues": [{
        "id": 1,
        "name": "The Musical Hop",
        "num_upcoming_shows": 0,
      }, {
        "id": 3,
        "name": "Park Square Live Music & Coffee",
        "num_upcoming_shows": 1,
      }]
    }, {
      "city": "New York",
      "state": "NY",
      "venues": [{
        "id": 2,
        "name": "The Dueling Pianos Bar",
        "num_upcoming_shows": 0,
      }]
    }]
    '''
  except:
    db.session.rollback()
  finally:
    db.session.close()
    if data:
      return render_template('pages/venues.html', areas=data)
    else:
      return render_template('errors/404.html')

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.[done]
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  word ='%{}%'.format(request.form["search_term"])
  results = Venue.query.filter(Venue.name.ilike(word)).all()
  response = {
    "count": len(results),
    "data": []
  }

  for r in results:
    result = {
      "id": r.id,
      "name": r.name,
      "num_upcoming_shows": Show.query.filter(Show.date > datetime.datetime.now(tz=pytz.UTC), Show.venue_id == r.id).count(),
    }
    response["data"].append(result)

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id [done]
  data = {}
  try:
    venue = Venue.query.get(venue_id)
    genres = []
    
    # return all genres of the venue in a list
    for genre in venue.genres:
      genres.append(genre.name)
    
    # get upcoming shows
    all_upcoming_shows = Show.query.filter(Show.date > datetime.datetime.now(tz=pytz.UTC), Show.venue_id == venue.id).all()
    upcoming_shows=[]
    for i in range(len(all_upcoming_shows)):
      show = {
        "artist_id": venue.shows[i].artist_id,
        "artist_name": venue.shows[i].artist.name,
        "artist_image_link":venue.shows[i].artist.image_link,
        "start_time": venue.shows[i].date.strftime('%Y-%m-%d %H:%M:%S')
      }
      upcoming_shows.append(show)
      
    # get past shows
    all_past_shows = Show.query.filter(Show.date < datetime.datetime.now(tz=pytz.UTC), Show.venue_id == venue.id).all()
    past_shows=[]
    for i in range(len(all_past_shows)):
      show = {
        "artist_id": venue.shows[i].artist_id,
        "artist_name": venue.shows[i].artist.name,
        "artist_image_link":venue.shows[i].artist.image_link,
        "start_time": venue.shows[i].date.strftime('%Y-%m-%d %H:%M:%S')
      }
      past_shows.append(show)
  
    # format the data
    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": Show.query.filter(Show.date < datetime.datetime.now(tz=pytz.UTC), Show.venue_id == venue.id).count(),
        "upcoming_shows_count": Show.query.filter(Show.date > datetime.datetime.now(tz=pytz.UTC), Show.venue_id == venue.id).count(),
    }
  except:
    db.session.rollback()
  finally:
    db.session.close()
    if data:
      return render_template('pages/show_venue.html', venue=data)
    else:
      return render_template('errors/404.html')


  '''  data1={

    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
        }
        data2={
          "id": 2,
          "name": "The Dueling Pianos Bar",
          "genres": ["Classical", "R&B", "Hip-Hop"],
          "address": "335 Delancey Street",
          "city": "New York",
          "state": "NY",
          "phone": "914-003-1132",
          "website": "https://www.theduelingpianos.com",
          "facebook_link": "https://www.facebook.com/theduelingpianos",
          "seeking_talent": False,
          "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
          "past_shows": [],
          "upcoming_shows": [],
          "past_shows_count": 0,
          "upcoming_shows_count": 0,
        }
        data3={
          "id": 3,
          "name": "Park Square Live Music & Coffee",
          "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
          "address": "34 Whiskey Moore Ave",
          "city": "San Francisco",
          "state": "CA",
          "phone": "415-000-1234",
          "website": "https://www.parksquarelivemusicandcoffee.com",
          "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
          "seeking_talent": False,
          "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
          "past_shows": [{
            "artist_id": 5,
            "artist_name": "Matt Quevedo",
            "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
            "start_time": "2019-06-15T23:00:00.000Z"
          }],
          "upcoming_shows": [{
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-01T20:00:00.000Z"
          }, {
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-08T20:00:00.000Z"
          }, {
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-15T20:00:00.000Z"
          }],
          "past_shows_count": 1,
          "upcoming_shows_count": 1,
        }
        data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  '''

   

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET','POST'])
def create_venue_form():

  form = VenueForm()
  information = {
      'name' : form.name.data,
      'city' : form.city.data,
      'state' : form.state.data,
      'address': form.address.data,
      'phone' :  form.phone.data,
      'image_link' : form.image_link.data,
      'genres' : form.genres.data,
      'facebook_link' : form.facebook_link.data,
      'website_link' : form.website_link.data,
      'seeking_talent' : form.seeking_talent.data,
      'seeking_description' : form.seeking_description.data
  }    

  if form.validate_on_submit():
      create_venue_submission(information)

  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create/<venue>')
def create_venue_submission(venue):
  # TODO: insert form data as a new Venue record in the db, instead
  #flash(venue['seeking_description'])
  try:
    #add a venue
    new_venue = Venue(
    name= venue['name'],
    city= venue['city'],
    state= venue['state'],
    address= venue['address'],
    phone= venue['phone'],
    image_link= venue['image_link'],
    facebook_link= venue['facebook_link'],
    website_link= venue['website_link'],
    seeking_talent= venue['seeking_talent'],
    seeking_description= venue['seeking_description'],)
    db.session.add(new_venue)
    db.session.commit()
  
    #add genres
    for genre in venue['genres']:
      new_genre = VenueGenre(name=genre,venue=new_venue.id)
      db.session.add(new_genre)
      db.session.commit()
    # on successful db insert, flash success
    # TODO: modify data to be the data object returned from db insertion
    flash('Venue ' + new_venue.name + ' was successfully listed!')

  except :
    # TODO: on unsuccessful db insert, flash an error instead.
    db.session.rollback()
    flash('An error occurred. Venue ' + venue['name'] + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
 
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  
  
  try:
    VenueGenre.query.filter(VenueGenre.venue==venue_id).delete()
    Show.query.filter(Show.venue_id==venue_id).delete()
    Venue.query.filter(Venue.id==venue_id).delete()
    db.session.commit()
    flash('Venue Deleted!') 
  except:
    flash('An error ocured')
    db.session.rollback()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  finally:
    db.session.close()
    return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = []
  arists = db.session.query(Artist.id,Artist.name).all()
  for artist in arists:
    new_artist = {
      "id": artist[0],
      "name": artist[1]
    }
    data.append(new_artist)
  if data:
    return render_template('pages/artists.html', artists=data)
  else: 
    return render_template('errors/404.html')

  '''data=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }]'''
  

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.[done]
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  word ='%{}%'.format(request.form["search_term"])
  results = Artist.query.filter(Artist.name.ilike(word)).all()
  response = {
    "count": len(results),
    "data": []
  }
  for r in results:
    result = {
      "id": r.id,
      "name": r.name,
      "num_upcoming_shows": Show.query.filter(Show.date > datetime.datetime.now(tz=pytz.UTC), Show.artist_id == r.id).count(),
    }
    response["data"].append(result)

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


'''
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
'''

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id [done]
  data = []
  try:
    artist = Artist.query.get(artist_id)
    genres = []
    
    # return all genres in a list
    for genre in artist.genres:
      genres.append(genre.name)
    # return all past and upcoming shows in lists
    
    # get upcoming shows
    all_upcoming_shows = Show.query.filter(Show.date > datetime.datetime.now(tz=pytz.UTC), Show.artist_id == artist.id).all()
    upcoming_shows=[]
    for i in range(len(all_upcoming_shows)):
      show = {
        "venue_id": artist.shows[i].venue_id,
        "venue_name": artist.shows[i].venue.name,
        "venue_image_link":artist.shows[i].venue.image_link,
        "start_time": artist.shows[i].date.strftime('%Y-%m-%d %H:%M:%S')
      }
      upcoming_shows.append(show)
      
    # get past shows
    all_past_shows = Show.query.filter(Show.date < datetime.datetime.now(tz=pytz.UTC), Show.artist_id == artist.id).all()
    past_shows=[]
    for i in range(len(all_past_shows)):
      show = {
        "venue_id": artist.shows[i].venue_id,
        "venue_name": artist.shows[i].venue.name,
        "venue_image_link":artist.shows[i].venue.image_link,
        "start_time": artist.shows[i].date.strftime('%Y-%m-%d %H:%M:%S')
      }
      past_shows.append(show)
    
    #format data
    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venues,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": Show.query.filter(Show.date < datetime.datetime.now(tz=pytz.UTC), Show.artist_id == artist.id).count(),
        "upcoming_shows_count": Show.query.filter(Show.date > datetime.datetime.now(tz=pytz.UTC), Show.artist_id == artist.id).count(),
    }

  except:
    db.session.rollback()
  finally:
    db.session.close()
    if data:
      return render_template('pages/show_artist.html', artist=data)
    else:
      flash
      return render_template('errors/404.html')

  '''
    data1={
      "id": 4,
      "name": "Guns N Petals",
      "genres": ["Rock n Roll"],
      "city": "San Francisco",
      "state": "CA",
      "phone": "326-123-5000",
      "website": "https://www.gunsnpetalsband.com",
      "facebook_link": "https://www.facebook.com/GunsNPetals",
      "seeking_venue": True,
      "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
      "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "past_shows": [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        "start_time": "2019-05-21T21:30:00.000Z"
      }],
      "upcoming_shows": [],
      "past_shows_count": 1,
      "upcoming_shows_count": 0,
    }
    data2={
      "id": 5,
      "name": "Matt Quevedo",
      "genres": ["Jazz"],
      "city": "New York",
      "state": "NY",
      "phone": "300-400-5000",
      "facebook_link": "https://www.facebook.com/mattquevedo923251523",
      "seeking_venue": False,
      "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "past_shows": [{
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
      }],
      "upcoming_shows": [],
      "past_shows_count": 1,
      "upcoming_shows_count": 0,
    }
    data3={
      "id": 6,
      "name": "The Wild Sax Band",
      "genres": ["Jazz", "Classical"],
      "city": "San Francisco",
      "state": "CA",
      "phone": "432-325-5432",
      "seeking_venue": False,
      "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "past_shows": [],
      "upcoming_shows": [{
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
      }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
      }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
      }],
      "past_shows_count": 0,
      "upcoming_shows_count": 3,
    }
    data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
    return render_template('pages/show_artist.html', artist=data)
  '''

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET','POST'])
def edit_artist(artist_id):
  try:
    artist_info = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist_info)
    
    artist={
      "id": artist_info.id,
      "name": artist_info.name,
      "genres":[genre.name for genre in artist_info.genres ],
      "city": artist_info.city,
      "state": artist_info.state,
      "phone": artist_info.phone,
      "website_link": artist_info.website_link,
      "facebook_link": artist_info.facebook_link,
      "seeking_venue": artist_info.seeking_venues,
      "seeking_description": artist_info.seeking_description,
      "image_link": artist_info.image_link
    }

    if form.validate_on_submit():
        edit_artist_submission(artist_id,form)
        return redirect(url_for('show_artist', artist_id=artist_id))  
    else:
      db.session.rollback()
      #flash(form.seeking_venues.data)
      #flash(form.errors)
      #flash(form.validate_on_submit())
  except:
    db.session.rollback()
  finally:
    db.session.close()
    
  # TODO: populate form with fields from artist with ID <artist_id> [done]
  return render_template('forms/edit_artist.html', form=form, artist=artist)
  
'''artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
}'''

@app.route('/artists/<int:artist_id>/edit/<form>')
def edit_artist_submission(artist_id,form):
  # TODO: take values from the form submitted, and update existing [done]
  # artist record with ID <artist_id> using the new attributes
  try:
    artist = Artist.query.get(artist_id)
    # check data match 
    if artist.name != form.name.data:
      artist.name = form.name.data

    if artist.city != form.city.data:
      artist.city = form.city.data

    if artist.state != form.state.data:
      artist.state = form.state.data

    if artist.phone != form.phone.data:
      artist.phone = form.phone.data

    if artist.website_link != form.website_link.data:
      artist.website_link = form.website_link.data

    if artist.facebook_link != form.facebook_link.data:
      artist.facebook_link = form.facebook_link.data

    if artist.seeking_venues != form.seeking_venues.data:
      artist.seeking_venues = form.seeking_venues.data

    if artist.seeking_description != form.seeking_description.data:
      artist.seeking_description = form.seeking_description.data

    if artist.image_link != form.image_link.data:
      artist.image_link = form.image_link.data
    
    # submit new genres 
    for genre_name in form.genres.data:
      genre = ArtistGenre.query.filter(ArtistGenre.artist==artist_id).delete()
      db.session.commit()

    for genre_name in form.genres.data:
      genre = ArtistGenre(name=genre_name)
      artist.genres.append(genre)
    db.session.add(artist)
    db.session.commit()

  except:
    db.session.rollback()
    flash("An error ocurred, artist couldn't be updated")
  finally:
    db.session.close()

  
@app.route('/venues/<int:venue_id>/edit', methods=['GET','POST'])
def edit_venue(venue_id):
  try:
    venue_info = Venue.query.get(venue_id)
    form = VenueForm(obj=venue_info)
    
    #format data
    venue={
      "id": venue_info.id,
      "name": venue_info.name,
      "genres":[genre.name for genre in venue_info.genres ],
      "city": venue_info.city,
      "state": venue_info.state,
      "phone": venue_info.phone,
      "address": venue_info.address,
      "website_link": venue_info.website_link,
      "facebook_link": venue_info.facebook_link,
      "seeking_talent": venue_info.seeking_talent,
      "seeking_description": venue_info.seeking_description,
      "image_link": venue_info.image_link
    }

    if form.validate_on_submit():
      edit_venue_submission(venue_id,form)
      flash('venue have benn edited sucssesfully')
      return redirect(url_for('show_venue', venue_id=venue_id))   
    else:
      db.session.rollback()
    
  except:
    db.session.rollback()
  finally:
    db.session.close()
    # TODO: populate form with fields from venue with ID <venue_id> [done]
    return render_template('forms/edit_venue.html', form=form, venue=venue)
    
  '''form = VenueForm()
    venue={
      "id": 1,
      "name": "The Musical Hop",
      "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
      "address": "1015 Folsom Street",
      "city": "San Francisco",
      "state": "CA",
      "phone": "123-123-1234",
      "website": "https://www.themusicalhop.com",
      "facebook_link": "https://www.facebook.com/TheMusicalHop",
      "seeking_talent": True,
      "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
      "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    return render_template('forms/edit_venue.html', form=form, venue=venue)
  '''

@app.route('/venues/<int:venue_id>/edit/<form>')
def edit_venue_submission(venue_id,form):
  # TODO: take values from the form submitted, and update existing [done]
  # venue record with ID <venue_id> using the new attributes
  try:
    venue = Venue.query.get(venue_id)

    # match existing data
    if venue.name != form.name.data:
      venue.name = form.name.data

    if venue.city != form.city.data:
      venue.city = form.city.data

    if venue.state != form.state.data:
      venue.state = form.state.data

    if venue.phone != form.phone.data:
      venue.phone = form.phone.data
    
    if venue.address != form.address.data:
      venue.address = form.address.data

    if venue.website_link != form.website_link.data:
      venue.website_link = form.website_link.data

    if venue.facebook_link != form.facebook_link.data:
      venue.facebook_link = form.facebook_link.data

    if venue.seeking_talent != form.seeking_talent.data:
      venue.seeking_talent = form.seeking_talent.data

    if venue.seeking_description != form.seeking_description.data:
      venue.seeking_description = form.seeking_description.data

    if venue.image_link != form.image_link.data:
      venue.image_link = form.image_link.data

    # submit new genres
    for genre_name in form.genres.data:
      genre = VenueGenre.query.filter(VenueGenre.venue==venue_id).delete()
      db.session.commit()

    for genre_name in form.genres.data:
      genre = VenueGenre(name=genre_name)
      venue.genres.append(genre)
    db.session.add(venue)
    db.session.commit()

  except :
    db.session.rollback()
    flash("An error ocurred, venue couldn't be updated")
  finally:
    db.session.close()



#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET','POST'])
def create_artist_form():
  form = ArtistForm()
  artist = {
      'name' : form.name.data,
      'city' : form.city.data,
      'state' : form.state.data,
      'phone' :  form.phone.data,
      'image_link' : form.image_link.data,
      'genres' : form.genres.data,
      'facebook_link' : form.facebook_link.data,
      'website_link' : form.website_link.data,
      'seeking_venues' : form.seeking_venues.data,
      'seeking_description' : form.seeking_description.data
  } 
  if form.validate_on_submit():
      create_artist_submission(artist)

  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create/<artist>')
def create_artist_submission(artist):
  # TODO: insert form data as a new Artist record in the db, instead [done]
  try:
    #add a venue
    new_artist = Artist(
    name= artist['name'],
    city= artist['city'],
    state= artist['state'],
    phone= artist['phone'],
    image_link= artist['image_link'],
    facebook_link= artist['facebook_link'],
    website_link= artist['website_link'],
    seeking_venues= artist['seeking_venues'],
    seeking_description= artist['seeking_description'],)
    db.session.add(new_artist)
    db.session.commit()

    #add genres
    if new_artist.id:
      for genre in artist['genres']:
        new_genre = ArtistGenre(name=genre,artist=new_artist.id)
        db.session.add(new_genre)
        db.session.commit()
    
    # on successful db insert, flash success
    # TODO: modify data to be the data object returned from db insertion
    flash('Artist ' + new_artist.name + ' was successfully listed!')

  except:
    # TODO: on unsuccessful db insert, flash an error instead.
    db.session.rollback()
    flash('An error occurred. Venue ' + artist['name'] + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  finally:
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data. [done]
  # num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  shows = Show.query.all()
  for show in shows:
    new_show = {
    "venue_id": show.venue_id,
    "venue_name": show.venue.name,
    "artist_id": show.artist_id,
    "artist_name": show.artist.name,
    "artist_image_link": show.artist.image_link,
    "start_time": show.date.strftime("%Y-%m-%d %H:%M:%S")
    }
    data.append(new_show)
  if data:
    return render_template('pages/shows.html', shows=data)
  else:
    return render_template('errors/404.html')


'''data=[
    {
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
'''

@app.route('/shows/create', methods=['POST','GET'])
def create_shows():
  form = ShowForm()
  if form.validate_on_submit():
      information = {
        'artist' : form.artist_id.data,
        'venue': form.venue_id.data,
        'date_time' : form.start_time.data.strftime("%Y-%m-%d %H:%M:%S")
      }
      create_show_submission(information)

  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create/<show>')
def create_show_submission(show):
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead [done]
  try:
    add_show = Show(artist_id=show['artist'],venue_id=show['venue'],date=show['date_time'])
    db.session.add(add_show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:  
    # TODO: on unsuccessful db insert, flash an error instead. [done]
    db.session.rollback()
    flash("An error occurred. Show could not be listed.")
  finally:
    db.session.close()
    return render_template('pages/home.html')
    
  # e.g., flash('An error occurred. Show could not be listed.
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# specify port manually:
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


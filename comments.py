""" 
__table_args__ = (db.UniqueConstraint('name', 'address'), )

from app import Artist,Venue, Show,State,Genre,artist_genre,venue_genre
from app import db
state = State(state='KA')
venue = Venue(name='jawhara', city='oran' ,state=1, address='21 kaisa', phone='216-546-1234',image_link='https://www.youtube.com/image',facebook_link='https://www.facebook.com/me',website_link='https://www.me.com/',seeking_talent=True,seeking_description='atcho chwia')

artist = Artist(name='sohaib', city='bousaada' ,state=1, phone='651-214-5244',image_link='https://www.youtube.com/image',facebook_link='https://www.facebook.com/me',website_link='https://www.me.com/',seeking_venues=True,seeking_description='hatolna n5dmo awedi')

objects = [state,artist,venue]

for object in objects:
  db.session.add(object)
db.session.commit()
db.session.rollback()

"""

# from app import db, Artist,Venue,VenueGenre,Show,ArtistGenre
# Artist.query.all()

'''
venue1 = Venue(name='jawhara', city='5245' ,state='sd', address='21 kaisa', phone='216-546-1234',image_link='https://www.youtube.com/image',facebook_link='https://www.facebook.com/me',website_link='https://www.me.com/',seeking_talent=True,seeking_description='atcho chwia')
venue2 = Venue(name='mariadoo', city='242' ,state='sd', address='21 kaisa', phone='216-546-1234',image_link='https://www.youtube.com/image',facebook_link='https://www.facebook.com/me',website_link='https://www.me.com/',seeking_talent=True,seeking_description='atcho chwia')
venue3 = Venue(name='botas', city='ora2544n' ,state='sd', address='21 kaisa', phone='216-546-1234',image_link='https://www.youtube.com/image',facebook_link='https://www.facebook.com/me',website_link='https://www.me.com/',seeking_talent=True,seeking_description='atcho chwia')
artist1 = Artist(name='zaki', city='25' ,state='sd', phone='216-546-1234',image_link='https://www.youtube.com/image',facebook_link='https://www.facebook.com/me',website_link='https://www.me.com/',seeking_venues=True,seeking_description='atcho chwia')
artist2 = Artist(name='amani', city='ora42525n' ,state='sd', phone='216-546-1234',image_link='https://www.youtube.com/image',facebook_link='https://www.facebook.com/me',website_link='https://www.me.com/',seeking_venues=True,seeking_description='atcho chwia')
artist3 = Artist(name='omi', city='45254' ,state='sd', phone='216-546-1234',image_link='https://www.youtube.com/image',facebook_link='https://www.facebook.com/me',website_link='https://www.me.com/',seeking_venues=True,seeking_description='atcho chwia')
db.session.add(venue1,venue2,venue3,artist1,artist2,artist3)
db.session.commit()

'''

#Show.query.filter(Show.date >= datetime.strftime('%Y-%m-%d %H:%M:%S')).all()
# #Show.query.filter(Show.date  >= datetime.strptime(start, '%Y-%m-%d'), Show.date  <= datetime.strptime(end, '%Y-%m-%d')).all()
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
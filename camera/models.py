from extenstions import db

class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    video_type = db.Column(db.String(255))
    video_link = db.Column(db.String(255))
    frame_skip_size = db.Column(db.String(255))
    address=db.Column(db.String(1000))
    lat=db.Column(db.Float)
    long=db.Column(db.Float)

    def __init__(self, name, location,video_type,video_link,frame_skip_size,address,lat,long):
        self.name = name
        self.location = location
        self.video_type = video_type
        self.video_link = video_link
        self.frame_skip_size = frame_skip_size
        self.address = address
        self.lat=lat
        self.long=long

    def __repr__(self):
        return f'<Camera {self.name}>'
    
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location':self.location, 
            'video_type':self.video_type,
            'video_link':self.video_link,
            'frame_skip_size':self.frame_skip_size,
            'address':self.address,
            'lat':self.lat,
            'long':self.long
        }
from extenstions import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255), nullable=False)
    video_name = db.Column(db.String(255))
    date_time = db.Column(db.String(255))
    Threat_status = db.Column(db.String(255))
    image_path = db.Column(db.String(255))
    weapon_images=db.Column(db.String(500))
    timestamp=db.Column(db.DateTime)

    def __init__(self, status,video_name,date_time,Threat_status,image_path,weapon_images,timestamp):
        self.status = status
        self.video_name = video_name
        self.date_time = date_time
        self.Threat_status = Threat_status
        self.image_path = image_path
        self.weapon_images=weapon_images
        self.timestamp=timestamp

    def __repr__(self):
        return f'<Camera {self.name}>'
    
    def as_dict(self):
        return {
            'id': self.id,
            'status':self.status, 
            'video_name':self.video_name,
            'date_time':self.date_time,
            'Threat_status':self.Threat_status,
            'image_path':self.image_path,
            'weapon_images':self.weapon_images,
            'timestamp':self.timestamp
        }
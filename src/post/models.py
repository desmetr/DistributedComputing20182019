from post import postDB
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin

class Post(postDB.Model):
	id = postDB.Column(postDB.Integer, primary_key=True)
	postText = postDB.Column(postDB.String(144), index=True)
	user = postDB.Column(postDB.String(64), index=True)
	timestamp = postDB.Column(postDB.DateTime, nullable=False)
	image = postDB.Column(postDB.String(),nullable=True)

	def __repr__(self):
		return "<Post {}, text = \"{}\" by user {}>".format(self.id, self.postText, self.user)

	def serialize(self):
		return {
			"id": self.id,
			"postText": self.postText,
			"user": self.user,
			"timestamp": self.timestamp,
			"image":self.image
		}		
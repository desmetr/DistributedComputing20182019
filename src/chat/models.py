#To hold database model
from chat import chatDB


class Chat(chatDB.Model):
    id=chatDB.Column(chatDB.Integer, primary_key=True)
    user1=chatDB.Column(chatDB.String(20))
    user2=chatDB.Column(chatDB.String(120))

    def __repr__(self):
        return f"chat('{self.id}','{self.user1}','{self.user2}')"
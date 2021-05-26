from ..extensions import db


class Bookkeeping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_event_timestamp = db.Column(db.DateTime, nullable=True)
    last_event_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<{self.__name__} {self.id}:{self.last_event_id}:{self.last_event_timestamp}>"

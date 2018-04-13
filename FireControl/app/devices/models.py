from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from datetime import date,datetime

db = SQLAlchemy()

class CRUD():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

class Devices(db.Model, CRUD):
    __tablename__ = "devices"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    types = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer)
    user_company = db.Column(db.Integer)
    trouble = db.Column(db.String(250))
    check_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, types, location):
        self.name = name
        self.types = types
        self.location = location

    def to_dict(self, fields=None, date_to_str=True):
        '''
        将model转化为dict
            param fields：要取出的字段
            param date_to_str：是否将日期转化为字符串。格式为 2018-01-01 11:11:11
            return：dict or None
        '''
        if not hasattr(self, '__table__'):
            return

        def convert_data(value):
            if date_to_str:
                return value if not isinstance(value, (datetime, date)) else str(value)
            else:
                return value

        if not fields:
            return {col: convert_data(getattr(self, col, None))
                    for col in self.__table__.columns.keys()}
        else:
            return {key: convert_data(getattr(self, key, None))
                    for key in fields}

class DevicesSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=not_blank)
    types = fields.String(validate=not_blank)
    location = fields.String(validate=not_blank)
    creation_time = fields.DateTime()

     #self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/devices/"
        else:
            self_link = "/devices/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'devices'

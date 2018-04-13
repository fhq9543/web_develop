from flask import Blueprint, request, jsonify, make_response, Response
from app.devices.models import Devices, DevicesSchema, db
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from app.devices import devices
import json
import time

schema = DevicesSchema()
api = Api(devices)

# devices
class DevicesCheck(Resource):
    '''
    扫码巡检。
    '''
    def get(self, name):
        '''
        获取设备信息
        '''
        device_query = Devices.query.filter(Devices.name == name).first()
        if not device_query:
            return None;
        results = device_query.to_dict(fields=['name', 'location', 'trouble'])
        results['check_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return results

    def patch(self, name):
        '''
        更新设备状态，是否正常。
        如不正常，获取不正常原因。
        '''
        device = Devices.query.filter(Devices.name == name).first()
        if not device:
            return None;
        try:
            if request.get_data():
                device_dict = json.loads(request.get_data())
                value = device_dict['trouble']
                if value:
                    setattr(device, 'trouble', value)
            setattr(device, 'check_time', time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            device.update()
            response = make_response()
            response.status_code = 204
            return response
        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp

class DevicesRegister(Resource):
    '''
    扫码注册设备。
    需输入设备名称，设备位置，设备类型。
    '''
    def post(self):
        try:
            device_dict = json.loads(request.get_data())
            device = Devices(device_dict['name'],device_dict['types'],device_dict['location'])
            device.add(device)
        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp

class DevicesUpdate(Resource):
    '''
    设备属性更新(除设备ID，名称)。
    更改位置，更改使用者，删除设备。
    '''
    def get(self, name):
        '''
        获取设备信息
        '''
        device_all = Devices.query.all()
        results = [device.to_dict() for device in device_all]
        return results

    def patch(self, name):
        device = Devices.query.filter(Devices.name == name).first()
        if not device:
            return None;
        try:
            device_dict = json.loads(request.get_data())
            for key, value in device_dict.items():
                if key == 'id' or key =='name':
                    continue
                setattr(device, key, value)
            device.update()
            response = make_response()
            response.status_code = 204
            return response
        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp

    def delete(self, name):
        device = Devices.query.filter(Devices.name == name).first()
        if not device:
            return None;
        try:
            delete = device.delete(device)
            response = make_response()
            response.status_code = 204
            return response
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp

api.add_resource(DevicesRegister, '/register.json')
api.add_resource(DevicesCheck, '/check/<string:name>.json')
api.add_resource(DevicesUpdate, '/update/<string:name>.json')

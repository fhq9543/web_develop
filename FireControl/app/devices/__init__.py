# -*- coding: utf-8 -*-
from flask import Blueprint

devices = Blueprint('devices',__name__)

from app.devices import views

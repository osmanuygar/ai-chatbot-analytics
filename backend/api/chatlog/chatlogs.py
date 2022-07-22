#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import json
from backend.api.rest import api
from flask_restplus import Resource
from Helper import build_response
from backend.api.chatlog.controller import chatlogController as Controller
from flask import Flask, jsonify
from flask_cors import CORS

log = logging.getLogger(__name__)

ns = api.namespace('db', description='Chatlogs')
app = Flask(__name__)
CORS(app)


@ns.route("/chatlogs/limit/exports/<int:limit>/")
class DatasetCollection(Resource):

    def get(self, limit):
        """
        Returns list of chatlogs according to limit and order by last creation date.
        """
        data = Controller.get_chatlogs_with_limit(limit)
        return jsonify(data)


@ns.route('/chatlogs/export/excel')
class ChatlogExportAll(Resource):

    def get(self):
        """
        Returns list of chatlogs.
        """
        return Controller.get_excel_export_for_all_chatlogs()


@ns.route('/chatlogs/lastdate/export/excel/<int:value>')
class ChatlogExportAll(Resource):

    def get(self, value):
        """
        Returns list of chatlogs.
        """
        return Controller.get_excel_export_for_chatlogs_acoording_to_lastdate(value)

@ns.route('/chatlogs/lastdate/export/ucexcel/<int:value>/<int:key>')
class ChatlogExportAll(Resource):

    def get(self, value, key):
        """
        Returns list of chatlogs.
        """
        return Controller.get_excel_export_for_chatlogs_acoording_to_lastdate(value)


@ns.route('/chatlogs/export/excel/<int:year>/<int:month>/<int:day>')
class ChatlogExportAllDate(Resource):

    def get(self, year, month, day):
        """
        Returns list of chatlogs.
        """
        return Controller.get_excel_export_for_chatlogs_acoording_to_date(year, month, day)


@ns.route('/intents/export/excel')
class IntentExportAll(Resource):

    def get(self):
        """
        Returns list of intents.
        """
        return Controller.get_excel_export_for_all_intents()

@ns.route('/intents/export/ucexcel/<int:key>')
class IntentExportAll(Resource):

    def get(self, key):
        """
        Returns list of intents.
        """
        return Controller.get_excel_export_for_all_intents()


@ns.route('/chatlogs/sessions/count')
class ChatlogExportAll(Resource):

    def get(self):
        """
        Returns list of chatlogs.
        """
        return build_response.build_json(Controller.get_chatlogs_session_count())


@ns.route('/chatlogs/fallback/count')
class ChatlogExportAll(Resource):

    def get(self):
        """
        Returns list of chatlogs.
        """
        return build_response.build_json(Controller.get_chatlogs_fallback_count())

@ns.route('/chatlogs/sessions/day/count/<int:day>')
class ChatlogExportAll(Resource):

    def get(self, day):
        """
        Returns list of chatlogs.
        """
        return build_response.build_json(Controller.get_chatlogs_sessions_count_last_x_days(day))


@ns.route('/chatlogs/fallback/day/count/<int:day>')
class ChatlogExportAll(Resource):

    def get(self, day):
        """
        Returns list of chatlogs.
        """
        return build_response.build_json(Controller.get_chatlogs_fallbacks_count_last_x_days(day))


@ns.route('/chatlogs/fallback/monthly/test')
class ChatlogExportAll(Resource):

    def get(self):
        """
        Returns list of chatlogs.
        """
        return build_response.build_json(Controller.get_chatlogs_monthly_count())


@ns.route('/chatlogs/analytics')
class ChatlogExportAll(Resource):

    def get(self):
        """
        Returns list of chatlogs.
        """
        return build_response.build_json(Controller.get_chatlogs_analytics())


@ns.route('/chatlogs/test_results/<int:key>')
class GetTestResults(Resource):

    def get(self,key):
        """
        Returns Test Results.
        """
        return Controller.get_excel_test_results()


"""
Module to fetch data from the database
"""
from os import environ as env
from bson import ObjectId
from pymongo import MongoClient, DESCENDING

from settings import load_env

load_env()
MC = MongoClient(env['MONGODB_URI']).get_database()

def get_all(last_id=None, notice_count=15):
    """
    Get latest notice_count notices from each noticeboard
    """
    notices = {}
    collections = MC.list_collection_names()
    for collection in collections:
        type_notices = get_type(collection, last_id)
        notices[collection] = type_notices
    return notices

def get_type(notice_type, last_id=None, notice_count=15):
    """
    Get latest notice_count notices from notice_type
    """
    collections = MC.list_collection_names()
    if notice_type in collections:
        if last_id is None:
            cursor = MC[notice_type].find().sort('_id', DESCENDING).limit(notice_count)
        else:
            cursor = MC[notice_type].find({'_id': {'$lt': ObjectId(last_id)}}).sort('_id', DESCENDING).limit(notice_count)
        notices = [notice for notice in cursor]
        if not notices:
            return {
                "data": [],
                "next_cursor": last_id,
                "success": 204
            }
        last_id = notices[-1]['_id']
        return {
            "data": notices,
            "next_cursor": last_id,
            "success": 200
        }
    else:
        invalid_type = {
            "data": [],
            "next_cursor": None,
            "success": 400
        }
        return invalid_type

if __name__ == "__main__":
    get_all()

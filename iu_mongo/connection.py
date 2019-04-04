from pymongo.mongo_client import MongoClient
from pymongo.read_preferences import ReadPreference
from iu_mongo.errors import ConnectionError
import collections

__all__ = ['connect', '_get_db']

_connections = {}
_dbs = {}
_db_to_conn = {}


def _get_db(db_name):
    global _dbs, _connections, _db_to_conn
    if db_name not in _dbs or not _dbs[db_name]:
        conn_name = _db_to_conn.get(db_name, None)
        conn = _connections.get(conn_name, None)
        _dbs[db_name] = conn and conn[db_name]
    return _dbs[db_name]


def clear_all():
    global _connections, _dbs, _db_to_conn
    _connections = {}
    _dbs = {}
    _db_to_conn = {}


def connect(host='localhost', conn_name='main', db_names=[],
            port=27017, max_pool_size=None,
            socketTimeoutMS=None, connectTimeoutMS=None, waitQueueTimeoutMS=None):
    global _connections, _db_to_conn

    mongo_client_kwargs = {
        'host': host,
        'port': port,
        'maxPoolSize': max_pool_size,
        'socketTimeoutMS': socketTimeoutMS,
        'connectTimeoutMS': connectTimeoutMS,
        'waitQueueTimeoutMS': waitQueueTimeoutMS,
        'connect': False
    }
    keys = [k for k in mongo_client_kwargs.keys()]
    for k in keys:
        if mongo_client_kwargs[k] is None:
            del mongo_client_kwargs[k]

    # Connect to the database if not already connected
    if conn_name not in _connections:
        try:
            conn = MongoClient(**mongo_client_kwargs)
            conn.admin.command('ismaster')
            _connections[conn_name] = conn
        except Exception as e:
            raise ConnectionError(
                'Cannot connect to the database: %s' % str(e))

        if db_names:
            for db in db_names:
                _db_to_conn[db] = conn_name

    return _connections[conn_name]

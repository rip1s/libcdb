__author__ = 'nonick'

import json
import sys
import requests

APIURL = 'https://libc.ml/api.php'


class LIBC:
    '''
    LIBC object

    Provides dict-like access method.

    Automatically load all libc data if key NOT found.
    '''

    def __init__(self, data=None, id=None):
        self.data = {}
        self.id = id
        self.base = 0
        if data is not None:
            self.parse(data)

    def parse(self, data):
        self.id = data['ver']
        self.data[data['fun']] = int(data['addr'], 16)

    def __getitem__(self, item):
        if item in self.data:
            return self.data[item] + self.base
        elif self.fetchall():
            if item in self.data:
                return self.data[item] + self.base
            else:
                return None
        else:
            return None

    def fetchall(self):
        if self.id:
            j = query_libc_raw(self.id)

            for x in j:
                self[x['fun']] = int(x['addr'], 16)
            return True
        else:
            return False

    def __setitem__(self, key, value):
        self.data[key] = value

    def __repr__(self):
        if self.id:
            return 'Libc version:{}'.format(self.id)
        else:
            return 'Libc (Unknow version)'


def __checkifstring(s):
    '''
    Simply check if parameter is a string or not
    :param s:
    :return:
    '''
    if sys.version_info >= (3, 0, 0):
        # for Python 3
        if isinstance(s, bytes) or isinstance(s, str):
            return True
        return False
    else:
        # for Python 2
        if isinstance(s, unicode) or isinstance(s, str):
            return True
        return False


def __standardize_address(n):
    '''
    Standardize the address for api query.
    :param n:
    :return:
    '''
    if isinstance(n, int) or isinstance(n, float):
        tmp = int(n)
    elif __checkifstring(n):
        if n.startswith('0x'):
            tmp = int(n, 16)
        else:
            tmp = int(n)
    else:
        raise ValueError('Error parameter!')

    tmp &= 0xfff
    return hex(tmp)


def search_libc(condition):
    '''
    Search libc database for specific condition
    condition address can be string or hex or int.

    example:
        search_libc({'fun':'system','adr':'0x90'})
        search_libc({'fun':'system','adr':0x90})
        search_libc(('system','0x90'))
        search_libc(('system',0x90))
    :param condition:
    :return: A LIBC object
    '''
    if __checkifstring(condition):
        querystr = str(condition)
    elif isinstance(condition, list) or isinstance(condition, tuple):
        querystr = {}
        querystr['fun'] = condition[0]
        querystr['adr'] = __standardize_address(condition[1])
    elif isinstance(condition, dict):
        querystr = {}
        querystr['fun'] = condition['fun']
        querystr['adr'] = __standardize_address(condition['adr'])
    else:
        raise ValueError('Error parameter!')

    r = requests.get(APIURL, params=querystr)

    if r.status_code == 404:
        raise ValueError('API backend returned :Error parameter!')

    try:
        j = json.loads(r.content)
    except:
        raise ValueError('API return data error! (Maybe network problem)')
    result = []

    for x in j:
        result.append(LIBC(x))
    return result


def query_libc_raw(id):
    '''
    Query raw json data for specific id
    :param id:
    :return: Raw libc json data
    '''
    try:
        id = str(id)
    except:
        raise ValueError('Error parameter!')

    r = requests.get(APIURL, params={'ver': id})
    if r.status_code == 404:
        raise ValueError('API backend returned :Error parameter!')

    try:
        j = json.loads(r.content)
    except:
        raise ValueError('API return data error! (Maybe network problem)')

    return j


def query_libc(id):
    '''
    Query specific libc based on id

    example:
        query_libc('libc6_2.24-7ubuntu2_amd64')
    :param id:
    :return: A LIBC object
    '''
    j = query_libc_raw(id)
    result = LIBC()
    for x in j:
        result.parse(x)
    return result

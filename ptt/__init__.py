import os
import configparser
import requests as rq
from pyquery import PyQuery as pq
from ptt import global_var
from datetime import datetime as dt
import sqlite3 as DB
import sqlalchemy as sa

# get the home page for webName
def get_index(webName):
    website = "/bbs/"+webName+"/index.html"
    return website

# get the weburl for website
def get_weburl(website):
    weburl = 'https://www.ptt.cc/'+website
    return weburl

# get the current working directory
def abs_path(rel_path):
    ptt_path = os.path.split(os.path.realpath(sys.argv[0]))[0]  
    return os.path.join(ptt_path, rel_path)

# gen proxy url if needed
def gen_proxy_url():
    if proxy_url:
        proxies = {'http': proxy_url,
             'https': proxy_url}
    else:
        proxies = proxy_url
    return proxies        

# get session
def get_session(proxies=''):
    session = rq.session()
    headers = {
        "user-agent": "mozilla/5.0 (x11; linux x86_64) applewebkit/537.36 "
                      "(khtml, like gecko) "
                      "chrome/46.0.2490.86 safari/537.36"}
    session.headers.update(headers)
    if proxies:
        session.proxies.update(proxies)
    return session

# get database path
def get_DB(DB_path):
    conndb = DB.connect(DB_path)
    curr = conndb.cursor()  
    return [conndb,curr]

# check if table is exist in database
def checkTableisExist(webName):
    result = curr.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(webName))
    if result.fetchone():
        return True
    else:
        return False

# read config file for setting parameters
def readConfig(config_path):
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
        return config
    else:
        print('Config File Loss, Quit the ptt crawler.')
        return

# initialize config with config file path
config_path = 'config.ini'
config = readConfig(config_path)

# Read Parameters with config
updatePageNum = eval(config['CRAWLER']['updatePageNum'])
proxy_url = config['ENV']['proxy_server_url']
sqlite_path = config['SQL']['sqlite_path']
boardlist = eval(config['CRAWLER']['boardlist'])
deadline = dt.strptime(config['CRAWLER']['deadline'],'%Y/%m/%d')
token = config['NOTIFY']['token']
[conndb,curr] = get_DB(sqlite_path)
session = get_session()
engine = sa.create_engine(f"sqlite:///{sqlite_path}")

# make variables global if needed
global_var.deadline = deadline
global_var.token = token
global_var.conndb = conndb
global_var.curr = curr
global_var.session = session
global_var.engine = engine


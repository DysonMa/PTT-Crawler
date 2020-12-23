import requests as rq
from pyquery import PyQuery as pq
import time
import pandas as pd
import os
import sys
import traceback
import re
from datetime import datetime as dt
from tqdm import tqdm_notebook
from ptt import *

# global variables
session = global_var.session
conndb = global_var.conndb
curr = global_var.curr
deadline = global_var.deadline
token = global_var.token
engine = global_var.engine

# get web documents
def _get_soup(website):
    session.post('https://www.ptt.cc/ask/over18', data = {'from': website, 'yes': 'yes'})
    weburl = get_weburl(website)
    res = session.get(weburl)
    doc = pq(res.text)
    return doc

# seperate articles from board rules
def _sep_Articles(doc):
    r_list_sep = doc.find('.r-list-sep') 
    if r_list_sep != []:
        r_ent = r_list_sep.prevAll('.r-ent') 
    else:
        r_ent = doc(".r-ent")
    return r_ent

# get webName from spliting from website
def _get_webName_from_website(website):
    webName = website.split('/')[2]
    return webName

# set dataframe columns name
def set_df_names():
    names=['ArticleID','PushTag','Author','Title','Date','Content','Comment_PushTag','Comment_Content','Comment_ID','Crawler_at']
    names = dict(zip(range(len(names)),names))
    return names

# get articles basic information from one page -> [attr,pushTag,authorID,title]
def _get_BasicInfo(each):
    try:
        basic_Info = []
        pushTag = each('.nrec > span').text()
        # index = str(each(".title a").attr("href")).split("/bbs/"+webName+"/")[-1].split(".html")[0]
        authorID = each('.meta > .author').text()
        title = each(".title a").text()
        # date = each('.date').text()
        attr = str(each(".title a").attr("href"))
        basic_Info = [attr,pushTag,authorID,title]
    except Exception as e:
        print('{} get_BasicInfo出錯!!'.format(attr))
        print(_error_msg(e))
    return basic_Info 


# get articles contents and post dates -> [date,content]
def _get_ArtContent(attr):
    # get each article's web documents
    Restdoc = _get_soup(attr)
    try:
        if Restdoc(".article-metaline").text() != "": # Example: 'Aug 25 14:37:26 2020'
            timeIndex = re.findall(
                r'[\w]+ [\d \d:\d:\d \d]+',
                Restdoc(".article-meta-value").text())
            # choose the last pair as timeIndex when regex matches wrong
            if len(timeIndex) != 0:
                timeIndex = timeIndex[-1]
            # /w: [a-zA-Z0-9_] , /d: [0-9]
            (month,date,clock,year) = timeIndex.split()
            content = u"".join(re.findall(r'\S+',Restdoc("#main-content").text().split("-- ※")[0].split(timeIndex+"\n")[-1]))
            # date = "{}/{}/{} {}".format(year,month,date,clock)
            date = dt.strptime(" ".join([year,month,date,clock]),"%Y %b %d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")

        # look for the comment below when some articles have no information field  
        else:
            if Restdoc(".f2:nth-child(1)").text() != "": # Example: ' 07/28/2020 17:49:56'
                try:
                    timeIndex = re.findall(r' [\d/\d/\d \d:\d:\d]+',Restdoc(".f2:nth-child(1)").text())[0]
                    clock = timeIndex.split()[-1]
                    (month,date,year) = timeIndex.split()[0].split("/")
                    date = "{}/{}/{} {}".format(year,month,date,clock)
                    #  date = dt.strptime(year+month+date+clock,"%Y%b%d%H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
                    content = "".join(re.findall(r'\S+',Restdoc("#main-content").text().split("※"))[0])
                except:
                    date = 'None'
                    content = Restdoc("#main-content").text().split("※")[0]
                    print(attr + ' 此篇找不到文章的時間資訊!!')
    except Exception as e:
        print('{} get_ArtContent 出錯!!'.format(attr))
        print(_error_msg(e))
    return [date,content]


# get push comment's contents ->  [cp_tag,cp_content,cp_ID] , cp:comment_push
def _get_PushContent(attr):
    try:
        Restdoc = _get_soup(attr)
        cp_Tag = [] 
        cp_Content = []
        cp_ID = []
        for each in Restdoc(".push").items():
            # attr.split("/bbs/"+webName+"/")[-1].split(".html")[0].replace(".","_"))
            cp_Tag.append(each("span.f1.hl.push-tag").text() or each("span.hl.push-tag").text())
            cp_Content.append(each("span.f3.push-content").text())
            cp_ID.append(each("span.f3.hl.push-userid").text())
        # record crawling date
        crawler_at = dt.now().strftime('%Y/%m/%d %H:%M:%S')
        push = ["⟴".join(cp_Tag),"⟴".join(cp_Content),"⟴".join(cp_ID),crawler_at]
    except Exception as e:
        print('{} get_PushContent 出錯!!'.format(attr))
        print(_error_msg(e))
    return push

# change to next page 
def _nextPage(doc,website):
    website = doc(".btn-group.btn-group-paging > a:nth-child(2)").attr("href")
    return website 

# read the last time executing crawler as the deadline for this time
def _read_latest_time(webName, deadline):
    result = curr.execute("SELECT Date FROM {} WHERE Date != 'None' ORDER BY Date".format(webName))
    if result.fetchone() == None:
        return deadline
    else:
        latest_time = dt.strptime(result.fetchall()[-1][0],'%Y/%m/%d %H:%M:%S')
        return latest_time
    
# create table for each board
def _create_Table(webName):
    # sqlite will throw error during creating board name if "-" is in string
    if "-" in webName:
        webName = webName.replace('-','_')
    curr.execute(
                '''
                CREATE TABLE IF NOT EXISTS {}(
                ArticleID text,
                PushTag text,
                Author text,
                Title text,
                Date text,
                Content text,
                Comment_PushTag text,
                Comment_Content text,
                Comment_ID text,
                Crawler_at text
                );
                '''.format(webName))
    conndb.commit()
    return webName

# insert data into table
def _insert_data(batch_data,webName):
    curr.executemany("INSERT INTO {} VALUES(?,?,?,?,?,?,?,?,?,?)".format(webName),batch_data)
    conndb.commit() # commit the changes

# update data in table
def _update_data(data, webName):
    curr.execute(
                '''
                UPDATE {} SET 
                PushTag = '{}',
                Comment_PushTag = '{}',
                Comment_Content = '{}',
                Comment_ID = '{}',
                Crawler_at = '{}'
                WHERE ArticleID = '{}';
                '''.format(webName,data[1],data[6],data[7],data[8],data[9],data[0]))
    
# check if Article_ID is exist in table
def _checkIDisExist(webName,art_id):
    result = curr.execute("SELECT ArticleID FROM {} WHERE ArticleID = '{}'".format(webName,art_id))
    if result.fetchone() == None:
        return False
    else:
        return True

# call line-notify service for notification
def _lineNotifyMessage(msg):
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = rq.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code

# detail exception error message
def _error_msg(e):
    error_class = e.__class__.__name__            # get error type
    detail = e.args[0]                            # get detail content
    cl, exc, tb = sys.exc_info()                  # get Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1]  # get the last Call Stack
    fileName = lastCallStack[0]                   # get file name where error occurs
    lineNum = lastCallStack[1]                    # get line number where error occurs
    funcName = lastCallStack[2]                   # get function name where error occurs
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    return errMsg

# execute crawling by page
def CrawlingByPage(website, page, save=False, update=False):
    webName = _get_webName_from_website(website)
    df = pd.DataFrame()
    bar_page = tqdm_notebook(range(1,page+1))
    for i,each in enumerate(bar_page):
        bar_page.set_description('目標往前更新%s %d頁' %(webName,page))
        doc = _get_soup(website)
        r_ent = _sep_Articles(doc)
        try:
            bar_article = tqdm_notebook(r_ent.items())
            for i,each in enumerate(bar_article):
                bar_article.set_description('正在爬取第%d篇文章' %(i+1))
                basic_Info = _get_BasicInfo(each)
                attr = basic_Info[0]
                # no attr will find when article is deleted
                if attr == "None":
                    continue
                basic_Info[0] = re.findall( r'[A-Z]*.[0-9]+.[A-Z]*.[A-Z0-9]+',attr)[0]
                data = basic_Info + _get_ArtContent(attr) + _get_PushContent(attr)
                print(data[3])  # Title
                df = df.append([data])
        except Exception as e:
            print(_error_msg(e))
        website = _nextPage(doc,website)
    df = df.rename(columns=set_df_names())
    if save:
        df.to_sql(webName, engine, if_exists="append", index=False)
    if (checkTableisExist(webName) and update):
        for i in range(df.shape[0]):
            _update_data(tuple(df.iloc[i]), webName)
        print('更新成功')
    elif not checkTableisExist(webName):
        print(f'更新失敗，資料表裏頭沒有{webName}')
    return df
            
# execute crawling by date
def CrawlingByDate(website, deadline, save=False, update=False):
    webName = _get_webName_from_website(website)
    StopCrawl = global_var.StopCrawl
    df = pd.DataFrame()
    while True:
        if StopCrawl:
            break
        doc = _get_soup(website)
        r_ent = _sep_Articles(doc)
        batch_data = []
        for each in r_ent.items():
            try:
                basic_Info = _get_BasicInfo(each)
                attr = basic_Info[0]
                # no attr will find when article is deleted
                if attr == "None":
                    continue
                basic_Info[0] = re.findall( r'[A-Z]*.[0-9]+.[A-Z]*.[A-Z0-9]+',attr)[0]
                data = basic_Info + _get_ArtContent(attr) + _get_PushContent(attr)
                # when this article doesn't contains time field
                if data[4] == "None":
                    Article_date = ""
                else:
                    Article_date = dt.strptime(data[4],"%Y/%m/%d %H:%M:%S")
                    if Article_date < deadline:
                        if update:
                            _update_data(data, webName)
                            print(f'{data[3]} 已更新!') # title
                        StopCrawl = True
                        continue
                    elif Article_date == deadline:
                        if (_checkIDisExist(webName,data[0]) and update):
                            _update_data(data, webName)
                            print(f'{data[3]} 已更新!') # title
                        else:
                            batch_data.append(tuple(data))
                            print(data[3], data[4])
                    elif Article_date > deadline:
                        print(data[3], data[4]) # title, date
                        batch_data.append(tuple(data))
                        df = df.append([data])
            except Exception as e:
                print(webName,website,_error_msg(e))
                continue
        try:  
            if save:
                # insert batch data into table for each page
                _insert_data(batch_data,webName)
            website = _nextPage(doc,website) 
        except Exception as e:
            print(_error_msg(e))
    if save:
        return website
    else:
        df = df.rename(columns=set_df_names())
        return df



        

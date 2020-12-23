from ptt.crawler import *
from ptt.crawler import _create_Table, CrawlingByDate,_lineNotifyMessage, _read_latest_time,CrawlingByPage, _error_msg, checkTableisExist, _update_data
from ptt import get_index
from datetime import datetime as dt
from tqdm import tqdm_notebook

# first time crawling, for boards never crawled before
def firstCrawling(webName, deadline, website):
    try:
        webName = _create_Table(webName)
        start_time = dt.now()
        CrawlingByDate(website, deadline, save=True, update=False)
        stop_time = dt.now()
        _lineNotifyMessage("爬完{}版，歷時{}".format(webName, stop_time-start_time))
    except Exception as e:
        print(_error_msg(e))

# second time crawling, for boards have already exist in database
def secondCrawling(webName, deadline, website, page=1):
    try:
        deadline = _read_latest_time(webName, deadline)
        start_time = dt.now()
        website = CrawlingByDate(website, deadline, save=True, update=True)
        print(website)
        # if time meets deadline, continue crawling N page for updating old information 
        df = CrawlingByPage(website, page, save=True, update=False)
        stop_time = dt.now()
        _lineNotifyMessage("爬完{}版，歷時{}".format(webName, stop_time-start_time))
    except Exception as e:
        print(_error_msg(e))


def schedule():
    print('爬蟲停止時間: %s' %deadline)
    print('爬取板名: %s' %boardlist)
    print('停止爬蟲後，往前更新頁數: %s' %updatePageNum)
    bar = tqdm_notebook(boardlist)
    for i,webName in enumerate(bar):
        web_index = get_index(webName)
        if checkTableisExist(webName):
            bar.set_description('%s already exists, start crawling and updating!' %webName)
            secondCrawling(webName, deadline, web_index, updatePageNum)
            print(f'\n------------{webName} is end--------------\n')
        else:
            bar.set_description('%s does not exist yet, start crawling!' %webName)
            firstCrawling(webName, deadline, web_index)
            print(f'\n------------{webName} is end--------------\n')
        conndb.commit()
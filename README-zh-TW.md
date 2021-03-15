<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

[English README.md(英文版 README.md)](https://github.com/DysonMa/PTT-Crawler/blob/master/README.md)

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <!-- <a href="https://github.com/othneildrew/Best-README-Template"> -->
    <img src="./image/ptt.PNG" alt="Logo" width="80" height="80">
  <!-- </a> -->

  <h3 align="center">PTT 爬蟲</h3>

  <p align="center">
    這是一個利用requests, pyquery, pandas, SQLite爬蟲的程式，爬取 PTT 網站並將資料存入SQLite資料庫，並串接至 LINE Notify 通知服務。
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>目錄</summary>
  <ol>
    <li>
      <a href="#about-the-project">關於</a>
      <ul>
        <li><a href="#built-with">建立的環境與套件</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">如何開始</a>
      <ul>
        <li><a href="#installation">下載</a></li>
      </ul>
    </li>
    <li><a href="#usage">如何使用</a></li>
    <li><a href="#license">憑證</a></li>
    <li><a href="#contact">聯絡方式</a></li>
    <li><a href="#acknowledgements">致謝</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## 關於

PTT 是台灣最常使用到的社群(鄉民)網站之一。

因為每天的資訊量太過龐大，難以完全的消化，所以我們可以透過爬蟲的技術來快速地蒐集資料。
之外，將資料存入資料庫將有利於後續的分析，如: 機器學習、深度學習、大眾輿情分析...等等。

![date](/image/date.PNG)


![db](/image/db.PNG)

### 建立的環境與套件

* [Python](https://www.python.org/)
* [LINE Notify](https://notify-bot.line.me/zh_TW/)
* [SQLite](https://www.sqlite.org/download.html)
* Pandas
* requests
* pyquery

<!-- GETTING STARTED -->
## 如何開始

### 下載

1. Clone the repo
   ```
   git clone https://github.com/DysonMa/PTT-Crawler.git
   ```
2. 編輯 `config.ini`

    `boardlist`: 輸入ptt爬蟲的版名

    `deadline`: 設定爬蟲停止的截止日期

    `sqlite_path`: SQLite資料庫的存取路徑

    `token`: LINE Notification service token

<!-- USAGE EXAMPLES -->
## 如何使用

首先，利用前述提到的必要參數要來創建一個 `config.ini` 檔，這個檔案的路徑必須和 `main.ipynb` 相同。

底下是一個簡單的例子:

* 載入 ptt 套件
```
from ptt.crawler import * 
from ptt.schedule import *
```
* 檢查參數是否正確
```
print('config_path:', config_path)
print('deadline:', deadline)
print('boardlist:', boardlist)
print('updatePageNum:', updatePageNum)
print('sqlite_path:', sqlite_path)
```
>config_path: config.ini<br>
deadline: 2020-12-19 00:00:00<br>
boardlist: ['Civil', 'Soft_Job', 'NBA']<br>
updatePageNum: 1<br>
sqlite_path: D:\ptt_test.db<br>
* 依據特定的版名來命名 `website` 這個變數名稱
```
website = get_index('civil')
print(get_weburl(website))
```
https://www.ptt.cc//bbs/civil/index.html

* 利用 **頁數** 來爬取PTT網站 
```
df = CrawlingByPage(website, page=2, save=True, update=True)
```
![page](/image/page.PNG)
![page df](/image/page_df.PNG)

* 利用 **日期時間** 來爬取PTT網站
```
df = CrawlingByDate(website, deadline, save=True, update=True)
```
![date df](/image/date_df.PNG)

* 利用 **排程** 來定期爬取PTT網站
```
schedule()
```
![schedule](/image/schedule.PNG)

Line Notification 通知服務

<img src='/image/line-notification.png' width="250"></img> 


<!-- LICENSE -->
## 憑證

Distributed under the MIT License.

<!-- CONTACT -->
## 聯絡方式

Dyson Ma - [Gmail](madihsiang@gmail.com)

Project Link: [https://github.com/DysonMa/PTT-Crawler](https://github.com/DysonMa/PTT-Crawler)

<!-- ACKNOWLEDGEMENTS -->
## 致謝

* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/dysonma/PTT-Crawler?style=for-the-badge
[contributors-url]: https://github.com/DysonMa/PTT-Crawler/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/dysonma/PTT-Crawler?style=for-the-badge
[forks-url]: https://github.com/DysonMa/PTT-Crawler/network/members
[stars-shield]: https://img.shields.io/github/stars/dysonma/PTT-Crawler?style=for-the-badge
[stars-url]: https://github.com/DysonMa/PTT-Crawler/stargazers
[issues-shield]: https://img.shields.io/github/issues/dysonma/PTT-Crawler?style=for-the-badge
[issues-url]: https://github.com/DysonMa/PTT-Crawler/issues
[license-shield]: https://img.shields.io/github/license/dysonma/PTT-Crawler?style=for-the-badge
[license-url]: https://github.com/DysonMa/PTT-Crawler/blob/master/LICENSE

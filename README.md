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

[繁體中文 README.md(Traditional Chinese README.md)](https://github.com/DysonMa/PTT-Crawler/blob/master/README-zh-TW.md)

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <!-- <a href="https://github.com/othneildrew/Best-README-Template"> -->
    <img src="./image/ptt.PNG" alt="Logo" width="80" height="80">
  <!-- </a> -->

  <h3 align="center">PTT Crawler</h3>

  <p align="center">
    Use requests, pyquery, pandas, SQLite to build a crawler to crawl the PTT website and save crawled data to sqlite database, and connect to LINE Notifiy for notification.
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About

PTT is one of the most commonly used social media in Taiwan. 

Because the amount of daily information is too much to be completely digested, we can collect data quickly through crawlers.

In addition, storing the crawled data into the database can also be used for subsequent analysis, such as machine learning, deep learning, public opinion analysis.

![date](/image/date.PNG)


![db](/image/db.PNG)

### Built With

* [python](https://www.python.org/)
* [LINE Notify](https://notify-bot.line.me/zh_TW/)
* [SQLite](https://www.sqlite.org/download.html)
* Pandas
* requests
* pyquery

<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Clone the repo
   ```
   git clone https://github.com/DysonMa/PTT-Crawler.git
   ```
2. Edit `config.ini`

    `boardlist`: List the board names for ptt crawling

    `deadline`: Set deadline for crawler stopping

    `sqlite_path`: Path of SQLite database for storing crawled data 

    `token`: LINE Notification service token

<!-- USAGE EXAMPLES -->
## Usage

First, you should create `config.ini` with required parameters, and save it into the path as same as the `main.ipynb`.

Below is a simple example:

* import ptt package
```
from ptt.crawler import * 
from ptt.schedule import *
```
* Check parameters
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
* Name the `website` variable from specific board name
```
website = get_index('civil')
print(get_weburl(website))
```
https://www.ptt.cc//bbs/civil/index.html

* Crawl the PTT website by **Page**
```
df = CrawlingByPage(website, page=2, save=True, update=True)
```
![page](/image/page.PNG)
![page df](/image/page_df.PNG)

* Crawl the PTT website by **Date**
```
df = CrawlingByDate(website, deadline, save=True, update=True)
```
![date df](/image/date_df.PNG)

* Regularly crawl the PTT website by **Schedule**
```
schedule()
```
![schedule](/image/schedule.PNG)

Line Notification

![Notification](/image/line-notification.png)

<!-- LICENSE -->
## License

Distributed under the MIT License.

<!-- CONTACT -->
## Contact

Dyson Ma - [Gmail](madihsiang@gmail.com)

Project Link: [https://github.com/DysonMa/PTT-Crawler](https://github.com/DysonMa/PTT-Crawler)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

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

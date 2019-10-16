#### Task

Scrap facebook live gaming page and extracts users and push them to faktory worker to parse their 
detail(name, uid, username, number of follower, number of likes, contact details - email, social links) 
and their posts(post-id, text, datetime, hashtags, links) and finally save them in MongoDB

#### Setup

* Install [faktory](https://github.com/contribsys/faktory) server.
* Install MongoDB and create database `aggero_db` and two collection `user_details` and `posts`.
* pip install -r requirements.txt
* Change `URL_FACTORY` password in `utils.py` file.
* Configure `MongoConnnection.py` file.
* Run first `consumer.py` and then `producer.py`. Scraping should be started now.

#### Todo 
* Build a error database and send daily error report email to admin.
* for now kept not retry mechanism, may be in future.
* Pagination through live gaming page is done to aprse all live user 
but got few issues to paginate for infinite depth, for now its just first page to scrap.May be in future I will fix this issue.
* By default I am running one worker process but you can modify it in `consumer.py` file as number of cores in your pc.



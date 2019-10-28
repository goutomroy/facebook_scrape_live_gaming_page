#### Task

Scrap facebook live gaming page and extracts live users and push them to faktory worker to parse their 
detail(name, uid, username, number of follower, number of likes, contact details - email, social links) 
and their posts(post-id, text, datetime, hashtags, links, images) and finally save them in MongoDB.

#### Setup

* Install [faktory](https://github.com/contribsys/faktory) server.
* Download `geckodriver` for firefox from [here](https://github.com/mozilla/geckodriver/releases/), then extract and 
update variable `MOZILLA_DRIVER_PATH` in `utils.py`.
* Install MongoDB and create database `aggero_fb` and two collection `user_details` and `posts`.
* pip install -r requirements.txt
* Change `URL_FACTORY` password in `utils.py` file.

#### Run
* Navigate to `main` package.
* First run `python3 consumer.py`
* Then `python3 producer.py -nup 10 -nps 3`. You must need to provide `-nup` and `-nps`
     * `-nup` - Number of live users to parse
        * Choices : `int` value greater than 0 or `str` value `all` 
     * `-nps` - Number of scroll while parsing user posts. Every scroll gives about 18 posts. 
        * Choices : `int` value greater than 0 or `str` value `all` 
     * `-nup 10 -nps 3` works best for testing, `all` may be used in production.
  
* Scraping should be started now.

#### Todo 
* Configure Tor for proxy.
* Build a error database and send daily error report email to admin.
* By default I am running one worker process but you can modify it in `consumer.py` file as number of cores in your pc.
* Create index for MongoDB.
* Write tests.

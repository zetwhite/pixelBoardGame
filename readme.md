# Server Side Setting 

### Need to install Mysql and set Database
For saving users' infomation and score, we need to make table as follow:<br>
database name : roonmap<br>
table name : userinfo <br>
|column name|properties|
|-------|--------|
|no|not null, auto-inc, int|
|id|varchar[16], not null, unique key|
|pw|varchar[16], not null, unique key|
|email|varchar[30], not null, unique key|
|score|int, not null|

after making table, go to utility.c<br>
and change `password` variable in `mysql_connection` to your password. 

### Dependencies 
```sh
sudo apt-get install libmysqlclient-dev 
````

# Client Side Setting
###Dependencies
download python3(>=3.5.2) and pygame<br> 
```sh
sudo apt-get install python3-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-de
svn co svn://seul.org/svn/pygame/trunk pygame
cd pygame
python3 setup.py build
sudo python setup.py install 
```
run game
```sh
cd ./client
Makefile
python3 ./Pixel\ Board.py
```

if you have some error, try to upgrade python version.
```sh
sudo apt-get update
sudo apt-get upgrade python3
```

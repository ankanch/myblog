## myblog

for more information: http://akakanch.com

##### Requirements

* Ubuntu 16.04
* Python >= 3
* MySql Server >= 5.6
* systemd
* gunicorn
* flask
* pymysql

### Install Guides

Before install myblog on your server , please make sure you have all conponments above installed, and you also need to have a user account with the name as `ubuntu` in your systems.

```shell
git clone https://github.com/ankanch/myblog.git
```

After you cloned this repo, change the directory to the `setup_myblog` directory.
```shell
cd ./myblog/setup_myblog
```
Then, let's run `x_initialize_myblog.py` to start up set up guide, after this guide , you should able to visit your blog via your IP or domain
```shell
sudo python3 x_initialize_myblog.py
```
Following steps in guide above, and you will be asked to input following information in myblog setup:
* `database IP address` and password for database root user

* `external IP address` which will be used to visit, and an `internal IP address` which will be used to bind by flask app(if you don't have it, please fill it with `127.0.0.1`)

* You will also be asked to set an password for myblog database user `myblogx` and user account for myblog admin which you will be used to login to manage your blog.

##### Samples
![index](https://github.com/ankanch/myblog/blob/master/sample_images/myblog_index.png)
![articles](https://github.com/ankanch/myblog/blob/master/sample_images/myblog_articles.png)
![editarticle](https://github.com/ankanch/myblog/blob/master/sample_images/myblog_editarticle.png)
![admin](https://github.com/ankanch/myblog/blob/master/sample_images/myblog_admin.png)

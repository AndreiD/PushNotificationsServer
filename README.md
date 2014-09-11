GCM Flask Server
========================


Integration of https://github.com/geeknam/python-gcm into flask

Features:
- Everything that python-gcm has: Supports multicast message, Resend messages using exponential back-off, Proxy support, Easily handle errors
- Admin panel with user managment
- REST API for easy posting from your android app
- Sending messages to all or only to specific categories


![alt text](https://github.com/AndreiD/PushNotificationsServer/blob/master/app/static/img/pic_0.jpg "How the app looks 1")


![alt text](https://github.com/AndreiD/PushNotificationsServer/blob/master/app/static/img/pic_1.jpg "Send a message")


#### How to use it:

- `git clone https://github.com/AndreiD/PushNotificationsServer.git <project_name>` or download the zip
- `pip install -r requirements.txt`
- edit the `config.py` with your settings!
- in **run.py** edit the port of the app (Default: 1337)
- `python run.py` -> http://server_ip:1337
- play with it
- modify the API KEY and admin user/password (TODO: move them to config)


#### The android client

- Option 1: step by step follow the official tutorials
- Option 2: https://github.com/AndreiD/PushNotificationsApp 



#### Attention:

About security: at the moment the api is protected only by a secret key. Use ProGuard in your android app, SSL, other auth methods, etc etc

optional edit `/app/templates/base.html`

> <!DOCTYPE html>
> <html lang="en" class="no-js">
> {% set bootstrap_version = '3.2.0' %}
> {% set jquery_version = '2.1.1' %}
> {% set modernizer_version = '2.8.2' %}
> {% set bootswatch_version = '3.2.0' %}
> {% set bootswatch_theme = 'slate' %}


In case a new version appears, and you want to use it. modify it. also you can chose a nice theme from http://bootswatch.com/

in __/app/models.py__ an example with "expenses list" is added.

an example with PAGINATION

##### Extras:

- a supervisord.conf [supervisor is used to monitor the web application and restart it, also starts the app in case you restart your server]
- a simple nginx.conf


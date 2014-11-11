# How to create a server to send push notifications to android devices using python

### Introduction

Push notifications will let your application notify a user of an event even when the user is not using your app. The goal of this tutorial is to send a simple push notification to your app. We'll use Ubuntu 14.04 and Python 2.7

While you can follow this tutorial without any application, it's better if you have an android phone and a test app in order to test that everything is ok. I'll use the term ***DO server*** when I talk about your server, the one that we're going to implement on digial ocean and ***GCM*** about the "google's" server, the one the is between the android device and your server.

## Quick intro into push notifications

Google-provided GCM Connection Servers take messages from a 3rd-party application server and send these messages to a GCM-enabled Android application (the "client app") running on a device. Currently Google provides connection servers for HTTP and XMPP.

![architecture](https://developer.android.com/images/gcm/GCM-arch.png "arch")

In other words, you need a server to communicate with google's server in order to send the notifications. Your server send messages to a GCM (Google Cloud Messaging) connection server, then the connection server enqueues and stores the message, and then sends it to the device when the device is online.

## Step 1 -The Google API Project

We need to create a google api project in order to enable GCM for our app

- Open the [Google Developers Console](https://console.developers.google.com) 
- Click Create Project.
- Enter a project name and click Create.
- Once the project has been created, a page appears that displays your project ID and project number. 
- **Copy the project number**. You'll use it in your android app client

## Step 2 - Enable GCM in your project

![step 1](http://i.imgur.com/Vj2gaDJ.jpg "step 1")
![step 2](http://i.imgur.com/Hrbtuyx.jpg "step 2")

- In the sidebar on the left, select APIs & auth.
- In the displayed list of APIs, turn the Google Cloud Messaging for Android toggle to ON.
- In the sidebar on the left, select APIs & auth > Credentials.
- Under Public API access, click Create new key.
- In the Create a new key dialog, click Server key.
- Supply your server's IP address. If you want to open it to all put 0.0.0.0/0.
- Click Create and **copy the key**. You'll need in the server that we'll write

## Step 3 - OPTION 1 (Easy, just for testing) 
   
   Install from google play a test app that will just tell you your device reg. id. [download from google play](http://play.google.com/store/apps/details?id=com.pushnotificationsapp.app)
   Or you can install it manually, directly from an apk. (Make sure you allow unsigned apps, check security -> allow untrusted apps) from here https://github.com/AndreiD/PushNotificationsApp/blob/master/PushNotificationsApp/PushNotificationsApp-PushNotificationsApp.apk
   The application is already compiled with project number **283442064750** so in your **DO Server** you'll have to use the api key from this project number.
   

## Step 3 - OPTION 2 Setup a test android app (more difficult)

In order to test the notifications, we need to link the app to the google api project that we made. If you are familiar with android apps then skip this step.

- [optional] follow the official guide from [Android Client for push notifications](https://developer.android.com/google/gcm/client.html) 
- get the official sources from here [test client sources](https://code.google.com/p/gcm/) 

Note that the sources are not updated, so you'll have to modify the gradle 

***gcm-client/ GcmClient/ build.gradle***
~~~~
compile "com.google.android.gms:play-services:4.0.+"
~~~~

to 

~~~~
compile "com.google.android.gms:play-services:5.0.89+"
~~~~ 


In the MainActivity.class replace 

~~~~String SENDER_ID = "YOUR_PROJECT_NUMBER_HERE";~~~~

Each time a device registers to GCM it receives a registration ID. We will need this registration id in order to test the server. To get it easy just modify in the **DemoActivity.class**

~~~~
            if (regid.isEmpty()) {
                registerInBackground();
            }else{
                Log.e("==========================","=========================");
                Log.e("regid",regid);
                Log.e("==========================","=========================");
            }
~~~~

after you run the app, look in the logcat and copy-paste the regid somwhere in a text file.


## Step 4 -The 3rd Party Server Quick Intro

Google-provided GCM Connection Servers take messages from a 3rd-party application server and send them to a GCM-enabled Android application (the "client app") running on a device. For example, Google provides connection servers for HTTP and CCS (XMPP).

In this tutorial we'll talk about the **HTTP** part. The HTTP server is downstream only: cloud-to-device. This means you can only send messages from the server to the devices. 

Roles of the server we make

- Able to communicate with your client.
- Able to fire off properly formatted requests to the GCM server.
- Able to handle requests and resend them as needed, using exponential back-off.
- Able to store the API key and client registration IDs. The API key is included in the header of POST requests that send messages.
- Able to generate message IDs to uniquely identify each message it sends. Message IDs should be unique per sender ID.

The client will communicate with your server by sending the registration ID of the device for you to store it and use it when you send the notification. Don't worry now about managing it, it's very simple and GCM provides you with help by giving you error messages in case a registration ID is invalid.

## Step 5 - Setup Python GCM Simple Server 

The following steps are done on a clean Ubuntu 14 droplet.

~~~~ 
sudo apt-get install python-pip python-dev build-essential 
pip install python-gcm 
~~~~

Find out more about python-gcm here https://github.com/geeknam/python-gcm

Create a new python file somewhere on the server. Let's say **/home/test_push.py**
~~~~
nano /home/test_push.py**
~~~~

copy paste the below code

~~~~
from gcm import *

gcm = GCM("AIzaSyDejSxmynqJzzBdyrCS-IqMhp0BxiGWL1M")
data = {'the_message': 'You have x new friends', 'param2': 'value2'}

reg_id = 'APA91bHDRCRNIGHpOfxivgwQt6ZFK3isuW4aTUOFwMI9qJ6MGDpC3MlOWHtEoe8k6PAKo0H_g2gXhETDO1dDKKxgP5LGulZQxTeNZSwva7tsIL3pvfNksgl0wu1xGbHyQxp2CexeZDKEzvugwyB5hywqvT1-UxxxqpL4EUXTWOm0RXE5CrpMk'

gcm.plaintext_request(registration_id=reg_id, data=data)
~~~~

### Explanation:

~~~~ 
from gcm import *
~~~~
We import the Python client for Google Cloud Messaging for Android

~~~~ 
gcm = GCM("AIzaSyDejSxmynqJzzBdyrCS-IqMhp0BxiGWL1M")
~~~~ 
This is our key from the GCM **used in the test app**. Use this key if you plan to test the server using the pre-made android app.

If you made your own android app, enter your project https://console.developers.google.com. The key is under API & Auth - Credentials. Make sure at the allowed server ip is your DO droplet ip (you can find it with the command ifconfig).

~~~~ 
reg_id = 'APA91bHDRCRNIGHpOfxivgwQt6ZFK3isuW4aTUOFwMI9qJ6MGDpC3MlOWHtEoe8k6PAKo0H_g2gXhETDO1dDKKxgP5LGulZQxTeNZSwva7tsIL3pvfNksgl0wu1xGbHyQxp2CexeZDKEzvugwyB5hywqvT1-UxxxqpL4EUXTWOm0RXE5CrpMk' 
~~~~

Now when you run your test app, CGM will give you a reg id. It's written on the screen, just copy paste it into your email or share it.

It will also appear in the log of the android app like this.
~~~~
=======================================
10-04 17:21:07.102    7550-7550/com.pushnotificationsapp.app E/==========================﹕ APA91bHDRCRNIGHpOfxivgwQt6ZFK3isuW4aTUOFwMI9qJ6MGDpC3MlOWHtEoe8k6PAKo0H_g2gXhETDO1dDKKxgP5LGulZQxTeNZSwva7tsIL3pvfNksgl0wu1xGbHyQxp2CexeZDKEzvugwyB5hywqvT1-UJY0KNqpL4EUXTWOm0RxccxpMk
10-04 17:21:07.102    7550-7550/com.pushnotificationsapp.app E/==========================﹕ =======================================
~~~~


Finally, run

~~~~
python test_push.py
~~~~

### Troubleshoting. 

In case no notification appeared on your device after approximately 10 seconds. Follow this steps

- Is your smartphone/tablet connected to the internet ?
- Do you have the correct project key/number ?
- Do you have the correct regid from the app ?
- Is the server is connected to the internet ?

Still nothing appears ? What do the google server responds ?
Check the app's logcat for some errors. 
Still doesn't work. Write the errors that you encountered in the comments.

![push notification example](http://i.imgur.com/GxRGsQ4.png)

## Where to go from here

Once you've done this simple test, you'll probably want to send the notifications to all your users. Remember that you have to send them in pairs of 1000, also if the CGM responds with invalid id, you must remove it from your database. 

If you find this article interesting, share and write your thoughts in the comments.

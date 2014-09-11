# How to create a server to send push notifications to android devices using python

### Introduction

Push notifications will let your application notify a user of an event even when the user is not using your app. We will learn now how to configure a server to send push notifications to the users. In this guide we'll use Ubuntu 14.04 and Python 2.7

While you can follow this tutorial without any test app, it's better if you have a test app in order to test that everything is ok. I'll use the term ***server*** when I talk about your server, the one that we're going to implement on digial ocean and ***GCM*** about the "google's" server, the one the is between the android device and your server.

### Quick intro into push notifications

Google-provided GCM Connection Servers take messages from a 3rd-party application server and send these messages to a GCM-enabled Android application (the "client app") running on a device. Currently Google provides connection servers for HTTP and XMPP.

![alt text](https://developer.android.com/images/gcm/GCM-arch.png "arch")

In other words, you need a server to communicate with google's server in order to send the notifications. Your server send messages to a GCM (Google Cloud Messaging) connection server, then the connection server enqueues and stores the message, and then sends it to the device when the device is online.

### The Google API Project

We need to create a google api project in order to enable GCM for our app

- Open the [Google Developers Console](http://example.net/) 
- Click Create Project.
- Enter a project name and click Create.
- Once the project has been created, a page appears that displays your project ID and project number. 
- **Copy the project number**. You'll use it in your android app client

### Enable GCM in your project

- In the sidebar on the left, select APIs & auth.
- In the displayed list of APIs, turn the Google Cloud Messaging for Android toggle to ON.
- In the sidebar on the left, select APIs & auth > Credentials.
- Under Public API access, click Create new key.
- In the Create a new key dialog, click Server key.
- Supply your server's IP address. If you want to open it to all put 0.0.0.0/0.
- Click Create and **copy the key**. You'll need in the server that we'll write

### Setup a test android app

In order to test the notifications, we need to link the app to the google api project that we made. If you are familiar with this, then skip this step.

You have some options here
- follow the official guide from [Android Client for push notifications](https://developer.android.com/google/gcm/client.html) 
- get the official sources from here [test client sources](https://code.google.com/p/gcm/) 

Note that the sources are not updates, so you'll have to modify the gradle 

***gcm-client/ GcmClient/ build.gradle***
~~~~compile "com.google.android.gms:play-services:4.0.+"~~~~

to 

~~~~compile "com.google.android.gms:play-services:5.0.89+"~~~~ 


In the main activity replace 

~~~~String SENDER_ID = "YOUR_PROJECT_NUMBER_HERE";~~~~

Each time a device registers to GCM it receives a registration ID. We will need this registration id in order to test the server. To get it easy just modify in the main file

~~~~
            if (regid.isEmpty()) {
                registerInBackground();
            }else{
                Log.e("==========================","=========================");
                Log.e("regid",regid);
                Log.e("==========================","=========================");
            }
~~~~

and when you start the app, copy-paste the regid somewhere.


### The 3rd Party Server Setup

Google-provided GCM Connection Servers take messages from a 3rd-party application server and send them to a GCM-enabled Android application (the "client app") running on a device. For example, Google provides connection servers for HTTP and CCS (XMPP).

In this tutorial we'll talk about HTTP part. The HTTP server is downstream only: cloud-to-device. This means you can only send messages from the server to the devices. 

Roles of the server

- Able to communicate with your client.
- Able to fire off properly formatted requests to the GCM server.
- Able to handle requests and resend them as needed, using exponential back-off.
- Able to store the API key and client registration IDs. The API key is included in the header of POST requests that send messages.
- Able to generate message IDs to uniquely identify each message it sends. Message IDs should be unique per sender ID.

The client will communicate with your server by sending the registration ID of the device for you to store it and use it when you send the notification. Don't worry now about managing it, it's very simple and GCM provides you with help by giving you error messages in case a registration ID is invalid.

Let's begin.

In case you don't have pip installed

~~~~sudo apt-get install python-pip python-dev build-essential ~~~~

pip is a package management system used to install and manage software packages





#! /usr/bin/python
#
# apt-get install python-yaml python-requests

import yaml
import requests
import paho.mqtt.client as mqtt
import time



apikey = yaml.load(open("/home/pi/.octoprint/config.yaml"))['api']['key']   #load apikey from machine
header = { 'X-Api-Key': apikey } 						                    #make some headervoodoo to transmit the apikey
baseurl = 'http://octoprint-printer/api/printer/'				            #baseurl for the API call
topictool = 'sometopic/temp/tool'				                            #topic to post to for the tool
topicbed = 'sometopic/temp/bed'	                    			            #topic to post to for the bed
hostname = 'hostname'	        						                    #hostname for the mqtt stuff
broker = 'brokerurl'		        					                    #broker
port = 1883									                                #port of the broker
inverval = 15                                                               #interval in seconds


tool = requests.get(url=baseurl+'tool', headers=header).json
bed = requests.get(url=baseurl+'bed', headers=header).json

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))

def now():
        return int(time.time())

stamp = now()

mqttc = mqtt.Client(hostname,True)
mqttc.connect_async(broker,1883,60)
mqttc.loop_start()


while True:
  if now() - stamp > interval:
    tool = requests.get(url=baseurl+'tool', headers=header).json
    bed = requests.get(url=baseurl+'bed', headers=header).json


    temptool = tool['tool0']['actual']
    tempbed = bed['bed']['actual']
    mqttc.publish(topictool,temptool,0)
    mqttc.publish(topicbed,tempbed,0)
    stamp = now()


# !bin/env python3
# Author(s): cryptopal85
#
# Version history: June 12 2022 - initialising lamp controller
#                  June 12 2022 - Certificate-based SSL/TLS support added
#                               - for the lamp controller
#
# Notes: this interactive shell communicates the broker over SSL/TLS, including
# certificate-based authentication, then presents options to change state of
# sensors/devices. 'mqtt-simulator' simulates all states automatically,
# however, 'mqtt-controller' allows you to manually change state of any
# authenticated sensors/devices' state based on the provided inputs


import time
import random
import ssl
import paho.mqtt.client as mqtt


options = dict()
brokers = "localhost"
options["broker"] = brokers
options["port"] = 8884


def on_message(client, userdata, message):
	print("message received ", str(message.payload.decode("utf-8")))
	print("message topic=", message.topic)
	print("message qos=", message.qos)
	print("message retain flag=", message.retain)


def on_log(client, userdata, level, buf):
	print('log: ', buf)


def on_disconnect(client, userdata, rc=0):
	print("Disconnect: ", str(rc))
	client.loop_stop()


def on_publish(client, userdata, mid):
	print("mid: ", str(mid))


def send_data_to_broker(message, topic, broker, port):
	print("creating new instance")
	client = mqtt.Client("P1", protocol=mqtt.MQTTv5)
	client.on_message = on_message
	client.on_publish = on_publish
	client.on_disconnect = on_disconnect
	
	print("connecting to the broker located in: "+str(broker)+":"+str(port))
	client.tls_set(
		ca_certs='/Users/gurkanhuray/projects/smartdevices/certs/ca/ca.crt',
		certfile='/Users/gurkanhuray/projects/smartdevices/certs/device-sensor/ssa2022client.crt',
		keyfile='/Users/gurkanhuray/projects/smartdevices/certs/device-sensor/ssa2022client.key',
		tls_version=ssl.PROTOCOL_TLSv1_2
	)
	client.connect(options["broker"], options["port"], keepalive=60)
	print("subscribing to topic ", topic)
	client.subscribe(topic=topic)
	print("publishing message to ", topic)
	client.publish(topic, message)
	time.sleep(4)


while True:
	print("\n\n\n\n\n\n[1]: Turn on the sensor/device \n[2]: Turn off the sensor/device\n")
	Scenario = input(
		"What you would like to do? Type 1 for ON - Type 2 for OFF "
	)
	if Scenario == '1':
		topic = input("What topic would you like to store your data under: ")
		message = input("What do you want to send: ")
		send_data_to_broker(message, topic, options["broker"], options["port"])
	elif Scenario == '2':
		topic = input("What topic would you like to store your data under: ")
		message = input("What do you want to send: ")
		send_data_to_broker(message, topic, options["broker"], options["port"])
	else:
		pass
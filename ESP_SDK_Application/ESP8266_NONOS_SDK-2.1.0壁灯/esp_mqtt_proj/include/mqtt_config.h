#ifndef __MQTT_CONFIG_H__
#define __MQTT_CONFIG_H__

#define CFG_HOLDER	0x00FF55A5	/* Change this value to load default configurations */
#define CFG_LOCATION	0x79	/* Please don't change or if you know what you doing */
#define MQTT_SSL_ENABLE

/*DEFAULT CONFIGURATIONS*/

#define MQTT_HOST			"x1000.top" //or "mqtt.yourdomain.com"
#define MQTT_PORT			1884
#define MQTT_BUF_SIZE		1024
#define MQTT_KEEPALIVE		60	 /*second*/

#define MQTT_CLIENT_ID		"DVES_%08X"
#define MQTT_USER			"DVES_USER"
#define MQTT_PASS			"DVES_PASS"

#define STA_SSID "TP-LINK_xuqi2"
#define STA_PASS "xgm10503"
#define STA_TYPE AUTH_WPA2_PSK

#define MQTT_RECONNECT_TIMEOUT 	5	/*second*/

#define DEFAULT_SECURITY	0
#define QUEUE_BUFFER_SIZE		 		2048

#define PROTOCOL_NAMEv31	/*MQTT version 3.1 compatible with Mosquitto v0.15*/
//PROTOCOL_NAMEv311			/*MQTT version 3.11 compatible with https://eclipse.org/paho/clients/testing/*/

#endif // __MQTT_CONFIG_H__

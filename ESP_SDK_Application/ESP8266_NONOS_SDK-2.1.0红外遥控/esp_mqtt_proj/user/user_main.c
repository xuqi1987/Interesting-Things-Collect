/* main.c -- MQTT client example
*
* Copyright (c) 2014-2015, Tuan PM <tuanpm at live dot com>
* All rights reserved.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
*
* * Redistributions of source code must retain the above copyright notice,
* this list of conditions and the following disclaimer.
* * Redistributions in binary form must reproduce the above copyright
* notice, this list of conditions and the following disclaimer in the
* documentation and/or other materials provided with the distribution.
* * Neither the name of Redis nor the names of its contributors may be used
* to endorse or promote products derived from this software without
* specific prior written permission.
*
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
* IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
* ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
* LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
* CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
* SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
* INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
* CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
* ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
* POSSIBILITY OF SUCH DAMAGE.
*/
#include "ets_sys.h"
#include "driver/uart.h"
#include "osapi.h"
#include "mqtt.h"
#include "wifi.h"
#include "config.h"
#include "debug.h"
#include "gpio.h"
#include "user_interface.h"
#include "mem.h"
#include "driver/Adafruit_NeoPixel.h"
#include <string.h>
#include "ir_remote.h"
#include <ctype.h>


MQTT_Client mqttClient;
LOCAL os_timer_t timer;

uint8_t currentColor[3];
uint8_t lastColor[3];

char zt = 1;


int c2i(char ch)
{
        if(isdigit(ch))
                return ch - 48;

        if( ch < 'A' || (ch > 'F' && ch < 'a') || ch > 'z' )
                return -1;
        if(isalpha(ch))
                return isupper(ch) ? ch - 55 : ch - 87;

        return -1;
}


int hex2dec(char *hex)
{
        int len;
        int num = 0;
        int temp;
        int bits;
        int i;
        
        len = strlen(hex);

        for (i=0, temp=0; i<len; i++, temp=0)
        {
                temp = c2i( *(hex + i) );

                bits = (len - i - 1) * 4;
                temp = temp << bits;
                num = num | temp;
        }
        return num;
}





LOCAL void ICACHE_FLASH_ATTR send_code_task(void *arg)
{
	ir_remote_send_samsung(0xE0E040BF, 32); // power on/off code for Yamaha RX-700
}


void wifiConnectCb(uint8_t status)
{
	if(status == STATION_GOT_IP){
		MQTT_Connect(&mqttClient);
	} else {
		MQTT_Disconnect(&mqttClient);
	}
}
void mqttConnectedCb(uint32_t *args)
{
	MQTT_Client* client = (MQTT_Client*)args;
	INFO("MQTT: Connected\r\n");
	MQTT_Subscribe(client, "/home/#", 0);
	MQTT_Publish(client, "/home/colorlight/status", "on", 3, 0, 0);
	//MQTT_Publish(client, "/mqtt/topic/0", "hello0", 6, 0, 0);
	//MQTT_Publish(client, "/mqtt/topic/1", "hello1", 6, 1, 0);
	//MQTT_Publish(client, "/mqtt/topic/2", "hello2", 6, 2, 0);

}

void mqttDisconnectedCb(uint32_t *args)
{
	MQTT_Client* client = (MQTT_Client*)args;
	INFO("MQTT: Disconnected\r\n");
	MQTT_Publish(client, "/home/colorlight/status", "off", 4, 0, 0);
}

void mqttPublishedCb(uint32_t *args)
{
	MQTT_Client* client = (MQTT_Client*)args;
	INFO("MQTT: Published\r\n");
}


void processMqttMsg(const char* topic,char *data)
{
	char* tmp = NULL;
	uint8_t buff[4];
	uint8_t i =0;

	if (strcmp(topic,"/home/irremote") == 0)
	{
		ir_remote_send_samsung(hex2dec(data), 32);
	}
	else
	{

	}
}

void mqttDataCb(uint32_t *args, const char* topic, uint32_t topic_len, const char *data, uint32_t data_len)
{
	char *topicBuf = (char*)os_zalloc(topic_len+1),
			*dataBuf = (char*)os_zalloc(data_len+1);

	MQTT_Client* client = (MQTT_Client*)args;

	os_memcpy(topicBuf, topic, topic_len);
	topicBuf[topic_len] = 0;

	os_memcpy(dataBuf, data, data_len);
	dataBuf[data_len] = 0;
	
	processMqttMsg(topicBuf,dataBuf);
	INFO("Receive topic: %s, data: %s \r\n", topicBuf, dataBuf);
	
	os_free(topicBuf);
	os_free(dataBuf);

}


/******************************************************************************
 * FunctionName : user_rf_cal_sector_set
 * Description  : SDK just reversed 4 sectors, used for rf init data and paramters.
 *                We add this function to force users to set rf cal sector, since
 *                we don't know which sector is free in user's application.
 *                sector map for last several sectors : ABCCC
 *                A : rf cal
 *                B : rf init data
 *                C : sdk parameters
 * Parameters   : none
 * Returns      : rf cal sector
 *******************************************************************************/
uint32 ICACHE_FLASH_ATTR
user_rf_cal_sector_set(void)
{
    enum flash_size_map size_map = system_get_flash_size_map();
    uint32 rf_cal_sec = 0;

    switch (size_map) {
        case FLASH_SIZE_4M_MAP_256_256:
            rf_cal_sec = 128 - 5;
            break;

        case FLASH_SIZE_8M_MAP_512_512:
            rf_cal_sec = 256 - 5;
            break;

        case FLASH_SIZE_16M_MAP_512_512:
        case FLASH_SIZE_16M_MAP_1024_1024:
            rf_cal_sec = 512 - 5;
            break;

        case FLASH_SIZE_32M_MAP_512_512:
        case FLASH_SIZE_32M_MAP_1024_1024:
            rf_cal_sec = 1024 - 5;
            break;

        case FLASH_SIZE_64M_MAP_1024_1024:
            rf_cal_sec = 2048 - 5;
            break;
        case FLASH_SIZE_128M_MAP_1024_1024:
            rf_cal_sec = 4096 - 5;
            break;
        default:
            rf_cal_sec = 0;
            break;
    }

    return rf_cal_sec;
}

void timer_callback()
{

	if(zt == 1) {
		//SEND_WS_0();
		//GPIO_OUTPUT_SET(GPIO_ID_PIN(2),1);
		//WS2812B_Init();
		INFO("1");
		zt = 0;
	}
	else{
		//GPIO_OUTPUT_SET(GPIO_ID_PIN(2),0);
		zt = 1;
		//WS2812B_Test();
		INFO("0");
		}


	
}

void user_init(void)
{
	uart_init(BIT_RATE_115200, BIT_RATE_115200);
	ir_remote_init(PERIPHS_IO_MUX_GPIO2_U, FUNC_GPIO2, 2, true);


	os_delay_us(60000);

	CFG_Load();

	//MQTT_InitConnection(&mqttClient, sysCfg.mqtt_host, sysCfg.mqtt_port, sysCfg.security);
	MQTT_InitConnection(&mqttClient, "x1000.top", 1884, 0);
	
	MQTT_InitClient(&mqttClient, sysCfg.device_id, sysCfg.mqtt_user, sysCfg.mqtt_pass, sysCfg.mqtt_keepalive, 1);
	//MQTT_InitClient(&mqttClient, "client_id", "user", "pass", 120, 1);

	MQTT_InitLWT(&mqttClient, "/lwt", "offline", 0, 0);
	MQTT_OnConnected(&mqttClient, mqttConnectedCb);
	MQTT_OnDisconnected(&mqttClient, mqttDisconnectedCb);
	MQTT_OnPublished(&mqttClient, mqttPublishedCb);
	MQTT_OnData(&mqttClient, mqttDataCb);
	
	WIFI_Connect(sysCfg.sta_ssid, sysCfg.sta_pwd, wifiConnectCb);
	
	//os_timer_disarm(&timer);
	//os_timer_setfn(&timer, (os_timer_func_t *)send_code_task, (void *)0);
	//os_timer_arm(&timer, 2000, 1);

	INFO("\r\nSystem started ...\r\n");
}

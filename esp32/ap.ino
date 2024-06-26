#include <WiFi.h>
#include "esp_wifi.h"

const char* ssid     = "ESP32_AP_REVOLT";
const char* password = "123456789";

const int   channel        = 10;
const bool  hide_SSID      = false;
const int   max_connection = 10;

WiFiServer server(80);

int previousClientCount = 0;

void setup(){
  Serial.begin(115200);
  Serial.println("\n[*] Creating AP");
  WiFi.mode(WIFI_AP);

  WiFi.softAP(ssid, password, channel, hide_SSID, max_connection);
  Serial.print("[+] AP Created with IP Gateway ");
  Serial.println(WiFi.softAPIP());

  server.begin();
}

void loop(){
  int currentClientCount = WiFi.softAPgetStationNum();

  if (currentClientCount != previousClientCount) {
    if (currentClientCount > previousClientCount) {
      Serial.println("[Client Connected]");
    } else {
      Serial.println("[Client Disconnected]");
    }
    displayClientInfo();
    previousClientCount = currentClientCount;
  }

  WiFiClient client = server.available();   // Listen for incoming clients

  if (client) {
    Serial.println("[New Client]");
    while (client.connected()) {
      if (client.available()) {
        String request = client.readStringUntil('\r');
        Serial.println(request);
        client.flush();
        
        // Respond to client
        client.println("HTTP/1.1 200 OK");
        client.println("Content-Type: text/html");
        client.println("");
        client.println("<!DOCTYPE HTML>");
        client.println("<html>");
        client.println("<h1>Hello from ESP32</h1>");
        client.println("</html>");
        break;
      }
    }
    delay(1);
    client.stop();
    Serial.println("[Client Disconnected]");
  }
}

void displayClientInfo() {
  wifi_sta_list_t wifi_sta_list;
  tcpip_adapter_sta_list_t adapter_sta_list;

  memset(&wifi_sta_list, 0, sizeof(wifi_sta_list));
  memset(&adapter_sta_list, 0, sizeof(adapter_sta_list));

  esp_wifi_ap_get_sta_list(&wifi_sta_list);
  tcpip_adapter_get_sta_list(&wifi_sta_list, &adapter_sta_list);

  Serial.println("Connected clients:");
  for (int i = 0; i < adapter_sta_list.num; i++) {
    tcpip_adapter_sta_info_t station = adapter_sta_list.sta[i];
    Serial.print("Station IP: ");
    Serial.println(IPAddress(station.ip.addr));
    Serial.print("Station MAC: ");
    Serial.printf("%02X:%02X:%02X:%02X:%02X:%02X\n",
                  station.mac[0], station.mac[1], station.mac[2],
                  station.mac[3], station.mac[4], station.mac[5]);
  }
  Serial.println();
}

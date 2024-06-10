import sys
from scapy.all import rdpcap, DNSQR

def parse_pcap(file_path):
    packets = rdpcap(file_path)
    connections = set()
    dns_queries = set()

    for packet in packets:
        if packet.haslayer('IP'):
            ip_layer = packet['IP']
            if packet.haslayer('TCP'):
                proto = 'TCP'
                src_port = packet['TCP'].sport
                dst_port = packet['TCP'].dport
            elif packet.haslayer('UDP'):
                proto = 'UDP'
                src_port = packet['UDP'].sport
                dst_port = packet['UDP'].dport

                if packet.haslayer(DNSQR):  # Check for DNS queries
                    dns_layer = packet[DNSQR]
                    dns_query = (
                        ip_layer.src,
                        src_port,
                        ip_layer.dst,
                        dst_port,
                        'DNS',
                        dns_layer.qname.decode('utf-8') if isinstance(dns_layer.qname, bytes) else dns_layer.qname
                    )
                    dns_queries.add(dns_query)
                    continue
            else:
                continue

            connection = (
                ip_layer.src,
                src_port,
                ip_layer.dst,
                dst_port,
                proto
            )
            connections.add(connection)

    return connections, dns_queries

def display_connections(connections, dns_queries):
    print(f"{'Source IP':<20} {'Source Port':<12} {'Destination IP':<20} {'Destination Port':<15} {'Protocol':<8}")
    print("-" * 80)
    for conn in connections:
        src_ip, src_port, dst_ip, dst_port, proto = conn
        print(f"{src_ip:<20} {src_port:<12} {dst_ip:<20} {dst_port:<15} {proto:<8}")
    
    if dns_queries:
        print("\nDNS Queries:")
        print(f"{'Source IP':<20} {'Source Port':<12} {'Destination IP':<20} {'Destination Port':<15} {'Protocol':<8} {'Query':<30}")
        print("-" * 120)
        for query in dns_queries:
            src_ip, src_port, dst_ip, dst_port, proto, qname = query
            print(f"{src_ip:<20} {src_port:<12} {dst_ip:<20} {dst_port:<15} {proto:<8} {qname:<30}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <pcap_file>")
        sys.exit(1)

    pcap_file = sys.argv[1]
    connections, dns_queries = parse_pcap(pcap_file)
    display_connections(connections, dns_queries)
import socket

def send_udp_packets(destination_ip, destination_port, packet_size, num_packets):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destination_address = (destination_ip, destination_port)
    data = b'a' * packet_size

    try:
        for _ in range(num_packets):
            udp_socket.sendto(data, destination_address)

        print(f"Wysłano {num_packets} pakietów UDP do {destination_ip}:{destination_port}")

    except Exception as e:
        print(f"Wystąpił błąd podczas wysyłania pakietów: {e}")

    finally:
        udp_socket.close()

destination_ip = '192.168.114.255'
destination_port = 12054
packet_size = 65000 # w przypadku wysyłania maksymalnej długości 65515, terminal daje nam informację, że wiadmość jest za długa  
num_packets = 100000 

send_udp_packets(destination_ip, destination_port, packet_size, num_packets)

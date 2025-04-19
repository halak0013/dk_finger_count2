import socket
import cv2


class DKConnection:
    def __init__(self):
        self.udp_ip = "0.0.0.0"  # For receiving
        self.udp_port = 14537
        
        # Create socket for sending broadcasts
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Set socket option for broadcast
        self.send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Create separate socket for receiving (if needed)
        self.recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_sock.bind((self.udp_ip, self.udp_port))

    def send_message(self, message):
        try:
            message_bytes = message.encode('utf-8')
            self.send_sock.sendto(message_bytes, ("255.255.255.255", self.udp_port))
        except Exception as e:
            print("Error in sending data:", e)
            
    def receive_message(self, buffer_size=1024):
        """Receive incoming messages"""
        try:
            data, addr = self.recv_sock.recvfrom(buffer_size)
            return data.decode('utf-8'), addr
        except Exception as e:
            print("Error in receiving data:", e)
            return None, None

    def close(self):
        self.send_sock.close()
        self.recv_sock.close()
        print("Sockets closed")


def main():
    import time
    dk_connection = DKConnection()
    while True:
        dk_connection.send_message("[0,0,0,0,0]")

        time.sleep(1)

    # Close the connection
    dk_connection.close()
if __name__ == "__main__":
    main()
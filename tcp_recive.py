import socket
import json
from datetime import datetime
import paho.mqtt.client as mqtt
mqtt_client = mqtt.Client(client_id="mqtt_data_sender")
mqtt_client.connect("192.168.64.1", 1883)
mqtt_client.loop_start()


def bytes_to_integers(data: bytes) -> list:
    return [
        int.from_bytes(data[i:i + 2], byteorder='little', signed=True)
        for i in range(0, len(data), 2)
    ]


def send_mqtt_data(channel_buffers):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    channels = {}
    for channel_index, buffer in enumerate(channel_buffers):
        if buffer:
            channels[f"ch{channel_index + 1}"] = buffer
            channel_buffers[channel_index] = []
    if channels:
        message = {
            "ts": timestamp,
            "channels": channels
        }
        print(json.dumps(message, indent=2))
        mqtt_client.publish("device/channel", json.dumps(message), qos=1)


def main():
    host = '127.0.0.1'
    port = 7777
    buffer_size = 5328
    bytes_per_send = 511488
    channel_buffers = [[] for _ in range(16)]
    data_cache = b''
    total_received = 0
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f'Listening on {host}:{port}...')
    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Connection from {client_address} established.')
        try:
            while True:
                data = client_socket.recv(buffer_size)
                if not data:
                    break
                data_cache += data
                total_received += len(data)
                if total_received >= bytes_per_send:
                    process_length = bytes_per_send - 512
                    reals = bytes_to_integers(data_cache[:process_length])
                    for i, value in enumerate(reals):
                        channel = i % 16
                        channel_buffers[channel].append(value)
                    send_mqtt_data(channel_buffers)
                    data_cache = data_cache[bytes_per_send:]
                    total_received = len(data_cache)
        except Exception as e:
            print(f'Error: {e}')
        finally:
            client_socket.close()
            print('Client disconnected.')


if __name__ == '__main__':
    main()
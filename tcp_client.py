import math
import socket
import time
import random
SAMPLE_RATE = 200000
WAVEFORM_LENGTH = SAMPLE_RATE
SERVER_IP = '127.0.0.1'
SERVER_PORT = 7777
SAMPLE_PER_BATCH = 1000
SEND_INTERVAL = 0.001


def generate_waveform(amplitude, offset, frequency=50.0):
    waveform = []
    for t in range(WAVEFORM_LENGTH):
        base = offset + amplitude * math.sin(2 * math.pi * frequency * t / SAMPLE_RATE)
        noise = random.uniform(-0.02, 0.02) * base
        noisy_value = base + noise
        int_value = int(noisy_value * 100)
        waveform.append(int_value)
    return waveform


def generate_waveforms():
    return [
        generate_waveform(amplitude=100, offset=220, frequency=50),
        generate_waveform(amplitude=20, offset=15, frequency=10),
        generate_waveform(amplitude=80, offset=230, frequency=60),
        generate_waveform(amplitude=25, offset=10, frequency=5)
    ]


def generate_interleaved_data(waveforms, index, sample_count):
    data = bytearray()
    for i in range(sample_count):
        pos = (index + i) % WAVEFORM_LENGTH
        for ch in range(4):
            value = waveforms[ch][pos]
            value = min(max(value, 0), 65535)
            data.extend(value.to_bytes(2, byteorder='big'))
    return bytes(data)


def connect_to_server(ip, port):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            print(f"[✓] Connected to {ip}:{port}")
            return sock
        except Exception as e:
            print(f"[×] Connection failed: {e}, retrying in 3s...")
            time.sleep(3)


def main():
    waveforms = generate_waveforms()
    current_index = 0
    while True:
        client_socket = connect_to_server(SERVER_IP, SERVER_PORT)
        try:
            while True:
                data = generate_interleaved_data(waveforms, current_index, SAMPLE_PER_BATCH)
                client_socket.sendall(data)
                print(f"[→] Sent {len(data)} bytes")
                current_index = (current_index + SAMPLE_PER_BATCH) % WAVEFORM_LENGTH
                time.sleep(SEND_INTERVAL)
        except Exception as e:
            print(f"[!] Send error or connection lost: {e}")
        finally:
            client_socket.close()
            print("[⨯] Connection closed, retrying...")
            time.sleep(2)


if __name__ == '__main__':
    main()
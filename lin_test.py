import serial
import time
from BitVector import BitVector


def add_parity(x): # Add the P0 and P1 parity bits to the PID
    ar = BitVector(rawbytes = x)
    ar[1] =  ar[7] ^ ar[6] ^ ar[5] ^ ar[3]
    ar[0] = ar[6] ^ ar[4] ^ ar[3] ^ ar[2] ^ 1
    return int(ar).to_bytes(1, 'big')

def chksum(x): # Generate the enhanced checksum byte (data + pid)
    sum = 0
    for i in x:
        sum = sum + i
        if(sum > 256):
            sum = sum -255
    cksum = ~sum & 0xFF
    return cksum.to_bytes(1, 'big')

def send_break(): #hacky way to send a break longer than a byte
    ser = serial.Serial('/dev/ttyUSB0', 10000)
    ser.write({0x00})
    ser.close()
    time.sleep(0.001)
    
def send_req(pid):
    send_break()
    rx_pid = pid
    rx_pid = add_parity(rx_pid)
    ser = serial.Serial('/dev/ttyUSB0', 20000)
    ser.timeout = 0.1
    tx_bytes = bytearray(b"\x55" + rx_pid)
    ser.write(tx_bytes)
    time.sleep(0.05)
    in_bytes = ser.in_waiting
    out = ser.read(in_bytes)
    #if(in_bytes > 3):
    b0_str = (" RPM:" + str(int.from_bytes(out[3:4], "big")*23.6))
    volt_str = ("\tVolt:" + str(int.from_bytes(out[4:5], "big")/10.0))
    b2_str = ("\tT:" + str(int.from_bytes(out[5:6], "big")))
    b3_str = ("\tI:" + str(int.from_bytes(out[6:7], "big")))
    b4_str = ("\tB4:" + str(int.from_bytes(out[7:8], "big")))
    b5_str = ("\tB5:" + str(int.from_bytes(out[8:9], "big")))
    b6_str = ("\tB6:" + str(int.from_bytes(out[9:10], "big")))
    ser.close()
    return(b0_str + volt_str + b2_str + b3_str + b4_str + b5_str + b6_str)
    
def send_data(pid, data):
    send_break()
    tx_pid = pid
    tx_pid = add_parity(tx_pid)
    tx_data = data
    tx_ck = chksum(tx_pid+tx_data)
    ser = serial.Serial('/dev/ttyUSB0', 20000)
    ser.timeout = 0.1
    tx_bytes = bytearray(b"\x55" + tx_pid + tx_data + tx_ck)
    ser.write(tx_bytes)
    while(ser.out_waiting):
        time.sleep(0.01)
    ser.reset_input_buffer()
    ser.close()
    return("TX:" + tx_bytes[2:-1].hex())

def rpm_sweep():
    with open('log.txt', 'w') as f:
        for i in range(0x0000, 0xFFFF, 0x100):
            for j in range(9):
                send_req(b'\x25')
                send_data(b'\x26', (i.to_bytes(2, 'big')),)

            rx_msg = send_req(b'\x25')
            tx_msg = send_data(b'\x26', (i.to_bytes(2, 'big')))
            print(tx_msg + rx_msg)
            f.write(tx_msg + rx_msg + "\r")
        tx_msg = send_data(b'\x26', b'\x00\x00')

if __name__ == '__main__':
    rpm_sweep()


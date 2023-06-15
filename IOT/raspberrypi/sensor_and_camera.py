import fcntl
import time
import unittest
import os
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import threading

class SHT21:
    """Class to read temperature and humidity from SHT21, much of class was
    derived from:
    http://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/Humidity/Sensirion_Humidity_SHT21_Datasheet_V3.pdf
    and Martin Steppuhn's code from http://www.emsystech.de/raspi-sht21"""

    # control constants
    _SOFTRESET = 0xFE
    _I2C_ADDRESS = 0x40
    _TRIGGER_TEMPERATURE_NO_HOLD = 0xF3
    _TRIGGER_HUMIDITY_NO_HOLD = 0xF5
    _STATUS_BITS_MASK = 0xFFFC

    # From: /linux/i2c-dev.h
    I2C_SLAVE = 0x0703
    I2C_SLAVE_FORCE = 0x0706

    # datasheet (v4), page 9, table 7, thanks to Martin Milata
    # for suggesting the use of these better values
    # code copied from https://github.com/mmilata/growd
    _TEMPERATURE_WAIT_TIME = 0.086  # (datasheet: typ=66, max=85)
    _HUMIDITY_WAIT_TIME = 0.030     # (datasheet: typ=22, max=29)

    def __init__(self, device_number=0):
        """Opens the i2c device (assuming that the kernel modules have been
        loaded).  Note that this has only been tested on first revision
        raspberry pi where the device_number = 0, but it should work
        where device_number=1"""
        self.i2c = open('/dev/i2c-%s' % device_number, 'r+', 0)
        fcntl.ioctl(self.i2c, self.I2C_SLAVE, 0x40)
        self.i2c.write(chr(self._SOFTRESET))
        time.sleep(0.050)

    def read_temperature(self):    
        """Reads the temperature from the sensor.  Not that this call blocks
        for ~86ms to allow the sensor to return the data"""
        self.i2c.write(chr(self._TRIGGER_TEMPERATURE_NO_HOLD))
        time.sleep(self._TEMPERATURE_WAIT_TIME)
        data = self.i2c.read(3)
        if self._calculate_checksum(data, 2) == ord(data[2]):
            return self._get_temperature_from_buffer(data)

    def read_humidity(self):    
        """Reads the humidity from the sensor.  Not that this call blocks
        for ~30ms to allow the sensor to return the data"""
        self.i2c.write(chr(self._TRIGGER_HUMIDITY_NO_HOLD))
        time.sleep(self._HUMIDITY_WAIT_TIME)
        data = self.i2c.read(3)
        if self._calculate_checksum(data, 2) == ord(data[2]):
            return self._get_humidity_from_buffer(data)

    def close(self):
        """Closes the i2c connection"""
        self.i2c.close()

    def __enter__(self):
        """used to enable python's with statement support"""
        return self

    def __exit__(self, type, value, traceback):
        """with support"""
        self.close()

    @staticmethod
    def _calculate_checksum(data, number_of_bytes):
        """5.7 CRC Checksum using the polynomial given in the datasheet"""
        # CRC
        POLYNOMIAL = 0x131  # //P(x)=x^8+x^5+x^4+1 = 100110001
        crc = 0
        # calculates 8-Bit checksum with given polynomial
        for byteCtr in range(number_of_bytes):
            crc ^= (ord(data[byteCtr]))
            for bit in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ POLYNOMIAL
                else:
                    crc = (crc << 1)
        return crc


    @staticmethod
    def _get_temperature_from_buffer(data):
        """This function reads the first two bytes of data and
        returns the temperature in C by using the following function:
        T = -46.85 + (175.72 * (ST/2^16))
        where ST is the value from the sensor
        """
        unadjusted = (ord(data[0]) << 8) + ord(data[1])
        unadjusted &= SHT21._STATUS_BITS_MASK  # zero the status bits
        unadjusted *= 175.72
        unadjusted /= 1 << 16  # divide by 2^16
        unadjusted -= 46.85
        return unadjusted


    @staticmethod
    def _get_humidity_from_buffer(data):
        """This function reads the first two bytes of data and returns
        the relative humidity in percent by using the following function:
        RH = -6 + (125 * (SRH / 2 ^16))
        where SRH is the value read from the sensor
        """
        unadjusted = (ord(data[0]) << 8) + ord(data[1])
        unadjusted &= SHT21._STATUS_BITS_MASK  # zero the status bits
        unadjusted *= 125.0
        unadjusted /= 1 << 16  # divide by 2^16
        unadjusted -= 6
        return unadjusted


class SHT21Test(unittest.TestCase):
    """simple sanity test.  Run from the command line with
    python -m unittest sht21 to check they are still good"""

    def test_temperature(self):
        """Unit test to check the checksum method"""
        calc_temp = SHT21._get_temperature_from_buffer([chr(99), chr(172)])
        self.failUnless(abs(calc_temp - 21.5653979492) < 0.1)

    def test_humidity(self):
        """Unit test to check the humidity computation using example
        from the v4 datasheet"""
        calc_temp = SHT21._get_humidity_from_buffer([chr(99), chr(82)])
        self.failUnless(abs(calc_temp - 42.4924) < 0.001)

     def test_checksum(self):
        """Unit test to check the checksum method.  Uses values read"""
        self.failUnless(SHT21._calculate_checksum([chr(99), chr(172)], 2) == 249)
        self.failUnless(SHT21._calculate_checksum([chr(99), chr(160)], 2) == 132)

def gas_callback(channel):
    print("Gas detected\n")
    #client.publish("btn","0", qos = 0);
    #threading.Thread(target=run_camera).start()


def fire_callback(channel):
    print("fire detected\n")
    client2.publish("TruthCenter/101/fire","0", qos = 0);
    threading.Thread(target=run_camera).start()


def vibe_callback(channel):
    print("vibe detected\n")
    client2.publish("TruthCenter/101/vibrate","0" ,qos=0);

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: "+connack_string(rc))

def on_disconnect(client, userdata, rc):
    global flag_connected
    print("client disconnected")
    flag_connected = 0


def run_camera():
    os.system("ffmpeg -i /dev/video0 -t 10 http://192.168.0.45:8090/feed.ffm")

if __name__ == "__main__":
    client = mqtt.Client("GongHakGwan 1F")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client2 = mqtt.Client("GongHakGwan 1F urgent")
    client.connect("192.168.0.39","1883")
    client2.connect("192.168.0.39","1884")
    client2.loop_start()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.IN)
    GPIO.setup(6, GPIO.IN)
    GPIO.setup(12, GPIO.IN)
    GPIO.add_event_detect(16, GPIO.RISING, callback=gas_callback, bouncetime=200)
    GPIO.add_event_detect(6, GPIO.RISING, callback=fire_callback, bouncetime=200)
    GPIO.add_event_detect(12, GPIO.RISING, callback=vibe_callback, bouncetime=500)
    temp = 25
    humid= 55
    while(True):
        try:
            with SHT21(1) as sht21:
                temp = sht21.read_temperature()
                humid = sht21.read_humidity()
                print('Temperature: {}'.format(temp))
                print('Humidity: {}'.format(humid))                

        except IOError:
            print ("Error creating connection to i2c.  This must be run as root")
        print('Gas: {}'.format(GPIO.input(16)))
        print('fire: {}'.format(GPIO.input(6)))
        print('vibe: {}'.format(GPIO.input(12)))            

        client.publish("TruthCenter/101/gas","1" ,qos=0);
        client.publish("TruthCenter/101/fire","{}".format(GPIO.input(6)) ,qos=0);
        client.publish("TruthCenter/101/vibrate","{}".format(GPIO.input(12)) ,qos=0);
        client.publish("TruthCenter/101/temperature","{}".format(round(temp*100)/100) ,qos=0);
        client.publish("TruthCenter/101/humid","{}".format(round(humid*100)/100) ,qos=0);
        time.sleep(1)      

    client.close()
    GPIO.cleanup()
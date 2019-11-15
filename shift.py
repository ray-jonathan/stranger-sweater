import RPi.GPIO as GPIO
import time

# Special thanks to Dan McDougall (liftoff @ git) for the following repo as a starting point:
# https://gist.github.com/liftoff/a99317c12bbf068382fc


class Shifter(object):
    def __init__(self, data_pin=19, latch_pin=21, clock_pin=23, invert=False):
        self.data_pin = data_pin
        self.latch_pin = latch_pin
        self.clock_pin = clock_pin
        self.y = 13
        self.z = 15
        self.invert = invert
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.latch_pin, GPIO.OUT)  # Setup GPIO Pin to OUT
        GPIO.setup(self.clock_pin, GPIO.OUT)  # Setup GPIO Pin to OUT
        GPIO.setup(self.data_pin, GPIO.OUT)  # Setup GPIO Pin to OUT
        GPIO.setup(self.y, GPIO.OUT)
        GPIO.setup(self.z, GPIO.OUT)
        self.HIGH = True
        self.LOW = False
        self.dict_a_to_h = {
            'A': 0b00000001,
            'B': 0b00000010,
            'C': 0b00000100,
            'D': 0b00001000,
            'E': 0b00010000,
            'F': 0b00100000,
            'G': 0b01000000,
            'H': 0b10000000,
        }
        self.dict_i_to_p = {
            'I': 0b00000001,
            'J': 0b00000010,
            'K': 0b00000100,
            'L': 0b00001000,
            'M': 0b00010000,
            'N': 0b00100000,
            'O': 0b01000000,
            'P': 0b10000000,
        }
        self.dict_q_to_x = {
            'Q': 0b00000001,
            'R': 0b00000010,
            'S': 0b00000100,
            'T': 0b00001000,
            'U': 0b00010000,
            'V': 0b00100000,
            'W': 0b01000000,
            'X': 0b10000000,
        }

    def letter(self, ltr):
        if ltr in self.dict_a_to_h:
            self.shift_out(self.dict_a_to_h[ltr], 0b00000000, 0b00000000)
            GPIO.output(self.y, self.LOW)
            GPIO.output(self.z, self.LOW)
        elif ltr in self.dict_i_to_p:
            self.shift_out(0b00000000, self.dict_i_to_p[ltr], 0b00000000)
            GPIO.output(self.y, self.LOW)
            GPIO.output(self.z, self.LOW)
        elif ltr in self.dict_q_to_x:
            self.shift_out(0b00000000, 0b00000000, self.dict_q_to_x[ltr])
            GPIO.output(self.y, self.LOW)
            GPIO.output(self.z, self.LOW)
        elif ltr == 'Y':
            self.all(self.LOW)
            GPIO.output(self.y, self.HIGH)
        elif ltr == 'Z':
            self.all(self.LOW)
            GPIO.output(self.z, self.HIGH)
        else:
            self.all(self.LOW)

    def spell(self, txt):
        for ltr in txt.upper():
            self.letter(ltr)
            time.sleep(.5)
            self.all(self.LOW)
            time.sleep(.25)

    def shift_out(self, *values):
        bits = {'0': False, '1': True}
        if self.invert:
            bits = {'1': False, '0': True}
        GPIO.output(self.latch_pin, self.LOW)
        for val in reversed(values):
            for bit in '{0:08b}'.format(val):
                GPIO.output(self.clock_pin, self.LOW)
                GPIO.output(self.data_pin, bits[bit])
                GPIO.output(self.clock_pin, self.HIGH)
        GPIO.output(self.latch_pin, self.HIGH)

    def test(self):
        for i in range(16):
            self.shift_out(1 << i)
            time.sleep(0.25)
            self.shift_out(0)
            time.sleep(0.25)

    def all(self, state=False):
        if state:
            self.shift_out(0b11111111, 0b11111111, 0b11111111)
            GPIO.output(self.y, self.HIGH)
            GPIO.output(self.z, self.HIGH)
        else:
            self.shift_out(0b00000000, 0b00000000, 0b00000000)
            GPIO.output(self.y, self.LOW)
            GPIO.output(self.z, self.LOW)

    def radiate(self):
        GPIO.output(self.y, self.LOW)
        GPIO.output(self.z, self.LOW)
        # HGFEDCBA, PONMLKJI, XWVUTSRQ
        self.shift_out(0b00000000, 0b00010000, 0b00000000)
        time.sleep(.3)
        self.shift_out(0b00011100, 0b0011100, 0b01110000)
        time.sleep(.3)
        self.shift_out(0b00111110, 0b01111100, 0b11111000)
        time.sleep(.3)
        self.shift_out(0b01111111, 0b11111110, 0b11111100)
        GPIO.output(self.y, self.HIGH)
        time.sleep(.3)
        self.all(True)
        time.sleep(.3)


# if __name__ == '__main__':
#     print('Testing shift register connection...')
#     GPIO.setmode(GPIO.BOARD)  # Use board pin numbering
#     s = Shifter()
#     didNotRunTest = True
#     try:
#         while didNotRunTest:
#             s.test()
#             didNotRunTest = False
#     except KeyboardInterrupt:
#         print('Ctrl-C detected.  Quitting...')

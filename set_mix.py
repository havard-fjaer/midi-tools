import mido
import time

DEBUG = True
SLEEP_TIME = 0.01

INPUT_PORT_NAME = 'nanoKONTROL2 SLIDER/KNOB'
OUTPUT_PORT_NAME = 'ES-9 MIDI Out'

VENDOR_EXPERT_SLEEPERS = [0x00, 0x21, 0x27]
DEVICE_ES9 = [0x19]
MESSAGE_TYPE_SET_VIRTUAL_MIX = [0x34]


def main():
    try:
        out_port = mido.open_output(OUTPUT_PORT_NAME)
        in_port = mido.open_input(INPUT_PORT_NAME)

        while True:
            for message in in_port.iter_pending():
        
                print_debug(message)
                faders = message.control in range(0, 7)
                pots = message.control in range(16, 23)

                if message.type == 'control_change' and (faders or pots):
                    data = VENDOR_EXPERT_SLEEPERS + DEVICE_ES9 + MESSAGE_TYPE_SET_VIRTUAL_MIX + [message.control] + [message.value]
                    out_port.send(mido.Message('sysex', data=data))

            time.sleep(SLEEP_TIME)

    except KeyboardInterrupt:
        pass
    finally:
        in_port.close()
        out_port.close()


def print_debug(msg):
    if DEBUG:
        print(msg)

if __name__ == '__main__':
    main()        
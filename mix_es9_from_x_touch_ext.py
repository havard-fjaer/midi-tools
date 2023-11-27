""" Script for å kontrollere ES-9 med X-Touch Ext - NOT WORKING YET"""
import mido
import time

DEBUG = True
SLEEP_TIME = 0.1

X_TOUCH_INPUT_PORT_NAME = 'X-Touch-Ext X-TOUCH_INT'
X_TOUCH_OUTPUT_PORT_NAME = 'X-Touch-Ext X-TOUCH_INT'
ES9_OUTPUT_PORT_NAME = 'ES-9 MIDI Out'
ES9_INPUT_PORT_NAME = 'ES-9 MIDI In'

VENDOR_EXPERT_SLEEPERS = [0x00, 0x21, 0x27]
DEVICE_ES9 = [0x19]
MESSAGE_TYPE_SET_VIRTUAL_MIX = [0x34]
MESSAGE_TYPE_REQUEST_MIX = [0x2A]
CONTROL_INDEX = 5

def main():
    try:
        es9_in_port = mido.open_input(ES9_INPUT_PORT_NAME)
        es9_out_port = mido.open_output(ES9_OUTPUT_PORT_NAME)
        x_touch_in_port = mido.open_input(X_TOUCH_INPUT_PORT_NAME)
        x_touch_out_port = mido.open_output(X_TOUCH_OUTPUT_PORT_NAME)

        while True:
            for message in x_touch_in_port.iter_pending():
        
                print_debug(message)
                if message.type == 'pitchwheel':
                    scaled_pitch = scale_pitchwheel_value(message.pitch)
                    print_debug(scaled_pitch)
                    data = VENDOR_EXPERT_SLEEPERS + DEVICE_ES9 + MESSAGE_TYPE_SET_VIRTUAL_MIX + [0x00] + [scaled_pitch]  # eller annen tilpasset data
                    es9_out_port.send(mido.Message('sysex', data=data))
                    # Update motorized faders
                    x_touch_out_port.send(mido.Message('pitchwheel', channel=0, pitch=message.pitch))

            es9_out_port.send(mido.Message('sysex', data=VENDOR_EXPERT_SLEEPERS + DEVICE_ES9 + MESSAGE_TYPE_REQUEST_MIX))
            for message in es9_in_port.iter_pending():
                print_sysex_data(message.data[5:])        

            time.sleep(SLEEP_TIME)

    except KeyboardInterrupt:
        pass
    finally:
        es9_in_port.close()
        es9_out_port.close()
        x_touch_in_port.close()
        x_touch_out_port.close()


def print_debug(msg):
    if DEBUG:
        print(msg)

def print_sysex_data(sysex_data):
    # Anta at sysex_data er en liste av bytes, ekskluderer F0 og F7
    # De første 128*3 bytes er mix-innstillinger
    mix_settings = sysex_data[:128*3]
    virtual_mix_pan_settings = sysex_data[128*3:]

    print("Mix Innstillinger:")
    for channel in range(128):
        mix_value = mix_settings[channel*3:(channel+1)*3]
        #print(f"Kanal {channel + 1}: {mix_value}")

    print("\nVirtuelle Mix/Pan Innstillinger:")
    for channel in range(128):
        pan_value = virtual_mix_pan_settings[channel]
        print(f"Kanal {channel + 1}: {pan_value}", end=' ')



def scale_pitchwheel_value(pitch):
    # Definer området for pitchwheel
    min_pitch = -8192
    max_pitch = 8188 # Really 8191, but the X-Touch Ext sends max 8188

    # Definer målområdet (0-127)
    min_target = 0
    max_target = 127

    # Beregn skalafaktoren
    scale_factor = (max_target - min_target) / (max_pitch - min_pitch)

    # Skaler og konverter verdien
    scaled_value = int((pitch - min_pitch) * scale_factor + min_target)

    # Sikre at verdien er innenfor målområdet
    return max(min_target, min(max_target, scaled_value))



if __name__ == '__main__':
    main()        
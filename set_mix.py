import mido
import time

data = [0x00, 0x21, 0x27, 0x19, 0x34, 0x00, 0x01]
output_port_name = 'ES-9 MIDI Out'
input_port_name = 'nanoKONTROL2 SLIDER/KNOB'

# Åpner output-porten
outport = mido.open_output(output_port_name)

# Åpner input-porten
inport = mido.open_input(input_port_name)

try:
    while True:
        for msg in inport.iter_pending():
            print(msg)
            data[5] = msg.control
            data[6] = msg.value
            outport.send(mido.Message('sysex', data=data))
        time.sleep(0.1)
except KeyboardInterrupt:
    # Brukeren avslutter programmet (f.eks. ved å trykke Ctrl+C)
    pass
finally:
    # Lukker portene når programmet avsluttes
    inport.close()
    outport.close()

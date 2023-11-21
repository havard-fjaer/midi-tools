import mido

print("***********")
print("Inputs: ")
available_inputs = mido.get_input_names()
for input in available_inputs:
    print(input)

print("***********")
print("Outputs: ")
available_outputs = mido.get_output_names()
for output in available_outputs:
    print(output)



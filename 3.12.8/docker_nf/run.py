import subprocess
import json
import sys
import fileinput
# Read input from stdin

in_file = open('input.fasta', 'w')

lines_of_data = fileinput.input()
in_file.write(''.join(lines_of_data))
print(''.join(lines_of_data))
in_file.close()
# Run amrfinder command
amrfinder_output = subprocess.check_output(['amrfinder', '--plus', '-n', 'input.fasta'])

# Process amrfinder output
output_dict = {}
lines = amrfinder_output.decode().split('\n')
for line in lines:
    if line:
        fields = line.split('\t')
        output_dict[fields[0]] = fields[1]

# Convert output dictionary to JSON
output_json = json.dumps(output_dict)

# Print JSON output
print(output_json)

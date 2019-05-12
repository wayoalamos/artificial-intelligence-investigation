from shutil import copyfile
import random
import sys

def shuffle(input_file, output_file):
    # Copy model
    copyfile(input_file, output_file)

    # Read model
    print("Copying model...")
    nn_lookahead   = 0
    n_input_layers = 0
    input_info     = []

    with open(output_file) as f:
        lines = f.readlines()

        nn_lookahead   = int(lines[0].rstrip().split(' ')[0])
        n_input_layers = int(lines[0].rstrip().split(' ')[1])

        for i in range(n_input_layers):
            info = {};
            s = lines[i + 1].rstrip().split(' ');
            info['name'] = s[1]
            info['m']    = int(s[2])
            info['f_m']  = int(s[3])
            info['f_n']  = int(s[4])
            input_info.append(info)

            print(info)

    # Shuffle output file
    print("Saving shuffled output...")
    number_of_line = 0
    order = []
    with open(input_file + '_out.txt') as f_in:
        lines = f_in.readlines()
        
        number_of_line = len(lines)
        order = list(range(number_of_line))
        random.shuffle(order)
        
        with open(output_file + '_out.txt', 'w') as f_out:
        	for i in range(number_of_line):
        		f_out.write(lines[order[i]])


    # Shuffle input files
    print("Saving shuffled input...")

    for k in range(n_input_layers):
    	with open(input_file + '_in_' + input_info[k]['name'] + '.txt') as f_in:
    		print(" Input: " + input_info[k]['name'])
    		
    		lines = f_in.readlines()
    		
    		with open(output_file + '_in_' + input_info[k]['name'] + '.txt', 'w') as f_out:
    			for i in range(number_of_line):
    				f_out.write(lines[order[i]])

    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Not enough parameters')
        sys.exit()
    # Read input and output file paths
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    shuffle(input_file, output_file)    

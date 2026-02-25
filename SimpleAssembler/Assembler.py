import sys
import os

def extract_filepaths():
    """ 
    Extracts file paths from command line arguments.
    Expected usage:
    python3 Assembler.py <input_file> <output_file> [readable_output_file]

    """
    if len(sys.argv)<3:
        print("Error: Invalid number of Arguments")
        print("Usage: python3 Assembler.py <input_file> <output_file> [readable_output_file]")
        sys.exit(1)
    
    input_path=sys.argv[1]
    output_path=sys.argv[2]
    readable_outputpath=sys.argv[3]

    return input_path,output_path,readable_outputpath

def view_assemblycode(input_path):

    if not os.path.exists(input_path):
        print(f"Error: Input file not found:{input_path}")
        sys.exit(1)

    try:
        with open(input_path,"r") as file:
            instructions=[line.rstrip("\n") for line in file]
        return instructions
    except Exception as exc:
        print(f"Error while reading input file: {exc}")
        sys.exit(1)

def write_output(output_path, binary):
    try:
        with open(output_path,"w") as file:
            for line in binary:
                file.write(line +"\n")
    except Exception as exc:
        print(f"Error while writing output file:{exc}")
        sys.exit(1)

def write_readableoutput(readable_outputpath, binary):
    try:
        with open(readable_outputpath,"w") as file:
            for line in binary:
                file.write(line +"\n")
    except Exception as exc:
        print(f"Error while writing readable output file:{exc}")
        sys.exit(1)

def main():
    input_path, output_path, readable_path=extract_filepaths()
    assembly_lines=view_assemblycode

#assembler logic , we will generate binary output here and readable binary output

# binary_lines=[] , generated after logic implementation
#readable=[], readable binary output 

write_output(output_path,binary_lines)
write_readableoutput(readable_outputpath,readable)


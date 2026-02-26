import sys
import os
import re

OPCODES={"ADD" : 3, "SUB" : 3, "AND" : 3, "OR" : 3, "ADDI" : 3, "LW" : 2, "SW" : 2, "BEQ" : 3, "BNE" : 3, "J" : 1}

def extract_filepaths() :
    """ 
    Extracts file paths from command line arguments.
    Expected usage:
    python3 Assembler.py <input_file> <output_file> [readable_output_file]

    """
    if len(sys.argv)<3 :
        print("Error: Invalid number of Arguments")
        print("Usage: python3 Assembler.py <input_file> <output_file> [readable_output_file]")
        sys.exit(1)
    
    input_path=sys.argv[1]
    output_path=sys.argv[2]
    readable_outputpath=None 
    if len(sys.argv) >= 4 :
        readable_outputpath=sys.argv[3]

    return input_path,output_path,readable_outputpath

def reg_checker(reg) :
    if not reg.startswith("x") :
        return False

    n = reg[1:]

    return n.isdigit() and 0 <= int(n) <= 31

def valid_instruction(line , n) :
    line = line.split("#")[0].strip()
    
    if line == "" :
        return False
    
    part = line.replace(",", " ").split()
    
    opcode = part[0].upper()
    
    if opcode not in OPCODES :
        print(f"Syntax Error (Line {n}): Invalid opcode '{opcode}'")
        sys.exit(1)
        
    operands = part[1:]
    
    if len(operands) != OPCODES[opcode] :
        print(f"Syntax Error (Line {n}): Expected {OPCODES[opcode]} operands for '{opcode}', got {len(operands)}")
        sys.exit(1)
    
    for i in operands :
        if i.startswith("x") :
            if not reg_checker(i) :
                print(f"Syntax Error (Line {n}): Invalid register '{i}'")
                sys.exit(1)
    
    return line
    
def view_assemblycode(input_path) :

    if not os.path.exists(input_path) :
        print(f"Error: Input file not found:{input_path}")
        sys.exit(1)

    instructions=[]
    
    try :
        with open(input_path,"r") as file :
            
            m = 1 
            for line in file :
                good = valid_instruction(line, m)
                if good :
                    instructions.append(good)
                m+=1
                
        return instructions
    
    except Exception as exc :
        print(f"Error while reading input file: {exc}")
        sys.exit(1)

def write_output(output_path, binary) :
    try :
        with open(output_path,"w") as file :
            for line in binary :
                file.write(line +"\n")
    except Exception as exc :
        print(f"Error while writing output file:{exc}")
        sys.exit(1)

def write_readableoutput(readable_outputpath, binary) :
    try :
        with open(readable_outputpath,"w") as file :
            for line in binary :
                file.write(line +"\n")
    except Exception as exc :
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


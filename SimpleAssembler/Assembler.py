import sys
import os
import re

opcodes={


# R-TYPE

"add":  {"format": "R", "opcode": "0110011", "funct3": "000", "funct7": "0000000", "operands": 3},
"sub":  {"format": "R", "opcode": "0110011", "funct3": "000", "funct7": "0100000", "operands": 3},
"sll":  {"format": "R", "opcode": "0110011", "funct3": "001", "funct7": "0000000", "operands": 3},
"slt":  {"format": "R", "opcode": "0110011", "funct3": "010", "funct7": "0000000", "operands": 3},
"sltu": {"format": "R", "opcode": "0110011", "funct3": "011", "funct7": "0000000", "operands": 3},
"xor":  {"format": "R", "opcode": "0110011", "funct3": "100", "funct7": "0000000", "operands": 3},
"srl":  {"format": "R", "opcode": "0110011", "funct3": "101", "funct7": "0000000", "operands": 3},
"sra":  {"format": "R", "opcode": "0110011", "funct3": "101", "funct7": "0100000", "operands": 3},
"or":   {"format": "R", "opcode": "0110011", "funct3": "110", "funct7": "0000000", "operands": 3},
"and":  {"format": "R", "opcode": "0110011", "funct3": "111", "funct7": "0000000", "operands": 3},

# I-TYPE 

"addi":  {"format": "I", "opcode": "0010011", "funct3": "000", "operands": 3},
"slti":  {"format": "I", "opcode": "0010011", "funct3": "010", "operands": 3},
"sltiu": {"format": "I", "opcode": "0010011", "funct3": "011", "operands": 3},
"xori":  {"format": "I", "opcode": "0010011", "funct3": "100", "operands": 3},
"ori":   {"format": "I", "opcode": "0010011", "funct3": "110", "operands": 3},
"andi":  {"format": "I", "opcode": "0010011", "funct3": "111", "operands": 3},

"slli": {"format": "I", "opcode": "0010011", "funct3": "001", "funct7": "0000000", "operands": 3},
"srli": {"format": "I", "opcode": "0010011", "funct3": "101", "funct7": "0000000", "operands": 3},
"srai": {"format": "I", "opcode": "0010011", "funct3": "101", "funct7": "0100000", "operands": 3},


# LOADS

"lb":  {"format": "I", "opcode": "0000011", "funct3": "000", "operands": 2},
"lh":  {"format": "I", "opcode": "0000011", "funct3": "001", "operands": 2},
"lw":  {"format": "I", "opcode": "0000011", "funct3": "010", "operands": 2},
"lbu": {"format": "I", "opcode": "0000011", "funct3": "100", "operands": 2},
"lhu": {"format": "I", "opcode": "0000011", "funct3": "101", "operands": 2},

#storing 
"sb": {"format": "S", "opcode": "0100011", "funct3": "000", "operands": 2},
"sh": {"format": "S", "opcode": "0100011", "funct3": "001", "operands": 2},
"sw": {"format": "S", "opcode": "0100011", "funct3": "010", "operands": 2},

#branching 
"beq":  {"format": "B", "opcode": "1100011", "funct3": "000", "operands": 3},
"bne":  {"format": "B", "opcode": "1100011", "funct3": "001", "operands": 3},
"blt":  {"format": "B", "opcode": "1100011", "funct3": "100", "operands": 3},
"bge":  {"format": "B", "opcode": "1100011", "funct3": "101", "operands": 3},
"bltu": {"format": "B", "opcode": "1100011", "funct3": "110", "operands": 3},
"bgeu": {"format": "B", "opcode": "1100011", "funct3": "111", "operands": 3},


# jump

"jal":  {"format": "J", "opcode": "1101111", "operands": 2},
"jalr": {"format": "I", "opcode": "1100111", "funct3": "000", "operands": 2},

# u type 
"lui":   {"format": "U", "opcode": "0110111", "operands": 2},
"auipc": {"format": "U", "opcode": "0010111", "operands": 2},
}

def extract_filepaths() :
    """ 
    Extracts file paths from command instructionline arguments.
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

def reg_checker(register) :
    if not register.startswith("x") :
        return False

    n=register[1:]

    return n.isdigit() and 0<=int(n)<= 31

def build_label_table(instructions):
    label_table = {}
    program_counter = 0
    cleaned = []

    for line in instructions:
        if ":" in line:
            label = line.replace(":", "").strip()
            label_table[label] = program_counter

        else:
            cleaned.append(line)
            program_counter += 4

    return label_table, cleaned

def compute_offset(label, current_pc, label_table):
    if label not in label_table:
        print(f"Error: Undefined label '{label}'")
        sys.exit(1)

    return label_table[label] - current_pc

def translate_register():
    return None

def valid_instruction(instructionline , n) :
    instructionline=instructionline.split("#")[0].strip()
    
    if instructionline=="" :
        return False
    
    part = instructionline.replace(",", " ").split()
    
    opcode=part[0]
    
    if opcode not in opcodes:
        print(f"Syntax Error (Line {n}): Invalid opcode '{opcode}'")
        sys.exit(1)
        
    operands=part[1:]
    
    if len(operands) != opcodes[opcode]["operands"] :
        print(f"Syntax Error (Line {n}): Expected {opcodes[opcode]} operands for '{opcode}', got {len(operands)}")
        sys.exit(1)
    
    for i in operands :
        if i.startswith("x") :
            if not reg_checker(i) :
                print(f"Syntax Error (Line {n}): Invalid register '{i}'")
                sys.exit(1)
    
    return instructionline
    
def view_assemblycode(input_path) :

    if not os.path.exists(input_path) :
        print(f"Error: Input file not found:{input_path}")
        sys.exit(1)

    instructions=[]
    
    try :
        with open(input_path,"r") as file :
            
            m = 1 
            for instructionline in file :
                good = valid_instruction(instructionline, m)
                if good :
                    instructions.append(good)
                m+=1
                
        return instructions
    
    except Exception as exc :
        print(f"Error while reading input file: {exc}")
        sys.exit(1)

def translate_assemblycode(instructions,binary_lines):
    for instruction in instructions :
                instruction=instruction.replace(","," ")
                operands=instruction.split()

                if(operands[0] in opcodes and opcodes[operands[0]]["format"]=="S") :  #sw r2,imm(r1)
                    register2=translate_register(operands[1])        #r2
                    offset,base=operands[2].split("(")               #offset=imm, base=r1)
                    offset=int(offset)
                    register1=translate_register(base.replace(")",""))  #r1

                    imm = format(offset & 0xFFF,"012b")
                    
                    imm11_5=imm[0:7]
                    imm4_0=imm[7:12]

                    binarystring= (
                        imm11_5 + register2 + register1 + opcodes[operands[0]]["funct3"] + imm4_0 + opcodes[operands[0]]["opcode"]
                    )

                    binary_lines.append(binarystring)
                    
                if(operands[0] in opcodes and opcodes[operands[0]]["format"]=="B") :
                    register1=translate_register(operands[1])
                    register2=translate_register(operands[2])

                    label=operands[3]

                    offset=compute_offset(label,pc,label_table)

                    imm = format((offset >> 1) & 0x1FFF, "013b")

                    imm12 = imm[0]
                    imm10_5 = imm[1:7]
                    imm4_1 = imm[7:11]
                    imm11 = imm[11]

                    binarystring = (
                            imm12 +imm10_5 +rs2 +rs1 +opcodes[operands[0]]["funct3"] +imm4_1 +imm11 +opcodes[operands[0]]["opcode"]
                    )

                    binary_lines.append(binarystring)

                if(operands[0] in opcodes and opcodes[operands[0]]["format"]=="J") :
                    rd = translate_register(operands[1])
                    label = operands[2]

                    offset = compute_offset(label, pc, label_table)

                    imm = format((offset >> 1) & 0x1FFFFF, "021b")

                    imm20 = imm[0]
                    imm10_1 = imm[10:20]
                    imm11 = imm[9]
                    imm19_12 = imm[1:9]

                    binarystring = (
                            imm20 +imm10_1 +imm11+imm19_12 +rd +opcodes["jal"]["opcode"]
                    )
                    
                    binary_lines.append(binarystring)









def write_output(output_path, binary) :
    try :
        with open(output_path,"w") as file :
            for instructionline in binary :
                file.write(instructionline +"\n")
    except Exception as exc :
        print(f"Error while writing output file:{exc}")
        sys.exit(1)

def write_readableoutput(readable_outputpath, binary) :
    try :
        with open(readable_outputpath,"w") as file :
            for instructionline in binary :
                file.write(instructionline +"\n")
    except Exception as exc :
        print(f"Error while writing readable output file:{exc}")
        sys.exit(1)

def main():
    input_path, output_path, readable_path=extract_filepaths()
    assembly_lines=view_assemblycode(input_path)

#assembler logic , we will generate binary output here and readable binary output

    binary_lines=[] #, generated after logic implementation
    readable=[], #readable binary output
    
    translate_assemblycode(assembly_lines,binary_lines)
    
    
    write_output(output_path,binary_lines)
    write_readableoutput(readable_outputpath,readable)




import sys
import os
import re


abi = {
    "zero":0, "ra":1, "sp":2, "gp":3, "tp":4,
    "t0":5, "t1":6, "t2":7,
    "s0":8, "fp":8, "s1":9,
    "a0":10,"a1":11,"a2":12,"a3":13,"a4":14,"a5":15,"a6":16,"a7":17,
    "s2":18,"s3":19,"s4":20,"s5":21,"s6":22,"s7":23,"s8":24,"s9":25,"s10":26,"s11":27,
    "t3":28,"t4":29,"t5":30,"t6":31
}

def reg_to_bin(reg):
    return format(abi[reg], "05b")

Opcodes={


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

def valid_instruction(instructionline , n) :
    instructionline=instructionline.split("#")[0].strip()
    
    if instructionline=="" :
        return False
    
    part = instructionline.replace(",", " ").split()
    
    opcode=part[0]
    
    if opcode not in Opcodes:
        print(f"Syntax Error (Line {n}): Invalid opcode '{opcode}'")
        sys.exit(1)
        
    operands=part[1:]
    
    if len(operands) != Opcodes[opcode]["operands"] :
        print(f"Syntax Error (Line {n}): Expected {Opcodes[opcode]['operands']} operands for '{opcode}', got {len(operands)}")
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
        
def bin_to_hex(bin_str):
    decimal = int(bin_str, 2)
    return format(decimal, '08x')

def assemble_to_binary(assembly_lines, opcodes):
    binary_lines = []
    for line in assembly_lines:
        parts = line.replace(",", " ").split()
        opcode = parts[0]
        operands = parts[1:]
        
        instruction_format = opcodes[opcode]["format"]
        
        if instruction_format == "R":
            rd = reg_to_bin(operands[0])
            rs1 = reg_to_bin(operands[1])
            rs2 = reg_to_bin(operands[2])
            funct7 = opcodes[opcode]["funct7"]
            funct3 = opcodes[opcode]["funct3"]
            op = opcodes[opcode]["opcode"]
            binary = funct7 + rs2 + rs1 + funct3 + rd + op
            
        elif instruction_format == "I":
            rd = reg_to_bin(operands[0])
            rs1 = reg_to_bin(operands[1])
            imm = int(operands[2])
            imm_binary = format(imm & 0xFFF, "012b")
            funct3 = opcodes[opcode]["funct3"]
            op = opcodes[opcode]["opcode"]
            binary = imm_binary + rs1 + funct3 + rd + op
            
        elif instruction_format == "S":
            rs2 = reg_to_bin(operands[0])
            offset_part = operands[1].split("(")
            imm = int(offset_part[0])
            rs1 = reg_to_bin(offset_part[1].rstrip(")"))
            imm_binary = format(imm & 0xFFF, "012b")
            funct3 = opcodes[opcode]["funct3"]
            op = opcodes[opcode]["opcode"]
            imm_upper = imm_binary[:7]
            imm_lower = imm_binary[7:]
            binary = imm_upper + rs2 + rs1 + funct3 + imm_lower + op
            
        elif instruction_format == "B":
            rs1 = reg_to_bin(operands[0])
            rs2 = reg_to_bin(operands[1])
            imm = int(operands[2])
            imm_binary = format(imm & 0x1FFF, "013b")
            funct3 = opcodes[opcode]["funct3"]
            op = opcodes[opcode]["opcode"]
            binary = imm_binary[0] + imm_binary[1:7] + rs2 + rs1 + funct3 + imm_binary[7:12] + imm_binary[12] + op
            
        elif instruction_format == "U":
            rd = reg_to_bin(operands[0])
            imm = int(operands[1])
            imm_binary = format(imm & 0xFFFFF, "020b")
            op = opcodes[opcode]["opcode"]
            binary = imm_binary + rd + op
            
        elif instruction_format == "J":
            rd = reg_to_bin(operands[0])
            imm = int(operands[1])
            imm_binary = format(imm & 0x1FFFFF, "021b")
            op = opcodes[opcode]["opcode"]
            binary = imm_binary[0] + imm_binary[1:11] + imm_binary[11] + imm_binary[12:20] + rd + op
        
        hex_value = bin_to_hex(binary)
        binary_lines.append(hex_value)
    
    return binary_lines

def main():
    input_path, output_path, readable_path = extract_filepaths()
    
    assembly_lines = view_assemblycode(input_path)

    binary_lines = assemble_to_binary(assembly_lines, Opcodes)

    readable = binary_lines  

    write_output(output_path, binary_lines)

    if readable_path:
        write_readableoutput(readable_path, readable)


if __name__ == "__main__":
    main()

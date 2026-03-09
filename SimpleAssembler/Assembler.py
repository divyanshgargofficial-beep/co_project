import sys
import os
import re

regref={
    "zero":0, "ra":1, "sp":2, "gp":3, "tp":4,
    "t0":5, "t1":6, "t2":7,
    "s0":8, "fp":8, "s1":9,
    "a0":10,"a1":11,"a2":12,"a3":13,"a4":14,"a5":15,"a6":16,"a7":17,
    "s2":18,"s3":19,"s4":20,"s5":21,"s6":22,"s7":23,"s8":24,"s9":25,"s10":26,"s11":27,
    "t3":28,"t4":29,"t5":30,"t6":31
}

def addregs():
    for i in range(32):
        regref[f"x{i}"] = i

def regtobin(register):
    if register not in regref:
        print(f"Error found : Invalid register '{register}'")
        sys.exit(1)

    return format(regref[register], "05b")

Opcodes={

# R-TYPE

"add":  {"format": "R", "opcode": "0110011", "funct3": "000", "funct7": "0000000", "operands": 3},
"sub":  {"format": "R", "opcode": "0110011", "funct3": "000", "funct7": "0100000", "operands": 3},
"slt":  {"format": "R", "opcode": "0110011", "funct3": "010", "funct7": "0000000", "operands": 3},
"sltu": {"format": "R", "opcode": "0110011", "funct3": "011", "funct7": "0000000", "operands": 3},
"xor":  {"format": "R", "opcode": "0110011", "funct3": "100", "funct7": "0000000", "operands": 3},
"sll":  {"format": "R", "opcode": "0110011", "funct3": "001", "funct7": "0000000", "operands": 3},
"srl":  {"format": "R", "opcode": "0110011", "funct3": "101", "funct7": "0000000", "operands": 3},
"or":   {"format": "R", "opcode": "0110011", "funct3": "110", "funct7": "0000000", "operands": 3},
"and":  {"format": "R", "opcode": "0110011", "funct3": "111", "funct7": "0000000", "operands": 3},

# I-TYPE 

"addi":  {"format": "I", "opcode": "0010011", "funct3": "000", "operands": 3},
"sltiu": {"format": "I", "opcode": "0010011", "funct3": "011", "operands": 3},

# I-TYPE: LOAD and JUMP INSTRUCTIONS

"lw":  {"format": "I", "opcode": "0000011", "funct3": "010", "operands": 2},
"jalr": {"format": "I", "opcode": "1100111", "funct3": "000", "operands": 3},

# S-TYPE

"sw": {"format": "S", "opcode": "0100011", "funct3": "010", "operands": 2},

# B-TYPE

"beq":  {"format": "B", "opcode": "1100011", "funct3": "000", "operands": 3},
"bne":  {"format": "B", "opcode": "1100011", "funct3": "001", "operands": 3},
"blt":  {"format": "B", "opcode": "1100011", "funct3": "100", "operands": 3},
"bge":  {"format": "B", "opcode": "1100011", "funct3": "101", "operands": 3},
"bltu": {"format": "B", "opcode": "1100011", "funct3": "110", "operands": 3},
"bgeu": {"format": "B", "opcode": "1100011", "funct3": "111", "operands": 3},

#J-TYPE

"jal":  {"format": "J", "opcode": "1101111", "operands": 2},

#U-TYPE

"lui":   {"format": "U", "opcode": "0110111", "operands": 2},
"auipc": {"format": "U", "opcode": "0010111", "operands": 2},
}


def extract_filepaths() :

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

def reg_checker(operands, n):
    for op in operands:
        if op not in regref and not op.lstrip('-').isdigit():
            print("Syntax Error (Line", n, "): Invalid register", op)
            sys.exit(1)

def label_table(instructions):
    labels={}
    pc=0
    new_ins=[]

    for line in instructions:
        if ":" in line:
            label, xtra =line.split(":", 1)
            label=label.strip()
            if label in labels:
                print(f"Error: Duplicate label '{label}'")
                sys.exit(1)

            labels[label]=pc

            if xtra.strip():
                new_ins.append(xtra.strip())
                pc += 4
        else:
            new_ins.append(line)
            pc+=4

    return labels,new_ins

def finding_offset(label, current_pc, label_table):
    if label not in label_table:
        print(f"Error: Undefined label '{label}'")
        sys.exit(1)

    return label_table[label] - current_pc


def valid_instruction(instructionline, n):

    instructionline=instructionline.split("#")[0].strip()
    if instructionline == "":
        return False

    temp=instructionline

    
    if ":" in instructionline:
        label,rest=instructionline.split(":", 1)

        if label.strip() == "":
            print(f"Syntax Error (Line {n}): Invalid label")
            sys.exit(1)

        temp=rest.strip()
        if temp == "":
            return instructionline

    parts = temp.replace(",", " ").split()
    opcode = parts[0]

    if opcode not in Opcodes:
        print(f"Syntax Error (Line {n}): Invalid opcode '{opcode}'")
        sys.exit(1)

    operands = parts[1:]

    if len(operands) != Opcodes[opcode]["operands"]:
        print(f"Syntax Error (Line {n}): Expected {Opcodes[opcode]['operands']} operands for '{opcode}', got {len(operands)}")
        sys.exit(1)

    return instructionline
    
def viewer(input_path) :

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

def translator(instructions, binary_lines, label_table):
    pc = 0
    for instruction in instructions :
                instruction=instruction.replace(","," ").strip()
                operands=instruction.split()
                
                info = Opcodes[operands[0]]
                format_type = info["format"]

                #R                    
                if format_type == "R":

                    final_reg=regtobin(operands[1])
                    rs1=regtobin(operands[2])
                    rs2=regtobin(operands[3])

                    instruction_info=Opcodes[operands[0]]

                    binarystring=(
                        instruction_info["funct7"] +rs2 +rs1 +instruction_info["funct3"] +final_reg +instruction_info["opcode"])

                    binary_lines.append(binarystring)
                
                #I 
                elif format_type == "I":
                    final_reg = regtobin(operands[1])

                    if operands[0] == "lw":
                        offset, base = operands[2].split("(")
                        reg1 = regtobin(base.replace(")", ""))
                        offset = int(offset,0)

                    elif operands[0] == "jalr":
                        reg1 = regtobin(operands[2])
                        offset = int(operands[3],0)
                        
                    else:
                        reg1 = regtobin(operands[2])
                        offset = int(operands[3],0)

                    if (offset<-2048 or offset > 2047):
                        print("Error: Immediate out of range")
                        sys.exit(1)

                    immediate = format(offset & 0xFFF,"012b")

                    binarystring=(
                        immediate +reg1 +Opcodes[operands[0]]["funct3"] +final_reg +Opcodes[operands[0]]["opcode"]
                        )

                    binary_lines.append(binarystring)

                #S 
                elif(format_type == "S") :  
                    reg2=regtobin(operands[1])        
                    offset,base=operands[2].split("(")              
                    offset=int(offset,0)

                    if (offset<-2048) or (offset>2047):      
                        print("Error: Immediate out of range")
                        sys.exit(1)
                              
                    reg1=regtobin(base.replace(")",""))  

                    immediate = format(offset & 0xFFF,"012b")
                    
                    imm11_5=immediate[0:7]
                    imm4_0=immediate[7:12]

                    binarystring= (
                        imm11_5 + reg2 + reg1 + Opcodes[operands[0]]["funct3"] + imm4_0 + Opcodes[operands[0]]["opcode"])

                    binary_lines.append(binarystring)
                                        
                #B
                elif format_type == "B":

                    rs1=regtobin(operands[1])
                    rs2=regtobin(operands[2])
                    target=operands[3]

                    try:
                        offset=int(target,0)
                    except ValueError:
                        offset=finding_offset(target, pc, label_table)

                    if offset%2!=0:
                        print("Error: Branch offset must be aligned")
                        sys.exit(1)
                    if (offset<-4096 or offset>4094):
                        print("Error! Branch offset out of range")
                        sys.exit(1)

                    if offset<0:
                        offset=(1<<13)+offset

                    imm12=(offset>>12) & 1
                    imm10_5=(offset >> 5) & 0x3F
                    imm4_1=(offset >> 1) & 0xF
                    imm11=(offset >> 11) & 1

                    binarystring = (
                        format(imm12,"1b") +format(imm10_5,"06b") +rs2 +rs1 +Opcodes[operands[0]]["funct3"] +format(imm4_1,"04b") +format(imm11,"1b") +Opcodes[operands[0]]["opcode"]
                    )

                    binary_lines.append(binarystring)

                #U    
                elif (format_type == "U"):

                    final_reg = regtobin(operands[1])
                    try:
                        imm_value=int(operands[2])
                    except:
                        print(f"Error: Invalid immediate '{operands[2]}'")
                        sys.exit(1)

                    
                    if imm_value<-524288 or imm_value>524287:
                        print(f"Error: Immediate out of 20-bit range")
                        sys.exit(1)

                    # Convert to 20bituint
                    if imm_value < 0:
                        imm_value = (1 << 20) + imm_value

                    immediate = format(imm_value, "020b")

                    binarystring = (immediate +final_reg +Opcodes[operands[0]]["opcode"])
                    
                    binary_lines.append(binarystring)
                
                #J
                elif format_type == "J":

                    final_reg=regtobin(operands[1])
                    label=operands[2]

                    offset=finding_offset(label,pc,label_table)

                    if offset%2 !=0:
                        print("Error: Offset must be aligned")
                        sys.exit(1)
                    if (offset<-1048576 or offset>1048574):
                        print("Error: Offset is out of range")
                        sys.exit(1)
                        
                    if offset < 0:
                        offset = (1 << 21) + offset

                    imm20=(offset >> 20) & 1
                    imm10_1 = (offset >> 1)  & 0x3FF
                    imm11   = (offset >> 11) & 1
                    imm19_12= (offset >> 12) & 0xFF

                    binarystring = (format(imm20,"1b") +format(imm10_1,"010b") +format(imm11,"1b") +
                        format(imm19_12,"08b") +
                        final_reg +
                        Opcodes["jal"]["opcode"]
                    )

                    binary_lines.append(binarystring)
                    
                pc+=4

def outputer(path , binary) :
    try :
        with open(path,"w") as file :
            for instruction in binary :
                file.write(instruction +"\n")
    except Exception as exc :
        print(f"Error while writing output file:{exc}")
        sys.exit(1)

def main():
    
    addregs()
    
    input, output= extract_filepaths()

    assembly_lines = viewer(input)

    table , cleaned_instructions = label_table(assembly_lines)

    if len(cleaned_instructions) > 64:
        print("Error: Program memory overflow (max 64 instructions)")
        sys.exit(1)

    if len(cleaned_instructions) == 0:
        print("Error: Empty program")
        sys.exit(1)

    halt_found = False

    for inst in cleaned_instructions:
        parts = inst.replace(",", " ").split()

        if(len(parts)== 4 and parts[0] == "beq" and parts[1] in ["zero", "x0"] and parts[2] in ["zero", "x0"] and parts[3] == "0"):
            halt_found=True
            break

    if not halt_found:
        print("Error: Missing Virtual Halt instruction")
        sys.exit(1)

    binary_lines = []

    translator(cleaned_instructions, binary_lines, table)

    outputer(output, binary_lines)

if __name__ == "__main__":
    main()
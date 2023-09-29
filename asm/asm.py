import sys
import re

class AsmSyntaxParseError (RuntimeError):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Token:
    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value


class Label (Token):
    __labels = {}

    def __init__(self, name):
        self.name = str(name)

    @staticmethod
    def registerLabel(name, value):
        Label.__labels[name] = value

    def getValue(self):
        try:
            return Label.__labels[self.name]
        except KeyError:
            raise AsmSyntaxParseError('Undefined label "' + self.name + '"')

def packArguments(operation, lhs=0, rhs=0, im=None):
    bytes = []

    if lhs== 'CONTROL':
        t= Token(((int(operation) << 4) | (int(rhs) & 0b1111)) & 0xff)
    else:
        t= Token(((int(operation) << 4) | ((int(lhs) & 0b11) << 2) | ((int(rhs) & 0b11) << 0)) & 0xff)

    bytes.append(t)

   
    if im:
        if re.match(r'0x[0-9a-f]{2}', im, flags=re.I):
            bytes.append(Token(int(im, 0) & 0xff))
        else:
            bytes.append(Label(im))

    return bytes


def assemble(asm):
    asm = re.sub(r'[ ]*([;#].*)?$', '', asm, flags=re.M) # remove comments
    asm = re.sub(r':', ':\n', asm, flags=re.M) # move labels to new lines
    asm = re.sub(r'^\s+', '', asm, flags=re.M) # remove blank lines ans useless spaces

    lines = asm.split('\n')

    registers = {
        'A' : '0',
        'B' : '1',
        'C' : '2',
        'D' : '3'
    }
    
    tokens = []

    operations = [
        (r'MOV\s*([A-D])L\s*,\s*([A-D])L', lambda r: packArguments(0x0, registers[r[0]], registers[r[1]], im='0x00')), # rr
        
        (r'MOV\s*([A-D])L\s*,\s*\[\s*([^BL]+)\s*\]', lambda r: packArguments(0x4, registers[r[0]], '0', im=r[1])), # dir
        (r'MOV\s*([A-D])L\s*,\s*\[\s*BL\s*\]', lambda r: packArguments(0x4, registers[r[0]], '1', im='0x00')), # ind
        (r'MOV\s*([A-D])L\s*,\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0x4, registers[r[0]], '2', im=r[1])), # inm
        
        (r'MOV\s*\[\s*([^BL]+)\s*\],\s*([A-D])L\s*', lambda r: packArguments(0x8, registers[r[1]], '0', im=r[0])), # dir
        (r'MOV\s*(\[\s*BL\s*\])\s*,\s*([A-D])L\s*', lambda r: packArguments(0x8, registers[r[1]], '1', im='0x00')), # ind

        (r'ADD\s*([A-D])L\s*,\s*([A-D])L', lambda r: packArguments(0x1, registers[r[0]], registers[r[1]], im='0x00')), # rr
        
        (r'ADD\s*([A-D])L\s*,\s*\[\s*([^BL]+)\s*\]', lambda r: packArguments(0x5, registers[r[0]], '0', im=r[1])), # dir
        (r'ADD\s*([A-D])L\s*,\s*\[\s*BL\s*\]', lambda r: packArguments(0x5, registers[r[0]], '1', im='0x00')), # ind
        (r'ADD\s*([A-D])L\s*,\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0x5, registers[r[0]], '2', im=r[1])), # inm
        
        (r'ADD\s*\[\s*([^BL]+)\s*\],\s*([A-D])L\s*', lambda r: packArguments(0x9, registers[r[1]], '0', im=r[0])), # dir
        (r'ADD\s*(\[\s*BL\s*\])\s*,\s*([A-D])L\s*', lambda r: packArguments(0x9, registers[r[1]], '1', im='0x00')), # ind
        
        (r'SUB\s*([A-D])L\s*,\s*([A-D])L', lambda r: packArguments(0x2, registers[r[0]], registers[r[1]], im='0x00')), # rr
        
        (r'SUB\s*([A-D])L\s*,\s*\[\s*([^BL]+)\s*\]', lambda r: packArguments(0x6,  registers[r[0]], '0', im=r[1])), # dir
        (r'SUB\s*([A-D])L\s*,\s*\[\s*BL\s*\]', lambda r: packArguments(0x6,  registers[r[0]], '1', im='0x00')), # ind
        (r'SUB\s*([A-D])L\s*,\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0x6,  registers[r[0]], '2', im=r[1])), # inm
        
        (r'SUB\s*\[\s*([^BL]+)\s*\],\s*([A-D])L\s*', lambda r: packArguments(0xA, registers[r[1]], '0', im=r[0])), # dir
        (r'SUB\s*(\[\s*BL\s*\])\s*,\s*([A-D])L\s*', lambda r: packArguments(0xA, registers[r[1]], '1', im='0x00')), # ind
        
        (r'CMP\s*([A-D])L\s*,\s*([A-D])L', lambda r: packArguments(0x3, registers[r[0]], registers[r[1]], im='0x00')), # rr
        
        (r'CMP\s*([A-D])L\s*,\s*\[\s*([^BL]+)\s*\]', lambda r: packArguments(0x7, registers[r[0]], '0', im=r[1])), # dir
        (r'CMP\s*([A-D])L\s*,\s*\[\s*BL\s*\]', lambda r: packArguments(0x7, registers[r[0]], '1', im='0x00')), # ind
        (r'CMP\s*([A-D])L\s*,\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0x7, registers[r[0]], '2', im=r[1])), # inm
        
        (r'CMP\s*\[\s*([^BL]+)\s*\],\s*([A-D])L\s*', lambda r: packArguments(0xB, registers[r[1]], '0', im=r[0])), # dir
        (r'CMP\s*(\[\s*BL\s*\])\s*,\s*([A-D])L\s*', lambda r: packArguments(0xB, registers[r[1]], '1', im='0x00')), # ind
        
        (r'JMP\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0xC,'CONTROL', '0', im=r[0])),
        (r'JZ\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0xC, 'CONTROL', '1', im=r[0])),
        (r'JNZ\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0xC,'CONTROL', '2', im=r[0])),
        (r'JC\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0xC, 'CONTROL', '3', im=r[0])),
        (r'JNC\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0xC, 'CONTROL', '4', im=r[0])),
        (r'JS\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0xC, 'CONTROL', '5', im=r[0])),
        (r'JNS\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0xC, 'CONTROL', '6', im=r[0])),
        (r'JO\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0xC,'CONTROL', '7', im=r[0])),
        (r'JNO\s*(0x[0-9a-f]{2}|[a-z]+)', lambda r: packArguments(0xC,'CONTROL', '8', im=r[0])),
        
        (r'NOP', lambda r: packArguments(0xF,'CONTROL', '0', im='0x00')),
        (r'HLT', lambda r: packArguments(0xF,'CONTROL', '1', im='0x00'))


    ]

    for line in lines:
        found = False

        for pattern, action in operations:
            r = re.match(pattern, line, flags=re.I)
            if r:
                tokens.extend(action(r.groups()))
                found = True
                break

        if not found:
            r = re.match(r'([a-z]+):', line, flags=re.I)
            if r:
                Label.registerLabel(r.groups()[0], len(tokens))
                found = True
        
        if not found:
            r = re.match(r"\s*(DB|db)\s*0x([0-9a-f]{2}+)", line, flags=re.I)
            print(line)
            if r:
                print(r.groups()[0])
                print(r[0])
                print(r[1])
                print(r[2])
                t= Token(r[2])
                tokens.extend(t)
                print(tokens)
                #Label.registerLabel(r[2])
                found = True

        if not found:
            raise AsmSyntaxParseError('Unknown syntax "' + line + '"')

    return tokens


def main(args):
    if len(args) > 1:
        filename = str(args[1])

        
        with open(filename, 'r') as inputFile:
            tokens = assemble(inputFile.read())

            asm = " ".join(map(lambda t: format(t.getValue(), '02x'), tokens))
            print('Result [' + str(len(tokens)) + ' bytes]:')
            print(asm)

            if len(args) > 2:
                resultFilename = str(args[2])
                with open(resultFilename, "w") as outputFile:
                    outputFile.write('v2.0 raw\n' + asm)
                    print('\nSaved result to file "' + resultFilename + '"')



if __name__ == '__main__':
    main(sys.argv)


from capstone            import Cs, CS_ARCH_X86, CS_MODE_32
from pygments            import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers     import get_lexer_by_name
from colorama            import Fore

class Instruccion:
    def __init__(self, address, mnemonic, op_str, _bytes) -> None:
        self.address     = address
        self.mnemonic    = mnemonic
        self.op_str      = op_str
        self.instruccion = mnemonic + " " + op_str
        self.bytes       = _bytes

def disassemble_bytes(data, arch=CS_ARCH_X86, mode=CS_MODE_32, offset=0):
    instrucciones = {}
    md = Cs(arch, mode)
    # Determina la arquitectura basada en el nombre del archivo.
    # Por ejemplo, para x86, se utilizaría CS_ARCH_X86.
    for insn in md.disasm(data, offset):
        instrucciones.update({insn.address : Instruccion(insn.address, insn.mnemonic, insn.op_str, insn.bytes)})

    return instrucciones

def disassemble_file(file_path, arch=CS_ARCH_X86, mode=CS_MODE_32):
    with open(file_path, 'rb') as f:
        data = f.read()

    return disassemble_bytes(data, arch=arch, mode=mode)

    # Desensambla el código de máquina y lo imprime
    # for insn in md.disasm(data, 0):
    #     print(f"0x{insn.address:x}: {insn.mnemonic} {insn.op_str}")

def print_instrucciones(Instrucciones):
    for i in range(list(Instrucciones.keys())[0], list(Instrucciones.keys())[-1]):
        try:

            #print(f"{Instrucciones[i].address:#018x}: \t{' '.join(f'{hex(b).split('0x')[0]:02}' for b in Instrucciones[i].bytes):<20} {Instrucciones[i].mnemonic} {Instrucciones[i].op_str}")
            print(
                #highlight(
                #    code=
                    "{3}{0:#018x}:  {4}{1:<32}{5} {2}".format(
                        Instrucciones[i].address,
                        ' '.join(
                            '{:02}'.format(
                                "".join(hex(b).split('0x'))
                                ) for b in Instrucciones[i].bytes
                            ),
                        highlight(
                            code="{} {}".format(Instrucciones[i].mnemonic, Instrucciones[i].op_str),
                            lexer= get_lexer_by_name("nasm"),
                            formatter=Terminal256Formatter(style="dracula")
                        ),
                        Fore.LIGHTWHITE_EX, Fore.LIGHTYELLOW_EX, Fore.RESET
                    ),
                #    lexer= get_lexer_by_name("nasm"),
                #    formatter=Terminal256Formatter(style="monokai")
                #)
            end='')

        except KeyError:
            pass

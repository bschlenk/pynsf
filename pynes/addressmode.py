import struct

class BaseMode1(object):
    """these routines don't take any arguments"""
    num_bytes = 1


class BaseMode2(object):
    """contains routines to parse 2 byte opcodes"""
    _struct_fmt = '<BB'
    _struct_len = struct.calcsize(_struct_fmt)
    num_bytes = 2

    def parse_args(self):
        return struct.unpack(self._struct_fmt, self.core.memory_str[self.core.pc:self.core.pc+self._struct_len])


class BaseMode3(BaseMode2):
    """contains routines to parse 3 byte opcodes"""
    _struct_fmt = '<BH'
    _struct_len = struct.calcsize(_struct_fmt)
    num_bytes = 3


class Immediate(BaseMode2):
    """In this mode the operand's value is given in the instruction itself. In
    assembly language this is indicated by "#" before the operand.
    eg.  LDA #$0A - means "load the accumulator with the hex value 0A"
    In machine code different modes are indicated by different codes. So LDA
    would be translated into different codes depending on the addressing mode.
    In this mode, it is: $A9 $0A
    """

    def init_args(self):
        args = self.parse_args()
        self.get_arg = lambda: args[1]
        # no set_arg function, doesn't make sense for immediate addressing
        

class ZeroPage(BaseMode2):
    """Absolute and Zero-page Absolute
    In these modes the operands address is given.
    eg.  LDA $31F6 - (assembler)
    $AD $31F6 - (machine code)
    If the address is on zero page - i.e. any address where the high byte is
    00 - only 1 byte is needed for the address. The processor automatically
    fills the 00 high byte.
    eg.  LDA $F4
    $A5 $F4
    Note the different instruction codes for the different modes.
    Note also that for 2 byte addresses, the low byte is store first, eg.
    LDA $31F6 is stored as three bytes in memory, $AD $F6 $31.
    Zero-page absolute is usually just called zero-page.
    """
    
    def init_args(self):
        args = self.parse_args()
        self.get_arg = lambda: self.core.memory[args[1]]


class ZeroPageX(BaseMode2):
    def init_args(self):
        args = self.parse_args()
        self.get_arg = lambda: self.core.memory[args[1] + self.core.x]


class ZeroPageY(BaseMode2):
    def init_args(self):
        args = self.parse_args()
        self.get_arg = lambda: self.core.memory[args[1] + self.core.y]


class Absolute(BaseMode3):
    def init_args(self):
        args = self.parse_args()
        self.get_arg = lambda: self.core.memory[args[1]]


class AbsoluteX(BaseMode3):
    def init_args(self):
        args = self.parse_args()
        self.get_arg = lambda: self.core.memory[args[1] + self.core.x]


class AbsoluteY(object):
    def init_args(self):
        args = self.parse_args()
        self.get_arg = lambda: self.core.memory[args[1] + self.core.y]


class Indirect(BaseMode3):
    def init_args(self):
        args = self.parse_args()
        def _get_arg():
            return struct.unpack('<H', self.core.memory_str[args[1]:args[1]+2])[0]
        self.get_arg = _get_arg


class IndirectX(BaseMode2):
    def init_args(self):
        args = self.parse_args()
        def _get_arg():
            mem_loc = args[1] + self.core.x
            val = struct.unpack('<H', self.core.memory_str[mem_loc:mem_loc+2])[0]
            return self.core.memory[val]
        self.get_arg = _get_arg


class IndirectY(BaseMode2):
    """In this mode the contents of a zero-page address (and the following byte)
    give the indirect addressm which is added to the contents of the Y-register
    to yield the actual address of the operand. Again, inassembly language,
    the instruction is indicated by parenthesis.
    eg.  LDA ($4C), Y
    Note that the parenthesis are only around the 2nd byte of the instruction
    since it is the part that does the indirection.
    Assume the following -        byte       value
                                  $004C      $00
                                  $004D      $21
                                  Y-reg.     $05
                                  $2105      $6D
    Then the instruction above executes by:
    (i)   getting the address in bytes $4C, $4D = $2100
    (ii)  adding the contents of the Y-register = $2105
    (111) loading the contents of the byte $2105 - i.e. $6D into the
          accumulator.
    Note: only the Y-register is used in this mode.
    """
    def init_args(self):
        args = self.parse_args(opcode)
        def _get_arg():
            val = struct.unpack('<H', self.core.memory_str[args[1]:args[1]+2])[0]
            return self.core.memory[val + self.core.y]
        self.get_arg = _get_arg


class Accumulator(BaseMode1):
    """In this mode the instruction operates on data in the accumulator. A set_arg
    function is defined to set the value in the accumulator
    """
    def init_args(self):
        self.get_arg = lambda: self.core.acc
        def _set_arg(self, val):
            self.core.acc = val
        self.set_arg = _set_arg


class Relative(BaseMode2):
    """ This mode is used with Branch-on-Condition instructions. It is probably
    the mode you will use most often. A 1 byte value is added to the program
    counter, and the program continues execution from that address. The 1
    byte number is treated as a signed number - i.e. if bit 7 is 1, the number
    given byt bits 0-6 is negative; if bit 7 is 0, the number is positive. This
    enables a branch displacement of up to 127 bytes in either direction.
    eg  bit no.  7 6 5 4 3 2 1 0    signed value          unsigned value
        value    1 0 1 0 0 1 1 1    -39                   $A7
        value    0 0 1 0 0 1 1 1    +39                   $27
    Instruction example:
        BEQ $A7
        $F0 $A7
    This instruction will check the zero status bit. If it is set, 39 decimal
    will be subtracted from the program counter and execution continues from
    that address. If the zero status bit is not set, execution continues from
    the following instruction.
    Notes:  a) The program counter points to the start of the instruction
               after the branch instruction before the branch displacement is added.
               Remember to take this into account when calculating displacements.
            b) Branch-on-condition instructions work by checking the relevant
               status bits in the status register. Make sure that they have been set or
               unset as you want them. This is often done using a CMP instruction.
            c) If you find you need to branch further than 127 bytes, use the
               opposite branch-on-condition and a JMP.
    """

    _struct_fmt = '<Bb'
    _struct_len = struct.calcsize(_struct_fmt)

    def init_args(self):
        args = self.parse_args(opcode)
        self.get_arg = lambda: args[0]


class Implied(BaseMode1):
    """No operand addresses are required for this mode. They are implied by the
    instruction.
    """


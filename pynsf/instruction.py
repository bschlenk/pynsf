import struct

class Instruction(object):

    def __init__(self, instruction):
        self.opcode = instruction >> 6 & 0xFF
        try:
            init_args(self.opcode)
        except AttributeError:
            pass

    def get_arg(self, opcode):
        """gets overwritten by an addressmode mixin"""

    def __call__(self, core):
        """implemented by derived classes"""
    

class ADC(Instruction):
    """Add Memory to Accumulator with Carry"""

    def __call__(self, core):
        arg = self.get_arg(core)
        core.acc = arg + core.acc + core.status.c


class AND(Instruction):
    """"AND" Memory with Accumulator"""
    def __call__(self, core):
        arg = self.get_arg(core)
        core.acc &= arg


# TODO: implement a set_arg function to set the location of the address mode
class ASL(Instruction):
    """Shift Left One Bit (Memory or Accumulator)"""


class BCC(Instruction):
    """Branch on Carry Clear"""
    def __call__(self, core):
        if not core.status.c:
            core.pc = self.get_arg(core)


class BCS(Instruction):
    """Branch on Carry Set"""
    def __call__(self, core):
        if core.status.c:
            core.pc = self.get_arg(core)


class BEQ(Instruction):
    """Branch on Result Zero"""
    def __call__(self, core):
        if core.status.z:
            core.pc = self.get_arg(core)


class BIT(Instruction):
    """Test Bits in Memory with Accumulator"""
    def __call__(self, core):
        val = core.acc & self.get_arg(core)
        core.status.z = not val
        core.status.v = bool((val >> 6) & 0x01)
        core.status.s = bool((val >> 7) & 0x01)


class BMI(Instruction):
    """Branch on Result Minus"""
    def __call__(self, core):
        if self.core.s:
            core.pc = self.get_arg(core)


class BNE(Instruction):
    """Branch on Result not Zero"""
    def __call__(self, core):
        if not self.core.z:
            core.pc = self.get_arg(core)


class BPL(Instruction):
    """Branch on Result Plus"""
    def __call__(self, core):
        if self.core.z:
            core.pc = self.get_arg(core)


class BRK(Instruction):
    """Force Break"""
    def __call__(self, core):
        core.stack.push(core.pc + 2)
        core.stack.push(core.status)
        core.status.i = True
    

class BVC(Instruction):
    """Branch on Overflow Clear"""
    def __call__(self, core):
        if not self.status.v:
            core.pc = self.get_arg(core)


class BVS(Instruction):
    """Branch on Overflow Set"""
    def __call__(self, core):
        if self.status.v:
            core.pc = self.get_arg(core)


class CLC(Instruction):
    """Clear Carry Flag"""
    def __call__(self, core):
        core.status.c = False


class CLD(Instruction):
    """Clear Decimal Mode"""
    def __call__(self, core):
        core.status.d = False


class CLI(Instruction):
    """Clear interrupt Disable Bit"""
    def __call__(self, core):
        core.status.i = False


class CLV(Instruction):
    """Clear Overflow Flag"""
    def __call__(self, core):
        core.status.v = False


class CMP(Instruction):
    """Compare Memory and Accumulator"""
    def __call__(self, core):
        core.set_status_from_value(core.acc - self.get_value(core), core.acc, False)


class CPX(Instruction):
    """Compare Memory and Index X"""
    def __call__(self, core):
        core.set_status_from_value(core.x - self.get_value(core), core.x, False)


class CPY(Instruction):
    """Compare Memory and Index Y"""
    def __call__(self, core):
        core.set_status_from_value(core.y - self.get_value(core), core.y, False)


# TODO: this needs to update status registers
class DEC(Instruction):
    """Decrement Memory by One"""
    def __call__(self, core):
        self.set_arg(core, self.get_arg(core) - 1)


# TODO: this needs to update status registers
class DEX(Instruction):
    """Decrement Index X by One"""
    def __call__(self, core):
        core.x -= 1


# TODO: this needs to update status registers
class DEY(Instruction):
    """Decrement Index Y by One"""
    def __call__(self, core):
        core.y -= 1


class EOR(Instruction):
    """"Exclusive-Or" Memory with Accumulator"""
    def __call__(self, core):
        core.acc = self.get_arg(core) ^ core.acc
    

class INC(Instruction):
    """Increment Memory by One"""
    def __call__(self, core):
        self.set_arg(core, self.get_arg(core) + 1)


class INX(Instruction):
    """Increment Index X by One"""
    def __call__(self, core):
        core.x += 1


class INY(Instruction):
    """Increment Index Y by One"""
    def __call__(self, core):
        core.y += 1


# TODO: not sure on what this is supposed to do
class JMP(Instruction):
    """Jump to New Location"""
    def __call__(self, core):
        core.pc = self.get_arg(core)


class JSR(Instruction):          
    """JSR Jump to new location saving return address"""
    def __call__(self, core):
        core.stack.push(core.pc + 2)
        core.pc = self.get_arg(core)


# TODO: don't update the status registers!
class LDA(Instruction):
    """LDA Load accumulator with memory"""
    def __call__(self, core):
        core.acc = self.get_arg(core)


class LDX(Instruction):
    """LDX Load index X with memory"""
    def __call__(self, core):
        core.x = self.get_arg(core)
            
class LDY(Instruction):
    """LDY Load index Y with memory"""
    def __call__(self, core):
        core.y = self.get_arg(core)


# TODO: get status bits right
class LSR(Instruction):
    """LSR Shift right one bit (memory or accumulator)"""
    def __call__(self, core):
        self.set_arg(core, self.get_arg(core) >> 1)


class NOP(Instruction):
    """NOP No operation"""
    def __call__(self, core):
        pass


# TODO: get status bits right
class ORA(Instruction):
    """ORA "OR" memory with accumulator"""
    def __call__(self, core):
        core.acc = core.acc | self.get_arg(core)


class PHA(Instruction):
    """PHA Push accumulator on stack"""
    def __call__(self, core):
        core.stack.push(core.acc)


class PHP(Instruction):
    """PHP Push processor status on stack"""
    def __call__(self, core):
        core.stack.push(core.status)


#TODO: don't affect status registers
class PLA(Instruction):
    """PLA Pull accumulator from stack"""
    def __call__(self, core):
        core.acc = core.stack.pop()
                        
class PLP(Instruction):
    """PLP Pull processor status from stack"""
    def __call__(self, core):
        core.status = core.stack.pop()


# TODO: this instruction
class ROL(Instruction):
    """ROL Rotate one bit left (memory or accumulator)"""
    def __call__(self, core):
        """
        +------------------------------+
        |         M or A               |
        |   +-+-+-+-+-+-+-+-+    +-+   |
    Operation:   +-< |7|6|5|4|3|2|1|0| <- |C| <-+         N Z C I D V
        +-+-+-+-+-+-+-+-+    +-+             / / / _ _ _
            (Ref: 10.3)
        """


# TODO: this instruction
class ROR(Instruction):
    """ROR Rotate one bit right (memory or accumulator)"""
    def __call__(self, core):
        """
        +------------------------------+
        |                              |
        |   +-+    +-+-+-+-+-+-+-+-+   |
        Operation:   +-> |C| -> |7|6|5|4|3|2|1|0| >-+         N Z C I D V
        +-+    +-+-+-+-+-+-+-+-+             / / / _ _ _
        (Ref: 10.4)
        """

class RTI(Instruction):
    """RTI Return from interrupt"""
    def __call__(self, core):
        core.status = core.stack.pop()
        core.pc = core.stack.pop()


class RTS(Instruction):
    """RTS Return from subroutine"""
    def __call__(self, core):
        core.pc = core.stack.pop() + 1


# TODO: this function
class SBC(Instruction):
    """SBC Subtract memory from accumulator with borrow"""
    def __call__(self, core):
        """
        Operation:  A - M - C -> A                            N Z C I D V
            -                                              / / / _ _ /
                Note:C = Borrow             (Ref: 2.2.2)
        """

class SEC(Instruction):
    """SEC Set carry flag"""
    def __call__(self, core):
        core.status.c = True

class SED(Instruction):
    """SED Set decimal mode"""
    def __call__(self, core):
        core.status.d = True

class SEI(Instruction):
    """SEI Set interrupt disable status"""
    def __call__(self, core):
        core.status.i = True


# TODO: this function
class STA(Instruction):
    """STA Store accumulator in memory"""
    def __call__(self, core):
        """
        Operation:  A -> M              N Z C I D V
                                        _ _ _ _ _ _
                (Ref: 2.1.2)
        """
                                            

# TODO: this function
class STX(Instruction):
    """STX Store index X in memory"""
    def __call__(self, core):
        """
        Operation: X -> M         N Z C I D V
                                  _ _ _ _ _ _
                (Ref: 7.2)
        """

# TODO: this function
class STY(Instruction):
    """STY Store index Y in memory"""
    def __call__(self, core):
        """
        Operation: Y -> M      N Z C I D V
                               _ _ _ _ _ _
                (Ref: 7.3)
        """
                                                    
                                                    
class TAX(Instruction):
    """TAX Transfer accumulator to index X"""
    def __call__(self, core):
        core.x = core.acc


class TAY(Instruction):
    """TAY Transfer accumulator to index Y"""
    def __call__(self, core):
        core.y = core.acc


class TSX(Instruction):
    """TSX Transfer stack pointer to index X"""
    def __call__(self, core):
        core.x = len(core.stack)


# TODO: all transfer functions should affect the S and Z status flags
# (except for transfer to stack pointer)
class TXA(Instruction):
    """TXA Transfer index X to accumulator"""
    def __call__(self, core):
        core.acc = core.x


# TODO: allow this to work
class TXS(Instruction):
    """TXS Transfer index X to stack pointer"""
    def __call__(self, core):
        pass


class TYA(Instruction):
    """TYA Transfer index Y to accumulator"""
    def __call__(self, core):
        core.acc = core.y


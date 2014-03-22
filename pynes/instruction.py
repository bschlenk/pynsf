import struct

class Instruction(object):
    """Base class for all 6502 instructions"""
    def __init__(self, core):
        if not hasattr(self, 'is_branch'):
            self.is_branch = False
        self.core = core
        self.opcode = core.memory[core.pc]
        try:
            self.init_args()
        except AttributeError:
            pass


    def get_arg(self):
        """gets overwritten by an addressmode mixin
        will return an argument as a function of the core
        state and the addressmode of the operation"""


    def set_arg(self, val):
        """gets overwritten by an addressmode mixin
        will set a value in memory as a function of the core state
        and the addressmode of the operation"""


    def __call__(self):
        """implemented by derived classes"""


class Branch(object):
    is_branch = True
    

class ADC(Instruction):
    """Add Memory to Accumulator with Carry"""
    def __call__(self):
        core = self.core
        arg = self.get_arg()
        core.acc = core.add(arg)


class AND(Instruction):
    """"AND" Memory with Accumulator"""
    def __call__(self):
        core = self.core
        arg = self.get_arg()
        core.acc &= arg


class ASL(Instruction):
    """Shift Left One Bit (Memory or Accumulator)"""
    def __call__(self):
        core = self.core
        val = self.get_arg()
        core.status.c = bool(val >> 7 & 0x01)
        self.set_arg(core, val << 1)


class BCC(Instruction, Branch):
    """Branch on Carry Clear"""
    def __call__(self):
        core = self.core
        if not core.status.c:
            core.pc = self.get_arg()
        else:
            core.pc += self.num_bytes


class BCS(Instruction, Branch):
    """Branch on Carry Set"""
    def __call__(self):
        core = self.core
        if core.status.c:
            core.pc = self.get_arg()
        else:
            core.pc += self.num_bytes


class BEQ(Instruction, Branch):
    """Branch on Result Zero"""
    def __call__(self):
        core = self.core
        if core.status.z:
            core.pc = self.get_arg()
        else:
            core.pc += self.num_bytes


class BIT(Instruction):
    """Test Bits in Memory with Accumulator"""
    def __call__(self):
        core = self.core
        val = core.acc & self.get_arg()
        core.status.z = not val
        core.status.v = bool(val >> 6 & 0x01)
        core.status.s = bool(val >> 7 & 0x01)


class BMI(Instruction, Branch):
    """Branch on Result Minus"""
    def __call__(self):
        if self.core.s:
            self.core.pc = self.get_arg()
        else:
            self.core.pc += self.num_bytes


class BNE(Instruction, Branch):
    """Branch on Result not Zero"""
    def __call__(self):
        if not self.core.z:
            self.core.pc = self.get_arg()
        else:
            self.core.pc += self.num_bytes


class BPL(Instruction, Branch):
    """Branch on Result Plus"""
    def __call__(self):
        if self.core.z:
            self.core.pc = self.get_arg()
        else:
            self.core.pc += self.num_bytes


class BRK(Instruction):
    """Force Break"""
    def __call__(self):
        self.core.stack.push(core)
        self.core.stack.push(core)
        self.core.status.i = True
    

class BVC(Instruction, Branch):
    """Branch on Overflow Clear"""
    def __call__(self):
        if not self.status.v:
            self.core.pc = self.get_arg()
        else:
            self.core.pc += self.num_bytes


class BVS(Instruction, Branch):
    """Branch on Overflow Set"""
    def __call__(self):
        if self.status.v:
            self.core.pc = self.get_arg()
        else:
            self.core.cp += self.num_bytes


class CLC(Instruction):
    """Clear Carry Flag"""
    def __call__(self):
        self.core.status.c = False


class CLD(Instruction):
    """Clear Decimal Mode"""
    def __call__(self):
        self.core.status.d = False


class CLI(Instruction):
    """Clear interrupt Disable Bit"""
    def __call__(self):
        self.core.status.i = False


class CLV(Instruction):
    """Clear Overflow Flag"""
    def __call__(self):
        self.core.status.v = False


class CMP(Instruction):
    """Compare Memory and Accumulator"""
    def __call__(self):
        val = self.core.sub(self.core.acc, self.get_arg(), False)
        self.core.update_zero_neg(val)


class CPX(Instruction):
    """Compare Memory and Index X"""
    def __call__(self):
        val = self.core.sub(self.core.x, self.get_arg(), False)
        self.core.update_zero_neg(val)


class CPY(Instruction):
    """Compare Memory and Index Y"""
    def __call__(self):
        val = self.core.sub(self.core.y, self.get_arg(), False)
        self.core.update_zero_neg(val)


class DEC(Instruction):
    """Decrement Memory by One"""
    def __call__(self):
        val = self.get_arg() - 1
        self.core.set_zero_neg(val)
        self.set_arg(core, val)


class DEX(Instruction):
    """Decrement Index X by One"""
    def __call__(self):
        core.x -= 1


class DEY(Instruction):
    """Decrement Index Y by One"""
    def __call__(self):
        core.y -= 1


class EOR(Instruction):
    """"Exclusive-Or" Memory with Accumulator"""
    def __call__(self):
        core.acc = self.get_arg() ^ core.acc
    

class INC(Instruction):
    """Increment Memory by One"""
    def __call__(self):
        val = self.get_arg() + 1
        self.core.set_zero_neg(val)
        self.set_arg(self.core, val)


class INX(Instruction):
    """Increment Index X by One"""
    def __call__(self):
        self.core.x += 1


class INY(Instruction):
    """Increment Index Y by One"""
    def __call__(self):
        self.core.y += 1


# TODO: not sure on what this is supposed to do
class JMP(Instruction, Branch):
    """Jump to New Location"""
    def __call__(self):
        self.core.pc = self.get_arg()


class JSR(Instruction, Branch):          
    """JSR Jump to new location saving return address"""
    def __call__(self):
        sef.core.stack.push(self.core + 2)
        self.core.pc = self.get_arg()


class LDA(Instruction):
    """LDA Load accumulator with memory"""
    def __call__(self):
        self.core.acc = self.get_arg()


class LDX(Instruction):
    """LDX Load index X with memory"""
    def __call__(self):
        self.core.x = self.get_arg()

            
class LDY(Instruction):
    """LDY Load index Y with memory"""
    def __call__(self):
        self.core.y = self.get_arg()


class LSR(Instruction):
    """LSR Shift right one bit (memory or accumulator)"""
    def __call__(self):
        val = self.get_arg()
        self.core.status.c = val & 0x01
        val >>= 1
        self.set_arg(val)
        self.core.update_zero_neg(val)


class NOP(Instruction):
    """NOP No operation"""
    def __call__(self):
        pass


class ORA(Instruction):
    """ORA "OR" memory with accumulator"""
    def __call__(self):
        core.acc = core.acc | self.get_arg()


class PHA(Instruction):
    """PHA Push accumulator on stack"""
    def __call__(self):
        self.core.stack.push(self.core.acc)


class PHP(Instruction):
    """PHP Push processor status on stack"""
    def __call__(self):
        self.core.stack.push(self.core.status)


class PLA(Instruction):
    """PLA Pull accumulator from stack"""
    def __call__(self):
        # we don't want to affect the status registers
        self.core._acc = self.core.stack.pop()

                        
class PLP(Instruction):
    """PLP Pull processor status from stack"""
    def __call__(self):
        self.core.status = self.core.stack.pop()


class ROL(Instruction):
    """ROL Rotate one bit left (memory )"""
    def __call__(self):
        def __call__(self):
            val = self.get_arg()
            c = val >> 7 & 0x01
            val <<= 1
            val |= int(self.core.status.c)
            self.set_arg(self.core, val)
            self.core.status.c = bool(c)
            self.core.set_zero_neg(val)


class ROR(Instruction):
    """ROR Rotate one bit right (memory )"""
    def __call__(self):
        val = self.get_arg()
        c = val & 0x01
        val >>= 1
        val |= (int(self.core.status.c) << 7)
        self.set_arg(self.core, val)
        self.core.status.c = bool(c)
        self.core.set_zero_neg(val)


class RTI(Instruction, Branch):
    """RTI Return from interrupt"""
    def __call__(self):
        self.core.status = self.core.stack.pop()
        self.core.pc = self.core.stack.pop()


class RTS(Instruction, Branch):
    """RTS Return from subroutine"""
    def __call__(self):
        self.core.pc = self.core.stack.pop() + 1


class SBC(Instruction):
    """SBC Subtract memory from accumulator with borrow"""
    def __call__(self):
        self.core.acc = self.core.sub(acc, self.get_arg())


class SEC(Instruction):
    """SEC Set carry flag"""
    def __call__(self):
        self.core.status.c = True


class SED(Instruction):
    """SED Set decimal mode"""
    def __call__(self):
        self.core.status.d = True


class SEI(Instruction):
    """SEI Set interrupt disable status"""
    def __call__(self):
        self.core.status.i = True


class STA(Instruction):
    """STA Store accumulator in memory"""
    def __call__(self):
        self.set_arg(self.core, self.core.acc)
                                            

class STX(Instruction):
    """STX Store index X in memory"""
    def __call__(self):
        self.set_arg(self.core, self.core.x)


class STY(Instruction):
    """STY Store index Y in memory"""
    def __call__(self):
        self.set_arg(self.core, self.core.y)
                                                    
                                                    
class TAX(Instruction):
    """TAX Transfer accumulator to index X"""
    def __call__(self):
        self.core.x = self.core.acc


class TAY(Instruction):
    """TAY Transfer accumulator to index Y"""
    def __call__(self):
        self.core.y = self.core.acc


class TSX(Instruction):
    """TSX Transfer stack pointer to index X"""
    def __call__(self):
        self.core.x = self.core.stack.sp


class TXA(Instruction):
    """TXA Transfer index X to accumulator"""
    def __call__(self):
        self.core.acc = self.core.x


class TXS(Instruction):
    """TXS Transfer index X to stack pointer"""
    def __call__(self):
        self.core.stack.sp = self.core.x


class TYA(Instruction):
    """TYA Transfer index Y to accumulator"""
    def __call__(self):
        self.core.acc = self.core.y


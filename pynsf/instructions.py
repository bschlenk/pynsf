#!/usr/bin/env python
from pynfs.instruction import *
from pynfs.addressmode import *

def create_instruction(func, mode):
    """creates a dynamic type using "func" and "mode" as base classes"""
    return type(func.__name__ + mode.__name__, (func, mode), {})

instruction_map = {
    # ADC instructions
    0x69: create_instruction(ADC, Immediate),
    0x65: create_instruction(ADC, ZeroPage),
    0x75: create_instruction(ADC, ZeroPageX),
    0x60: create_instruction(ADC, Absolute),
    0x70: create_instruction(ADC, AbsoluteX),
    0x79: create_instruction(ADC, AbsoluteY),
    0x61: create_instruction(ADC, IndirectX),
    0x71: create_instruction(ADC, IndirectY),

    # AND instructions
    0x29: create_instruction(AND, Immediate),
    0x25: create_instruction(AND, ZeroPage),
    0x35: create_instruction(AND, ZeroPageX),
    0x2D: create_instruction(AND, Absolute),
    0x3D: create_instruction(AND, AbsoluteX),
    0x39: create_instruction(AND, AbsoluteY),
    0x21: create_instruction(AND, IndirectX),
    0x31: create_instruction(AND, IndirectY),

    # ASL instructions
    0x0A: create_instruction(ASL, Accumulator),
    0x06: create_instruction(ASL, ZeroPage),
    0x16: create_instruction(ASL, ZeroPageX),
    0x0E: create_instruction(ASL, Absolute),
    0x1E: create_instruction(ASL, AbsoluteX),
    
    # BCC instructions
    0x90: create_instruction(BCC, Relative),

    # BCS instructions
    0xB0: create_instruction(BCS, Relative),

    # BEQ instructions
    0xF0: create_instruction(BEQ, Relative),

    # BIT instructions
    0x24: create_instruction(BIT, ZeroPage),
    0x2C: create_instruction(BIT, Absolute),

    # BMI instructions
    0x30: create_instruction(BMI, Relative),

    #BNE instructions
    0xD0: create_instruction(BNE, Relative),

    # BPL instructions
    0x10: create_instruction(BPL, Relative),

    # BRK instructions
    0x00: create_instruction(BRK, Implied),

    #BVC instructions
    0x50: create_instruction(BVC, Relative),

    # BVS instructions
    0x70: create_instruction(BVS, Relative),

    # CLC instructions
    0x18: create_instruction(CLC, Implied),

    # CLD instructions
    0xD8: create_instruction(CLD, Implied),

    # CLI instructions
    0x58: create_instruction(CLI, Implied),

    # CLV instructions
    0xB8: create_instruction(CLV, Implied),

    # CMP instructions
    0xC9: create_instruction(CLV, Immediate),
    0xC5: create_instruction(CLV, ZeroPage),
    0xD5: create_instruction(CLV, ZeroPageX),
    0xCD: create_instruction(CLV, Absolute),
    0xDD: create_instruction(CLV, AbsoluteX),
    0xD9: create_instruction(CLV, AbsoluteY),
    0xC1: create_instruction(CLV, IndirectX),
    0xD1: create_instruction(CLV, IndirectY),

    # CPX instructions
    0xE0: create_instruction(CPX, Immediate),
    0xE4: create_instruction(CPX, ZeroPage),
    0xEC: create_instruction(CPX, Absolute),

    # CPY instructions
    0xC0: create_instruction(CPY, Immediate),
    0xC4: create_instruction(CPY, ZeroPage),
    0xCC: create_instruction(CPY, Absolute),

    # DEC instructions
    0xC6: create_instruction(DEC, ZeroPage),
    0xD6: create_instruction(DEC, ZeroPageX),
    0xCE: create_instruction(DEC, Absolute),
    0xDE: create_instruction(DEC, AbsoluteX),

    # DEX instructions
    0xCA: create_instruction(DEX, Implied),

    # DEY instructions
    0x88: create_instruction(DEY, Implied),

    # EOR instructions
    0x49: create_instruction(EOR, Immediate),
    0x45: create_instruction(EOR, ZeroPage),
    0x55: create_instruction(EOR, ZeroPageX),
    0x40: create_instruction(EOR, Absolute),
    0x50: create_instruction(EOR, AbsoluteX),
    0x59: create_instruction(EOR, AbsoluteY),
    0x41: create_instruction(EOR, IndirectX),
    0x51: create_instruction(EOR, IndirectY),

    # INC instructions
    0xE6: create_instruction(INC, ZeroPage),
    0xF6: create_instruction(INC, ZeroPageX),
    0xEE: create_instruction(INC, Absolute),
    0xFE: create_instruction(INC, AbsoluteX),

    # INX instructions
    0xE8: create_instruction(INX, Implied),

    # INY instructions
    0xC8: create_instruction(INY, Implied),
    
    # JMP instructions
    0x4C: create_instruction(JMP, Absolute),
    0x6C: create_instruction(JMP, Indirect),

    # JSR instructions
    0x20: create_instruction(JSR, Absolute),

    # LDA instructions
    0xA9: create_instruction(LDA, Immediate),
    0xA5: create_instruction(LDA, ZeroPage),
    0xB5: create_instruction(LDA, ZeroPageX),
    0xAD: create_instruction(LDA, Absolute),
    0xBD: create_instruction(LDA, AbsoluteX),
    0xB9: create_instruction(LDA, AbsoluteY),
    0xA1: create_instruction(LDA, IndirectX),
    0xB1: create_instruction(LDA, IndirectY),

    # LDX instructions
    0xA2: create_instruction(LDX, Immediate),
    0xA6: create_instruction(LDX, ZeroPage),
    0xB6: create_instruction(LDX, ZeroPageY),
    0xAE: create_instruction(LDX, Absolute),
    0xBE: create_instruction(LDX, AbsoluteY),

    # LDY instructions
    0xA0: create_instruction(LDY, Immediate),
    0xA4: create_instruction(LDY, ZeroPage),
    0xB4: create_instruction(LDY, ZeroPageX),
    0xAC: create_instruction(LDY, Absolute),
    0xBC: create_instruction(LDY, AbsoluteX),

    # LSR instructions
    0x4A: create_instruction(LSR, Accumulator),
    0x46: create_instruction(LSR, ZeroPage),
    0x56: create_instruction(LSR, ZeroPageX),
    0x4E: create_instruction(LSR, Absolute),
    0x5E: create_instruction(LSR, AbsoluteX),
    
    
    # NOP instructions
    0xEA: create_instruction(NOP, Implied),
    
    # ORA instructions
    0x09: create_instruction(ORA, Immediate),
    0x05: create_instruction(ORA, ZeroPage),
    0x15: create_instruction(ORA, ZeroPageX),
    0x0D: create_instruction(ORA, Absolute),
    0x1D: create_instruction(ORA, AbsoluteX),
    0x19: create_instruction(ORA, AbsoluteY),
    0x01: create_instruction(ORA, IndirectX),
    0x11: create_instruction(ORA, IndirectY),
    
    
    # PHA instructions
    0x48: create_instruction(PHA, Implied),
    
    # PHP instructions
    0x08: create_instruction(PHP, Implied),
    
    # PLA instructions
    0x68: create_instruction(PLA, Implied),
    
    # PLP instructions
    0x28: create_instruction(PLP, Implied),
    
    # ROL instructions
    0x2A: create_instruction(ROL, Accumulator),
    0x26: create_instruction(ROL, ZeroPage),
    0x36: create_instruction(ROL, ZeroPageX),
    0x2E: create_instruction(ROL, Absolute),
    0x3E: create_instruction(ROL, AbsoluteX),
    
    
    # ROR instructions
    0x6A: create_instruction(ROR, Accumulator),
    0x66: create_instruction(ROR, ZeroPage),
    0x76: create_instruction(ROR, ZeroPageX),
    0x6E: create_instruction(ROR, Absolute),
    0x7E: create_instruction(ROR, AbsoluteX),
    
    # RTI instructions
    0x4D: create_instruction(RTI, Implied),
    
    # RTS instructions
    0x60: create_instruction(RTS, Implied),
    
    # SBC instructions
    0xE9: create_instruction(SBC, Immediate),
    0xE5: create_instruction(SBC, ZeroPage),
    0xF5: create_instruction(SBC, ZeroPageX),
    0xED: create_instruction(SBC, Absolute),
    0xFD: create_instruction(SBC, AbsoluteX),
    0xF9: create_instruction(SBC, AbsoluteY),
    0xE1: create_instruction(SBC, IndirectX),
    0xF1: create_instruction(SBC, IndirectY),
    
    
    # SEC instructions
    0x38: create_instruction(SEC, Implied),
    
    # SED instructions
    0xF8: create_instruction(SED, Implied),
    
    # SEI instructions
    0x78: create_instruction(SEI, Implied),
    
    # STA instructions
    0x85: create_instruction(STA, ZeroPage),
    0x95: create_instruction(STA, ZeroPageX),
    0x80: create_instruction(STA, Absolute),
    0x90: create_instruction(STA, AbsoluteX),
    0x99: create_instruction(STA, AbsoluteY),
    0x81: create_instruction(STA, IndirectX),
    0x91: create_instruction(STA, IndirectY),
    
    
    # STX instructions
    0x86: create_instruction(STX, ZeroPage),
    0x96: create_instruction(STX, ZeroPageY),
    0x8E: create_instruction(STX, Absolute),
    
    
    # STY instructions
    0x84: create_instruction(STY, ZeroPage),
    0x94: create_instruction(STY, ZeroPageX),
    0x8C: create_instruction(STY, Absolute),
    
    
    # TAX instructions
    0xAA: create_instruction(TAX, Implied),
    
    # TAY instructions
    0xA8: create_instruction(TAY, Implied),
    
    # TSX instructions
    0xBA: create_instruction(TSX, Implied),
    
    # TXA instructions
    0x8A: create_instruction(TXA, Implied),
    
    # TXS instructions
    0x9A: create_instruction(TXS, Implied),
    
    # TYA instructions
    0x98: create_instruction(TYA, Implied),
}

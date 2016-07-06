class CoreStatus():
    """The status register flags"""

    def __init__(self):
        """S - Sign flag: this is set if the result of an operation is
        negative, cleared if positive.
        """
        self.s = False

        """V - Overflow flag: when an arithmetic operation produces a result
        too large to be represented in a byte, V is set.
        """
        self.v = False

        """Bit 4 - B: this is set when a software interrupt (BRK instruction) is
        executed.
        """
        self.b = False

        """D: this is the decimal mode status flag. When set, and an Add with
        Carry or Subtract with Carry instruction is executed, the source values are
        treated as valid BCD (Binary Coded Decimal, eg. 0x00-0x99 = 0-99) numbers.
        The result generated is also a BCD number.
        """
        self.d = False

        """I: this is an interrupt enable/disable flag. If it is set,
        interrupts are disabled. If it is cleared, interrupts are enabled.
        """
        self.i = False

        """Z - Zero flag: this is set to 1 when any arithmetic or logical
        operation produces a zero result, and is set to 0 if the result is
        non-zero.
        """
        self.z = False

        """C - Carry flag: this holds the carry out of the most significant
        bit in any arithmetic operation. In subtraction operations however, this
        flag is cleared - set to 0 - if a borrow is required, set to 1 - if no
        borrow is required. The carry flag is also used in shift and rotate
        logical operations.
        """
        self.c = False


#!/bin/python3
import binascii

class BigInt():
    bytebuff:bytearray = bytearray()
    byteMask=255

    def __init__(self,src):
        if type(src) == str:
            self.setHex(src)
        elif type(src) == bytearray:
            self.setBytearray(src)
    
    def setHex(self,src: str):
        self.bytebuff = bytearray.fromhex(src)[::-1]
        return
    def setBytearray(self,src: bytearray):
        self.bytebuff = src
        return
    def setInt(self,src: int):
        self.bytebuff = bytearray(src.to_bytes((src.bit_length() + 7) // 8,'little'))
        return
    
    def getHex(self):
        return binascii.hexlify(self.bytebuff[::-1])
    def getByteArray(self):
        return self.bytebuff
    def getByte(self,index: int):
        return self.bytebuff[index]
    
    def isNeg(self):
        return BigInt.__defNeg(self.bytebuff)
# ================================================================
    def __autoPad(in1: bytearray,in2: bytearray):
        count1 = len(in1)
        count2 = len(in2)
        if count1 < count2:
            in1 = BigInt.__padByteArray(in1,count2-count1)
        elif count1 > count2:
            in2 = BigInt.__padByteArray(in2,count1-count2)
        return in1, in2
    def __padByteArray(input: bytearray, num: int):
        if BigInt.__defNeg(input):
            pad=255
        else:
            pad=0
        start = len(input)
        for i in range(start, start + num, 1):
            input.append(pad)
        return input
    def __defNeg(input: bytearray):
        return(input[len(input)-1] & 128) != 0
    def __makeByteArray(input):
        if type(input) == int:
            lbuf = bytearray(input.to_bytes((input.bit_length() + 7) // 8,'little'))
        elif type(input) == BigInt:
            lbuf = input.bytebuff
        elif type(input) != BigInt:
            raise Exception("wrong argument type")
        return lbuf
# ================================================================
    # Binary Operators:
    # Operator Magic Method
    # + 
    def __add__(self, other):
        buf1 = self.bytebuff
        buf2 = BigInt.__makeByteArray(other)
        
        buf1, buf2 = BigInt.__autoPad(buf1,buf2)
        count = len(buf1)
        tmpReturn = bytearray()
        sum: int = 0
        for i in range(0,count):
            sum += buf1[i] + buf2[i]
            tmpReturn.append(sum & self.byteMask)
            print(buf1[i], buf2[i], sum,sum >> 8)
            sum >>= 8
            
        # for i in range(lcount,hcount):
        #     sum += hbuf[i]
        #     tmpReturn.append(sum & self.byteMask)
        #     sum >>= 8

        if sum > 0:
            tmpReturn.append(sum)

        return BigInt(tmpReturn)

    # – 
    def __sub__(self, other):
        tmp = BigInt(BigInt.__makeByteArray(other))
        return self + (~other + 1)
    # * __mul__(self, other)
    # / __truediv__(self, other)
    # // __floordiv__(self, other)
    # % __mod__(self, other)
    # ** __pow__(self, other)
    # >> 
    def __rshift__(self, other: int):
        count = len(self.bytebuff)
        if other > count * 8:
            return 0
        tmpReturn = bytearray()
        start = other//8
        shift = other % 8
        byte: int = 0
        for i in range(start,count-1):
            byte = (self.bytebuff[i] + (self.bytebuff[i+1] << 8)) >> shift
            tmpReturn.append(byte)
        tmpReturn.append(self.bytebuff[count-1] >> shift)
        return BigInt(tmpReturn)
    # << 
    def __lshift__(self, other):        
        count = len(self.bytebuff)
        start = other//8
        tmpReturn = bytearray(start)
        
        shift: int = other % 8
        byte : int = 0
        for i in range(count):
            byte += (self.bytebuff[i] << shift)
            tmpReturn.append(byte & self.byteMask)
            byte >>= 8
        if byte > 0:
            tmpReturn.append(byte & self.byteMask)
        return BigInt(tmpReturn)


#===================================================
#===================================================
#===================================================
#===================================================
        return
    # & 
    def __and__(self, other):
        count = min(len(self.bytebuff),len(other.bytebuff))
        tmpReturn = bytearray()
        for i in range(count):
            tmpReturn.append(self.bytebuff[i] & other.bytebuff[i])
        return BigInt(tmpReturn)
    # | 
    def __or__(self, other):
        count = min(len(self.bytebuff),len(other.bytebuff))
        tmpReturn = bytearray()
        for i in range(count):
            tmpReturn.append(self.bytebuff[i] | other.bytebuff[i])
        if len(self.bytebuff) > count:
            buf = self.bytebuff
        elif len(other.bytebuff) > count:
            buf = other.bytebuff
        for i in range(count,len(buf)):
            tmpReturn.append(buf[i])
        return BigInt(tmpReturn)
    # ^ 
    def __xor__(self, other):
        count = min(len(self.bytebuff),len(other.bytebuff))
        tmpReturn = bytearray()
        for i in range(count):
            tmpReturn.append(self.bytebuff[i] ^ other.bytebuff[i])
        if len(self.bytebuff) > count:
            buf = self.bytebuff
        elif len(other.bytebuff) > count:
            buf = other.bytebuff
        for i in range(count,len(buf)):
            tmpReturn.append(buf[i])
        return BigInt(tmpReturn)

    # Comparison Operators :
    # Operator Magic Method
    # == 
    def __eq__(self, other: 'BigInt'):
        count = len(self.bytebuff)
        if len(other.bytebuff) != count:
            return False
        
        for i in range(count):
            if self.bytebuff[i] != other.bytebuff[i]:
                return False
        return True
    # < 
    def __lt__(self, other: 'BigInt'):
        if self == other:
            return False
        
        count = len(self.bytebuff)
        if len(other.bytebuff) > count:
            return True
        if len(other.bytebuff) < count:
            return False
                
        for i in reversed(range(count)):
            if self.bytebuff[i] > other.bytebuff[i]:
                return False
        return True
    # > 
    def __gt__(self, other: 'BigInt'):
        if self < other:
            return False
        return True
    # <= 
    def __le__(self, other: 'BigInt'):
        if self > other:
            return False
        return True
    # >= 
    def __ge__(self, other: 'BigInt'):
        if self < other:
            return False
        return True
    # !=
    def __ne__(self, other: 'BigInt'):
        if self == other:
            return False
        return True

    # Assignment Operators :
    # Operator Magic Method
    # -= __ISUB__(SELF, OTHER)
    # += 
    def __iadd__(self, other):
        return BigInt((self + other).bytebuff)

    # *= __IMUL__(SELF, OTHER)
    # /= __IDIV__(SELF, OTHER)
    # //= __IFLOORDIV__(SELF, OTHER)
    # %= __IMOD__(SELF, OTHER)
    # **= __IPOW__(SELF, OTHER)
    # >>= __IRSHIFT__(SELF, OTHER)
    # <<= __ILSHIFT__(SELF, OTHER)
    # &= __IAND__(SELF, OTHER)
    # |= __IOR__(SELF, OTHER)
    # ^= __IXOR__(SELF, OTHER)
    # Unary Operators :
    # Operator Magic Method
    # – __NEG__(SELF, OTHER)
    # + __POS__(SELF, OTHER)
    # ~
    def __invert__(self):
        tmpReturn = bytearray()
        for i in range(len(self.bytebuff)):
            tmpReturn.append(~self.bytebuff[i] & self.byteMask)
        return BigInt(tmpReturn)

a = BigInt("deadbeef")
print(a.getHex())
print(a.getByte(0))
print(a.getByte(1))
print(a.getByte(2))
print(a.getByte(3))

b = BigInt("abcabc")
c = BigInt(b.getByteArray())
e = BigInt('deadbeff')
print(b.getHex())
print(b.bytebuff)
print((~b).getHex())
print((~b).bytebuff)
print(c.getHex())

print(b==c," - True")
print(b==a,"- False")
print(b<c, "- False")
print(c<b, "- False")
print(b<a, " - True")
print(a<b, "- False")
print(a<e, " - True")
print(e<a, "- False")

d = a + b
print(d.getByteArray())
print(d.getHex(), '= DF59 89AB')
a = a + 1
print(a.getHex())
a+=1
print(a.getHex())

print(BigInt("8FFFFF").isNeg())
print(BigInt("7FFFFF").isNeg())
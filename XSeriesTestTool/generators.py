def charfilter(fileobj, *invalids):
    for char in fileobj.read():
        if char not in invalids:
            yield char

def xpacketextractor(streamgenerator):
    hexptr = streamgenerator
    dict = {0x00: 126, 0x22: 126, 0xA3: 15,
            0x70: 22, 0x71: 34}
    while True:
        BUFFER = bytearray()
        BUFFER.append(hexptr.next())
        BUFFER.append(hexptr.next())
        assert(BUFFER[0] == 0xFF)
        for i in range(dict.get(BUFFER[1])):
            BUFFER.append(hexptr.next())
        #yield ''.join(["%02X" % x for x in BUFFER]) # temporary fix
        yield [x for x in BUFFER]
        
def charpacket(astream, size = 1):
    while True:
        x = ''
        while len(x) < size:
            x += astream.next()
        yield int(x, 16)
    
# to remove once all functions been moved over to packetextractor
def datablockdispatcher(streamgenerator):
# INPUT: stream
# OUTPUT: array of packets
    hexptr = streamgenerator
    dict = {'00': 126, '22': 126, 'A3': 15,
            '70': 22, '71': 34}
    while True:
        BUFFER = [hexptr.next(), hexptr.next()]
        assert(BUFFER[0] == 'FF')
        for i in range(dict.get(BUFFER[1])):
            BUFFER.append(hexptr.next())
        yield BUFFER

def datablockfilter(streamgenerator, *match):
    for BUFFER in streamgenerator:
        if BUFFER[1] in match:
            yield BUFFER
        
def diffpacketfilter(listgenerator):
    duplicates = {}
    for packet in listgenerator:
        if packet != duplicates.get(packet[1]):
            yield packet
        duplicates[packet[1]] = packet
import machine, utime
led = machine.Pin(25, machine.Pin.OUT)

#init pins
rs = machine.Pin(15, machine.Pin.OUT)
readWrite = machine.Pin(16, machine.Pin.OUT)
enable = machine.Pin(17, machine.Pin.OUT)
db0 = machine.Pin(18, machine.Pin.OUT)
db1 = machine.Pin(19, machine.Pin.OUT)
db2 = machine.Pin(20, machine.Pin.OUT)
db3 = machine.Pin(21, machine.Pin.OUT)
db4 = machine.Pin(22, machine.Pin.OUT)
db5 = machine.Pin(26, machine.Pin.OUT)
db6 = machine.Pin(27, machine.Pin.OUT)
db7 = machine.Pin(28, machine.Pin.OUT)

# prepare to write data
def SetData(data) :
    db0.value(data & 0x1);
    db1.value((data & 0x2) >> 1);
    db2.value((data & 0x4) >> 2);
    db3.value((data & 0x8) >> 3);
    db4.value((data & 0x10) >> 4);
    db5.value((data & 0x20) >> 5);
    db6.value((data & 0x40) >> 6);
    db7.value((data & 0x80) >> 7);

# set pin mode
def SetPinStatus(mode) :
    db0.init(mode)
    db1.init(mode)
    db2.init(mode)
    db3.init(mode)
    db4.init(mode)
    db5.init(mode)
    db6.init(mode)
    db7.init(mode)

def ExecFunc(funcParam) :
    SetPinStatus(machine.Pin.OUT)
    rs.value(0)
    utime.sleep(0.005)
    enable.value(1)
    readWrite.value(0)
    SetData(funcParam)
    enable.value(0)
    utime.sleep(0.005)

def WriteData(data) :
    SetPinStatus(machine.Pin.OUT)
    rs.value(1)
    utime.sleep(0.005)
    enable.value(1)
    readWrite.value(0)
    SetData(data)
    enable.value(0)
    utime.sleep(0.005)

# lock until busy flag clear
def WaitBusyClear() :
    SetPinStatus(machine.Pin.IN)
    rs.value(0)
    utime.sleep(0.1)
    readWrite.value(1)
    busy = 1;
    while busy == 1:
        enable.value(0)
        utime.sleep(0.005)
        busy = db7.value()
        enable.value(1)
    utime.sleep(0.005)
    enable.value(0)

#init and wait 0.5sec
enable.value(1)
led.value(1)
utime.sleep(0.5)

led.value(0)

#reset unmatch
for i in range(5) :
    WriteData(0x00)

led.value(1)

# function set(JP fontset)
ExecFunc(0x38)

led.value(0)

#check busy
WaitBusyClear()

led.value(1)

# display on
ExecFunc(0x0f)

led.value(0)

#check busy
WaitBusyClear()

led.value(1)

# display clear
ExecFunc(0x01)

led.value(0)

#check busy
WaitBusyClear()

led.value(1)

# return home
ExecFunc(0x02)

led.value(0)

#check busy
WaitBusyClear()

led.value(1)

# entry mode set
ExecFunc(0x06) # Incriment bit, Cursor Move

#check busy
WaitBusyClear()

#cursor shift
ExecFunc(0x14)

#check busy
WaitBusyClear()

ExecFunc(0x17)

#check busy
WaitBusyClear()

led.value(0)

while True:
    ExecFunc(0x01)
    WaitBusyClear()
    ExecFunc(0x02)
    WaitBusyClear()
    for i in range(12) :
        ExecFunc(0x80 + i)
        WaitBusyClear()
        WriteData(0x30 + i)
        WaitBusyClear()
    for i in range(12) :
        ExecFunc(0xc0 + i)
        WaitBusyClear()
        WriteData(0x30 + i)
        WaitBusyClear()
    utime.sleep(1)

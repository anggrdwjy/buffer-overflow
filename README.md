## Buffer Overflow Exploitation

#### Type Buffer Overflow
* Stack-Based Buffer Overflow
* EBP (Extended Base Pointer)
* ESP (Extended Stack Pointer)
* EIP (Extended Instruction Pointer)
* ESI (Extended Source Index)
* EDI (Extended Destination Index)


## Simple Buffer Overflow in C Programming

#### Stack Buffer Overflow
* Save File stack_bufferoverflow.c
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
* Compile
```
gcc stack_bufferoverflow.c
```

* Testing
```
./a.out
```

#### Heap Buffer Overflow
* Save File heap_bufferflow.c
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

* Compile
```
gcc heap_overflow.c
```

* Testing
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

### Perform Spiking

### Perform Fuzzing

### Identify Offset

### Overwrite EIP Register

### Identify Bad Characters

### Generate Shellcode

### Gain Root Access

## Bug

#### Support

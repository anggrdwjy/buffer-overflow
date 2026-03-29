#include<studio.h>
#include<stdlib.h>
#include<string.h>
int buffer(char str[]) {
	char buff[12];
	strcpy(buff, str);
	return 1;
}
int main(int argc, char **argy) {
	buffer("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD");
	printf("After buffer overflow\n");
	return 1;
}

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

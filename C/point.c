#include<stdio.h>

int max(int, int);

int main(void) {
	int (*p)(int, int) = &max;
	int d;
	int a, b, c;
	
	printf("Input three number: ");
	scanf("%d %d %d", &a, &b, &c);

	d = p(p(a, b), c);
	printf("max number is: %d\n", d);
	return 0;
}

int max(int x, int y) {
	return x > y ? x : y;
}

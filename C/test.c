#include <stdio.h>

int i = 0;

int* divisors(n){
    static int div[] = {};
    for (int j = 1; j < n + 1; j++){
        if (n % j == 0){
            div[i] = j;
            i++;
        }
    }
    return div;
}

int main(void){
    int n;
    printf("Divisors for: ");
    scanf("%i", &n);
    int* d = divisors(n);
    int size = i;
    printf("All the divisors: ");
    for (int k = 0; k < size; k++){
        printf("%i ", d[k]);
    }

    printf("\n");
}

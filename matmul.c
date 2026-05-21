#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

#define N 1024

// Allocate matrices globally to avoid stack overflow
float A[N][N];
float B[N][N];
float C[N][N];

int main() {
    // Populate matrices with dummy data
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            A[i][j] = (float)(i + j);
            B[i][j] = (float)(i - j);
            C[i][j] = 0.0f;
        }
    }

    struct timeval start, end;
    gettimeofday(&start, NULL);

    // The core matrix multiplication loop
    for (int i = 0; i < N; i++) {
        for (int k = 0; k < N; k++) {
            for (int j = 0; j < N; j++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    gettimeofday(&end, NULL);
    
    double time_taken = (end.tv_sec - start.tv_sec) + (end.tv_usec - start.tv_usec) * 1e-6;
    printf("Execution Time: %f seconds\n", time_taken);

    return 0;
}
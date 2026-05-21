#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

// Allocate 400 MB of RAM (100 million 4-byte integers)
#define ARRAY_SIZE 100000000 

int main() {
    int *data = malloc(ARRAY_SIZE * sizeof(int));
    if (data == NULL) {
        printf("Memory allocation failed!\n");
        return 1;
    }

    struct timeval start, end;

    // Start the stopwatch
    gettimeofday(&start, NULL);

    // Spam the RAM with write requests
    for (int i = 0; i < ARRAY_SIZE; i++) {
        data[i] = i;
    }

    // Stop the stopwatch
    gettimeofday(&end, NULL);

    // Calculate time elapsed
    double time_taken = (end.tv_sec - start.tv_sec) * 1e6;
    time_taken = (time_taken + (end.tv_usec - start.tv_usec)) * 1e-6;

    // Calculate Bandwidth in GB/s (400MB / time)
    double bytes_moved = ARRAY_SIZE * sizeof(int);
    double gb_per_sec = (bytes_moved / time_taken) / 1e9;

    printf("Time taken: %f seconds\n", time_taken);
    printf("Memory Bandwidth: %f GB/s\n", gb_per_sec);

    free(data);
    return 0;
}
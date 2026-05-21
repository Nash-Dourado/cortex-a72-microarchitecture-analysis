#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <arm_neon.h>

#define N 1024
#define BLOCK_SIZE 64 // Tuned for Cortex-A72 Cache

// Align memory to 16 bytes for optimal NEON vector loading
float A[N][N] __attribute__((aligned(16)));
float B[N][N] __attribute__((aligned(16)));
float C[N][N] __attribute__((aligned(16)));

int main() {
    // Populate matrices
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            A[i][j] = (float)(i + j);
            B[i][j] = (float)(i - j);
            C[i][j] = 0.0f;
        }
    }

    struct timeval start, end;
    gettimeofday(&start, NULL);

    // Stage 1: Loop Tiling (Cache Blocking)
    for (int i = 0; i < N; i += BLOCK_SIZE) {
        for (int k = 0; k < N; k += BLOCK_SIZE) {
            for (int j = 0; j < N; j += BLOCK_SIZE) {
                
                // Inner Block Execution
                for (int ii = i; ii < i + BLOCK_SIZE; ii++) {
                    for (int kk = k; kk < k + BLOCK_SIZE; kk++) {
                        
                        // Load a single scalar from A and duplicate it across a NEON vector
                        float32x4_t a_vec = vdupq_n_f32(A[ii][kk]);
                        
                        // Stage 2: NEON SIMD Vectorization (Unrolling by 4)
                        for (int jj = j; jj < j + BLOCK_SIZE; jj += 4) {
                            // Load 4 floats from B and C
                            float32x4_t b_vec = vld1q_f32(&B[kk][jj]);
                            float32x4_t c_vec = vld1q_f32(&C[ii][jj]);
                            
                            // Fused Multiply-Add: C = C + (A * B)
                            c_vec = vmlaq_f32(c_vec, a_vec, b_vec);
                            
                            // Store the 4 floats back into C
                            vst1q_f32(&C[ii][jj], c_vec);
                        }
                    }
                }
            }
        }
    }

    gettimeofday(&end, NULL);
    
    double time_taken = (end.tv_sec - start.tv_sec) + (end.tv_usec - start.tv_usec) * 1e-6;
    printf("Optimized Execution Time: %f seconds\n", time_taken);

    return 0;
}
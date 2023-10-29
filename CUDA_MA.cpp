#include <iostream>
#include <cmath>
#include <cuda_runtime.h>

__global__ void movingAverage(float* data, float* output, int size, int period) {
    int tid = threadIdx.x + blockIdx.x * blockDim.x;
    float sum = 0.0f;

    if (tid >= period - 1) {
        for (int i = tid - (period - 1); i <= tid; i++) {
            sum += data[i];
        }
        output[tid] = sum / period;
    }
}

int main() {
    const int size = 10;
    const int period = 3;

    float data[size] = {10.0f, 20.0f, 30.0f, 40.0f, 50.0f, 60.0f, 70.0f, 80.0f, 90.0f, 100.0f};
    float movingAverages[size];

    float* d_data;
    float* d_movingAverages;

    cudaMalloc((void**)&d_data, size * sizeof(float));
    cudaMalloc((void**)&d_movingAverages, size * sizeof(float));

    cudaMemcpy(d_data, data, size * sizeof(float), cudaMemcpyHostToDevice);

    // Define the number of blocks and threads per block
    int threadsPerBlock = 256;
    int blocksPerGrid = (size + threadsPerBlock - 1) / threadsPerBlock;

    movingAverage<<<blocksPerGrid, threadsPerBlock>>>(d_data, d_movingAverages, size, period);

    cudaMemcpy(movingAverages, d_movingAverages, size * sizeof(float), cudaMemcpyDeviceToHost);

    for (int i = 0; i < size; i++) {
        std::cout << "Moving Average for Element " << i << ": " << movingAverages[i] << std::endl;
    }

    cudaFree(d_data);
    cudaFree(d_movingAverages);

    return 0;
}

import numpy as np

# solves Y = Z * B, where Y are the prices and Z is a sparse time matrix
def calc(prices, times):
    #print times
    times_t = times.transpose()
    #print times_t
    times_product = np.dot(times_t, times)
    #print times_product
    times_product_inverse = np.linalg.inv(times_product)
    #print times_product_inverse
    time_res = np.dot(times_product_inverse, times_t)
    return np.exp(np.dot(time_res, prices))

def main():
    prices = np.array([[np.log(1.05)], [np.log(1.1)]])
    times = np.array([[1], [1]])
    print calc(prices, times)

if __name__ == "__main__":
    main()

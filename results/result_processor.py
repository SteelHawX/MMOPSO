import statistics as stat
import numpy as np
import matplotlib.pyplot as plt

def get_stats():
    fnc_num_range = ['1', '2', '3', '4', '5']
    fnc_dim_range = ['10', '30']
    pso_types = ['', '_basic']

    for fnc_num in fnc_num_range:
        for fnc_dim in fnc_dim_range:
            for type in pso_types:
                filename = 'test_f_0' + fnc_num + '_d' + fnc_dim + type + '.txt'
                with open(filename) as f:
                    lines = f.readlines()
                    raw_line = lines[-1]
                    strings = raw_line.split(' ')
                    numbers = [float(i) for i in strings]
                    numbers.sort()
                    # numbers = []
                    # for s in strings:
                    #    numbers.append(float(s))
                    with open("results_" + filename, 'w') as res:
                        res.write(f'Best is: {numbers[0]}\n')
                        res.write(f'Worst is: {numbers[-1]}\n')
                        res.write(f'Mean is: {stat.mean(numbers)}\n')
                        res.write(f'Median is: {stat.median(numbers)}\n')
                        res.write(f'Standard deviation is: {stat.stdev(numbers)}')

if __name__ == '__main__':
    fnc_num_range = ['1', '2', '3', '4', '5']
    fnc_dim_range = ['10', '30']
    pso_types = ['', '_basic']
    x = [0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    for fnc_num in fnc_num_range:
        for fnc_dim in fnc_dim_range:
            for type in pso_types:
                filename = 'test_f_0' + fnc_num + '_d' + fnc_dim + type + '.txt'
    #x_label = ['0.01','0.02','0.03','0.04','0.05', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9','1']
                #filename = 'test_f_01_d10.txt'
                with open(filename) as f:
                    lines = f.readlines()
                    raw_line = lines[-1]
                    strings = raw_line.split(' ')
                    numbers = [float(i) for i in strings]
                    data_set = np.empty((10, 14))
                    iteration_num = 0
                    test_num = 0
                    for result in numbers:
                        data_set[test_num][iteration_num] = result
                        iteration_num += 1
                        if iteration_num == 14:
                            iteration_num = 0
                            test_num += 1
                            if test_num == 10:
                                break
                    for i in range(10):
                        #plt.axhline(data_set[i][0], color='gray', lw=0.5)
                        plt.plot(x, data_set[i])
                    plt.yscale("log")
                    plt.show()






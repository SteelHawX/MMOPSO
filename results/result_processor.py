import statistics as stat

if __name__ == '__main__':
    fnc_num_range = ['1', '2', '3', '4', '5']
    fnc_dim_range = ['10', '30']
    pso_types = ['', '_basic']

    for fnc_num in fnc_num_range:
        for fnc_dim in fnc_dim_range:
            for type in pso_types:
                filename = 'test_f_0'+fnc_num+'_d'+fnc_dim+type+'.txt'
                with open(filename) as f:
                    lines = f.readlines()
                    raw_line = lines[-1]
                    strings = raw_line.split(' ')
                    numbers = [float(i) for i in strings]
                    numbers.sort()
                    #numbers = []
                    #for s in strings:
                    #    numbers.append(float(s))
                    with open("results_"+filename, 'w') as res:
                        res.write(f'Best is: {numbers[0]}\n')
                        res.write(f'Worst is: {numbers[-1]}\n')
                        res.write(f'Mean is: {stat.mean(numbers)}\n')
                        res.write(f'Median is: {stat.median(numbers)}\n')
                        res.write(f'Standard deviation is: {stat.stdev(numbers)}')




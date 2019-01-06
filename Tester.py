import TestFunctions as tf
import MMOPSONumPyV2 as mpso
import BasicSwarmV2 as bpso

if __name__ == '__main__':
    # pso = mpso.MMOpso(tf.test01_D10, 10, -100, 100)
    # for it in range(100000):
    #     pso.next_iteration()
    # print("MMOpso:")
    # print(pso.best_found_log[-1])
    # pso2 = bpso.BasicPSO(tf.test01_D10, 10, -100, 100)
    # for it in range(100000):
    #     pso2.next_iteration()
    # print("Basicpso:")
    # print(pso2.best_found_log[-1])
    f = open("test1_to_5_final.txt", "w+")
    print('Testing function 01:')
    results = list()
    for n in range(10):
        print(n)
        pso = mpso.MMOpso(tf.test01_D10, 10, -100, 100)
        for it in range(100000):
            pso.next_iteration()
        results.append(str(pso.best_found[-1]))
    f.write(' '.join(results))
    f.write('\n')
    print('Testing function 02:')
    results = list()
    for n in range(10):
        print(n)
        pso = mpso.MMOpso(tf.test02_D10, 10, -100, 100)
        for it in range(100000):
            pso.next_iteration()
        results.append(str(pso.best_found[-1]))
    f.write(' '.join(results))
    f.write('\n')
    print('Testing function 03:')
    results = list()
    for n in range(10):
        print(n)
        pso = mpso.MMOpso(tf.test03_D10, 10, -100, 100)
        for it in range(100000):
            pso.next_iteration()
        results.append(str(pso.best_found[-1]))
    f.write(' '.join(results))
    f.write('\n')
    print('Testing function 04:')
    results = list()
    for n in range(10):
        print(n)
        pso = mpso.MMOpso(tf.test04_D10, 10, -100, 100)
        for it in range(100000):
            pso.next_iteration()
        results.append(str(pso.best_found[-1]))
    f.write(' '.join(results))
    f.write('\n')
    print('Testing function 05:')
    results = list()
    for n in range(10):
        print(n)
        pso = mpso.MMOpso(tf.test05_D10, 10, -100, 100)
        for it in range(100000):
            pso.next_iteration()
        results.append(str(pso.best_found[-1]))
    f.write(' '.join(results))
    f.write('\n')
    f.close()
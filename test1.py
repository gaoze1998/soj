import multiprocessing


def target():
    s = input("")
    print(s)


p = multiprocessing.Process(target=target)
p.start()
p.join()

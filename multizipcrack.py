import zipfile
from multiprocessing import Pool, Manager
from functools import partial
from sys import argv, exit

def runner(event, zipf, endword, password):
    if event.is_set():
        return
    password = password.strip('\n')
    try:
        zipf.extractall(pwd=password)
        print('Password found: {}'.format(password))
        event.set()
    except:
        pass
    if password == endword:
        event.set()

def crack_zip(zipf_name, wordlist, processes=15):
    zipf = zipfile.ZipFile(zipf_name)
    pool = Pool(processes)
    mgr = Manager()
    event = mgr.Event()
    with open(wordlist) as f:
        wordlist = f.readlines()
    endword = wordlist[-1].strip('\n')
    part = partial(runner, event, zipf, endword)
    pool.map_async(part, wordlist)
    print("Cracking...")
    event.wait()
    print("Shutting down workers")
    pool.terminate()
    return 0

if __name__ == '__main__':
    if len(argv) == 3:
        exit(crack_zip(argv[1], argv[2]))
    elif len(argv) == 4:
        exit(crack_zip(argv[1], argv[2], int(argv[3])))
    else:
        print("Usage: {} zipfile wordlist [num processes]".format(argv[0]))

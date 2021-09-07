from disk_manager import DiskManager
from challenge import Challenge
from shutil import copyfile

copyfile('original_100000.d', 'dataset_100000.d')
dm = DiskManager()

try:
    app = Challenge(dm)

    events_and_queries = [
        "1 1 210",
        "0 1 10001 hamed 1618497229",
        "0 2 21 1 1618497229",
        "1 2 210 1618497229",
        "0 4 210 120 0",
        "0 3 210 120 0"
    ]

    # events_and_queries = [
    #     "0 1 10001 marmof 1618497229",
    #     "0 4 10001 1 1",
    #     "0 4 10001 2 1",
    #     "0 4 10001 3 1",
    #     "1 1 550",
    #     "1 2 1 1618497229"
    # ]

    app.run(events_and_queries)

    print(dm.cost, end='')
finally:
    # dm.de_shuffle()
    pass

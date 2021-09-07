class BlockManager:
    def __init__(self, challenge):
        self.challenge = challenge

    def get_user_block(self, uid):
        self.disk_seek(uid)
        users = self.challenge.dm.read_block(self.challenge.main_disk)

        for user in users:
            data = user.split(' ')
            user_id = int(data[0])
            name = data[1]
            number_of_friends = int(data[2])
            friends = [int(uid) for uid in data[3:number_of_friends + 3]]
            status = data[number_of_friends + 3]
            last_seen = int(data[number_of_friends + 4])
            self.challenge.network.set_user_from_dataset(uid, user_id, name, friends, status, last_seen)

    def set_user_block(self, uid, user):
        self.disk_seek(uid)
        self.challenge.dm.write_block(self.challenge.main_disk, [user])

    def disk_seek(self, uid):
        cursor = int(self.challenge.dm.disks[self.challenge.main_disk]['cursor'] / self.challenge.dm.ENTRY_LENGTH)
        delta = uid - cursor - 1
        self.challenge.dm.disk_seek(self.challenge.main_disk, delta)

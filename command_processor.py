class CommandProcessor:
    # Events
    EVENT = 0
    NEW_USER = 1
    ONLINE_OFFLINE = 2
    OFFLINE = 0
    ONLINE = 1
    BLOCK_UNBLOCK = 3
    UNBLOCK = 0
    BLOCK = 1
    FOLLOW_UNFOLLOW = 4
    UNFOLLOW = 0
    FOLLOW = 1
    # Queries
    QUERY = 1
    ONLINE_FRIENDS = 1
    FOLLOW_RECOMMENDATION = 2

    def __init__(self, network):
        self.network = network

    def process(self, command):
        data = command.split(' ')
        command_type = int(data[0])
        command_subtype = int(data[1])

        if command_type == self.EVENT:
            if command_subtype == self.NEW_USER:
                uid = int(data[2])
                name = data[3]
                last_seen = int(data[4])
                self.network.new_user(uid, name, last_seen)
            elif command_subtype == self.ONLINE_OFFLINE:
                uid = int(data[2])
                action_type = int(data[3])
                last_seen = int(data[4])
                if action_type == self.OFFLINE:
                    self.network.user_offline(uid, last_seen)
                elif action_type == self.ONLINE:
                    self.network.user_online(uid)
            elif command_subtype == self.BLOCK_UNBLOCK:
                uid1 = int(data[2])
                uid2 = int(data[3])
                action_type = int(data[4])
                if action_type == self.UNBLOCK:
                    self.network.unblock_user(uid1, uid2)
                elif action_type == self.BLOCK:
                    self.network.block_user(uid1, uid2)
            elif command_subtype == self.FOLLOW_UNFOLLOW:
                uid1 = int(data[2])
                uid2 = int(data[3])
                action_type = int(data[4])
                if action_type == self.UNFOLLOW:
                    self.network.unfollow_user(uid1, uid2)
                elif action_type == self.FOLLOW:
                    self.network.follow_user(uid1, uid2)
        elif command_type == self.QUERY:
            if command_subtype == self.ONLINE_FRIENDS:
                uid = int(data[2])
                ids = self.network.get_online_friends(uid)
                for uid in ids:
                    print(uid, end=" ")
                print()
            elif command_subtype == self.FOLLOW_RECOMMENDATION:
                uid = int(data[2])
                time = int(data[3])
                recommendations = self.network.get_follow_recommendation(uid, time)
                for uid in recommendations:
                    print(uid, end=" ")
                print()

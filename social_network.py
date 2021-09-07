from datetime import datetime
import heapq

"""
Status:
0: offline
1: online
"""


# A class to represent the user node
class User:
    OFFLINE = 0
    ONLINE = 1

    def __init__(self, uid, name, status, last_seen):
        self.uid = uid
        self.name = name
        self.status = status
        self.last_seen = last_seen
        self.followings = []
        self.blocks = []
        self.recommendations = []
        self.last_recommendation = 0
        self.value = 0
        self.modified = False

    def __str__(self):
        value = str(self.uid) + " " + self.name + " " + str(len(self.followings))
        for uid in self.followings:
            value += " " + str(uid)
        value += " online " if self.status == self.ONLINE else " offline "
        value += str(self.last_seen)

        return value

    def __repr__(self):
        return str(self.uid)

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value


class SocialNetwork:
    MAX_USER = 200
    FRIENDS_FRIEND_RECOMMENDATION = 10
    FOLLOWER_RECOMMENDATION = 10

    def __init__(self, block_manager):
        self.cache = []
        self.users = dict()
        self.block_manager = block_manager

    def set_user_from_dataset(self, request_uid, uid, name, friends, status, last_seen):
        user = User(uid, name, User.ONLINE if status == 'online' else User.OFFLINE, last_seen)
        user.value = len(friends)
        for friend in friends:
            user.followings.append(friend)

        if uid not in self.users:
            if len(self.cache) < self.MAX_USER:
                heapq.heappush(self.cache, user)
                self.users[uid] = user
            else:
                if uid == request_uid:
                    to_remove = heapq.heapreplace(self.cache, user)
                else:
                    to_remove = heapq.heappushpop(self.cache, user)
                    if to_remove.uid == request_uid:
                        to_remove = heapq.heapreplace(self.cache, to_remove)
                self.users[uid] = user
                self.users.pop(to_remove.uid)
                if to_remove.modified:
                    self.block_manager.set_user_block(to_remove.uid, str(to_remove))

    def new_user(self, uid, name, last_seen):
        user = User(uid, name, User.ONLINE, last_seen)
        if len(self.cache) < self.MAX_USER:
            self.users[uid] = user
            heapq.heappush(self.cache, user)
        else:
            self.block_manager.set_user_block(uid, str(user))

    def user_online(self, uid):
        user = self.get_user(uid)
        user.status = User.ONLINE
        user.modified = True

    def user_offline(self, uid, last_seen):
        user = self.get_user(uid)
        user.status = User.OFFLINE
        user.last_seen = last_seen
        user.modified = True

    def block_user(self, uid1, uid2):
        user1 = self.get_user(uid1)
        user1.blocks.append(uid2)
        user1.modified = True
        if uid2 in user1.followings:
            user1.followings.remove(uid2)
        user2 = self.get_user(uid2)
        if uid1 in user2.followings:
            user2.followings.remove(uid1)
            user2.modified = True

    def unblock_user(self, uid1, uid2):
        user = self.get_user(uid1)
        if uid2 in user.blocks:
            user.blocks.remove(uid2)
            user.modified = True

    def follow_user(self, uid1, uid2):
        user1 = self.get_user(uid1)
        user2 = self.get_user(uid2)
        if uid2 in user1.blocks or uid1 in user2.blocks:
            return
        user1.followings.append(uid2)

        if uid2 in user1.recommendations:
            user1.recommendations.remove(uid2)
        # todo: add follower
        user1.modified = True

    def unfollow_user(self, uid1, uid2):
        user = self.get_user(uid1)
        if uid2 in user.followings:
            user.followings.remove(uid2)
            user.modified = True

    def get_online_friends(self, uid):
        ids = []
        user = self.get_user(uid)
        for friend_uid in user.followings:
            friend = self.get_user(friend_uid)
            if friend.status == User.ONLINE:
                ids.append(friend_uid)
        return ids

    def get_follow_recommendation(self, uid, time):
        user = self.get_user(uid)
        new_recommendation = []

        done = False
        for friend_uid in user.followings:
            friend = self.get_user(friend_uid)
            for friend_friend_uid in friend.followings:
                if len(new_recommendation) == self.FRIENDS_FRIEND_RECOMMENDATION:
                    done = True
                    break
                else:
                    if friend_friend_uid not in user.followings and friend_friend_uid not in user.recommendations:
                        new_recommendation.append(friend_friend_uid)
            if done:
                break

        for user_id in self.users:
            a_user = self.users[user_id]
            if uid in a_user.followings:
                if len(new_recommendation) == self.FOLLOWER_RECOMMENDATION + self.FRIENDS_FRIEND_RECOMMENDATION:
                    break
                else:
                    if user_id not in user.followings and user_id not in user.recommendations:
                        new_recommendation.append(user_id)
        # todo: celebrities
        # todo: followers

        elapsed = datetime.fromtimestamp(time) - datetime.fromtimestamp(user.last_recommendation)
        user.last_recommendation = time
        if elapsed.days <= 10:
            new_recommendation.extend(user.recommendations)

        user.recommendations.clear()
        user.recommendations.extend(new_recommendation)
        return user.recommendations[0:20]

    def get_user(self, uid):
        if uid not in self.users:
            self.block_manager.get_user_block(uid)
        user = self.users[uid]

        user.value += 1
        heapq.heapify(self.cache)

        return user

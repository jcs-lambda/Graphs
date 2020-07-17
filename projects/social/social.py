from queue import SimpleQueue
from random import choice
from names import get_full_name

class User:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        self._add_friend_calls = 0

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
            self._add_friend_calls += 1

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for _ in range(num_users):
            self.add_user(get_full_name())

        # Create friendships
        for _ in range(num_users * avg_friendships // 2):
            # random user
            uid = choice(list(self.users))

            # make potential friends list from users,
            # removing self and any current friends
            potential_friends = set(self.users)
            potential_friends.remove(uid)
            for friend in self.friendships[uid]:
                potential_friends.remove(friend)

            # add random new friend
            friend = choice(list(potential_friends))
            self.add_friendship(uid, friend)

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        
        queue = SimpleQueue()
        # for fid in self.friendships[user_id]:
        #     queue.put([user_id, fid])
        queue.put([user_id])
        while not queue.empty():
            path = queue.get()
            uid = path[-1]
            if uid not in visited:
                visited[uid] = path

            for fid in self.friendships[uid]:
                if fid not in visited and fid != user_id:
                    queue.put(path + [fid])
        
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(1000, 5)
    print(sg.friendships)
    user = 1
    connections = sg.get_all_social_paths(user)
    print(connections)
    print(sg._add_friend_calls)
    print(f'{(len(connections) - 1) / sg.last_id * 100:.2f}%')

    # for x in sorted(connections):
    #     print(x, connections[x])
    n = [len(v) for k,v in connections.items() if k != user]
    print(sum(n) / len(n))

import re


class HashTable():
    def __init__(self) -> None:
        self.n = 1023
        self.__buckets = [[] for _ in range(self.n)]

    def search(self, key):
        keyhash = self.__hash(key) % len(self.__buckets)
        bucket = self.__buckets[keyhash]

        for kv_pair in bucket:
            k, v, = kv_pair
            if key == k:
                return v

        return None

    def insert(self, key, value):
        keyhash = self.__hash(key) % len(self.__buckets)
        bucket = self.__buckets[keyhash]

        for kv_pair in bucket:
            k, v, = kv_pair
            if key == k:
                kv_pair = (k, value)
                return

        bucket.append((key, value))

    def __hash(self, key):
        p = 51
        p_pow = 1
        hash_value = 0

        for c in key:
            hash_value = (hash_value + ord(c) - ord('a') * p_pow) % self.n
            p_pow = (p_pow * p) % self.n

        return hash_value

    def __str__(self):
        s = ''
        for bucket in self.__buckets:
            for elem in bucket:
                k, v = elem
                s += str(k) + ': ' + str(v) + '\n'

        return s

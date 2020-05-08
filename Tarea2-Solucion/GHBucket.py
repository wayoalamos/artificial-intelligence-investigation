class Bucket:
    def __init__(self, g, h):
        self.g = g
        self.h = h
        self.hash = hash(tuple((g, h)))
        self.list = []

    def __hash__(self):
        return self.hash

    def push(self, node):
        self.list.append(node)
        node.bucket_index = len(self.list-1)

    def pop(self, index=-1):
        node = self.list.pop(index)
        node.bucket_index = -1

    def is_empty(self):
        return len(self.list) == 0

class GHBucketQueue:
    def __init__(self, weight):
        self.fmin = 0
        self.weight = weight
        self.gh_sorted_buckets = []  # contiene los buckets existentes ordenados por g+h
        self.potential_sorted_buckets = []  # contiene los buckets existentes ordenados por la función potencial
        self.buckets = set()  # conjunto de buckets usado para acceder rápidamente a un (g,h)-bucket

    def potential(self, something):
        return (self.fmin * self.weight - something.g)/something.h

    def _reorder_buckets(self):
        self.potential_sorted_buckets.sort(lambda x: (self.fmin - x.g)/x.h)

    def insert(self, node):
        '''
            Inserta a node en la cola de prioridades. Si node ya está en la cola supone que
            está cambiando de prioridad y lo ubica en el bucket correspondiente
        '''
        def insert_gh():
            for i in range(0, len(self.gh_sorted_buckets)):
                if node.g + node.h <= self.gh_sorted_buckets[i].g + self.gh_sorted_buckets[i].h:
                    self.gh_sorted_buckets.insert(i, bucket)
                    break

        def insert_potential():
            for i in range(0, len(self.gh_sorted_buckets)):
                if self.potential(node) <= self.potential(self.gh_sorted_buckets[i]):
                    self.potential_sorted_buckets.insert(i, bucket)
                    break

        if node.bucket_index == -1:
            # el nodo no existe en un bucket
            bucket = self.buckets.get(tuple(node.g, node.h))
            if self.buckets.get(tuple(node.g, node.h)) is None:
                bucket = Bucket(node.g, node.h)
                insert_gh()
                insert_potential()
                if self.fmin > node.g + node.h:
                    self.fmin = node.g + node.h
                    self._reorder_buckets()

            bucket.push(node)
        else:



    def

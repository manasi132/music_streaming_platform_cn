class Buffer:
    def __init__(self, filename):
        self.file = open(filename, "wb")
        self.total_bytes = 0

    def add_chunk(self, data):
        self.file.write(data)
        self.total_bytes += len(data)

    def close(self):
        self.file.close()

    def get_total_bytes(self):
        return self.total_bytes


class Utils():
    #　場コードの多重リストを解消
    @staticmethod
    def flatten_2d(data):
        for block in data:
            for elem in block:
                yield elem

class Utils():
    
    def flatten_2d(data):
        for block in data:
            for elem in block:
                yield elem


            
    def atoi(text):
        return int(text) if text.isdigit() else text

    def natural_keys(text):
        return [ atoi(c) for c in re.split(r'(\d+)', text) ]

#     sorted(l, key=natural_keys)























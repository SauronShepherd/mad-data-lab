from hashlib import sha256

class StableRng:
    def __init__(self, case_id, template_version, generator_version, seed):
        self.prefix = f"{case_id}|{template_version}|{generator_version}|{seed}|"
    def bytes(self, namespace, counter=0):
        return sha256(f"{self.prefix}{namespace}|{counter}".encode()).digest()
    def choice(self, namespace, values, counter=0):
        return values[int.from_bytes(self.bytes(namespace, counter), 'big') % len(values)]

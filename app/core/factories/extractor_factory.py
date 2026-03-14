
class ExtractorFactory():

    @classmethod
    def register(cls, name: str, subclass):
        cls._registry[name] = subclass

    def create(self, name: str):
        subclass = self._registry.get(name)
        if not subclass:
            raise ValueError(f"Unknown component: {name}")
        return subclass()

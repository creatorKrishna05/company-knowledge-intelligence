class LoaderRegistry:

    def __init__(self):
        self._loaders = {}

    def register(self, extension, loader):
        extension = extension.strip().lower()

        if extension in self._loaders:
            raise ValueError(f"Loader already registered for: {extension}")
        
        self._loaders[extension] = loader

    def get_loader(self, extension):
        extension = extension.strip().lower()
        return self._loaders.get(extension)
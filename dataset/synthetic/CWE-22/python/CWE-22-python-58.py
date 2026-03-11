import os


class TemplateRegistry:

    def __init__(self, config):
        self.config = config

    def resolve(self, template_id):
        root = self.config["views"]
        location = os.path.join(root, template_id)

        with open(location, "r", encoding="utf-8") as fh:
            return fh.read()


class TemplateService:

    def __init__(self, registry):
        self.registry = registry

    def render(self, name):
        return self.registry.resolve(name)


def start():
    cfg = {"views": os.path.join(os.getcwd(), "views")}
    service = TemplateService(TemplateRegistry(cfg))

    name = input("template id: ").strip()
    content = service.render(name)

    print(content[:60])


if __name__ == "__main__":
    start()
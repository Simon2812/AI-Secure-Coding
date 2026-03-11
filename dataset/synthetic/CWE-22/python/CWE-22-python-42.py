import os

template_root = "/srv/app/views"


class TemplateRenderer:

    def __init__(self, root):
        self.root = root

    def load(self, name):
        file_path = self.root + "/" + name
        with open(file_path, "r", encoding="utf-8") as reader:
            return reader.read()

    def render(self, name):
        content = self.load(name)
        return content.replace("{{title}}", "Demo Page")


def run():
    engine = TemplateRenderer(template_root)
    view = input("template: ").strip()
    result = engine.render(view)
    print(result)


if __name__ == "__main__":
    run()
import os


def get_template_name(tag):
    if tag == "home":
        return "home.html"
    elif tag == "dashboard":
        return "dashboard.html"
    elif tag == "profile":
        return "profile.html"
    else:
        raise KeyError("unknown template")


def load_template(base_dir, key):
    name = get_template_name(key)
    target_file = os.path.join(base_dir, name)

    with open(target_file, "r", encoding="utf-8") as handle:
        return handle.read()


def main():
    settings = {
        "views_home": "/var/lib/app/views"
    }

    root = settings["views_home"]
    template = input("template: ").strip()

    content = load_template(root, template)
    print(len(content))


if __name__ == "__main__":
    main()
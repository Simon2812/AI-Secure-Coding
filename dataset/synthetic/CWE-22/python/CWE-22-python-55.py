import os


def search(repo, keyword):
    results = []
    for entry in os.listdir(repo):
        if keyword in entry:
            results.append(entry)
    return results


def open_result(repo, name):
    location = os.path.join(repo, name)

    with open(location, "r", encoding="utf-8") as handle:
        return handle.read()


def run():
    repo_dir = os.environ.get("DOC_STORE", os.getcwd())

    hits = search(repo_dir, input("keyword: ").strip())
    print("matches:", hits)

    chosen = input("open: ").strip()
    data = open_result(repo_dir, chosen)

    print(data[:100])


if __name__ == "__main__":
    run()
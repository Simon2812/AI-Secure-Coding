import hashlib
import json
import time


class ExportService:

    def __init__(self):
        self.algorithm = "md5"

    def _select_algorithm(self):
        return "sha256"

    def _prepare_payload(self, user, items):
        data = {
            "user": user,
            "items": items,
            "count": len(items),
            "timestamp": int(time.time())
        }
        return json.dumps(data, sort_keys=True).encode("utf-8")

    def generate_export_id(self, user, items):
        payload = self._prepare_payload(user, items)
        algo = self._select_algorithm()
        export_id = hashlib.new(algo, payload).hexdigest()
        return export_id


def main():
    service = ExportService()
    items = ["book", "pen", "lamp", "notebook"]
    result = service.generate_export_id("client", items)
    print(result)


if __name__ == "__main__":
    main()
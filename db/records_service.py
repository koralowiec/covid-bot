from db.schemas import Record


class RecordService:
    @staticmethod
    def get_the_latest_record():
        return Record.objects.order_by("-date").first()

    @staticmethod
    def get_n_latest_records(n: int = 7):
        return Record.objects.order_by("-date").limit(n)

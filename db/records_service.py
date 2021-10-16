from db.schemas import Records


class RecordService:
    @staticmethod
    def get_the_latest_record():
        return Records.objects.order_by("-date").first()

    @staticmethod
    def get_n_latest_records(n: int = 7):
        return Records.objects.order_by("-date").limit(n)

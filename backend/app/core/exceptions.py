class DataLoadingError(Exception):
    """Raised when campaign source data cannot be loaded or validated."""


class AdNotFoundError(Exception):
    def __init__(self, ad_id: str) -> None:
        self.ad_id = ad_id
        super().__init__(f"Ad '{ad_id}' was not found")

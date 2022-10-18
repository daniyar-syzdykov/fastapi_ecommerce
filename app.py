from fastapi import FastAPI


class CustomFastAPI(FastAPI):
    def __init__(self, session, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.session = session

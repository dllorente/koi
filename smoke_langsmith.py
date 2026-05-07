import langsmith as ls
from langsmith import traceable
from app.core.config import settings

client = ls.Client(
    api_key=settings.langchain_api_key, api_url=settings.langchain_endpoint
)


@traceable(name="koi_smoke_test", project_name="koi")
def smoke() -> str:
    return "ok"


with ls.tracing_context(
    client=client,
    project_name="koi",
    enabled=True,
):
    print(smoke())

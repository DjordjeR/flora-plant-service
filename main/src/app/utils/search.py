import meilisearch
from meilisearch import client

from ..schema.plant import PlantOut_Pydantic


from app.core.config import settings


def get_client():
    client = meilisearch.Client(
        settings.MEILISEARCH_URL, settings.MEILISEARCH_MASTER_KEY
    )
    return client


def update_or_add_plant(plant: PlantOut_Pydantic):
    doc_dict = plant.dict()
    doc_dict["plant_id"] = "".join(ch for ch in plant.latin_name if ch.isalnum())
    client = get_client()
    index = client.index("plants")
    documents = [doc_dict]
    index.add_documents(documents)


def search(q, opt_params):
    client = get_client()
    index = client.index("plants")
    ret_dict = index.search(q, opt_params=opt_params)
    try:
        for hit in ret_dict["hits"]:
            del hit["plant_id"]
    except Exception:
        pass
    return ret_dict

import pandas as pd
from tqdm import tqdm
import marqo
import colorama
import os
from typing import Dict
import random
import requests
from io import StringIO
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")

marqo.set_log_level("WARN")

NumberOfDocs = os.getenv("N_DOCUMENTS", None)
CLIENT = marqo.Client()
INDEX_NAME = os.getenv("MARQO_INDEX_NAME", None)
REQUEST_CHUNK_SIZE = 16
CLIENT_BATCH_SIZE = 16


def print_banner(message: str) -> None:
    print("Application setup running...")


def _create():
    print("Check docker logs for updates...")
    CLIENT.create_index(
        INDEX_NAME,
        treat_urls_and_pointers_as_images=True,
        model="open_clip/ViT-B-32/laion2b_s34b_b79k",
        normalize_embeddings=True,
    )


def create_index() -> None:
    """
    This function has a lot of extra checks to make it pretty hard to shoot yourself in the foot
    """
    try:
        _create()
        print("Finished creating index...")
    except Exception as e:
        print(colorama.Fore.RED + "Exception occured:" + colorama.Style.RESET_ALL)
        print(e)
        choice = None
        while choice not in {"y", "n"}:
            choice = input(
                "Would you like to reset the index if it exists? (y/n): "
            ).strip()
        if choice == "y":
            try:
                CLIENT.delete_index(INDEX_NAME)
                _create()
                print("Finished creating index...")
            except Exception as e:
                print(
                    colorama.Fore.RED + "Exception occured:" + colorama.Style.RESET_ALL
                )
                print(e)


def get_data() -> Dict[str, str]:
    """
    Fetch the dataset from a local file
    """
    # Update this path to the location where you've saved the CSV file
    local_file_path = "ecommerce_data_clean.csv"
    
    if not os.path.isfile(local_file_path):
        raise FileNotFoundError(f"The file {local_file_path} does not exist. Please download the CSV file and place it in the project directory.")

    data = pd.read_csv(local_file_path)
    data["image"] = data["s3_http"]
    documents = data[["image", "title"]].to_dict(orient="records")
    for i in range(len(documents)):
        documents[i]["_id"] = documents[i]["image"].split("/")[-1]

    random.shuffle(documents)
    print("Data completed.\n")
    if NumberOfDocs is not None:
        documents = documents[: int(NumberOfDocs)]

    return documents


def index_data(documents: Dict[str, str]) -> None:
    print(f"Indexing data with requests of {REQUEST_CHUNK_SIZE} documents....")
    for i in tqdm(range(0, len(documents), REQUEST_CHUNK_SIZE), desc="Indexing data"):
        chunk = documents[i : i + REQUEST_CHUNK_SIZE]

        CLIENT.index(INDEX_NAME).add_documents(
            chunk,
            client_batch_size=CLIENT_BATCH_SIZE,
            mappings={
                "image_title_multimodal": {
                    "type": "multimodal_combination",
                    "weights": {"title": 0.1, "image": 0.9},
                }
            },
            tensor_fields=["image_title_multimodal"],
        )

    print(
        colorama.Fore.GREEN + "\nFinished indexing data!\n" + colorama.Style.RESET_ALL
    )


def setupApp() -> None:
    colorama.init()
    banner = "App Setup"
    print_banner(banner)

    documents = get_data()

    create_index()

    index_data(documents)

    colorama.deinit()

    print("Done.")

if __name__ == "__main__":
    setupApp()

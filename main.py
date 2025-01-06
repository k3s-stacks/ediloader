import os, requests, logging, tempfile
from datetime import datetime
from typing import Dict
import pandas as pd
from google.cloud import secretmanager, storage
from google.api_core.exceptions import GoogleAPICallError

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(name=__name__)

project_id = os.getenv("PROJECT_ID")
edinet_api_key = os.getenv("EDINET_API_KEY")
bucket_name = os.getenv("BUCKET_NAME")

secret_manager_client = secretmanager.SecretManagerServiceClient()
storage_client = storage.Client()


def download_metadata(date: str) -> Dict:
    url = "https://disclosure.edinet-fsa.go.jp/api/v2/documents.json"
    params = {
        "date": date,
        "type": 2,
        "Subscription-Key": edinet_api_key,
    }
    try:
        response = requests.get(url=url, params=params)
        response.raise_for_status()
        data = response.json()
        if "results" not in data:
            raise ValueError(
                "EDINET 書類一覧 API(提出書類一覧及びメタデータ)に'results'が含まれていません。"
            )
        return data["results"]
    except requests.exceptions.RequestException as e:
        logger.error(
            f"EDINET 書類一覧 API(提出書類一覧及びメタデータ)のリクエストに失敗しました: {e}"
        )
        raise


def upload_to_gcs(date: str, source_file_path: str):
    try:
        bucket = storage_client.bucket(bucket_name=bucket_name)
        blob = bucket.blob(blob_name=f"{date}/metadata.csv")
        blob.upload_from_filename(filename=source_file_path)
    except GoogleAPICallError as e:
        logger.error(msg=f"GCSへのアップロードに失敗しました: {e}")
        raise


def main():
    date = datetime.now().strftime("%Y-%m-%d")
    metadata = download_metadata(date=date)
    df = pd.DataFrame(data=metadata)
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=True) as temp_file:
        source_file_path = temp_file.name
        df.to_csv(path_or_buf=source_file_path, encoding="utf-8", index=False)
        upload_to_gcs(date=date, source_file_path=source_file_path)


if __name__ == "__main__":
    main()

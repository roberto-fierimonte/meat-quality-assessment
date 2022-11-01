import opendatasets as od

DATASET_URL = """https://www.kaggle.com/datasets/crowww/meat-quality-assessment-based-on-deep-learning"""
DATA_FOLDER = "data"


def download_data(url: str, directory: str):
    """Download and extract data from a Zip file URL.

    Args:
        url (str): URL of the data to download and extract.
        directory (str): Directory where to extract the file(s).
    """
    od.download(dataset_id_or_url=url, data_dir=directory)


if __name__ == "__main__":
    download_data(DATASET_URL, DATA_FOLDER)

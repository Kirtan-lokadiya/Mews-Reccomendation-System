from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)      # you don't have to give self in a dataclass CLASS
class DataIngestionConfig:
    root_dir: Path
    local_data_file: Path
    unzip_dir: Path


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path_usr: Path
    data_path_news: Path
    col_name: list


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    news: Path
    col_name: list
    model_name: str
    model_content: str
    ind2user: Path
    ind2item: Path
    batch_size: float


@dataclass(frozen=True)
class TrendingAPIConfig:
    training_data: Path
    validation_data: Path
    news_data: Path
    col_name: list
    item2ind_json: Path


@dataclass(frozen=True)
class FullNewsConfig:
    news_data: Path
    col_name: list
    item2ind_json: Path
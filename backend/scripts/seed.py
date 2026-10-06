"""Seed synthetic experiment data (20-30 rows)."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.modules.experiments.models import Experiment

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://app:change_me@localhost:5432/research",
)

DATA = [
    ("BERT baseline on news", "news-kz-10k", "bert-base", "completed", 0.87, 3600),
    ("XGBoost on churn", "churn-5k", "xgboost", "completed", 0.82, 900),
    ("LogReg on reviews", "reviews-ru-20k", "logreg-tfidf", "completed", 0.78, 300),
    ("LSTM sentiment", "reviews-ru-20k", "lstm-128", "completed", 0.84, 5400),
    ("CNN image class", "images-15k", "resnet18", "running", None, None),
    ("Transformer NMT kz-en", "parallel-kz-en-50k", "transformer-small", "running", None, None),
    ("KMeans clustering", "news-kz-10k", "kmeans-20", "completed", 0.61, 600),
    ("RandomForest fraud", "transactions-100k", "random-forest", "completed", 0.93, 1800),
    ("LightGBM CTR", "ads-200k", "lightgbm", "completed", 0.76, 1200),
    ("Whisper speech kz", "speech-kz-8k", "whisper-small", "failed", 0.45, 7200),
    ("MiniLM retrieval", "faq-3k", "minilm-l12", "completed", 0.89, 800),
    ("CatBoost ranking", "search-logs-80k", "catboost", "completed", 0.81, 2100),
    ("Naive Bayes spam", "sms-spam-5k", "naive-bayes", "completed", 0.95, 120),
    ("SVM tickets", "tickets-12k", "svm-linear", "planned", None, None),
    ("Prophet sales", "sales-36m", "prophet", "completed", 0.72, 500),
    ("ARIMA demand", "sales-36m", "arima", "completed", 0.68, 400),
    ("YOLO detection", "cctv-25k", "yolov8n", "running", None, None),
    ("U-Net segmentation", "med-2k", "unet", "planned", None, None),
    ("GPT-4o eval prompts", "prompts-500", "gpt-4o-mini", "completed", 0.91, 700),
    ("DistilBERT distilled", "news-kz-10k", "distilbert", "completed", 0.85, 2200),
    ("TabNet churn v2", "churn-5k", "tabnet", "failed", 0.55, 3000),
    ("Autoencoder anomaly", "transactions-100k", "autoencoder", "completed", 0.79, 2600),
    ("Meta-learning few-shot", "images-15k", "protonet", "planned", None, None),
    ("Linear regression price", "housing-10k", "linear-reg", "completed", 0.74, 200),
]


def main() -> None:
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    with Session() as s:
        if s.query(Experiment).count() > 0:
            print("seed: table not empty, skip")
            return
        for name, dataset, model, status, acc, dur in DATA:
            s.add(
                Experiment(
                    name=name,
                    dataset=dataset,
                    model_name=model,
                    status=status,
                    accuracy=acc,
                    duration_sec=dur,
                    notes=f"Synthetic seed: {model} on {dataset}",
                )
            )
        s.commit()
    print(f"seed: inserted {len(DATA)} experiments")


if __name__ == "__main__":
    main()

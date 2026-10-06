SAMPLE = {
    "name": "BERT baseline on news",
    "dataset": "news-kz-10k",
    "model_name": "bert-base",
    "status": "completed",
    "accuracy": 0.87,
    "duration_sec": 3600,
}


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_create_and_read(client):
    created = client.post("/experiments", json=SAMPLE)
    assert created.status_code == 201, created.text
    exp_id = created.json()["id"]
    response = client.get(f"/experiments/{exp_id}")
    assert response.status_code == 200
    assert response.json()["name"] == SAMPLE["name"]


def test_search_by_two_fields(client):
    client.post("/experiments", json=SAMPLE)
    client.post(
        "/experiments",
        json={**SAMPLE, "name": "XGBoost on churn", "dataset": "churn-5k", "model_name": "xgboost"},
    )
    r1 = client.get("/experiments", params={"q": "xgb"})
    assert [p["model_name"] for p in r1.json()] == ["xgboost"]
    r2 = client.get("/experiments", params={"q": "churn-5k"})
    assert len(r2.json()) == 1


def test_filter_by_status(client):
    client.post("/experiments", json=SAMPLE)
    client.post("/experiments", json={**SAMPLE, "name": "Run 2", "status": "running"})
    res = client.get("/experiments", params={"status": "running"})
    assert all(p["status"] == "running" for p in res.json())
    assert len(res.json()) == 1


def test_pagination_and_sort(client):
    for i in range(3):
        client.post("/experiments", json={**SAMPLE, "name": f"Exp {i}", "accuracy": 0.5 + i * 0.1})
    page1 = client.get(
        "/experiments",
        params={"limit": 2, "offset": 0, "sort_by": "accuracy", "sort_order": "desc"},
    )
    assert len(page1.json()) == 2
    assert page1.json()[0]["accuracy"] >= page1.json()[1]["accuracy"]
    page2 = client.get("/experiments", params={"limit": 2, "offset": 2})
    assert len(page2.json()) == 1


def test_stats(client):
    client.post("/experiments", json=SAMPLE)
    client.post(
        "/experiments", json={**SAMPLE, "name": "Second", "status": "failed", "accuracy": 0.5}
    )
    res = client.get("/experiments/stats")
    assert res.status_code == 200
    body = res.json()
    assert body["total"] == 2
    assert body["by_status"]["completed"] == 1
    assert body["best_accuracy"] == 0.87


def test_update(client):
    exp_id = client.post("/experiments", json=SAMPLE).json()["id"]
    response = client.patch(f"/experiments/{exp_id}", json={"accuracy": 0.91})
    assert response.json()["accuracy"] == 0.91


def test_delete(client):
    exp_id = client.post("/experiments", json=SAMPLE).json()["id"]
    assert client.delete(f"/experiments/{exp_id}").status_code == 204
    assert client.get(f"/experiments/{exp_id}").status_code == 404


def test_validation_error(client):
    response = client.post("/experiments", json={**SAMPLE, "accuracy": 5})
    assert response.status_code == 422
    bad_status = client.post(
        "/experiments", json={**SAMPLE, "name": "Bad status test", "status": "oops"}
    )
    assert bad_status.status_code == 422


def test_404(client):
    assert client.get("/experiments/99999").status_code == 404

import sys
from fastapi.testclient import TestClient
from src.api.main import app

def run_smoke_test():
    print("Running API Smoke Test...")
    client = TestClient(app)
    
    # 1. Health
    res = client.get("/api/v1/health")
    assert res.status_code == 200, "Health endpoint failed"
    print("Health OK")
    
    # 2. Configurations
    res = client.get("/api/v1/configurations")
    assert res.status_code == 200, "Configurations endpoint failed"
    print("Configurations OK")
    
    # 3. Valid Experiment
    payload = {
        "master_seed": 42,
        "demonstration_count": 3,
        "demonstration_complexity": 2,
        "extrapolation_levels": [0, 1, 2, 3],
        "tasks_per_level": 5,
        "evaluator_type": "deterministic"
    }
    res = client.post("/api/v1/experiments", json=payload)
    if res.status_code != 200:
        print(f"Experiment failed: {res.text}")
        sys.exit(1)
        
    data = res.json()
    assert "cliff_detected" in data
    print(f"Experiment OK - Cliff Detected: {data['cliff_detected']}")
    
    # 4. Invalid Request
    bad_payload = payload.copy()
    bad_payload["demonstration_count"] = -1
    res = client.post("/api/v1/experiments", json=bad_payload)
    assert res.status_code == 422, "Failed to reject invalid request"
    print("Invalid Request Rejection OK")
    
    print("API Smoke Test Passed!")

if __name__ == "__main__":
    run_smoke_test()

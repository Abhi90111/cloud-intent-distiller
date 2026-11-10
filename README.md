# Cloud Computing Mini Project (Roll 220103011)

**Student:** V Abhiram  
**Roll Number:** 220103011  
**Email:** dimpuabhiram19@gmail.com  
**Course:** Cloud Computing  

End-to-end knowledge distillation and deployment of an intelligent command parser: an open-weights Phi-3.5 teacher (interfaced via Ollama) provides structured semantic JSON ground truth for complex conversational queries, which is then distilled into a high-efficiency Pythia-70M student model. The resulting lightweight inference engine is packaged into an asynchronous FastAPI container service and deployed within a local k3d Kubernetes cluster, utilizing SeaweedFS S3-compatible object store for decoupled artifact retrieval.

* **GitHub Repository:** https://github.com/vabhiram/neural-command-distiller-k8s  
* **Release Artifacts:** Tag `v1.0`  

---

## 1. Prerequisites
Ensure the host environment is equipped with:
* Docker & Docker daemon running
* k3d and kubectl
* GNU Make and Bash
* Python 3 with `boto3`, `torch`, `transformers`, `fastapi`, and `pydantic` installed (preferably within a virtual environment)
* `curl`, `unzip`, `openssl`

---

## 2. Cluster Deployment & Bootstrapping
Clone and launch the end-to-end environment:
```bash
git clone https://github.com/vabhiram/neural-command-distiller-k8s
cd neural-command-distiller-k8s
make up
```

`make up` orchestrates three automated stages:
1. **Cluster Provisioning**: Creates the `cloudproj` k3d cluster according to `cluster/k3d.yaml`.
2. **Storage Bootstrapping (`scripts/bootstrap.sh`)**: Dynamically configures Kubernetes namespaces (`app`, `data`, `pipeline`), generates secure access credentials into Secrets, deploys SeaweedFS, creates S3 buckets (`datasets` and `models`), uploads command pools, and downloads pre-trained student weights (`model_v1.zip`, `model_v2.zip`).
3. **Application Deployment**: Builds the container image (`command-parser:v1.0`), imports it directly into the k3d nodes, and applies the Deployment, Service, Ingress, and Horizontal Pod Autoscaler (HPA) manifests.

---

## 3. Verification & Testing
Validate inference and system metrics:
```bash
# Test single prediction
curl -s -X POST http://localhost:8080/parse -H 'Content-Type: application/json' -d '{"text":"what is the weather in london"}'

# Run concurrent performance load test (4 users, 2 minutes)
locust -f tools/locustfile.py --headless --users 4 --spawn-rate 4 --run-time 2m --host http://localhost:8080 --csv results/loadtest

# Validate stateless NACL simulation
python tools/nacl_sim.py network/nacl.json network/packets_sample.jsonl --check

# Evaluate model validation metrics
python tools/score.py predictions.jsonl data/validation.jsonl --min-validity 95

# Run unit tests
pytest -q tests
```

---

## 4. Student Training Pipeline
To retrain the Pythia-70M student on cleaned distillation data (random seed `3011`):
```bash
# Full dataset training
make train

# Rapid validation subset training
make train SUBSET=50
```

---

## 5. Teardown
To cleanly remove the cluster and release allocated resources:
```bash
make down
```

---

## 6. Repository Structure
* `cluster/`, `k8s/`: Cluster specifications and manifests (`deployment.yaml`, `service.yaml`, `ingress.yaml`, `hpa.yaml`, `seaweedfs.yaml`).
* `worker/`: Distributed teacher query sharding and dataset cleaning pipeline (`clean.py`).
* `training/`: Fine-tuning harness (`train.py`), configuration (`config.yaml`), and loss logs.
* `service/`, `Dockerfile`: Inference microservice application and container definition.
* `network/`: CIDR subnetting specifications (`subnets.md`) and stateless NACL rules (`nacl.json`).
* `results/`: Performance benchmarks, load testing CSVs, score reports, and recovery logs.
* `.github/workflows/`: Automated CI pipeline (`ci.yml`) including linting, unit testing, quality gate, and secret scanning.
* `data/`: Raw command pool, schema specification, rate card, and gold validation benchmark.
* `scripts/`: Bootstrapping and automation scripts (`bootstrap.sh`).
* `tools/`: Scoring harness (`score.py`), Locust load test (`locustfile.py`), and NACL simulator (`nacl_sim.py`).
* `prompts/`, `AI_USE.md`: Prompt engineering definitions and transparent record of AI tool usage.
* `report/`: Comprehensive technical project report (`report.pdf`).

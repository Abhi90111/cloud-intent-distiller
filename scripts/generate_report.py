"""Comprehensive Report Generator for Cloud Computing Mini Project (Roll 220103011).

Compiles a fully compliant, multi-page technical report formatted cleanly with ReportLab,
structured with exactly one section per task (Task 1 to Task 7) plus AI usage disclosure.
"""

import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

def build_pdf(filename="report/report.pdf", repo_url="https://github.com/vabhiram/neural-command-distiller-k8s"):
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
        title="Cloud Computing Mini Project Report - 220103011",
        author="V Abhiram"
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=2
    )

    meta_style = ParagraphStyle(
        "DocMeta",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1d4ed8"),
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13.5,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "SubSectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.8,
        leading=11.5,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        "BulletText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor("#1e293b"),
        leftIndent=10,
        spaceAfter=2
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=8.8,
        textColor=colors.HexColor("#1e293b")
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.2,
        leading=9.2,
        textColor=colors.white
    )

    story = []

    # Document Header
    story.append(Paragraph("Cloud Computing (CS3081) Mini Project Report", title_style))
    story.append(Paragraph("Distributed Knowledge Distillation & High-Throughput Intent Inference on Kubernetes", ParagraphStyle("Sub", fontName="Helvetica", fontSize=9.5, leading=12, textColor=colors.HexColor("#475569"), spaceAfter=2)))
    story.append(Paragraph(f"Student: V Abhiram | Roll Number: 220103011 | Email: dimpuabhiram19@gmail.com | Repository: {repo_url} | Release Tag: v1.0", meta_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=6))

    # SECTION 1: TASK 1
    story.append(Paragraph("1. Task 1: Object Storage and Parallel Teacher Labelling", h1_style))
    story.append(Paragraph(
        "<b>Cluster Architecture & Persistent Object Storage:</b> A local single-node Kubernetes cluster was instantiated using k3d from <code>cluster/k3d.yaml</code>. Decoupled object storage was realized via SeaweedFS deployed in the <code>data</code> namespace, attached to a 5 GiB PersistentVolumeClaim. The bootstrapping pipeline (<code>scripts/bootstrap.sh</code>) configured required namespaces (<code>app</code>, <code>data</code>, <code>pipeline</code>), generated secure access credentials in Kubernetes Secrets (<code>s3-creds</code>, <code>seaweed-s3</code>), initialized S3 buckets (<code>datasets</code> and <code>models</code>), and uploaded the primary command corpus.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Parallel Teacher Sharding:</b> The 3,000 raw conversational prompts from <code>commands_pool.jsonl</code> were partitioned across parallel worker processes via deterministic modulo hashing: <code>line_number % SHARD_COUNT == SHARD_INDEX</code>. Two parallel batch Jobs (<code>teacher-worker-shard0</code> and <code>teacher-worker-shard1</code>) executed in the <code>pipeline</code> namespace (manifested in <code>k8s/worker-job.yaml</code>, execution logs in <code>results/pipeline_workers.txt</code>). Worker 0 processed 1,500 even queries (outputs in <code>results/teacher/shard-0.jsonl</code>), while Worker 1 processed 1,500 odd queries (outputs in <code>results/teacher/shard-1.jsonl</code>), maintaining zero partition collisions or record loss.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Dataset Cleaning Audit:</b> The dataset cleaning filter (<code>worker/clean.py</code>) screened all 3,000 generated responses against <code>schema.json</code>, removing syntax corruptions, unsupported intent categories, and slot hallucinations.",
        body_style
    ))

    t1_data = [
        [Paragraph(h, table_header_style) for h in ["Dataset Audit Category", "Evaluation Criteria", "Records Filtered", "Action Taken"]],
        [Paragraph("(a) Malformed JSON", table_cell_style), Paragraph("Syntax truncation or missing curly braces", table_cell_style), Paragraph("4", table_cell_style), Paragraph("Rejected", table_cell_style)],
        [Paragraph("(b) Invalid Key Schema", table_cell_style), Paragraph("Keys not strictly {intent, date, time, place}", table_cell_style), Paragraph("7", table_cell_style), Paragraph("Rejected", table_cell_style)],
        [Paragraph("(c) Out-of-Domain Intent", table_cell_style), Paragraph("Intent not in the 8 permitted categories", table_cell_style), Paragraph("0", table_cell_style), Paragraph("Rejected", table_cell_style)],
        [Paragraph("(d) Hallucinated Slots", table_cell_style), Paragraph("Extracted slot span not found verbatim in input query", table_cell_style), Paragraph("81", table_cell_style), Paragraph("Rejected", table_cell_style)],
        [Paragraph("(e) Duplicate Commands", table_cell_style), Paragraph("Repeated queries; lowest command ID retained", table_cell_style), Paragraph("48", table_cell_style), Paragraph("De-duplicated", table_cell_style)],
        [Paragraph("Verified Cleaned Records", table_header_style), Paragraph("Passed all validation filters into train.jsonl", table_header_style), Paragraph("2,860", table_header_style), Paragraph("Preserved", table_header_style)]
    ]
    t_clean = Table(t1_data, colWidths=[110, 240, 80, 110])
    t_clean.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#047857")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.HexColor("#f8fafc"), colors.white])
    ]))
    story.append(t_clean)
    story.append(Paragraph("Audit equation balances exactly: <code>Input (3,000) = 4 + 7 + 0 + 81 + 48 + 2,860 = 3,000</code>. Verified SHA-256 digest recorded in <code>train.sha256</code>.", body_style))

    # SECTION 2: TASK 2
    story.append(Paragraph("2. Task 2: Training the Student (Sequence-Level Knowledge Distillation)", h1_style))
    story.append(Paragraph(
        "<b>Model Training Setup:</b> The Pythia-70M student model was fine-tuned on CPU on the initial 1,500 verified records of <code>train.jsonl</code>. Prompt token masking was applied: <code>Command: {text}\\nJSON:</code> (conditioning prompt tokens masked with -100 to restrict loss calculation solely to predicted JSON target tokens). Hyperparameters in <code>training/config.yaml</code>: seed=3011, lr=0.0001, batch_size=8, epochs=3, max_len=128. Training executed via <code>make train</code> and validated using <code>make train SUBSET=50</code>.",
        body_style
    ))

    t2_data = [
        [Paragraph(h, table_header_style) for h in ["Model Architecture", "JSON Valid", "Intent", "Date", "Time", "Place", "Full Frame"]],
        [Paragraph("Untrained Pythia-70M", table_cell_style), Paragraph("0.0%", table_cell_style), Paragraph("0.0%", table_cell_style), Paragraph("0.0%", table_cell_style), Paragraph("0.0%", table_cell_style), Paragraph("0.0%", table_cell_style), Paragraph("0.0%", table_cell_style)],
        [Paragraph("Teacher (Phi-3.5)", table_cell_style), Paragraph("82.0%", table_cell_style), Paragraph("59.0%", table_cell_style), Paragraph("65.0%", table_cell_style), Paragraph("76.0%", table_cell_style), Paragraph("71.0%", table_cell_style), Paragraph("39.0%", table_cell_style)],
        [Paragraph("Student v1 (Deployed)", table_cell_style), Paragraph("99.0%", table_cell_style), Paragraph("74.0%", table_cell_style), Paragraph("85.0%", table_cell_style), Paragraph("74.0%", table_cell_style), Paragraph("61.0%", table_cell_style), Paragraph("29.0%", table_cell_style)],
        [Paragraph("Student v2 (Greedy)", table_cell_style), Paragraph("98.0%", table_cell_style), Paragraph("68.0%", table_cell_style), Paragraph("90.0%", table_cell_style), Paragraph("98.0%", table_cell_style), Paragraph("65.0%", table_cell_style), Paragraph("35.0%", table_cell_style)]
    ]
    t_eval = Table(t2_data, colWidths=[130, 65, 65, 65, 65, 65, 85])
    t_eval.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white])
    ]))
    story.append(t_eval)

    story.append(Paragraph("<b>Conceptual Distillation Analysis:</b>", h2_style))
    story.append(Paragraph("<b>(a) Sequence-Level Distillation Mechanics:</b> Sequence-level distillation (Kim & Rush, 2016) trains the student on decoded discrete text generated by the teacher model. Decoded teacher predictions function as pseudo ground-truth target tokens, trained using standard autoregressive cross-entropy loss without necessitating soft teacher logit tensors.", bullet_style))
    story.append(Paragraph("<b>(b) Logit-Based Distillation Principles:</b> Logit-based distillation aligns continuous probability distributions by minimizing the Kullback-Leibler (KL) divergence between teacher and student temperature-softened softmax output vectors across the full vocabulary, imparting nuanced structural knowledge regarding unselected tokens.", bullet_style))
    story.append(Paragraph("<b>(c) Vocabulary Incompatibility Constraints:</b> Logit distillation demands an identical vocabulary space. Phi-3.5 operates on a 32,064-token vocabulary, whereas Pythia-70M uses the 50,304-token GPT-NeoX tokenizer. Because their subword tokenization boundaries and token IDs do not align, logit-level distribution comparison is mathematically ill-defined without an ad-hoc projection layer. Furthermore, Ollama only returns discrete decoded strings.", bullet_style))
    story.append(Paragraph("<b>(d) Architectural Limitations:</b> Sequence-level distillation propagates systematic teacher errors: when Phi-3.5 hallucinates non-existent slots (such as the 81 filtered cases), the student accepts them as valid supervision signals. Additionally, Pythia-70M's minimal parameter budget limits generalization across multi-clause voice inputs.", bullet_style))

    # SECTION 3: TASK 3
    story.append(Paragraph("3. Task 3: The Inference Service in a Container", h1_style))
    story.append(Paragraph(
        "<b>Microservice Implementation:</b> The inference application is built using FastAPI (<code>service/app.py</code>) on Uvicorn listening on port 8000. It provides <code>GET /healthz</code> (200 OK while running), <code>GET /readyz</code> (503 Service Unavailable during weight pull/warmup, switching to 200 OK once loaded), and <code>POST /parse</code>. Headers <code>X-Model-Version</code> and <code>X-Served-By</code> accompany every HTTP response. Configuration is strictly environment-driven via <code>MODEL_URI</code>, <code>MODEL_VERSION</code>, <code>S3_ENDPOINT</code>, <code>MAX_NEW_TOKENS</code>, and <code>FAULT_INJECT</code>, pulling weights securely from SeaweedFS S3 via credentials injected from Secret <code>s3-creds</code>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Schema Validation & Fault Handling:</b> Incoming client payloads are parsed via Pydantic <code>CommandRequest</code>, and generated predictions are checked against <code>schema.json</code>. Under <code>FAULT_INJECT=1</code>, synthetic malformed output ('not json') is injected, causing the service to return HTTP 500 with body <code>{\"error\": \"invalid_model_output\"}</code>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Resource Constraints & Peak Memory Profiling:</b> Built on <code>python:3.11-slim</code> with CPU-only PyTorch (image size: 1.38 GB, well within the 2.0 GB budget). Fifty sequential parse requests sent to a container constrained to 1 CPU and 1 GiB RAM (<code>results/docker_50req.txt</code>) yielded 100% HTTP 200 responses, zero OOM events (<code>OOMKilled=false</code>), and peak memory usage of 468.2 MiB (45.72% of budget).",
        body_style
    ))

    # SECTION 4: TASK 4
    story.append(Paragraph("4. Task 4: Kubernetes Deployment, Scaling, and Reliability", h1_style))
    story.append(Paragraph(
        "<b>Deployment Topology & Ingress:</b> Deployed in the <code>app</code> namespace with 2 initial replicas. Liveness probes inspect <code>/healthz</code> while readiness probes inspect <code>/readyz</code>. Ingress routing maps external <code>/parse</code> requests directly to Service <code>parser</code>. As captured in <code>results/endpoints_during_startup.txt</code>, the Service maintains <code>&lt;none&gt;</code> endpoints until model weights are fully initialized.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Autoscaling (HPA):</b> HorizontalPodAutoscaler (<code>k8s/hpa.yaml</code>) targets 70% CPU utilization across 1-2 replicas. Under continuous Locust concurrency, aggregate CPU reached 195%, triggering scale-up from 1 to 2 replicas in under 45 seconds. Post-load cooldown (300 s window) smoothly scaled back to 1 replica (documented in <code>results/hpa_watch.txt</code>).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Failover, Recovery & Rollout:</b> Deleting an active pod under live load triggered Kubernetes replica recreation in 17.5 seconds, with 450 requests seeing only 4 transient 500 errors (0.89% error rate, strictly beneath the 2.0% limit). Rolling update from v1 to v2 exhibited only 2 errors across 500 requests (0.40% error rate, well below the 0.5% ceiling), with <code>kubectl rollout undo</code> restoring v1 seamlessly.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Cold Start & Load Balancing:</b> Container cold start to Ready state averaged a median of 7.1 s across 3 trials (runs: 8.2 s, 6.8 s, 7.1 s, evidence in <code>results/cold_start_logs_run*.txt</code>). Dual-replica traffic split balanced evenly: 172 requests to Pod A (50.6%) and 168 requests to Pod B (49.4%), comfortably surpassing the 30% per-pod minimum.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Local Cluster Environment Limitation:</b> Single-node k3d runs within a containerized runtime on one host machine. While validating control plane scheduling, controller lifecycles, and horizontal scaling, it cannot replicate physical power loss or rack-level network partitioning.",
        body_style
    ))

    # SECTION 5: TASK 5
    story.append(Paragraph("5. Task 5: Subnetting and Network Access Control", h1_style))
    story.append(Paragraph(
        "<b>VLSM Allocation Strategy (10.20.0.0/16):</b> Subnets were allocated in descending order of usable host capacity: app (1,000 hosts needed -> /22 prefix, 1,022 usable hosts, 10.20.0.0 - 10.20.3.255); public (250 hosts needed -> /24 prefix, 254 usable hosts, 10.20.4.0 - 10.20.4.255); data (100 hosts needed -> /25 prefix, 126 usable hosts, 10.20.5.0 - 10.20.5.127); management (20 hosts needed -> /27 prefix, 30 usable hosts, 10.20.5.128 - 10.20.5.159). Full working in <code>network/subnets.md</code>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Stateless NACL Configuration:</b> Configured in <code>network/nacl.json</code> (inbound deny 50 for 198.51.100.0/24, allow 100 for HTTP 80, allow 150 for HTTPS 443, allow 200 for SSH from management, allow 250 for app reply traffic; outbound allow 50 to app port 8000, allow 100 for client replies on ephemeral ports 1024-65535). Verified 100% correct (6/6 packets) via <code>python tools/nacl_sim.py network/nacl.json network/packets_sample.jsonl --check</code>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Stateless Mechanics & Rule Ordering:</b> Stateless NACLs inspect each packet individually without state tables. Consequently, ephemeral reverse return traffic requires explicit bidirectional allowance. Placing block rule 50 ahead of general HTTP/HTTPS allow rules ensures malicious IP ranges are dropped prior to reaching broader port permissions.",
        body_style
    ))

    # SECTION 6: TASK 6
    story.append(Paragraph("6. Task 6: Reproducibility, Testing, and CI/CD", h1_style))
    story.append(Paragraph(
        "<b>Single-Command Operations:</b> The entire environment builds, provisions storage, imports images, and deploys services from a fresh clone via <code>make up</code>. Clean cluster teardown executes via <code>make down</code>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Continuous Integration Pipeline (ci.yml):</b> GitHub Actions pipeline executes 5 sequential stages: (1) code-linting with ruff; (2) unit-testing running 4 tests in <code>tests/test_basic.py</code>; (3) security-secret-scan with Gitleaks; (4) model-evaluation downloading <code>model_v1.zip</code> from GitHub Release v1.0 and running <code>predict.py</code>; and (5) quality-gate running <code>score.py --min-validity 95</code>.",
        body_style
    ))
    story.append(Paragraph(
        f"<b>Quality Gate Failure Verification:</b> Triggering the pipeline with <code>use_base: true</code> runs inference with the untrained Pythia-70M baseline, producing 0% valid JSON and successfully triggering gate failure (exit status 1), as verified in CI workflow runs.",
        body_style
    ))

    # SECTION 7: TASK 7
    story.append(Paragraph("7. Task 7: Performance, Cost, and Review", h1_style))
    story.append(Paragraph(
        "<b>Benchmark Results (Locust 4 users, 2 min, 2 replicas):</b> 342 total requests, 2 failures (0.58% error rate, well under 1% limit). Median latency p50 = 1,250 ms, p95 = 2,700 ms (under 5,000 ms ceiling), throughput = 2.85 req/s. CPU load: 1928m and 1915m per pod. Memory: 742 MiB and 758 MiB. Load balanced: 172 / 168 requests (50.6% / 49.4%). Full metrics in <code>results/loadtest_stats.csv</code> and <code>results/loadtest_headers.json</code>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Cost Estimation Arithmetic:</b> Each replica is billed for 2 vCPU limit (2 x 3.50 = 7.00 INR/h) and 1 GiB memory limit (1 x 0.45 = 0.45 INR/h), totaling 7.45 INR/replica/h. Two replicas cost 14.90 INR/h. At 2.85 req/s (10,260 req/h), unit economic cost is: <code>(14.90 INR / 10,260 req) * 1,000 = 1.45 INR per 1,000 requests</code>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>SLO Formulation:</b> Objective defined as >= 99% successful requests over one load-test run (342 requests). Permitted error budget = 342 x 0.01 = 3.42 requests. Actual failures observed = 2 requests (58.5% of budget used, SLO fully met at 99.42% success).",
        body_style
    ))

    story.append(Paragraph("<b>Comprehensive Architecture Review Table:</b>", h2_style))
    rev_data = [
        [Paragraph(h, table_header_style) for h in ["Component or Concern", "Evidence (Measured Number)", "Identified Limitation", "Proposed Improvement"]],
        [
            Paragraph("Data & Storage", table_cell_style),
            Paragraph("7 files downloaded over cluster network at startup (median 7.1 s cold start)", table_cell_style),
            Paragraph("Single-node SeaweedFS without high-availability or volume caching", table_cell_style),
            Paragraph("Deploy replicated multi-node MinIO/Ceph; attach PVC node caches", table_cell_style)
        ],
        [
            Paragraph("Model Quality", table_cell_style),
            Paragraph("2 of 342 outputs rejected as invalid JSON (0.58% error rate)", table_cell_style),
            Paragraph("Compact 70M student exhibits occasional slot boundary errors", table_cell_style),
            Paragraph("Incorporate larger distillation pool and grammar-constrained decoding", table_cell_style)
        ],
        [
            Paragraph("Latency & Throughput", table_cell_style),
            Paragraph("p50 = 1,250 ms, p95 = 2,700 ms, 2.85 req/s on 2 replicas", table_cell_style),
            Paragraph("CPU-bound inference; thread contention occurs if unconstrained", table_cell_style),
            Paragraph("Apply INT8 ONNX Runtime quantization and continuous dynamic batching", table_cell_style)
        ],
        [
            Paragraph("Resource Utilization", table_cell_style),
            Paragraph("CPU peaked at 1928m of 2000m limit; RAM at 758 MiB of 1 GiB", table_cell_style),
            Paragraph("Pod capacity saturated near 100% under only 4 concurrent users", table_cell_style),
            Paragraph("Right-size resource limits, scale horizontally across multi-node cluster", table_cell_style)
        ],
        [
            Paragraph("Reliability & Recovery", table_cell_style),
            Paragraph("Pod failover restored Ready state in 17.5 s with only 4 errors (0.89%)", table_cell_style),
            Paragraph("Single-node k3d cluster lacks true machine-level fault tolerance", table_cell_style),
            Paragraph("Multi-node Kubernetes topology with PodDisruptionBudgets & anti-affinity", table_cell_style)
        ],
        [
            Paragraph("Security & Governance", table_cell_style),
            Paragraph("S3 credentials in Secret s3-creds; unit cost is 1.45 INR / 1k reqs", table_cell_style),
            Paragraph("Kubernetes Secret is only base64; Ingress lacks TLS encryption", table_cell_style),
            Paragraph("Integrate HashiCorp Vault / External Secrets Operator and cert-manager TLS", table_cell_style)
        ]
    ]
    t_rev = Table(rev_data, colWidths=[85, 145, 140, 170])
    t_rev.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white])
    ]))
    story.append(t_rev)
    story.append(Spacer(1, 4))

    # SECTION 8: AI USE
    story.append(Paragraph("8. Record of AI Tool Utilization", h1_style))
    story.append(Paragraph(
        "Antigravity (Gemini) and Anthropic Claude were utilized for architecture design, refactoring, Kubernetes manifests, and diagnosing PyTorch thread contention under CPU limits. Every suggested shell command, manifest, and Python refactor was executed locally and rigorously verified against automated testing suites. The stateless NACL was tested and verified with <code>tools/nacl_sim.py</code> (6/6 passing, 100%). Model scoring was audited with <code>tools/score.py</code>, and request timings were measured directly via Locust. AI inaccuracies (such as default Makefile target precedence and premature readiness probe pass) were identified, corrected, and documented. Distillation labels were produced exclusively by Phi-3.5 via Ollama without synthetic manual fabrication. Full verification logs are detailed in <code>AI_USE.md</code>.",
        body_style
    ))

    doc.build(story)
    print(f"Comprehensive report generated successfully: {filename}")
    if os.path.exists(filename):
        shutil.copyfile(filename, "report_final.pdf")
        print("Copied to report_final.pdf")

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "https://github.com/vabhiram/neural-command-distiller-k8s"
    build_pdf(repo_url=url)

# Use Case: Multi-Model SaaS Product

**Design doc:** [docs/DESIGN.md](./docs/DESIGN.md) — architecture, patterns, and why.


**Parent system design:** [01 — LLM Inference Serving](../01-llm-inference-serving.md)  
**Also references:** [09 — Multi-model routing / API platform](../09-multi-model-routing-api-platform.md)

## Users & problem

A product exposes several models (fast/cheap, default, frontier) in one UX. The platform must route correctly, keep fleets healthy independently, and avoid one large model outage taking down the whole app.

## Requirements & SLOs

| Requirement | Target |
|-------------|--------|
| Model choice | User or auto-router selects tier |
| Isolation | Failure domain per model fleet |
| Cost | Cheap tier absorbs majority of traffic |
| UX | Clear model identity in responses |

## Design (from parent)

```
Product BFF → Router (tier / auto)
  → Fleet A (small) | Fleet B (mid) | Fleet C (frontier)
  → Shared safety + streaming + conversation services
```

Reuse **01** per fleet (batching, KV, autoscaling).  
Shared: auth, conversations ([10](../10-global-realtime-product-surface.md)), safety ([06](../06-safety-moderation-pipeline.md)), streaming ([02](../02-streaming-token-delivery.md)).

## Specializations

| Concern | Design choice |
|---------|---------------|
| Blast radius | Separate deploy/canary per fleet |
| Auto route | Confidence/cost cascade; log chosen model |
| Quotas | Per-tier entitlements (free → small only) |
| Cache | Per-model prefix caches |

## Failure modes

- Frontier fleet down → degrade to mid with banner; don’t error the whole product.
- Auto-router oscillation → sticky per session; hysteresis on escalate/de-escalate.
- Cost blowup → default traffic to small; escalate only on hard prompts.




## Design walkthrough (opens on GitHub)

![Design overview](docs/video/design-overview.gif)

Full narrated video (download): [docs/video/design-overview.mp4](docs/video/design-overview.mp4)

## Run (self-contained POC)

This folder is a **standalone** project (safe to split into its own GitHub repo).

```bash
cd multi-model-saas-product
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=. python -m uvicorn app.main:app --reload --port 8000
```

```bash
curl -s http://127.0.0.1:8000/health | jq
```

curl -s -X POST http://127.0.0.1:8000/generate -H 'Content-Type: application/json' -d '{"prompt":"explain gravity","tier":"auto"}' | jq

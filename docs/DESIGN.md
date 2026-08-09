# Design: Multi-Model SaaS Product

**Project:** `multi-model-saas-product`  
**Parent system design:** `01-llm-inference-serving.md / 09-multi-model-routing-api-platform.md`

## 1. What this POC demonstrates

One product UX over multiple model fleets with auto tier selection and independent failure domains.

## 2. Architecture (POC)

```text
Request → pick fleet (fast|default|frontier) → MockLLM(model) → return chosen_model
```

## 3. Patterns used (and why)

| Pattern | Why used | Where in code |
|---------|----------|---------------|
| Fleet isolation by model id | Outage of frontier should not imply small-model failure. | Separate `MockLLM(model=…)` instances. |
| Auto-routing heuristic | Most traffic should hit cheap models. | Length-based `pick()`. |
| Transparent model identity | Users/debuggers must see what ran. | `chosen_model` in response. |

## 4. Key endpoints

`GET /health`, `POST /generate`

## 5. Tradeoffs / POC limits

Heuristic routing is illustrative; production uses confidence/cost classifiers.

## 6. How to run

See the **Run (self-contained POC)** section in [`../README.md`](../README.md).

This folder is self-contained and can be published as its own GitHub repository.

## 7. Design walkthrough video

Narrated with **ElevenLabs Debpro voice** and Debpro still image (via [GitaProject](/Users/deb/Development/GenAI/GitaProject)):

- Video: [`video/design-overview.mp4`](./video/design-overview.mp4)
- Script: [`video/narration.txt`](./video/narration.txt)


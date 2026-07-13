PulseAIController/
├── app/
│   ├── main.py                  # FastAPI app, lifespan, router registration
│   ├── config.py                # Pydantic Settings (env vars)
│   ├── dependencies.py          # DB session, Redis client, current key context
│   ├── middleware/
│   │   ├── auth.py              # Layer 1: Virtual Key validation
│   │   └── rate_limiter.py      # Layer 2: Token Bucket + budget check
│   ├── routers/
│   │   ├── proxy.py             # POST /v1/chat/completions (core proxy)
│   │   ├── keys.py              # CRUD for Virtual Keys
│   │   └── analytics.py         # Usage dashboard queries
│   ├── services/
│   │   ├── cache.py             # Layer 3: Exact + semantic cache
│   │   ├── router.py            # Layer 4: Complexity scoring + model selection
│   │   ├── upstream.py          # Layer 5: LiteLLM call wrapper
│   │   ├── fallback.py          # Layer 6: Circuit breaker + fallback chain
│   │   └── cost_tracker.py      # Layer 7: Token counting, cost calc, logging
│   └── models/
│       ├── database.py          # SQLAlchemy engine, session, Base
│       ├── schemas.py           # Pydantic request/response models
│       └── tables.py            # SQLAlchemy ORM table definitions
├── scripts/
│   └── seed.py                  # Create test user + virtual key
├── lua/
│   └── token_bucket.lua         # Atomic Redis rate-limit script
├── alembic/                     # Database migrations
├── tests/
├── Dockerfile
├── docker-compose.yml           # FastAPI + PostgreSQL + Redis
├── .env.example
├── requirements.txt
└── README.md                    # Architecture diagram + setup instructions

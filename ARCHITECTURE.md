# 🏗️ ResistNet — System Architecture

┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                          │
│  ┌─────────────────────┐  ┌─────────────────────────────┐   │
│  │   React Dashboard   │  │   Streamlit Dashboard       │   │
│  │   (20+ components)  │  │   (Rapid prototyping)       │   │
│  │   Leaflet.js maps   │  │   Plotly charts             │   │
│  │   Recharts analytics│  │                             │   │
│  └─────────┬───────────┘  └─────────────┬───────────────┘   │
│            │                            │                    │
└────────────┼────────────────────────────┼────────────────────┘
             │                            │
             ▼                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      API LAYER                               │
│  ┌───────────────────────────────────────────────────────┐   │
│  │                   FastAPI (12 endpoints)               │   │
│  │                                                       │   │
│  │  /api/stats          /api/districts    /api/states    │   │
│  │  /api/predictions    /api/alerts       /api/explain   │   │
│  │  /api/predict/district   /api/predict/high-risk       │   │
│  └───────────────────────────┬───────────────────────────┘   │
└──────────────────────────────┼────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      ML ENGINE                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │
│  │ Prophet  │ │ Random   │ │ XGBoost  │ │    LSTM      │   │
│  │ (Time    │ │ Forest   │ │ (Gradient│ │  (Deep       │   │
│  │ Series)  │ │ (Ensemble│ │ Boosting)│ │  Learning)   │   │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └──────┬───────┘   │
│       └─────────────┴────────────┴─────────────┘            │
│                          │                                   │
│                   ┌──────▼──────┐                            │
│                   │  Ensemble   │                            │
│                   │  (Averaging)│                            │
│                   └──────┬──────┘                            │
│                          │                                   │
│  ┌───────────────────────▼────────────────────────────┐      │
│  │              Explainability (SHAP)                 │      │
│  └────────────────────────────────────────────────────┘      │
└──────────────────────────────┬────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │   SQLite (Dev)  │  │  PostgreSQL     │                   │
│  │   7 Tables      │  │  (Production)   │                   │
│  │                 │  │  + PostGIS      │                   │
│  └─────────────────┘  └─────────────────┘                   │
│                                                              │
│  Tables: districts, pathogens, antibiotics,                  │
│          resistance_records, pharma_sales,                   │
│          predictions, alerts                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      DATA PIPELINE                           │
│                                                              │
│  ICMR Reports (PDF) ──► pdfplumber ──► Structured Data      │
│  Pharma Sales (CSV) ──► Pandas ──────► Feature Engineering  │
│                                                              │
│  50,160 records ──► 42 features ──► 5 models ──► Alerts     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      DEVOPS                                  │
│                                                              │
│  GitHub ──► GitHub Actions ──► Render (Auto Deploy)         │
│  Docker ──► Docker Compose (Local Dev)                      │
│  pytest ──► 14 tests ──► CI Pipeline                        │
└─────────────────────────────────────────────────────────────┘
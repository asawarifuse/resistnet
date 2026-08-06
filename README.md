# 🦠 ResistNet — AI-Powered AMR Early Warning & Response System

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB)](https://react.dev)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![IIT Bombay](https://img.shields.io/badge/Eureka!-IIT%20Bombay-orange)](https://ecell.in)

---

## 🎯 What ResistNet Does

ResistNet predicts antibiotic resistance outbreaks **48 hours before they happen**, recommends safer alternatives, alerts hospitals in 8 Indian languages, and learns from historical patterns — a complete **Predict → Recommend → Alert → Learn** loop.

**300,000+ Indians die annually from AMR. ResistNet is India's first district-level early warning system.**

---

## 🧠 4-Module Architecture

| Module | Function | Technology |
|--------|----------|------------|
| **Sanket** | Predicts resistance risk per district-pathogen pair | XGBoost, Prophet, LSTM, Random Forest, Ensemble, SHAP |
| **Marg** | Recommends alternative antibiotics with efficacy scores | WHO AWaRe guidelines, Clinical decision logic |
| **Sahay** | Alerts hospitals, checks pharmacy stock, sends multilingual SMS | Twilio, 8 Indian languages |
| **Smriti** | Compares with historical outbreaks, suggests prevention | Time-series similarity, Pattern matching |

---

## 📊 Key Metrics

| Metric | Value |
|--------|-------|
| Districts Covered | 114 (expandable to 766) |
| Pathogens Tracked | 5 |
| Antibiotics Monitored | 14 |
| Records Processed | 54,720 |
| ML Models | 5 (Ensemble) |
| API Endpoints | 12 |
| Dashboard Features | 50+ |
| Test Coverage | 14 passing |
| Languages Supported | 8 Indian languages |
| Total Cost | ₹0 (100% Open Source) |
| Build Time | 40 days (Solo) |

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Languages** | Python 3.12, JavaScript (ES6+) |
| **ML/DL** | XGBoost, Random Forest, Prophet, LSTM, Ensemble |
| **Explainability** | SHAP |
| **Backend** | FastAPI, Uvicorn |
| **Database** | SQLite (dev), PostgreSQL-ready (prod) |
| **Frontend** | React, Recharts, Leaflet.js, TailwindCSS |
| **DevOps** | Docker, GitHub Actions, Render, Vercel |
| **Alerts** | Twilio SMS, 8 Indian language templates |
| **Testing** | pytest (14 tests) |
| **Monitoring** | Drift detection, Rollback readiness |

---

## 🚀 Live Demo

| Service | URL |
|---------|-----|
| **Dashboard** | [resistnet.vercel.app](https://resistnet.vercel.app) |
| **API Docs** | [resistnet-api.onrender.com/docs](https://resistnet-api.onrender.com/docs) |
| **Health Check** | [resistnet-api.onrender.com/health](https://resistnet-api.onrender.com/health) |

---

resistnet/
    frontend/
        src/
            components/
            pages/
        public/
    src/
        api/
            main.py
            predict_endpoint.py
            marg_endpoint.py
        models/
        data_collection/
        database_setup.py
    data/
        raw/
        processed/
        resistnet.db
    dashboard/
    tests/
    Dockerfile
    requirements.txt
    README.md
---

🔄 System Flow

ICMR Data + Pharma Sales
        │
        ▼
   [Sanket] — Predict resistance (48-hr advance)
        │
        ▼
   [Marg] — Recommend alternative antibiotics
        │
        ▼
   [Sahay] — Alert hospitals + guide pharmacy stock
        │
        ▼
   [Smriti] — Learn from history, prevent recurrence
        │
        ▼
   Dashboard + SMS (8 languages)
---

## 🏆 Achievements

- ✅ Submitted to **Eureka! 2026, E-Cell IIT Bombay** (Under Review)
- ✅ Registered for **MEDHA MEDITHON 2026** (Category B, TRL 4+), VNIT Nagpur
- ✅ **SIH 2026** Project (Disaster Management Theme)
- ✅ **1,600+ LinkedIn impressions** on project post
- ✅ Built solo. ₹0 cost. 100% open-source.

---

## 🔜 Roadmap

| Priority | Feature | Timeline |
|----------|---------|----------|
| 🔴 Critical | Clinical validation with hospitals | 2-3 months |
| 🔴 Critical | HL7/FHIR integration | 1-2 months |
| 🔴 Critical | Production deployment (AWS/GCP) | 1 month |
| 🟡 High | Real-time ICMR data pipeline | 2-3 months |
| 🟡 High | Pharmacy inventory integration | 2-3 months |
| 🟢 Medium | Mobile app for clinicians | 3-4 months |
| 🟢 Medium | Multi-hospital pilot program | 6 months |

---

## 👩‍💻 Author

**Asawari Vasantrao Fuse**
- B.Tech CSE (Data Science), 3rd Year
- CDC Coordinator, St. Vincent Pallotti College of Engineering & Technology
- GitHub: [asawarifuse](https://github.com/asawarifuse)
- LinkedIn: [asawarifuse](https://linkedin.com/in/asawarifuse)
- Portfolio: [portfolio-sepia-theta-21.vercel.app](https://portfolio-sepia-theta-21.vercel.app)

---

## ⭐ Star This Repo

If ResistNet inspires you or helps with your own project, drop a star. It means a lot.

---

**Built with ❤️ for India's fight against superbugs.**

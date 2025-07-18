# 📊 EDA + AI Insight Generator

This project automates exploratory data analysis (EDA) and generates column-level insights using AI (OpenAI or Ollama). It also produces Markdown and PDF reports with plots and profiling.

---

## 🔧 Features

- ✅ Column profiling (numeric, categorical, missing, outliers)
- 🧠 AI-generated insights per column
- 📈 Auto-generated plots (histograms, boxplots)
- 📄 Markdown + PDF reports
- 📂 Organized outputs per source file

---

## 📁 Project Structure

```
eda_eda_an/
├── ai/                      # AI model integration (OpenAI, Ollama)
├── eda_core/               # Core EDA: profile, transform, plots, utils
├── outputs/                # Organized reports per dataset
├── sample_source/          # Input Excel files
├── tests/                  # CLI runners & tests
```

---

## 🚀 Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run pipeline on a sample Excel
python tests/cli_ai_insight_runner_v2.py sample_source/blahblah.xlsx
```

---

## 🧠 AI Models Supported

- 🔸 OpenAI (via API key in `.env`)
- 🔹 Ollama (local model like `gemma:2b`, `mistral`)

Set model in `.env`:

```env
AI_MODEL_TYPE=ollama
OLLAMA_MODEL=gemma:2b
```

---

## 📦 Outputs

Each Excel file processed creates an output folder:

```
outputs/
└── <source_name>/
    ├── insights/     # AI insights (JSON)
    ├── stats/        # Column + table profile
    ├── plots/        # Histograms, boxplots
    └── reports/      # Markdown + PDF report
```

---

## 📌 Output Files Example

- `outputs/blahblah/reports/blahblah_report.md`
- `outputs/blahblah/reports/blahblah_report.pdf`

---

## 📝 How to Contribute

1. Fork this repo
2. Add features or fix bugs
3. Submit a pull request

---

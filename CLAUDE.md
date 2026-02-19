# CLAUDE.md - AI Assistant Guide for Financial Control App

## Project Overview

This is a **financial data processing and P&L (Profit & Loss) analysis system** for the business plan "Umatch." It processes CSV exports from **Conta Azul** (a Brazilian accounting platform) and generates monthly P&L statements, dashboard KPIs, and financial forecasts.

**Primary language:** Portuguese (Brazilian) for business logic, variable names in financial contexts, and documentation. Code identifiers and API contracts are in English.

## Tech Stack

- **Backend:** Python 3.8+ with FastAPI, served by Uvicorn on port 8000
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** Scikit-learn (linear regression for forecasting)
- **Authentication:** JWT tokens (python-jose) + Argon2 password hashing
- **AI Integration:** OpenAI GPT for financial insights
- **Frontend:** HTML/CSS/JavaScript (Vanilla), built with Vite/npm
- **CI/CD:** GitHub Actions (PyLint on Python 3.8, 3.9, 3.10)

## Repository Structure

```
financeaooooop/
├── logic.py                    # Core financial processing engine (production)
├── logic_CORRECTED.py          # Improved version with 8 critical fixes
├── logic_BACKUP                # Backup of original logic.py
├── models.py                   # Pydantic/dataclass data models
├── pnl_transactions.py         # FastAPI endpoint for transaction drill-down
├── test_integration.py         # Integration test suite
├── test_upload.py              # CSV processing tests
├── validate_corrections.py     # Correction validation script
├── implementar_formulas_pl.py  # Excel formula implementation
├── adicionar_pl_formulas.py    # P&L worksheet creation
├── diff_detalhado.py           # Detailed change analysis tool
├── relatorio_analise_logic.py  # Analysis report generator
├── analise_estrutura.py        # Structure analysis utility
├── demo_documentation.py       # Documentation demo
├── Makefile                    # Dev task runner
├── build.sh                    # Full build script (frontend + backend)
├── .github/
│   ├── workflows/pylint.yml    # CI: PyLint on push
│   └── copilot-instructions.md # Development guidelines
├── README.md                   # System documentation
├── QUICK_DEPLOY_GUIDE.md       # 3-step deployment guide
├── EXECUTIVE_SUMMARY.md        # Validation checklist
├── FINAL_VALIDATION_REPORT.md  # Comprehensive validation report
├── DEPLOYMENT_REPORT.md        # Deployment status
├── DOCUMENTATION_SUMMARY.md    # Documentation update log
└── DOCUMENTATION_SHOWCASE.md   # Documentation demo
```

## Key Source Files

### `logic.py` (1062 lines) — Core Engine

The main production module. Entry points:

| Function | Purpose |
|---|---|
| `process_upload(bytes)` | Parse CSV uploads (multi-encoding: UTF-8, Latin-1, CP1252) |
| `get_initial_mappings()` | Return default cost-center-to-P&L-line mappings |
| `calculate_pnl(df, mappings, overrides, dates)` | Generate full P&L statement |
| `get_dashboard_data(df, mappings)` | Aggregate KPIs for dashboard |
| `calculate_forecast(df, mappings, months_ahead)` | Linear regression forecast |

Key helpers: `normalize_text()`, `converter_valor_br()`, `enforce_wages_cost_center()`, `parse_dates()`.

### `models.py` (46 lines) — Data Models

- `MappingItem` — Cost center/supplier to P&L line mapping
- `PnLItem` — Single P&L row (line_number, description, values, is_header, is_total)
- `PnLResponse` — Complete P&L (headers + rows)
- `DashboardData` — KPIs, monthly_data, cost_structure

### `pnl_transactions.py` (151 lines) — API Endpoint

- `GET /pnl/transactions/{line_number}` — Transaction drill-down with optional `?month=YYYY-MM` filter
- Uses JWT authentication via `get_current_user` dependency

## Development Commands

```bash
# Start backend
make dev-backend          # Runs ./run_backend.sh (Uvicorn on port 8000)

# Start frontend
make dev-frontend         # cd frontend && npm install && npm run dev

# Full build (frontend + backend)
./build.sh                # npm ci + build frontend, pip install backend deps

# Run integration tests
python test_integration.py

# Run CSV processing tests
python test_upload.py

# Validate corrections
python validate_corrections.py
```

## CI/CD

- **PyLint** runs on every push via GitHub Actions (`.github/workflows/pylint.yml`)
- Tested against Python 3.8, 3.9, 3.10
- Lints all `*.py` files tracked by git: `pylint $(git ls-files '*.py')`

## Environment Variables

Required in `.env` (never committed):

```
SECRET_KEY=<32+ character random string>     # JWT signing key
OPENAI_API_KEY=sk-proj-<key>                 # OpenAI API key
FRONTEND_URL=https://your-domain.com         # Optional, for CORS
```

## Critical Development Rules

### Financial Calculation Rules

1. **NEVER use `abs()` on revenue values.** Refunds and chargebacks must reduce revenue correctly by preserving negative signs.
2. **Payment Processing rate is hardcoded at 17.65%** of net revenue.
3. **Payroll transactions** must always route to "Wages Expenses" (P&L line 62). Detection keywords: folha, pro labore, salário, holerite, payroll.
4. **EBITDA** = Gross Profit - Operating Expenses.
5. **Net Result** = EBITDA (simplified).

### Code Organization Rules

1. **Always define helper functions at the top of the file**, before they are used. `normalize_text_helper()` must appear before any code that calls it.
2. **Use global constants** for keyword lists (e.g., `PAYROLL_KEYWORDS`, `PAYROLL_COST_CENTER`). Do not redefine inside functions.
3. **Use `logic_CORRECTED.py` as the reference** when implementing new features or fixes in `logic.py`.
4. **Use exact Conta Azul names** for cost center mappings (e.g., "Google Play Net Revenue", not "Receita Google").
5. **Remove unused imports** — PyLint CI will catch these.

### Code Style

- Google-style docstrings with Args, Returns, Raises sections
- Type hints on function signatures
- Constants in UPPER_SNAKE_CASE at module level
- No verbose inline comments explaining obvious logic

## P&L Line Number Reference

```
Line 16  - (=) RESULTADO LÍQUIDO (Net Result)
Line 25  - Google Play Net Revenue
Line 33  - App Store Net Revenue
Line 38  - Rendimentos de Aplicações (Investment Income)
Line 43-48 - Web Services COGS
Line 49  - Other Revenues
Line 52  - (=) CUSTOS DOS PRODUTOS VENDIDOS (CPV / COGS)
Line 55  - (=) LUCRO BRUTO (Gross Profit)
Line 56  - Marketing Expenses
Line 62  - Wages Expenses (Folha de Pagamento)
Line 68  - Tech Support
Line 72  - (=) EBITDA
Line 90  - Other Expenses (Devoluções/Returns)
```

## Testing Checklist

When modifying financial logic, always validate:

- [ ] Total Revenue calculates correctly with refunds (no `abs()`)
- [ ] Payment Processing = Revenue * 17.65%
- [ ] Gross Margin = (Gross Profit / Revenue) * 100
- [ ] EBITDA Margin = (EBITDA / Revenue) * 100
- [ ] Payroll transactions route to line 62
- [ ] Python compilation succeeds (`python -m py_compile logic.py`)
- [ ] Integration tests pass (`python test_integration.py`)
- [ ] PyLint passes (`pylint logic.py`)

## Architecture Notes

- **No persistent database in current codebase** — data is processed in-memory using Pandas DataFrames. PostgreSQL is referenced in documentation for the full production stack.
- **CSV parsing** supports multiple encodings (UTF-8, Latin-1, CP1252) and separators (comma, semicolon) with auto-detection.
- **Brazilian currency format** support: `1.234,56` is converted to `1234.56` float via `converter_valor_br()`.
- **Matching algorithm** uses O(1) dict lookup by cost center, with fuzzy text matching as fallback (normalized, accent-stripped comparison).
- **Forecasting** uses simple linear regression from scikit-learn (no seasonality adjustment).

## Known Corrections (logic_CORRECTED.py)

Eight critical fixes were applied and validated with 100% test pass rate:

1. Removed unused imports
2. Global constants for `PAYROLL_COST_CENTER` and `PAYROLL_KEYWORDS`
3. `normalize_text_helper()` moved to top of file
4. Revenue mapping names corrected ("Receita Google" -> "Google Play Net Revenue")
5. Removed `abs()` from revenue calculations to allow refunds
6. Added cost center field to payroll fuzzy match
7. Simplified Net Result calculation (= EBITDA)
8. Removed verbose/redundant comments

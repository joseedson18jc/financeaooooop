# Test Coverage Analysis

## Current State

### Overall Coverage: 36% (619 of 971 statements missed)

| File | Statements | Missed | Coverage | Notes |
|------|-----------|--------|----------|-------|
| `logic.py` | 376 | 120 | **68%** | Core module, partially tested |
| `logic_CORRECTED.py` | 369 | 369 | **0%** | Zero coverage - never imported by tests |
| `models.py` | 27 | 0 | **100%** | Fully covered (data classes) |
| `pnl_transactions.py` | 34 | 34 | **0%** | Zero coverage - API endpoint untested |
| `test_integration.py` | 87 | 18 | 79% | Test file itself |
| `test_upload.py` | 25 | 25 | **0%** | Requires external CSV file to run |
| `validate_corrections.py` | 53 | 53 | **0%** | Not run as part of test suite |

### Existing Test Infrastructure Problems

1. **No test framework usage**: Tests use raw `print()` and `try/except` instead of `pytest` or `unittest`. There are no assertions — failures are only visible by reading stdout output.
2. **False pass reporting**: `test_integration.py` prints "TODOS OS TESTES PASSARAM" even when sub-checks fail (e.g., Google/Apple mappings show "NÃO ENCONTRADO" but the test still reports success).
3. **No CI integration for tests**: The GitHub Actions workflow only runs `pylint`, not the test suite.
4. **`test_upload.py` is unusable**: It depends on a hardcoded CSV file (`Extratodemovimentações-2025-ExtratoFinanceiro.csv`) that doesn't exist in the repo.

---

## Gap Analysis by Module

### 1. `logic.py` — Core Business Logic (68% covered, critical gaps)

**Covered:**
- Basic CSV parsing (happy path with UTF-8, comma separator)
- Simple value conversion (Brazilian format)
- Transaction type sign application (Entrada/Saída)
- Basic P&L calculation flow
- Dashboard KPI generation
- Mapping initialization

**NOT Covered (120 missed statements):**

| Area | Lines | Risk | Description |
|------|-------|------|-------------|
| CSV encoding fallback | 94-121 | **High** | Fallback parsing with `on_bad_lines='skip'` for Latin-1, CP1252, etc. |
| Column alias mapping | 144-148 | Medium | Alternative column names from different Conta Azul exports |
| Missing columns error | 158-159 | **High** | `ValueError` when required columns are absent |
| Date format fallback | 176-178 | Medium | Non-Brazilian date formats (ISO, US) |
| Accounting negative formats | 209-215 | **High** | Parenthesized `(1.234,56)` and trailing-minus `1.234,56-` values |
| US number format | 223-228, 231 | Medium | `1,234.56` US-style numbers |
| No Tipo column fallback | 269 | Medium | CSVs that lack the Tipo column |
| Payroll keyword enforcement | 312 | Medium | Edge cases in payroll detection |
| Empty/null DataFrame | 541 | Low | `calculate_pnl` with empty input |
| Date range filtering | 546-551 | **High** | `start_date`/`end_date` parameters in `calculate_pnl` |
| Categoria 1 fallback matching | 598-603, 617-620 | Medium | Third-level matching in P&L calculation |
| Overrides mechanism | 753-762 | **High** | Manual override of Revenue/EBITDA/Net Result values |
| Zero-revenue margin safety | 807-808 | Medium | Division by zero in margin calculations |
| Forecast function | 997-1061 | **High** | `calculate_forecast()` completely untested (65 lines) |

### 2. `pnl_transactions.py` — API Endpoint (0% covered)

This FastAPI endpoint is completely untested. Critical paths include:
- No data loaded (404 response)
- Invalid line number mapping (404 response)
- Month filtering (both `YYYY-MM` string and integer format)
- Cost center filtering (case-insensitive substring)
- Supplier filtering (excluding "Diversos")
- Transaction list construction and total calculation
- The `line_mapping.descricao` attribute access (line 145) — `MappingItem` has no `descricao` attribute, this is a **latent bug** that would cause an `AttributeError` at runtime

### 3. `logic_CORRECTED.py` — Corrected Module (0% covered)

This is the "recommended for production" module with 8 critical bug fixes, yet it has zero test coverage. The existing tests import from `logic.py` (the uncorrected version), meaning the corrections are never validated in the test suite.

---

## Recommended Improvements (Priority Order)

### Priority 1: Fix Critical Testing Infrastructure

**1a. Convert to pytest with proper assertions**

The current tests print results but never actually assert correctness. A test that prints "NÃO ENCONTRADO" for Google/Apple mappings but still reports "all tests passed" is actively misleading. Every check should be a proper `assert` statement.

**1b. Add tests to CI pipeline**

The `.github/workflows/pylint.yml` workflow should also run `pytest` so regressions are caught on every push.

**1c. Test the correct module**

Tests should import from `logic_CORRECTED.py` (or the corrected logic should replace `logic.py`). Currently the test suite validates the buggy version.

### Priority 2: Unit Tests for `process_upload()` Edge Cases

This function handles real-world messy data. The following scenarios need dedicated test cases:

| Test Case | Why It Matters |
|-----------|---------------|
| Latin-1 encoded CSV | Brazilian systems often export Latin-1 |
| Semicolon-separated CSV | Common in European/Brazilian CSV exports |
| Missing required columns | Should raise `ValueError` with helpful message |
| Accounting-negative values `(1.234,56)` | Used in financial exports |
| Trailing-minus values `1.234,56-` | Alternative negative notation |
| US number format `1,234.56` | Mixed-format data |
| CSV with `on_bad_lines` (malformed rows) | Production data often has corrupt rows |
| Missing Tipo column | Some exports omit this column |
| Empty CSV | Should raise `ValueError` |
| Payroll keyword detection | Verify all payroll keywords route to Wages Expenses |

### Priority 3: Unit Tests for `calculate_pnl()` Financial Logic

These are the calculations that drive the entire P&L statement. Incorrect results here directly impact business decisions.

| Test Case | Why It Matters |
|-----------|---------------|
| Date range filtering (`start_date`, `end_date`) | Feature is implemented but never tested |
| Manual overrides on Revenue/EBITDA/Net Result | Feature is implemented but never tested |
| Override on non-allowed line (should be ignored) | Security boundary |
| Negative revenue (refunds) | `logic.py` uses `abs()` which hides refunds — this is the bug `logic_CORRECTED.py` fixes |
| Zero revenue month (margin division by zero) | Edge case in margin calculations |
| Categoria 1 fallback matching | Third-level matching hierarchy |
| Unmapped transactions (large values logged) | Ensure they don't silently distort P&L |
| Multi-month aggregation accuracy | Verify month-over-month values are independent |

### Priority 4: Unit Tests for `calculate_forecast()`

Currently 0% covered. This function uses ML (LinearRegression) to predict future revenue/EBITDA.

| Test Case | Why It Matters |
|-----------|---------------|
| Fewer than 3 months of data | Should return warning message |
| Exactly 3 months (minimum for regression) | Boundary condition |
| Negative revenue prediction (should be clamped to 0) | Business rule |
| Custom `months_ahead` parameter | Default is 3 |
| Empty DataFrame input | Should return empty forecast |

### Priority 5: API Endpoint Tests for `pnl_transactions.py`

This requires FastAPI `TestClient` tests.

| Test Case | Why It Matters |
|-----------|---------------|
| No data loaded (404) | Error handling |
| Invalid line number (404) | Error handling |
| Valid line number with data | Happy path |
| Month filter as `YYYY-MM` string | Filter behavior |
| Month filter as integer | Filter behavior |
| Supplier filter excluding "Diversos" | Business rule |
| **Bug: `line_mapping.descricao` AttributeError** | `MappingItem` has no `descricao` field — this is field `observacoes`. This would crash at runtime. |

### Priority 6: Model Validation Tests

`models.py` is 100% covered via import, but the dataclasses themselves have no behavioral tests.

| Test Case | Why It Matters |
|-----------|---------------|
| `MappingItem` creation with all fields | Verify data integrity |
| `PnLItem` with `is_header=True` vs `is_total=True` | Verify flag behavior |
| `PnLResponse` with empty rows/headers | Edge case |
| `DashboardData` with empty kpis | Edge case |

---

## Latent Bug Found During Analysis

**`pnl_transactions.py:145`** references `line_mapping.descricao`, but `MappingItem` (defined in `models.py`) does not have a `descricao` attribute. The correct attribute is `observacoes`. This will cause an `AttributeError` when the endpoint is called. This bug exists because there are no tests for this endpoint.

---

## Summary

| Category | Current | Target | Gap |
|----------|---------|--------|-----|
| Overall Coverage | 36% | 80%+ | 44% |
| `logic.py` | 68% | 90%+ | 22% |
| `logic_CORRECTED.py` | 0% | 90%+ | 90% |
| `pnl_transactions.py` | 0% | 80%+ | 80% |
| `calculate_forecast()` | 0% | 80%+ | 80% |
| Proper assertions | 0 | All tests | All tests |
| CI test integration | No | Yes | Missing |

The highest-impact changes are:
1. **Fix the test infrastructure** (use pytest, add assertions, add to CI)
2. **Test `process_upload()` edge cases** (encoding, formats, error handling)
3. **Test financial calculation accuracy** (P&L, overrides, refunds)
4. **Test `calculate_forecast()`** (completely untested ML feature)
5. **Test the API endpoint** (and fix the `descricao` bug)

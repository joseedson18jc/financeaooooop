# GitHub Copilot Instructions for financeaooooop

## Project Overview

This is a **Financial Control Application** for Business Plan Umatch, a comprehensive P&L (Profit & Loss) analysis and forecasting platform. The application processes CSV financial data from Conta Azul accounting system, performs complex financial calculations, and provides dashboard analytics with AI-powered insights.

**Tech Stack:**
- **Backend:** Python 3.8+ with FastAPI framework
- **Data Processing:** pandas, numpy, scikit-learn for linear regression forecasting
- **Authentication:** JWT tokens with Argon2 password hashing
- **AI Integration:** OpenAI API (gpt-4o-mini, gpt-4o, gpt-4-turbo, gpt-3.5-turbo)
- **Frontend:** React with TypeScript (Vite)
- **Testing:** pylint for code quality

## Repository Structure

```
/
├── logic.py                    # Core P&L calculation engine
├── logic_CORRECTED.py          # Updated version with corrections
├── pnl_transactions.py         # FastAPI router for P&L transaction endpoints
├── test_upload.py              # CSV upload testing script
├── Makefile                    # Development commands (dev-backend, dev-frontend)
├── build.sh                    # Build script
├── .github/
│   └── workflows/
│       └── pylint.yml          # CI pipeline for code quality
└── [utility scripts]           # Analysis and implementation helper scripts
```

## Key Components

### 1. Financial Calculations (logic.py)
- **CSV Processing:** Multi-encoding support (utf-8, latin-1, iso-8859-1, cp1252) with flexible separators
- **P&L Computation:** 18 standard P&L lines including Revenue, COGS, OpEx, EBITDA, Net Income
- **Account Mapping:** Maps Conta Azul accounts to P&L categories via MappingItem model
- **Formula Engine:** Supports complex formulas for derived P&L lines
- **Forecasting:** Linear regression-based projections for future periods

### 2. API Endpoints (pnl_transactions.py)
- Authentication required via `get_current_user` dependency
- RESTful routes for P&L line transaction details
- Monthly/period filtering capabilities

### 3. Data Models
- `MappingItem`: Account-to-P&L-line mappings
- `PnLItem`: Individual P&L line data
- `PnLResponse`: Complete P&L report structure
- `DashboardData`: Aggregated KPIs and metrics

## Coding Standards

### Python Style
- Follow PEP 8 conventions
- Use type hints for all function parameters and returns
- Include docstrings for all public functions and classes
- Logging: Use the configured logger with appropriate levels (INFO, WARNING, ERROR)
- Error Handling: Comprehensive try-catch blocks with user-friendly error messages

### Financial Calculations
- **CRITICAL:** All financial calculations must be mathematically precise
- Use pandas DataFrames for data manipulation
- Validate calculations with the following invariants:
  - Total Revenue = Sum of all revenue streams
  - Gross Profit = Revenue - Payment Processing - COGS
  - EBITDA = Gross Profit - Operating Expenses
  - Net Income = EBITDA (no D&A in current model)
- Always maintain 2 decimal precision for currency values
- Test mathematical consistency between P&L and Dashboard data

### Data Processing
- **Encoding:** Always try multiple encodings (utf-8, latin-1, iso-8859-1, cp1252)
- **CSV Parsing:** Handle various separators (comma, semicolon, tab)
- **Required Columns:** Ensure 'Data de competência' column exists in CSV files
- **Date Handling:** Use datetime for all date operations
- **Missing Data:** Handle NaN values gracefully with appropriate defaults

### Security
- **Authentication:** All protected endpoints must use `Depends(get_current_user)`
- **Password Hashing:** Use Argon2 for password storage (never plain text)
- **Environment Variables:** Store sensitive data (SECRET_KEY, OPENAI_API_KEY) in .env files
- **Input Validation:** Sanitize and validate all user inputs
- **API Keys:** Never commit API keys or secrets to version control

### AI Integration
- **Valid Models:** Only use: gpt-4o-mini, gpt-4o, gpt-4-turbo, gpt-3.5-turbo
- **Error Handling:** Gracefully handle API failures with fallback responses
- **Rate Limiting:** Implement appropriate retry logic for API calls

## Development Workflow

### Starting Development
```bash
# Backend
make dev-backend

# Frontend (if applicable)
make dev-frontend
```

### Testing Requirements
1. **Pre-commit:** Run pylint on modified Python files
2. **Unit Tests:** Create tests for new calculation logic
3. **Integration Tests:** Verify CSV upload → P&L → Dashboard flow
4. **Mathematical Validation:** Ensure all financial calculations maintain invariants
5. **Edge Cases:** Test with empty data, malformed CSVs, missing columns

### Code Quality
- All code must pass pylint without errors
- CI pipeline (pylint.yml) runs on every push
- Python versions: 3.8, 3.9, 3.10 supported

## Common Tasks

### Adding a New P&L Line
1. Update the P&L line enumeration/constants
2. Add calculation logic in `logic.py`
3. Update mapping system if needed
4. Add corresponding dashboard display logic
5. Write tests to validate calculations

### Modifying Financial Formulas
1. Document the mathematical formula clearly in code comments
2. Update both `logic.py` and `logic_CORRECTED.py` if applicable
3. Add test cases with known inputs/outputs
4. Verify invariants still hold (e.g., Revenue = sum of components)

### Adding New CSV Formats
1. Add encoding/separator to the detection loop in `process_upload()`
2. Map new column names to expected fields
3. Test with sample files
4. Handle edge cases (missing columns, date formats)

## Common Pitfalls to Avoid

❌ **DON'T:**
- Use non-existent OpenAI models (e.g., gpt-5, gpt-5.1, gpt-5-nano)
- Store passwords in plain text (always use Argon2 hashing)
- Commit .env files or API keys
- Remove financial validation checks
- Modify calculation logic without testing mathematical invariants
- Use unvalidated user input in SQL/queries
- Deploy without setting SECRET_KEY and OPENAI_API_KEY

✅ **DO:**
- Validate all financial calculations with test data
- Use existing helper functions for CSV parsing
- Maintain backward compatibility with existing P&L structure
- Document complex financial formulas
- Use type hints and docstrings
- Follow the existing code patterns
- Test with multiple CSV encodings and formats

## Environment Variables

Required in `.env` file:
```bash
SECRET_KEY=<32+ character random string>  # For JWT tokens
OPENAI_API_KEY=sk-proj-...               # For AI insights
FRONTEND_URL=<frontend URL>              # CORS configuration
```

Generate SECRET_KEY:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Important Notes for AI Assistants

1. **Financial Accuracy is Critical:** This application handles real financial data. All calculations must be precise and thoroughly tested.

2. **Data Validation:** The application processes CSV files with various formats. Always maintain robust error handling and validation.

3. **Security First:** Authentication and authorization are non-negotiable. Never bypass security checks.

4. **Maintain Compatibility:** Changes to core calculation logic may affect existing saved mappings and reports. Consider backward compatibility.

5. **Follow Established Patterns:** The codebase has established patterns for CSV processing, P&L calculations, and API endpoints. Follow these patterns for consistency.

## Getting Help

- Review `EXECUTIVE_SUMMARY.md` for comprehensive project validation details
- Check `QUICK_DEPLOY_GUIDE.md` for deployment instructions
- Examine `FINAL_VALIDATION_REPORT.md` for testing methodology
- Study existing code patterns in `logic.py` for calculation examples

---

**Last Updated:** 2025-12-18  
**Maintained for:** GitHub Copilot Coding Agent

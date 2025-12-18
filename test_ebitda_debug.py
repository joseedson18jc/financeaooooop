import pandas as pd
from logic import process_upload, calculate_pnl, get_initial_mappings

csv_data = """Data de competência,Valor (R$),Tipo,Centro de Custo 1,Nome do fornecedor/cliente,Categoria 1
31/01/2024,10000.00,Entrada,Google Play Net Revenue,GOOGLE BRASIL PAGAMENTOS LTDA,Receita Aplicativo
31/01/2024,5000.00,Entrada,App Store Net Revenue,App Store (Apple),Receita Aplicativo
31/01/2024,1000.00,Entrada,Rendimentos de Aplicações,CONTA SIMPLES,Rendimentos
31/01/2024,-500.00,Saída,Web Services Expenses,AWS,Custo Servidor
31/01/2024,-300.00,Saída,Web Services Expenses,Cloudflare,Custo CDN
31/01/2024,-2000.00,Saída,Marketing & Growth Expenses,MGA MARKETING LTDA,Marketing
31/01/2024,-3000.00,Saída,Wages Expenses,FOLHA DE PAGAMENTO LTDA,Salários
31/01/2024,-500.00,Saída,Tech Support,ZENDESK,Suporte
31/01/2024,-200.00,Saída,Other Expenses,Devolução,Estorno"""

df = process_upload(csv_data.encode('utf-8'))
mappings = get_initial_mappings()
pnl = calculate_pnl(df, mappings)

# Find EBITDA line (line 13)
for row in pnl.rows:
    if row.line_number == 13:
        print(f"EBITDA (Line 13): {row.values}")
        for month, val in row.values.items():
            print(f"  Month {month}: R$ {val:,.2f}")
    if row.line_number == 7:
        print(f"Gross Profit (Line 7): {row.values}")
    if row.line_number == 8:
        print(f"OpEx Total (Line 8): {row.values}")
    if row.line_number == 9:
        print(f"Marketing (Line 9): {row.values}")
    if row.line_number == 10:
        print(f"Wages (Line 10): {row.values}")
    if row.line_number == 11:
        print(f"Tech Support (Line 11): {row.values}")
    if row.line_number == 12:
        print(f"Other Expenses (Line 12): {row.values}")

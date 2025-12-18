import pandas as pd
from logic import process_upload, get_initial_mappings, normalize_text_helper

csv_data = """Data de competência,Valor (R$),Tipo,Centro de Custo 1,Nome do fornecedor/cliente,Categoria 1
31/01/2024,-500.00,Saída,Tech Support,ZENDESK,Suporte"""

df = process_upload(csv_data.encode('utf-8'))
print("Processed DataFrame:")
print(df[['Centro de Custo 1', 'Nome do fornecedor/cliente', 'Valor_Num']])

mappings = get_initial_mappings()
print("\nChecking mappings for 'tech support':")
for m in mappings:
    cc_norm = normalize_text_helper(m.centro_custo)
    if 'tech' in cc_norm or 'support' in cc_norm:
        print(f"  CC: {m.centro_custo}, Supplier: {m.fornecedor_cliente}, Line: {m.linha_pl}")

print("\nNormalized cost center from data:", normalize_text_helper("Tech Support"))
print("Normalized cost center from mapping:", normalize_text_helper("Tech Support & Services"))

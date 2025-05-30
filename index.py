from flask import Flask, request, send_file, render_template
import pandas as pd

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        archivo_sii = request.files['file']
        if not archivo_sii:
            return 'No se subió ningún archivo.'
        try:
            df_sii = pd.read_csv(archivo_sii, encoding='latin1', sep=None, engine='python', dtype=str)
            df_sii.columns = df_sii.columns.str.strip()
            df_filtrado = df_sii[df_sii['Nro'].astype(str) == '33']
            rut_proveedores = df_filtrado['Tipo Compra'].dropna().reset_index(drop=True)
            folios = df_filtrado['Razon Social'].astype(str).dropna().reset_index(drop=True)
            df_base = pd.read_csv('archivo_base_fijo.csv', encoding='latin1', sep=';', dtype=str)
            min_filas = min(len(rut_proveedores), len(folios))
            df_modificada = df_base.iloc[:min_filas].copy()
            df_modificada['Rut-DV'] = rut_proveedores[:min_filas]
            df_modificada['Folio_Doc'] = folios[:min_filas]
            output_path = 'archivo_modificado.csv'
            df_modificada.to_csv(output_path, index=False, sep=';', encoding='latin1')
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            return f'Error al procesar el archivo: {e}'
    return render_template('index.html')

def handler(request):
    return app
from flask import Flask, request, send_file
from flask_cors import CORS
import pandas as pd
import io

app = Flask(__name__)
# Permite que seu site no GitHub Pages converse com este servidor
CORS(app)

@app.route('/')
def home():
    return "API do Conversor está Online!"

@app.route('/converter', methods=['POST'])
def converter():
    if 'file' not in request.files:
        return "Nenhum arquivo enviado", 400
    
    file = request.files['file']
    
    try:
        # Lê o Excel (Pega a primeira aba por padrão)
        # O Pandas é muito mais eficiente com memória que o navegador
        df = pd.read_excel(file)
        
        # Formata colunas de data para dia/mês/ano
        # Ajuste aqui se precisar de formatos específicos
        for col in df.select_dtypes(include=['datetime64']).columns:
            df[col] = df[col].dt.strftime('%d/%m/%Y')

        # Salva o resultado na memória (buffer)
        output = io.BytesIO()
        df.to_csv(output, sep=';', index=False, encoding='utf-8-sig')
        output.seek(0)
        
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f"{file.filename.split('.')[0]}.csv"
        )

    except Exception as e:
        return f"Erro no processamento: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# climate.py

from data_validation import validar_string
from database import connect_to_db
import requests
import os
from datetime import datetime

def registrar_dados_climaticos():
    """
    Registra novos dados climáticos no banco de dados Oracle.
    """
    localizacao = input("Localização (cidade): ")
    localizacao = validar_string(localizacao, "Localização")
    if localizacao is None:
        return

    # Obter a chave de API das variáveis de ambiente
    api_key = os.getenv('92cfd369706cc347d8a6280dfb9f31e5')
    if not api_key:
        print("Chave de API não configurada. Defina a variável de ambiente OPENWEATHER_API_KEY.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={localizacao}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        dados = response.json()

        if dados.get('cod') != 200:
            print(f"Erro ao obter dados climáticos: {dados.get('message')}")
            return

        temperatura = dados['main']['temp']
        umidade = dados['main']['humidity']
        precipitacao = dados['rain']['1h'] if 'rain' in dados and '1h' in dados['rain'] else 0

    except Exception as e:
        print(f"Erro ao obter dados climáticos: {e}")
        return

    data_registro = datetime.now()

    # Calcular ETo (simplificado)
    eto = (0.408 * (temperatura + 17.8)) / (temperatura + 237.3)

    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = """
                INSERT INTO dados_climaticos (data_registro, localizacao, temperatura, umidade, precipitacao, eto)
                VALUES (:data_registro, :localizacao, :temperatura, :umidade, :precipitacao, :eto)
            """
            cursor.execute(sql, {
                'data_registro': data_registro,
                'localizacao': localizacao,
                'temperatura': temperatura,
                'umidade': umidade,
                'precipitacao': precipitacao,
                'eto': eto
            })
            connection.commit()
            print("Dados climáticos registrados com sucesso!")
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Erro ao registrar dados climáticos: {error.message}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Não foi possível conectar ao banco de dados.")
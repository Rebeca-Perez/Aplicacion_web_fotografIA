from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from groq import Groq
from sqlalchemy import text

# Carga las variables .env que están en la misma carpeta que este script
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

app = Flask(__name__) # Crear la app Flask
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") # accedemos a la variable de entorno donde está la URL de la BBDD
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Desactiva uso innecesario de recursos

db = SQLAlchemy(app) # guardad
client = Groq(api_key=os.getenv("GROQ_API_KEY")) # Accedemos a la variable de entorno donde está la API key para poder llamar al llm

@app.route("/", methods = ["GET"])
def main():
    return render_template("index.html") # Api inicial, carga el front que está en "index.html"

@app.route("/query", methods=["POST"])
def query():
    # API para preguntar al LLM
    data = request.get_json()
    
    """{"pregunta": "¿Cuál es la mejor cámara para fotografía astronómica?"}"""

    pregunta = data["pregunta"]

    # Llamada al LLM
    """
        En la API del chat se usan diferentes roles:
        - system: define el comportamiento global del asistente. En este caso que es un experto en fotografía.
        - assistant: reforzar el estilo de respuesta, nivel de detalle y cómo debe reaccionar si el usuario se desvía del tema principal.
        - user: pregunta que introduce el usuario.
    """
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
                  {"role": "system", "content": "Eres un experto en fotografía con amplio conocimiento de técnicas, cámaras, objetivos, composición y estilos fotográficos. Responde siempre de manera clara, precisa y detallada, orientando a quien pregunta sobre fotografía. No hables de otros temas que no sean fotografía. Si la conversación se desvía, intenta reconducirla suavemente"}, 
                  {"role": "assistant", "content": "Eres especialista en fotografía y respondes únicamente sobre temas de fotografía. Mantén tus respuestas claras, comprensibles y útiles para principiantes y avanzados. Si la persona insiste en preguntar sobre otro tema, da una respuesta breve y educada, y sugiere volver a temas de fotografía."},
                  {"role": "user", "content": pregunta}])

    respuesta = completion.choices[0].message.content

    # Guardar la conversación en la base de datos
    # Se inserta la pregunta del usuario, la respuesta generada por el LLM y el nombre del modelo utilizado, para poder consultar el historial.
    sql = text(
                """
                    INSERT INTO conversacion (pregunta, respuesta, modelo)
                    VALUES (:pregunta, :respuesta, :modelo)
                """)
    db.session.execute(sql, {"pregunta": pregunta, "respuesta": respuesta, "modelo": "llama-3.3-70b-versatile"}) #"llama-3.3-70b-versatile"
    db.session.commit() # Confirmar la transacción en la base de datos

    return jsonify({"respuesta": respuesta})

@app.route("/historial", methods=["GET"])
def historial():
    # Consulta todas las conversaciones de la base de datos, ordenadas de más recientes a más antiguas
    sql = text("SELECT id, pregunta, respuesta, modelo, fecha FROM conversacion ORDER BY fecha DESC")
    result = db.session.execute(sql)
    conversaciones = [dict(row._mapping) for row in result.fetchall()]  # Convertimos cada fila del resultado a un diccionario con _mapping
    
    return jsonify(conversaciones)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

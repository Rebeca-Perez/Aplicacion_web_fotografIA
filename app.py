from flask import Flask, request, jsonify, render_template
import os
from datetime import datetime
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from groq import Groq
from sqlalchemy import text

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/", methods = ["GET"])
def main():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    
    """{"pregunta": "¿Cuál es la mejor cámara para fotografía astronómica?"}"""

    pregunta = data["pregunta"]

    # Llamada al LLM
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
                  {"role": "system", "content": "Eres un experto en fotografía con amplio conocimiento de técnicas, cámaras, objetivos, composición y estilos fotográficos. Responde siempre de manera clara, precisa y detallada, orientando a quien pregunta sobre fotografía. No hables de otros temas que no sean fotografía. Si la conversación se desvía, intenta reconducirla suavemente"}, 
                  {"role": "assistant", "content": "Eres especialista en fotografía y respondes únicamente sobre temas de fotografía. Mantén tus respuestas claras, comprensibles y útiles para principiantes y avanzados. Si la persona insiste en preguntar sobre otro tema, da una respuesta breve y educada, y sugiere volver a temas de fotografía."},
                  {"role": "user", "content": pregunta}])
    
    respuesta = completion.choices[0].message.content

    # Guardar en la BBDD
    sql = text(
                """
                    INSERT INTO conversacion (pregunta, respuesta, modelo)
                    VALUES (:pregunta, :respuesta, :modelo)
                """)
    db.session.execute(sql, {"pregunta": pregunta, "respuesta": respuesta, "modelo": "llama-3.3-70b-versatile"}) #"llama-3.3-70b-versatile"
    db.session.commit()

    return jsonify({"respuesta": respuesta})

@app.route("/historial", methods=["GET"])
def historial():
    sql = text("SELECT id, pregunta, respuesta, modelo, fecha FROM conversacion ORDER BY fecha DESC")
    result = db.session.execute(sql)
    conversaciones = [dict(row._mapping) for row in result.fetchall()]
    
    return jsonify(conversaciones)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

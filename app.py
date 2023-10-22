from flask import Flask, render_template, request
import main  # Asegúrate de que tu script main.py esté en el mismo directorio que app.py

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('page.html')

@app.route('/escarbar', methods=['POST'])
def escarbar():
    url = request.form.get('url')
    # Aquí debes llamar a la función en main.py que realiza el web scraping.
    # Asegúrate de que esta función acepte la URL como argumento.
    resultado = main.web_scraping(url)
    return render_template('resultado.html', resultado=resultado)  # Asume que tienes un archivo resultado.html para mostrar los resultados

if __name__ == '__main__':
    app.run(debug=True)

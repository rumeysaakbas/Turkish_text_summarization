from flask import Flask,render_template,request
import model
import summarize

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        button = request.form['button']
        
        if button == 'Özetle':
            summary = summarize.summarize_text(text)
            classification = ""
        elif button == 'Sınıflandır':
            summary = ""
            text_vector = model.create_vector(text)
            result = model.forest.predict([text_vector])
            classification = result[0]
        else:
            summary = ""
            classification = ""
        
        return render_template('index.html', summary=summary, classification=classification, text=text)
    
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug = True)
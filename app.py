from flask import Flask, render_template, request, redirect, url_for
import pickle
import re

app = Flask(__name__)

vector = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('phising.pkl','rb'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        cleaned_url = re.sub(r'http[s]?://|www\.|/.*$', '', url)

        result = model.predict(vector.transform([cleaned_url]))[0]

        if result == 'bad':
            predict = "This is a Phishing Website"
        else:
            predict = "This is a safe website"

        # 🔥 REDIRECT after POST
        return redirect(url_for('result', prediction=predict))

    return render_template('index.html')


@app.route('/result')
def result():
    prediction = request.args.get('prediction')
    return render_template('index.html', predict=prediction)


if __name__ == '__main__':
    app.run(debug=True)

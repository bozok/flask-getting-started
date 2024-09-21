from flask import Flask,render_template,abort,jsonify,request,redirect,url_for

from model import db,save_db

app = Flask(__name__,template_folder='templates',static_folder='static')


@app.route('/')
def welcome():
    return render_template('welcome.html',cards=db)

@app.route('/card/<int:index>')
def card_view(index):
    try:
        card = db[index]
        return render_template('card.html', card=card,index=index,max_index=len(db)-1 )
    except IndexError:
        abort(404)

@app.route('/add-card', methods=['GET', 'POST'])
def add_card():
    if request.method == 'POST':
        card = {
            'question': request.form.get('question'),
            'answer': request.form.get('answer')
        }
        db.append(card)
        save_db()
        return redirect(url_for('card_view', index=len(db)-1))
    else:
        return render_template('add_card.html')
    
@app.route('/remove-card/<int:index>', methods=['GET','POST'])
def remove_card(index):
    if request.method == 'GET':
        card=db[index]
        return render_template('remove_card.html', card=card)
    else:
        del db[index]
        save_db()
        return redirect(url_for('welcome'))
    


@app.route('/api/card')
def api_card_list():
    return jsonify(db)


@app.route('/api/card/<int:index>')
def api_card_detail(index):
    try:
        return db[index]
    except IndexError:
        abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
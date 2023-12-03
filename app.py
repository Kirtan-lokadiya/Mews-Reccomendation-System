from flask import Flask, render_template, url_for, request, redirect, session

def get_category_news_api(category):
    return
def get_full_news(category):
    return
def get_personalized_news(username):
    return

def get_content_reccomendation(abstract):
    return


users = {'user1':'12345', 'user2':'12345'}



app = Flask(__name__)
app.secret_key = '11111'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/category/<category>')
def category(category):
    category_news_data = get_category_news_api(category)
    return render_template('category.html', category=category, category_news= category_news_data)

@app.route('/full_news/<news_id>')
def full_news(news_id:str):
    full_news_data = get_full_news(news_id)
    content_recommendation_news = get_content_reccomendation(full_news_data.abstract)
    return render_template('full_news.html', full_news=full_news_data, news_id=news_id, content_recc=content_recommendation_news)

def get_next_news_id(current_news_id):
    # implement logic
    return

def get_previous_news_id(current_news_id):
    # implement logic
    return


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username] == password:
            session['user_logged_in'] = True
            session['current_user'] = username
            return redirect(url_for('personalized', username=username))
        else:
            error_message = 'Please check your login credentials'
            return render_template('login.html', error_message=error_message)
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_logged_in', None)
    session.pop('current_user', None)
    return redirect(url_for('home'))

@app.route('/personalized/<username>')
def personalized(username):
    personalized_news_data = get_personalized_news(username)
    return render_template('personalized.html', username=username, personalized_news=personalized_news_data)




if __name__ == "__main__":
    app.run(debug=True)
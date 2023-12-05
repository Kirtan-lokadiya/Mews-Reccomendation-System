from flask import Flask, render_template, url_for, request, redirect, session

from News_Reccomendation_System.pipeline.step4_prediction import user_based_rec_api, content_based_rec_api
from News_Reccomendation_System.pipeline.step5_trending_api import trending_api
from News_Reccomendation_System.pipeline.step6_fullnews_api import get_fullnews_api

# def trending_api(category):
#     return
# def get_fullnews_api(category):
#     return
# def user_based_rec_api(username):
#     return

# def content_based_rec_api(abstract):
#     return


users = {'U8125':'12345', 'user2':'12345'}



app = Flask(__name__)
app.secret_key = '11111'

@app.route('/')
def home():
    home_news_data = trending_api()
    return render_template('home.html',home_news= home_news_data, user_logged_in=session.get('user_logged_in', False), current_user=session.get('current_user', '') )

@app.route('/category/<category>')
def category(category):
    if session.get('user_logged_in', False):
        personalized_news_data = user_based_rec_api(session['current_user'], category)
        return render_template('category.html', category=category, category_news= personalized_news_data, user_logged_in=session.get('user_logged_in', False), current_user=session.get('current_user', ''))
    category_news_data = trending_api(category)
    return render_template('category.html', category=category, category_news= category_news_data, user_logged_in=session.get('user_logged_in', False), current_user=session.get('current_user', ''))

@app.route('/full_news/<news_id>')
def full_news(news_id):
    full_news_data = get_fullnews_api(news_id)
    content_recommendation_news = content_based_rec_api(news_id= news_id)
    return render_template('full_news.html', full_news=full_news_data, news_id=news_id, content_recc=content_recommendation_news, user_logged_in=session.get('user_logged_in', False), current_user=session.get('current_user', ''))



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
    
    return render_template('login.html', user_logged_in=session.get('user_logged_in', False), current_user=session.get('current_user', ''))

@app.route('/logout')
def logout():
    session.pop('user_logged_in', None)
    session.pop('current_user', None)
    return redirect(url_for('home'))

@app.route('/personalized/<username>')
def personalized(username, category=None):
    personalized_news_data = user_based_rec_api(username, category= category)
    return render_template('personalized.html', username=username, personalized_news=personalized_news_data, user_logged_in=session.get('user_logged_in', False), current_user=session.get('current_user', ''), category=category)




if __name__ == "__main__":
    app.run(debug=True)
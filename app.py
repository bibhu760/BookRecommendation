import pandas as pd
import numpy as np
from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df=pickle.load(open('popular.pkl', 'rb'))
pt=pickle.load(open('pt.pkl', 'rb'))
books=pickle.load(open('books.pkl', 'rb'))
similarity_score=pickle.load(open('similarity_score.pkl', 'rb'))


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html',
                           book_name= list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_rating'].values),
                           rating=list(popular_df['avg_rating'].values),
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_input=request.form.get('user_input')
    book_index=np.where(pt.index==user_input)[0][0]
    similar_items=sorted(list(enumerate(similarity_score[book_index])),key=lambda x:x[1],reverse=True)[1:6]
    data=[]
    for i in similar_items:
        item=[]
        tem_df=books[books['Book-Title']==pt.index[i[0]]] # to print all the details
        item.extend(list(tem_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(tem_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(tem_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    # print(data)
    # return data
    return render_template('recommend.html',data=data)

@app.route('/Contact')
def Contact():
    return render_template('Contact.html')


if __name__ == '__main__':
    app.run(debug=True)
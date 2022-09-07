import pandas as pd
from sklearn.feature_extraction.text  import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Book
   

def combined_features(row):   
    return row['author']+" "+ row['description']+" "+row['title']+" "+row['bookformat']

def get_title_from_index(df,index,score):
    return df[df.index == index]["title"].values[0],score

def get_index_from_id(df,id):
    return df[df.id == id].index.values[0]

def get_recommendation_for_book(book_id):
    df = pd.DataFrame(list(Book.objects.all().values()))
    features = ['description','author','title','bookformat']
    for feature in features:
        df[feature] = df[feature].fillna('')

    df['combined_features'] = df.apply(combined_features,axis =1)

    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined_features"])
    cosine_sim = cosine_similarity(count_matrix)
    id = get_index_from_id(df,book_id)

    similar_books = list(enumerate(cosine_sim[id]*100))
    # print(similar_books)

    # lambda x:x[1] means sorted according to 1 column i.e % of similarity, 0 means id
    sorted_similar_books = sorted(similar_books, key = lambda x: x[1], reverse=True)

    i =1
    b_ids=[]

    # [1:] to eliminate first value of loop
    for book in sorted_similar_books[1:]:
        print(b_ids.append(get_title_from_index(df,book[0],book[1])))
        i = i+1
        if i>20:
            break
        
    return b_ids

    
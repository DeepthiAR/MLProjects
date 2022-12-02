import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


class Recommendation:
    
    def __init__(self):
        self.data = pickle.load(open('./models/trimmed_data.pkl','rb'))
        self.user_based = pickle.load(open('./models/user_based.pkl','rb'))
        self.model = pickle.load(open('./models/logistic_regression_v1.pkl','rb'))
        self.raw_data = pd.read_csv("./data/sample30.csv")
        
        
    def getTopProducts(self, reviews_username):
        if reviews_username in self.user_based.index:
            items = self.user_based.loc[reviews_username].sort_values(ascending=False)[0:20].index
            features = pickle.load(open('./models/vocab_features.pkl','rb'))
            vectorizer = TfidfVectorizer(vocabulary = features)
            temp=self.data[self.data.id.isin(items)]
            X = vectorizer.fit_transform(temp['review'])
            temp=temp[['id']]   
            temp['prediction'] = self.model.predict(X)
            temp['prediction'] = temp['prediction'].map({'Postive':1,'Negative':0})
            temp=temp.groupby('id').sum()
            temp['positive_percent']=temp.apply(lambda x: x['prediction']/sum(x), axis=1)
            final_list=temp.sort_values('positive_percent', ascending=False).iloc[:5,:].index
            return self.data[self.data.id.isin(final_list)]['name'].drop_duplicates().values.tolist()
        else:
            return None
        
        


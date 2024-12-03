import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib

def predict_disease(symptoms, pipeline):
    symptoms_str = ' '.join(symptoms)
    return pipeline.predict([symptoms_str])[0]

def train_and_save(data_path, model_path):
    # Tiền xử lý dữ liệu
    data = pd.read_csv(data_path)
    data['All_Symptoms'] = data.fillna('').iloc[:, 1:].agg(' '.join, axis=1)
    X = data['All_Symptoms']
    y = data['Disease']

    # Chia dữ liệu thành tập huấn luyện và tập kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Tạo pipeline và huấn luyện mô hình
    pipeline = make_pipeline(CountVectorizer(), MultinomialNB())
    pipeline.fit(X_train, y_train)

    # Tính độ chính xác trên tập kiểm tra
    accuracy = pipeline.score(X_test, y_test) * 100
    # Lưu mô hình
    joblib.dump(pipeline, model_path)
    return accuracy

if __name__ == '__main__':
    data_path = './data/dataset_translated.csv'
    model_path = './models/pipeline.pkl'
    accuracy = train_and_save(data_path, model_path)
    print(f"Độ chính xác trên tập kiểm tra: {accuracy:.2f}%")
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib
from services.database import create_connection, execute_query

datasetmanager_bp = Blueprint('datasetmanager', __name__)


@datasetmanager_bp.route('/datasetmanager')
def datasetmanager():
    connection = create_connection()
    query = '''
        SELECT * FROM dataset ORDER BY id DESC
    '''
    dataset = execute_query(connection, query)

    return render_template('datasetmanager.html', dataset=dataset)


@datasetmanager_bp.route('/datasetmanager/<int:dataset_id>')
def dataset_detail(dataset_id):
    connection = create_connection()
    query = f'''
        SELECT * FROM dataset WHERE id = {dataset_id}
    '''
    dataset = execute_query(connection, query)
    return jsonify(dataset[0])


@datasetmanager_bp.route('/datasetmanager/update/', methods=['POST'])
def update_dataset():
    connection = create_connection()
    id = request.form['id']
    disease = request.form['disease']
    symptom_0 = request.form['symptom_0']
    symptom_1 = request.form['symptom_1']
    symptom_2 = request.form['symptom_2']
    symptom_3 = request.form['symptom_3']
    symptom_4 = request.form['symptom_4']
    symptom_5 = request.form['symptom_5']
    symptom_6 = request.form['symptom_6']
    symptom_7 = request.form['symptom_7']
    symptom_8 = request.form['symptom_8']
    symptom_9 = request.form['symptom_9']
    symptom_10 = request.form['symptom_10']
    symptom_11 = request.form['symptom_11']
    symptom_12 = request.form['symptom_12']
    symptom_13 = request.form['symptom_13']
    symptom_14 = request.form['symptom_14']
    symptom_15 = request.form['symptom_15']
    symptom_16 = request.form['symptom_16']
    is_valid = request.form['is_valid']
    query = f'''
        UPDATE dataset
        SET disease = '{disease}',
            symptom_0 = '{symptom_0}', 
            symptom_1 = '{symptom_1}', 
            symptom_2 = '{symptom_2}', 
            symptom_3 = '{symptom_3}', 
            symptom_4 = '{symptom_4}', 
            symptom_5 = '{symptom_5}', 
            symptom_6 = '{symptom_6}', 
            symptom_7 = '{symptom_7}', 
            symptom_8 = '{symptom_8}', 
            symptom_9 = '{symptom_9}', 
            symptom_10 = '{symptom_10}', 
            symptom_11 = '{symptom_11}', 
            symptom_12 = '{symptom_12}', 
            symptom_13 = '{symptom_13}', 
            symptom_14 = '{symptom_14}', 
            symptom_15 = '{symptom_15}', 
            symptom_16 = '{symptom_16}', 
            is_valid = {is_valid}
        WHERE id = {id}
    '''
    # print(query)
    res = execute_query(connection, query)
    # print(res)
    # flash('Add dataset successfully', 'success')
    return jsonify(200)


@datasetmanager_bp.route('/datasetmanager/delete/<int:dataset_id>', methods=['POST'])
def delete_dataset(dataset_id):
    connection = create_connection()
    query = f'''
        DELETE FROM dataset WHERE id = {dataset_id}
    '''

    execute_query(connection, query)
    return jsonify(200)

@datasetmanager_bp.route('/datasetmanager/add', methods=['POST'])
def add_dataset():
    connection = create_connection()
    disease = request.form['disease']
    symptom_0 = request.form['symptom_0']
    symptom_1 = request.form['symptom_1']
    symptom_2 = request.form['symptom_2']
    symptom_3 = request.form['symptom_3']
    symptom_4 = request.form['symptom_4']
    symptom_5 = request.form['symptom_5']
    symptom_6 = request.form['symptom_6']
    symptom_7 = request.form['symptom_7']
    symptom_8 = request.form['symptom_8']
    symptom_9 = request.form['symptom_9']
    symptom_10 = request.form['symptom_10']
    symptom_11 = request.form['symptom_11']
    symptom_12 = request.form['symptom_12']
    symptom_13 = request.form['symptom_13']
    symptom_14 = request.form['symptom_14']
    symptom_15 = request.form['symptom_15']
    symptom_16 = request.form['symptom_16']
    is_valid = request.form['is_valid']

    query = f'''
        INSERT INTO dataset (disease, symptom_0, symptom_1, symptom_2, symptom_3, symptom_4, symptom_5, symptom_6, symptom_7, symptom_8, symptom_9, symptom_10, symptom_11, symptom_12, symptom_13, symptom_14, symptom_15, symptom_16, is_valid)
    '''
    query += f'''
        VALUES ('{disease}', '{symptom_0}', '{symptom_1}', '{symptom_2}', '{symptom_3}', '{symptom_4}', '{symptom_5}', '{symptom_6}', '{symptom_7}', '{symptom_8}', '{symptom_9}', '{symptom_10}', '{symptom_11}', '{symptom_12}', '{symptom_13}', '{symptom_14}', '{symptom_15}', '{symptom_16}', {is_valid})
        '''
    execute_query(connection, query)
    flash('Add dataset successfully', 'success')
    return redirect(url_for('datasetmanager.datasetmanager'))


@datasetmanager_bp.route('/datasetmanager/train')
def train():
    try:
        connection = create_connection()
        query = '''
                SELECT * FROM dataset WHERE is_valid = 1
            '''
        dataset = execute_query(connection, query)
        df = pd.DataFrame(dataset)
        df.columns = ['id', 'Disease', 'symptom_0', 'symptom_1', 'symptom_2', 'symptom_3', 'symptom_4', 'symptom_5', 'symptom_6', 'symptom_7',
                      'symptom_8', 'symptom_9', 'symptom_10', 'symptom_11', 'symptom_12', 'symptom_13', 'symptom_14', 'symptom_15', 'symptom_16', 'is_valid']
        df['All_Symptoms'] = df.fillna('').iloc[:, 2:16].agg(' '.join, axis=1)
        x = df['All_Symptoms']
        y = df['Disease']
        pipeline = make_pipeline(CountVectorizer(), MultinomialNB())
        pipeline.fit(x, y)
        joblib.dump(pipeline, './models/pipeline.pkl')
        flash('Train successfully', 'success')
        return redirect(url_for('datasetmanager.datasetmanager'))
    except Exception as e:
        print(e)
        flash('Train failed', 'danger')
        return redirect(url_for('datasetmanager.datasetmanager'))

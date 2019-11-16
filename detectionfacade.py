from flask import Flask, jsonify, render_template
from system import inputprocessing, detection, extractor #, search
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from keras import backend as K

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v1.0/detectionfacade/content-based/url/<string:url>', methods=['GET'])
def execute_detection_url(url):
    extractor_obj = extractor.Extractor()
    extracted_news = extractor_obj.extract_news(url)
    print(extracted_news)

    if(extracted_news == 'error extract1' or extracted_news == 'error extract2'):
        return jsonify({'error': 'Maaf, masalah dengan laman web'})

    elif(extracted_news == 'invalid URL'):
        return jsonify({'error': 'Maaf, salah URL laman web'})

    else:
        return execute_detection_news(extracted_news)


@app.route('/api/v1.0/detectionfacade/content-based/news/<string:news>', methods=['GET'])
def execute_detection_news(news):
    detection_result = preprocess_detect(news)
    #ner, subjectivity, sentiment, topic, influencer = semantics(news)
    print(news)
    #return jsonify({'news': news, 'detection_result': detection_result, 'ner': ner, 'subjectivity': subjectivity, 'sentiment': sentiment, 'topic': topic, 'influencer': influencer})
    return jsonify({'news': news, 'detection_result': detection_result})


def preprocess_detect(news):
    inputprocessing_obj = inputprocessing.InputProcessing()
    clean_news = inputprocessing_obj.preprocess_news(news)
    padded_texts = inputprocessing_obj.vectorize_news('content', clean_news, 100)
    print(clean_news)
    news = ' '.join(clean_news)
    print(news)
    detection_obj = detection.Detection()
    results = detection_obj.detect_fake_news('content', padded_texts, news)
    try:
        K.clear_session()
    except Exception as e:
        print(e)
    return results


# def semantics(news):
#     semantic_object = semantic.Semantic()
#
#     ner_features, OTHER, law, location, organization, person, quantity, time, event = semantic_object.get_NER_features(news)
#     ner = {'OTHER':OTHER, 'law':law, 'location':location, 'organization':organization, 'person':person, 'quantity':quantity, 'time':time, 'event':event}
#
#     subjectivity = semantic_object.get_subjectivity(news)
#     sentiment = semantic_object.get_sentiment(news)
#     topic = semantic_object.get_topics(news)
#     influencer = semantic_object.get_influencer(news)
#
#     return ner, subjectivity, sentiment, topic, influencer


@app.route('/api/v1.0/detectionfacade/stance-based/url/<string:url>', methods=['GET'])
def execute_stance_detection_url(url):
    extractor_obj = extractor.Extractor()
    extracted_news = extractor_obj.extract_news(url)
    print(extracted_news)

    if(extracted_news == 'error extract'):
        return jsonify({'error': 'Maaf, masalah dengan laman web'})

    elif(extracted_news == 'invalid URL'):
        return jsonify({'error': 'Maaf, salah URL laman web'})

    else:
        return execute_stance_detection_news(extracted_news)


@app.route('/api/v1.0/detectionfacade/stance-based/news/<string:news>', methods=['GET'])
def execute_stance_detection_news(news):
    detection_results = preprocess_detect_stance(news)
    return jsonify({'detection_results': detection_results})


def preprocess_detect_stance(news):
    inputprocessing_obj = inputprocessing.InputProcessing()
    clean_penyataan = inputprocessing_obj.preprocess_news(news)
    padded_penyataan = inputprocessing_obj.vectorize_news('stance', clean_penyataan, 100)
    print(clean_penyataan)

    # searching_obj = search.Searching()
    # searched_results = searching_obj.search_news(keyword=news)
    #
    # detection_results = []
    #
    # for i in range(len(searched_results)):
    #
    #     clean_sumber = inputprocessing_obj.preprocess_news(searched_results[i]['title'])
    #     padded_sumber = inputprocessing_obj.vectorize_news('stance', clean_sumber, 2000)
    #     print(clean_sumber)
    #
    #     detection_obj = detection.Detection()
    #     label, fake_probability, real_probability = detection_obj.detect_fake_news('stance', [padded_penyataan, padded_sumber])
    #     print(label, fake_probability, real_probability)
    #
    #     detection_result = {i: {'label': label, 'fake_prob': float(fake_probability), 'real_prob': float(real_probability) }}
    #     detection_results.append(detection_result)
    #
    #     K.clear_session()
    #
    # return detection_results


# @app.route('/api/v1.0/detectionfacade/stance-based-cs/dev/news/<string:news>', methods=['GET'])
# def detect_using_stance_consine_similarity(news):

    # searching_obj = search.Searching()
    # searched_results = searching_obj.search_news(keyword=news)
    #
    # title_searched_results = []
    # title_searched_results.append(news)
    #
    # for data in searched_results:
    #     title_searched_results.append(data['title'])
    #
    # tfidf_vectorizer = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}')
    # tfidf_matrix_train = tfidf_vectorizer.fit_transform(title_searched_results)
    #
    # cs = cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix_train)
    #
    # real_count, fake_count = 0, 0
    #
    # for i in range(len(title_searched_results)):
    #     print(title_searched_results[i])
    #     print(cs[0][i])
    #
    #     if cs[0][i] < 0.3:
    #         fake_count += 1
    #     elif cs[0][i] > 0.3:
    #         real_count += 1
    #
    # print('Real: ', real_count, 'Fake: ', fake_count)
    #
    # if real_count >= 3:
    #     label = 'Real'
    #
    # elif fake_count > real_count:
    #     label = 'Fake'
    #
    # detection_result = {'label': label, 'fake_prob': float(fake_count/len(searched_results)), 'real_prob': float(real_count/len(searched_results)) }
    # return jsonify({'detection_result': detection_result})


# @app.route('/api/v1.0/detectionfacade/stance-based-model/dev/news/<string:news>', methods=['GET'])
# def detect_using_stance_model(news):
#
#     inputprocessing_obj = inputprocessing.InputProcessing()
#     clean_penyataan = inputprocessing_obj.preprocess_news(news)
#     padded_penyataan = inputprocessing_obj.vectorize_news('stance', clean_penyataan, 100)
#     print(clean_penyataan)
#
#     searching_obj = search.Searching()
#     searched_results = searching_obj.search_news(keyword=news)
#
#     real_count, fake_count, real_prob_count, fake_prob_count = 0, 0, 0, 0
#
#     for i in range(len(searched_results)):
#
#         clean_sumber = inputprocessing_obj.preprocess_news(searched_results[i]['title'])
#         padded_sumber = inputprocessing_obj.vectorize_news('stance', clean_sumber, 2000)
#         print(clean_sumber)
#
#         detection_obj = detection.Detection()
#         label, fake_probability, real_probability = detection_obj.detect_fake_news('stance', [padded_penyataan, padded_sumber])
#
#         print(label, fake_probability, real_probability)
#
#         fake_prob_count += 1
#         real_prob_count += 1
#
#         if label == 'Fake':
#             fake_count += 1
#         elif label == 'Real':
#             real_count += 1
#
#         K.clear_session()
#
#     print('Real: ', real_count, 'Fake: ', fake_count)
#     print('Real Prob: ', real_prob_count, 'Fake Prob: ', fake_prob_count)
#
#     if fake_count > 2 & fake_count < 6:
#         return 'Fake'
#
#     elif real_count > fake_count:
#         return 'Real'


if __name__ == '__main__':
    app.run(debug=True)

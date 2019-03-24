from interface import implements, Interface
from keras.models import load_model
from keras import backend as K
import pickle


class IDetection(Interface):

    def detect_fake_news(self, type, news, clean_news):
        pass



class Detection(implements(IDetection)):

    def detect_fake_news(self, type, news, clean_news):

        # load detection model
        detection_model = self.load_detection_model(type)

        # predict probability
        probabilities = detection_model.predict(news)

        # get probability according to its assosiated class
        class_label, fake_prob, real_prob = self.get_class_label(probabilities)
        print('CNN-GRU:', class_label, fake_prob, real_prob)

        K.clear_session()

        cnn_gru = {'label': class_label, 'fake_prob': float(fake_prob), 'real_prob': float(real_prob) }


        lr = pickle.load(open('./model/lr.sav', 'rb'))
        probabilities = lr.predict_proba([clean_news])
        class_label, fake_prob, real_prob = self.get_class_label(probabilities)
        print('LR:', class_label, fake_prob, real_prob)
        lr = {'label': class_label, 'fake_prob': float(fake_prob), 'real_prob': float(real_prob) }

        svm = pickle.load(open('./model/svm.sav', 'rb'))
        probabilities = svm.predict_proba([clean_news])
        class_label, fake_prob, real_prob = self.get_class_label(probabilities)
        print('SVM:', class_label, fake_prob, real_prob)
        svm = {'label': class_label, 'fake_prob': float(fake_prob), 'real_prob': float(real_prob) }

        knn = pickle.load(open('./model/knn.sav', 'rb'))
        probabilities = knn.predict_proba([clean_news])
        class_label, fake_prob, real_prob = self.get_class_label(probabilities)
        print('KNN:', class_label, fake_prob, real_prob)
        knn = {'label': class_label, 'fake_prob': float(fake_prob), 'real_prob': float(real_prob) }

        return {'cnn_gru': cnn_gru, 'lr': lr, 'svm': svm, 'knn': knn}


    def load_detection_model(self, type):
        if(type == 'content'):
            return load_model('./model/content_model.h5')
        elif(type == 'stance'):
            return load_model('./model/stance_model.h5')


    def get_class_label(self, probabilities):

        for probability in probabilities:
            fake_prob = probability[0]
            real_prob = probability[1]

            if(fake_prob > real_prob):
                class_label = 'Fake'
            elif(real_prob > fake_prob):
                class_label = 'Real'

        return class_label, fake_prob, real_prob
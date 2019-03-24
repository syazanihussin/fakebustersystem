from interface import implements, Interface
import malaya, operator



class ISemantic(Interface):

    def get_NER_features(self, news):
        pass

    def get_subjectivity(self, news):
        pass

    def get_sentiment(self, news):
        pass

    def get_topics(self, news):
        pass

    def get_influencer(self, news):
        pass

    def get_language(self, news):
        pass



class Semantic(implements(ISemantic)):

    def get_NER_features(self, news):
        try:
            bahdanau = malaya.entity.deep_model('bahdanau')
        except Exception as e:
            print(e)
            malaya.clear_cache('entity/bahdanau')
            bahdanau = malaya.entity.deep_model('bahdanau')

        ner_features = bahdanau.predict(news)
        print(ner_features)

        OTHER, law, location, organization, person, quantity, time, event = [], [], [], [], [], [], [], []

        for data in ner_features:
            if(data[1] == 'OTHER'):
                OTHER.append(data[0])
            elif(data[1] == 'law'):
                law.append(data[0])
            elif(data[1] == 'location'):
                location.append(data[0])
            elif(data[1] == 'organization'):
                organization.append(data[0])
            elif(data[1] == 'person'):
                person.append(data[0])
            elif(data[1] == 'quantity'):
                quantity.append(data[0])
            elif(data[1] == 'time'):
                time.append(data[0])
            elif(data[1] == 'event'):
                event.append(data[0])

        return ner_features, OTHER, law, location, organization, person, quantity, time, event


    def get_subjectivity(self, news):
        try:
            hierarchical = malaya.subjective.deep_model('hierarchical')
        except Exception as e:
            print(e)
            malaya.clear_cache('subjective/hierarchical')
            hierarchical = malaya.subjective.deep_model('hierarchical')
        subjectivity = hierarchical.predict(news)
        print(subjectivity)
        return subjectivity


    def get_sentiment(self, news):
        try:
            luong = malaya.sentiment.deep_model('luong')
        except Exception as e:
            print(e)
            malaya.clear_cache('sentiment/luong')
            luong = malaya.sentiment.deep_model('luong')
        sentiment = luong.predict(news)
        print(sentiment)
        return sentiment


    def get_topics(self, news):
        topic = malaya.topic_influencer.fuzzy_topic(news)
        print(topic)
        return topic


    def get_influencer(self, news):
        influencer = malaya.topic_influencer.fuzzy_influencer(news)
        print(influencer)
        return influencer


    def get_language(self, news):
        try:
            xgb = malaya.language_detection.xgb()
        except Exception as e:
            print(e)
            malaya.clear_cache('language-detection/xgb')
            xgb = malaya.language_detection.xgb()
        language = xgb.predict(news)
        print(language)

        return max(language)
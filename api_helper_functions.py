from google_play_scraper import app
from google.cloud import language_v1

from azure.core.credentials import AzureKeyCredential
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.ai.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials


VISION_API_KEY = "a213fbf607b041829b03643240c6218f"
VISION_API_ENDPOINT = "https://tiesdeepvision.cognitiveservices.azure.com/"

TEXT_API_KEY = "1b926c23338948078f054591fafb82e5"
TEXT_API_ENDPOINT = "https://congserviceappp.cognitiveservices.azure.com/"


def scrape_app_details(app_id='com.rovio.abclassic22'):
    app_data = app(app_id,
                   lang='en',  # defaults to 'en'
                   country='us'  # defaults to 'us'
                   )

    icon_url = app_data['icon']
    app_desc = app_data['description']
    comments_list = app_data["comments"][:10]  # we only take to 10 reviews

    return icon_url, app_desc, comments_list


def get_icon_tags_azure(icon_url):
    computervision_client = ComputerVisionClient(VISION_API_ENDPOINT, CognitiveServicesCredentials(VISION_API_KEY))
    tags_result = computervision_client.tag_image(icon_url)

    tags = []

    if (len(tags_result.tags) == 0):
        print("No tags detected.")
    else:
        for tag in tags_result.tags:
            #print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
            tags.append((tag.name, tag.confidence))

    return tags


def get_icon_description_azure(icon_url):
    computervision_client = ComputerVisionClient(VISION_API_ENDPOINT, CognitiveServicesCredentials(VISION_API_KEY))
    descriptions = computervision_client.describe_image(icon_url, 3, 'en')

    desc = []
    for caption in descriptions.captions:
        #print(caption.text)
        desc.append(caption.text)

    return desc


def get_text_entities_gcp(some_string):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=some_string, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_entities(request={"document": document})

    entity_scores = {}
    for entity in response.entities:
        # print('=' * 20)
        # print('         name: {0}'.format(entity.name))
        # print('         type: {0}'.format(entity.type))
        # print('     metadata: {0}'.format(entity.metadata))
        # print('     salience: {0}'.format(entity.salience))
        entity_scores[entity.name] = entity.salience

    return entity_scores


def get_reviews_sentiment_azure(reviews_list):

    azure_key_cred = AzureKeyCredential(TEXT_API_KEY)
    text_analytics_client = TextAnalyticsClient(TEXT_API_ENDPOINT, azure_key_cred)

    reviews_sentiment = text_analytics_client.analyze_sentiment(reviews_list, show_opinion_mining=True)
    docs = [doc for doc in reviews_sentiment if not doc.is_error]

    positives = []
    neutrals = []
    negatives = []

    #print("Let's visualize the sentiment of each of these documents")
    for idx, doc in enumerate(docs):
        # print(doc)

        # print(f"Document text: {reviews_list[idx]}")
        # print(f"Overall sentiment: {doc.sentiment}")

        pos = 0
        neutral = 0
        negative = 0

        for sentence in doc.sentences:
            conf_scores = sentence.confidence_scores
            pos += conf_scores.positive
            neutral += conf_scores.neutral
            negative += conf_scores.negative

        mean_pos = pos / len(doc.sentences)
        mean_neutral = neutral / len(doc.sentences)
        mean_negative = negative / len(doc.sentences)
        positives.append(mean_pos)
        neutrals.append(mean_neutral)
        negatives.append(mean_negative)

    # return the average positive, neutral, negative sentiment score
    return sum(positives) / len(positives), sum(neutrals) / len(neutrals), sum(negatives) / len(negatives)

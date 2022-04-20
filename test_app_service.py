from google_play_scraper import app

from azure.core.credentials import AzureKeyCredential
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from azure.ai.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials


VISION_API_KEY = "a213fbf607b041829b03643240c6218f"
VISION_API_ENDPOINT = "https://tiesdeepvision.cognitiveservices.azure.com/"

TEXT_API_KEY = "1b926c23338948078f054591fafb82e5"
TEXT_API_ENDPOINT = "https://congserviceappp.cognitiveservices.azure.com/"

def main():
    app_data = app('com.rovio.abclassic22',
                   lang='en',  # defaults to 'en'
                   country='us'  # defaults to 'us'
                   )

    icon_url = app_data['icon']
    comments_list = app_data["comments"][:10]

    print(icon_url)

    azure_key_cred = AzureKeyCredential(TEXT_API_KEY)

    computervision_client = ComputerVisionClient(VISION_API_ENDPOINT, CognitiveServicesCredentials(VISION_API_KEY))
    text_analytics_client = TextAnalyticsClient(TEXT_API_ENDPOINT, azure_key_cred)

    reviews_sentiment = text_analytics_client.analyze_sentiment(comments_list, show_opinion_mining=True)
    docs = [doc for doc in reviews_sentiment if not doc.is_error]

    print("Let's visualize the sentiment of each of these documents")
    for idx, doc in enumerate(docs):
        #print(doc)
        print(f"Document text: {comments_list[idx]}")
        print(f"Overall sentiment: {doc.sentiment}")

        pos = 0
        neutral = 0
        negative = 0

        for sentence in doc.sentences:
            conf_scores = sentence.confidence_scores
            pos += conf_scores.positive
            neutral += conf_scores.neutral
            negative += conf_scores.negative

        print(f"Positive score = {pos/len(doc.sentences)}, Neutral core = {neutral/len(doc.sentences)}, Negative score = {negative/len(doc.sentences)}")

    #print(reviews_sentiment)

    tags_result = computervision_client.tag_image(icon_url)
    descriptions = computervision_client.describe_image(icon_url, 3, 'en')

    if (len(tags_result.tags) == 0):
        print("No tags detected.")
    else:
        for tag in tags_result.tags:
            print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
    print()

    for caption in descriptions.captions:
        print(caption.text)



if __name__ == "__main__":
    main()

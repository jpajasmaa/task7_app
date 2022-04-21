from google_play_scraper import app


from api_helper_functions import *


def main():

    app_id = 'com.rovio.abclassic22'
    icon_url, app_desc, review_comments = scrape_app_details(app_id)

    icon_tags = get_icon_tags_azure(icon_url)
    print(f"Icon Tags: {icon_tags}")

    icon_desc = get_icon_description_azure(icon_url)
    print(f"Icon Description: {icon_desc}")

    description_entities = get_text_entities_gcp(app_desc)
    print(f"Key game features (description entities): {description_entities} ")

    positive, neutral, negative = get_reviews_sentiment_azure(review_comments)
    print(f"Review Sentiments: Positive({positive}), Neutral({neutral}), Negative({negative})")



if __name__ == "__main__":
    main()

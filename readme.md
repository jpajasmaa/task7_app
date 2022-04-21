To use the the GCP services we need to do some setup. We will broadly follow this guide: https://cloud.google.com/natural-language/docs/sentiment-tutorial#audience

1. First you will need to install gcp CLI and then initialise it using your google account: https://cloud.google.com/sdk/docs/initializing
  - Install the CLI, run gcloud init, follow the steps to setup new config and login using your google account, and select the dlforcc-task7-app project
2. Then run pip install requirements.txt from the root of this project to install needed packages
3. You will need to add path to credentials json (I have sent json credentials to you) to your environment e.g.: GOOGLE_APPLICATION_CREDENTIALS="C:\Users\Daniel\Documents\dlforcc-task7-app-408630bbbee4" 
4. Now the gcloud stuff should work :) You can test it along with the azure stuff by running test_app_servicy.py

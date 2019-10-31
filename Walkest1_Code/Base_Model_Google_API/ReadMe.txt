**Set up Google Cloud: https://cloud.google.com/speech-to-text/docs/quickstart-gcloud

**Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the file path of the JSON file that contains your service account key. This variable only applies to your current shell session, so if you **open a new session, set the variable again.
export GOOGLE_APPLICATION_CREDENTIALS='/Path/My_First_Project-96ad2ce7490d.json'

**Optionally Re-Initialize:
'/Path/google-cloud-sdk-258.0.0-linux-x86_64/google-cloud-sdk/bin/gcloud' init

**To use Google speech transcription API or Translation API, first install the Python libraries (be sure to have opted for the API or 'Cloud module' in your project, aswell as to have set the path to GOOGLE_APPLICATION_CREDENTIALS (see further above):
pip install --upgrade google-cloud-speech
pip install --upgrade google-cloud-translate

** Following Link shows example script to contact API
https://cloud.google.com/speech-to-text/docs/reference/libraries#client-libraries-install-python

**Transcribe a Wav file using my Script (code inspired from link above)
/path/Base_Model_Google_API/script_Google_Speech_transcribe_API.py /path/Base_Model_Google_API/Audio_test2015/



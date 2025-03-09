import sys
from dotenv import load_dotenv
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    Part,
)
from google.cloud import storage
import time
import csv

PDF_MIME_TYPE = "application/pdf"

summarization_prompt = """You are a very professional document summarization specialist and a philosopher. Given a document, your task is to provide a detailed summary of the content of the document.

If it includes images, provide descriptions of the images.
If it includes tables, extract all elements of the tables.
If it includes graphs, explain the findings in the graphs.
Do not include any numbers that are not mentioned in the document.
Answer in portuguese.
"""
# Load the Gemini 1.5 Flash model
model = GenerativeModel(
    "gemini-1.5-flash",
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH
    },
)
# This Generation Config sets the model to respond in JSON format.
generation_config = GenerationConfig(
    temperature=0.0, response_mime_type="application/json"
)


def print_multimodal_prompt(contents: list) -> None:
    """
    Given contents that would be sent to Gemini,
    output the full multimodal prompt for ease of readability.
    """
    for content in contents:
        if not isinstance(content, Part):
            print(content)
        elif content.inline_data:
            display_pdf(content.inline_data.data)
        elif content.file_data:
            gcs_url = (
                "https://storage.googleapis.com/"
                + content.file_data.file_uri.replace("gs://", "").replace(" ", "%20")
            )
            print(f"PDF URL: {gcs_url}")


# Send Google Cloud Storage Document to Vertex AI
def process_document(
    prompt: str,
    file_uri: str,
    mime_type: str = PDF_MIME_TYPE,
    generation_config: GenerationConfig | None = None,
    print_prompt: bool = False,
    print_raw_response: bool = False,
) -> str:
    # Load file directly from Google Cloud Storage
    file_part = Part.from_uri(
        uri=file_uri,
        mime_type=mime_type,
    )

    # Load contents
    contents = [file_part, prompt]

    # Send to Gemini
    response = model.generate_content(
        contents, generation_config=generation_config)

    if print_prompt:
        print("-------Prompt--------")
        print_multimodal_prompt(contents)

    if print_raw_response:
        print("\n-------Raw Response--------")
        print(response)

    return response.text


def main(argv):
    print("starting...")
    storage_client = storage.Client()
    blob_list = storage_client.list_blobs(
        "blog-files-2024", prefix="all/pdf2/")
    with open('files/posts_summ.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["summ", "url"])
        for blob_post in blob_list:
            blob_uri = 'gs://' + \
                blob_post.id[:-(len(str(blob_post.generation)) + 1)]
            if ".pdf" not in blob_uri:
                continue
            try:
                response_text = process_document(
                    summarization_prompt,
                    blob_uri
                )
                print(blob_uri)
                spamwriter.writerow(
                    [response_text.replace("\n", " "), blob_uri])
                time.sleep(10)
            except:
                response_text = process_document(
                    summarization_prompt,
                    blob_uri
                )
                print(blob_uri)
                try:
                    spamwriter.writerow(
                      [response_text.replace("\n", " "), blob_uri])
                except:
                    continue
                time.sleep(10)


if __name__ == "__main__":
    main(sys.argv)

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

PDF_MIME_TYPE = "application/pdf"

classification_prompt = """You are a document classification assistant. Given a document, your task is to find which category the document belongs to from the list of document categories provided below.

 Antropologia
 Ciência
 Crônica
 Educação
 Epistemologia
 Ética
 Liberdade
 Linguagem
 Marxismo
 Mente
 Ontologia Social
 Poesia
 Política
 Psicanálise
 Tecnologia

Which category does the above document belong to? Answer with one of the predefined document categories only.
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
    with open('files/posts_class.csv', 'a') as the_file:
        the_file.write("class|url\n")
        for blob_post in blob_list:
            blob_uri = 'gs://' + \
                blob_post.id[:-(len(str(blob_post.generation)) + 1)]
            if ".pdf" not in blob_uri: continue
            try:
                response_text = process_document(
                    classification_prompt,
                    blob_uri,
                    print_prompt=False,
                )
                new_line = response_text.rstrip()+"|"+blob_uri+"\n"
                print(new_line)
                the_file.write(new_line)
                time.sleep(10)
            except:
                response_text = process_document(
                    classification_prompt,
                    blob_uri,
                    print_prompt=False,
                )
                new_line = response_text.rstrip()+"|"+blob_uri+"\n"
                print(new_line)
                the_file.write(new_line)
                time.sleep(10)


if __name__ == "__main__":
    main(sys.argv)

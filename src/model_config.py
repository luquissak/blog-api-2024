from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    SafetySetting,
)


def call_model(model_name: str,
               temp: float,
               prompt: str,
               content: str,
               generation_config: GenerationConfig | None = None,
               print_raw_response: bool = False,
               ) -> str:
    contents = [content, prompt]
    model = GenerativeModel(
        model_name=model_name,
        safety_settings=[
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=HarmBlockThreshold.BLOCK_NONE,
    ),
        ]
    )
    generation_config = GenerationConfig(
        temperature=temp, response_mime_type="application/json", top_p=0.95, seed=0
    )
    response = model.generate_content(
        contents, generation_config=generation_config)

    if print_raw_response:
        print("\n-------Raw Response--------")
        print(response)

    modelResp = ModelResp(response.to_dict())
    return modelResp


class ModelResp:
    def __init__(self, dict_response):
        sr = list()
        sr.append(dict_response["candidates"][0]["safety_ratings"][0])
        sr.append(dict_response["candidates"][0]["safety_ratings"][1])
        sr.append(dict_response["candidates"][0]["safety_ratings"][2])
        sr.append(dict_response["candidates"][0]["safety_ratings"][3])
        self.modelVersion = dict_response["model_version"]
        self.safetyRatings = sr
        self.totalTokenCount = dict_response["usage_metadata"]["total_token_count"]
        self.finish_reason = dict_response["candidates"][0]["finish_reason"]
        if self.finish_reason != "STOP":
            self.text = """{"authors": [{\"author\": \"CENSURADO\"}]}"""
        else:
            self.text = dict_response["candidates"][0]["content"]["parts"][0]["text"]

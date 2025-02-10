from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
)


def call_model(
        model_name: str, temp: float,
    prompt: str,
    content: str,
    generation_config: GenerationConfig | None = None,
    print_raw_response: bool = False,
) -> str:
    contents = [content, prompt]
    model = GenerativeModel(
        model_name=model_name,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH
        },
    )
    generation_config = GenerationConfig(
        temperature=temp, response_mime_type="application/json"
    )
    response = model.generate_content(
        contents, generation_config=generation_config)

    if print_raw_response:
        print("\n-------Raw Response--------")
        print(response)
    
    dict_response = response.to_dict()
    ModelResp.modelVersion = dict_response["model_version"]    
#    ModelResp.safetyRatings.add(dict_response["candidates"][0]["safety_ratings"][0]["severity_score"])
#    ModelResp.safetyRatings.append(dict_response["candidates"][0]["safety_ratings"][1]["severity_score"])
#    ModelResp.safetyRatings.append(dict_response["candidates"][0]["safety_ratings"][2]["severity_score"])
#    ModelResp.safetyRatings.append(dict_response["candidates"][0]["safety_ratings"][3]["severity_score"])
    ModelResp.totalTokenCount = dict_response["usage_metadata"]["total_token_count"]
    ModelResp.text = dict_response["candidates"][0]["content"]["parts"][0]["text"]
    return ModelResp

class ModelResp:

    modelVersion: str
    safetyRatings: list
    totalTokenCount: str
    text: str
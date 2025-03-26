classification_prompt = "" \
    "You are a document classification assistant. Given a document, your task is to find which category the document belongs to from the list of document categories provided below. "  \
    " " \
    " Antropologia " \
    " Ciência " \
    " Crônica " \
    " Educação " \
    " Epistemologia " \
    " Ética " \
    " Liberdade " \
    " Linguagem " \
    " Marxismo " \
    " Mente " \
    " Ontologia Social " \
    " Poesia " \
    " Política " \
    " Psicanálise " \
    " Tecnologia " \
    " " \
    "Which category does the above document belong to? Answer with one of the predefined document categories ONLY. " \
    "The response must be a json with one field named as category and other the justification of the answer, in portuguese."

summarization_prompt = "" \
    "You are a very professional document summarization specialist and a philosopher. Given a document, your task is to provide a detailed summary of the content of the document. " \
    " " \
    "If it includes images, provide descriptions of the images. " \
    "If it includes tables, extract all elements of the tables. " \
    "If it includes graphs, explain the findings in the graphs. " \
    "Do not include any numbers that are not mentioned in the document. " \
    "Answer in portuguese. " \
    "The response must be a json with one field named as abstract, in portuguese."

authors_prompt = "" \
    "You are a document entity extraction specialist. Given a document, your task is to extract the text value of the following entities: " \
    "{ " \
	"'authors': [ " \
	"	{ " \
	"		'author': '', " \
	"	}  " \
	"], " \
   "}  " \
    "  " \
    "- The JSON schema must be followed during the extraction. " \
    "- The values must only include text found in the document " \
    "- Do not normalize any entity value. " \
    "- If an entity is not found in the document, set the entity value to null. " \
    "- An author is any person name or philosopher found in the document. " \
    "- If an author is not found in the document, set the entity value to Luis Quissak. "
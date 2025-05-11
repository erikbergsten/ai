import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json

openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI language model
llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4o")

system = """You are a kubernetes validating webhook. Use the set of rules and the AdmissionReview object to decide if a configuration should be accepted or not. Answer with a json object containing two keys:
    "allowed": boolean,
    "motivation": "a short description of why the configuration was allowed or not"

Do not include any markdown formatting like code blocks around the JSON.

the rules are as follows:
{rules}
"""

chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", system),
    ("user", "Configuration is {config}"),
])

# Create a chain using LCEL
chain = chat_prompt_template | llm

test_config = """
{"kind": "AdmissionReview", "apiVersion": "admission.k8s.io/v1", "request": {"uid": "228b8910-ad10-48aa-bee4-3d6657bb2955", "kind": {"group": "", "version": "v1", "kind": "ConfigMap"}, "resource": {"group": "", "version": "v1", "resource": "configmaps"}, "requestKind": {"group": "", "version": "v1", "kind": "ConfigMap"}, "requestResource": {"group": "", "version": "v1", "resource": "configmaps"}, "name": "food", "namespace": "default", "operation": "CREATE", "userInfo": {"username": "system:admin", "groups": ["system:masters", "system:authenticated"]}, "object": {"kind": "ConfigMap", "apiVersion": "v1", "metadata": {"name": "food", "namespace": "default", "uid": "217ff9e6-305b-4bf6-baa7-729f4826c15a", "creationTimestamp": "2025-05-10T18:02:32Z"}}, "oldObject": null, "dryRun": false, "options": {"kind": "CreateOptions", "apiVersion": "meta.k8s.io/v1", "fieldManager": "kubectl-create", "fieldValidation": "Strict"}}}
"""

rules = """
1. configmaps whos name starts with the letter b are not allowed
2. users can create resources in the default namespace
3. users can create resources in a namespace with their name
"""


def validate(config):
    raw = chain.invoke({"config": config, "rules": rules})
    print("Raw response:", raw)
    return json.loads(raw.content)

#print("parsed result:", validate(test_config))

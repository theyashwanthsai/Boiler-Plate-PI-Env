import verifiers as vf
from openai import OpenAI

# Load your environment
env = vf.load_environment("mcq")

# Test with a model
client = OpenAI()
results = env.evaluate_sync(
    client=client,
    model="gpt-4.1-mini"
)

print(results)
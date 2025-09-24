import os
from dotenv import load_dotenv
load_dotenv(override=True)
print("OPENAI_DISABLE_TRACING:", os.getenv("OPENAI_DISABLE_TRACING"))
print("LANGFUSE_HOST:", os.getenv("LANGFUSE_HOST"))
print("LANGFUSE_PUBLIC_KEY:", os.getenv("LANGFUSE_PUBLIC_KEY"))
print("SECRET length:", len(os.getenv("LANGFUSE_SECRET_KEY") or ""))

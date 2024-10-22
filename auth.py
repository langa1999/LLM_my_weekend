import os


def get_openai_api_key():
    os.getenv("OPENAI_API_KEY")


def get_railway_api_key():
    os.getenv("RAILWAY_API_KEY")


import os

from dotenv import load_dotenv

if __name__ == "__main__":
    # load_dotenv()
    print("Hello LangChain!")
    # print(os.environ.get("COOL_API_KEY"))

    summary_template: str = """
        given the information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
    """

import cohere
from cohere.classify import Example
import json
import pandas as pd


def read_json(file_path):

    blog_titles = []
    company_codes = []
    with open(file_path, "r") as json_file:
        # Load the contents of the file into a Python dictionary
        data = json.load(json_file)

        for item in data:
            # If the current item is a dictionary, check for the presence of "blog_content"
            if isinstance(item, dict):
                # If "blog_content" is in the keys of the dictionary, increment the count
                if "blog_title" in item.keys():
                    company_codes.append(item["company_code"])
                    blog_titles.append(item["blog_title"])
                    

    return blog_titles, company_codes


def classification_cohere(blog_title):
    co = cohere.Client(
        "E48S7IYUh8R5rNF2eLHdCraJ1FFYXecvBqkeuGFk"
    )  # This is your trial API key
    response = co.classify(
        model="large",
        inputs=[blog_title],
        
        examples=[
            Example(
                "When it comes to the energy transition, analyst sees the market making an error",
                "RA",
            ),
            Example("Cramer's lightning round: Chart Industries is not a buy", "RA"),
            Example("I can not recommend this stock.", "RA"),
            Example(
                "There’s still too much risk in stock and bond markets. Earn this easy 4.5% return while you wait for stability, says trader who hit 2 big calls in 2022.",
                "RA",
            ),
            Example(
                "Stocks making the biggest moves midday: Chevron, Tesla, United Rentals and more",
                "RT",
            ),
            Example(
                "You have to rely on not only what the company does, but on what the whole industry does.",
                "RN",
            ),
            Example(
                "Citi names its top biotech stock picks for 2023 and gives one 73% upside",
                "RT",
            ),
            Example(
                "'Big Short' Michael Burry Bets on a Stock Market Crash",
                "RT",
            ),
            Example(
                "Here's how to play the 'January Effect' rally happening now in small cap stocks",
                "RT",
            ),
            Example(
                "It is also creating more high-paid roles at its auto care centers and recruiting employees to become truck drivers.",
                "RN",
            ),
            Example(
                "His firm has an exchange-traded fund, the Hartford Longevity Economy ETF , designed to invest in the aging global population.",
                "RN",
            ),
            Example(
                "Genetic Technologies Shares Jump After Strategic Alliance With Qiagen",
                "RN",
            ),
        ],
    )

    return response.classifications


def predict(texts):
    for text in texts:
        text = str(text)
        try:
            start_index = text.index('prediction: "') + len('prediction: "')
            end_index = text.index('", confidence: ')
            prediction = text[start_index:end_index]
        except ValueError:
            print(
                "Error: The substring 'prediction: \"' was not found in the input string."
            )
            prediction = ""

        try:
            start_index = text.index("confidence: ") + len("confidence: ")
            end_index = text.index(", labels:")
            confidence = text[start_index:end_index]
        except ValueError:
            print(
                "Error: The substring 'confidence: ' was not found in the input string."
            )
            confidence = ""

        print('prediction: "' + prediction + '"')
        print("confidence: " + confidence)
        

    return prediction, 

def create_csv(blog_titles, company_codes, risk_profile, filename):
    df = pd.DataFrame(company_codes, columns=["company_codes"])
    df = pd.DataFrame(blog_titles, columns=["blog_titles"])
    df = pd.DataFrame(risk_profile, columns=["risk_profile"])
    file = df.to_csv(filename, index=False)
    return file


if __name__ == "__main__":
    file_path = r"C:\Users\Asad Ali\Desktop\News_Data.json"
    filename = r"C:\Users\Asad Ali\Desktop\News_Data_cohere.csv"
    blog_titles, company_codes = read_json(file_path)
    risk_profile = []
    for ind, blog_title in enumerate(blog_titles):
        print(blog_title)
        print(company_codes[ind])
        text = classification_cohere(blog_title)
        prediction = predict(text)
        prediction = str(prediction)
        print(prediction)
        risk_profile.append(prediction)
    file = create_csv(blog_titles, company_codes, risk_profile, filename)

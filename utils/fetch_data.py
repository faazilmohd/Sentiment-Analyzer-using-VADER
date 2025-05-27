import pandas as pd
import random
from faker import Faker

fake = Faker()

def load_csv_dataset(file):
    df = pd.read_csv(file)
    return df
def generate_dummy_data(n=100):
    sentiments = ["Joy", "Anger", "Surprise", "Positive", "Disgust", "Sadness", "Fear", "Neutral"]
    phrases = {
        "Joy": [
            "Absolutely thrilled with the new update 😍🔥 #awesome",
            "Can't believe how good this is! Made my day 😊 #joy",
            "This is the best experience I've had in a while 🙌💯",
            "Super happy with the results! Thanks @company 💕",
            "Loving the vibes here 🥰 #blessed"
        ],
        "Anger": [
            "This is absolutely unacceptable 😡 #fail",
            "I'm furious. Why can't they fix this already? 🤬",
            "Terrible service! Never buying from @brand again 👎",
            "Such a waste of money 💸😤 #angry",
            "The product broke after one day. What a joke 😠"
        ],
        "Surprise": [
            "Whoa! Didn't expect this to work so well 😲✨",
            "I’m actually shocked this turned out great 🤯 #pleasantlysurprised",
            "Unexpectedly amazing features 🔍👏",
            "Wow! That escalated quickly 😳🚀",
            "Surprised by the excellent customer care @support 👏"
        ],
        "Positive": [
            "Absolutely love it 😍 Everything works perfectly!",
            "So impressed with the build quality and finish ⭐⭐⭐⭐⭐",
            "Great value for money! Would definitely recommend 👍",
            "Everything went smoothly from order to delivery 📦",
            "A+ service and very user-friendly interface 💡"
        ],
        "Disgust": [
            "Totally grossed out 🤮 This is horrible!",
            "Such a disgusting experience. Never again 😤",
            "@company this is not acceptable 🤢",
            "The worst customer service I've encountered 💀",
            "Filthy, broken, and completely disappointing 😡"
        ],
        "Sadness": [
            "Feeling really down after that experience 😞",
            "Such a letdown, I expected better 💔",
            "Can't believe how disappointed I am right now 😢",
            "It's just so sad that it turned out this way 😔",
            "Heartbroken over how this unfolded 💧"
        ],
        "Fear": [
            "Honestly terrified of what might happen next 😱",
            "This situation is really scary 😨 #anxiety",
            "Feeling uneasy about the changes 😬",
            "Not sure how to handle this, genuinely worried 😰",
            "Hope everything turns out fine, but still nervous 😟"
        ],
        "Neutral": [
            "It’s okay, nothing special. Just average.",
            "Neither good nor bad, just meh 🤷",
            "Not much to say, pretty standard.",
            "I guess it’s fine, but not impressed.",
            "Okay experience, not noteworthy."
        ]
    }

    data = []
    for _ in range(n):
        sentiment = random.choice(sentiments)
        text = random.choice(phrases[sentiment])

        # Adding variety in text length and structure
        if random.random() > 0.7:
            text += " " + fake.sentence(nb_words=random.randint(5, 15))
        if random.random() > 0.5:
            text += " #trending #viral"

        user = fake.user_name() + str(random.randint(1, 999)) + random.choice(["", "_", "."])
        location = f"{fake.city()}, {fake.country()}"

        # Generate a rating correlated to sentiment
        if sentiment in ["Joy", "Positive", "Surprise"]:
            rating = round(random.uniform(4, 5), 1)
            score = round(random.uniform(0.5, 1), 3)
        elif sentiment in ["Anger", "Disgust", "Sadness", "Fear"]:
            rating = round(random.uniform(1, 3), 1)
            score = round(random.uniform(-1, -0.5), 3)
        else:
            rating = round(random.uniform(2, 4), 1)
            score = round(random.uniform(-0.2, 0.2), 3)

        data.append({
            "Username": f"@{user}",
            "Location": location,
            "Text": text,
            "ExpectedSentiment": sentiment,
            "Rating": rating,
            "Score": score
        })

    return pd.DataFrame(data)
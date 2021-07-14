from flask import Flask, render_template
from faker import Faker


fake = Faker(["en_US", "ro_RO"])

app = Flask(__name__)


def procure(type="main"):
    imw = 400
    imh = 400
    if type == "main":
        count = 7
    if type == "hero":
        count = 1
        imw = 900
    if type == "feed":
        count = 4

    ret = [
        dict(
            image=fake.image_url(imw, imh),
            category=fake.sentence(nb_words=2)[:-1],
            title=fake.paragraph(nb_sentences=1),
            author=fake.name_nonbinary(),
            posted=fake.date_this_year().strftime("%d %b %Y"),
        )
        for _ in range(count)
    ]

    if type == "main":
        ret[0] = {
            **ret[0],
            "image": fake.image_url(400, 1200),
        }

    return ret


@app.route("/")
def index():
    nav = [
        dict(
            link=t.lower().replace(" ", "-"),
            text=t,
        )
        for t in [fake.sentence(nb_words=2)[:-1] for _ in range(6)]
    ]
    text = [
        dict(
            type=t,
            content=procure(t),
            link=nav[i].get("link"),
        )
        for i, t in enumerate(["main", "feed", "hero", "main", "hero", "feed"])
    ]
    return render_template(
        "index.html",
        nav=nav,
        text=text,
    )


if __name__ == "__main__":
    app.run(debug=True)

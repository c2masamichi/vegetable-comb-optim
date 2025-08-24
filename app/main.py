import json

"""
source:
文部科学省:食品成分データベース
https://fooddb.mext.go.jp/
各栄養素は可食部100g当たりの数値
"""
VEGITABLES = [
    {
        "name": "にんじん",
        "VitaminA": 720,
        "VitaminC": 6,
    },
    {
        "name": "青ピーマン",
        "VitaminA": 33,
        "VitaminC": 76,
    },
    {
        "name": "ほうれんそう",
        "VitaminA": 350,
        "VitaminC": 35,
    },
]

class Result():
    def __init__(self, grams, nutrients):
        self.grams = grams
        self.nutrients = nutrients

def main():
    config = load_config()
    recommende_list = config['data']

    max_gram = 200
    division_gram = 50
    result = []

    # TODO: 再起処理に変更
    for i in range(0, max_gram+1, division_gram):
        for j in range(0, max_gram+1, division_gram):
            for k in range(0, max_gram+1, division_gram):
                names = [v["name"] for v in VEGITABLES]
                grams = {
                    names[0]: i,
                    names[1]: j,
                    names[2]: k,
                }
                nutrients = {
                    "VitaminA": 0,
                    "VitaminC": 0,
                }
                for key in nutrients:
                    nutrients[key] = sum([
                        VEGITABLES[x][key] * grams[names[x]] / 100 for x in range(3)
                    ])
                result.append(Result(grams=grams, nutrients=nutrients))

    max_sum = max_gram * 10
    for r in result:
        recommended_all_clear = True
        for nutrient in recommende_list:
            name = nutrient["name"]
            recommended = nutrient["recommended"]
            if r.nutrients[name] < recommended:
                recommended_all_clear = False
                break

        if recommended_all_clear:
            new_sum = sum(r.grams.values())
            if new_sum <= max_sum:
                max_sum = new_sum
                print(r.grams)
                print(r.nutrients)
                print('----------')


def load_config():
    with open('./config.json') as f:
        config = json.load(f)
        return config


if __name__ == '__main__':
    main()

from pprint import pprint as pp

def match_factor(feature_value: bool, answer: str) -> float:
    """
    feature_value : キャラが持つ特徴
    answer        : 'yes', 'no', 'unknown'
    """
    if answer == "yes":
        return 1.0 if feature_value else 0.1

    elif answer == "no":
        return 1.0 if not feature_value else 0.1

    # elif answer == "unknown":
    #     return 1.0

    else:
        return 1.0

    # raise ValueError("answer must be yes / no / unknown")


def update_probabilities(characters, prob, question_key, answer):
    # 重み更新
    new_prob = {}
    for c in characters:
        name = c["name"]
        feature_value = c["features"][question_key]
        k = match_factor(feature_value, answer)
        new_prob[name] = prob[name] * k

    # 正規化
    total = sum(new_prob.values())
    for name in new_prob:
        new_prob[name] /= total

    return new_prob


def choose_best_question(characters, remaining_keys):
    best_key = None
    best_diff = float("inf")

    for key in remaining_keys:
        trues = sum(c["features"][key] for c in characters)
        falses = len(characters) - trues
        diff = abs(trues - falses)

        if diff < best_diff:
            best_diff = diff
            best_key = key

    return best_key


def run_akinator(characters, threshold=0.9):
    prob = {c["name"]: 1 / len(characters) for c in characters}
    remaining_keys = list(characters[0]["features"].keys())

    step = 1
    while True:
        print(f"\n--- Step {step} ---")


        best_name = max(prob, key=prob.get)
        best_prob = prob[best_name]

        print("現在の確率:")
        pp(prob)
        # for k, v in prob.items():
        #     print(f"  {k}: {v:.3f}")

        if best_prob >= threshold:
            print(f"\n✅ 推定結果: {best_name} ({best_prob:.3f})")
            break

        if not remaining_keys:
            print("\n⚠ 質問が尽きました")
            print(f"最有力: {best_name} ({best_prob:.3f})")
            break

        # 最有力か、質問が尽きればここでゲーム終了。

        question_key = choose_best_question(characters, remaining_keys)  # 次の質問を取得。
        if question_key is None:
            print("⚠ 次の質問を選べません")
            break
        remaining_keys.remove(question_key) # 残ってる質問キーから次の質問を削除

        answer = ask_answer(question_key)   # ユーザーのアンサーを取得

        prob = update_probabilities(
            characters,
            prob,
            question_key,
            answer
        )   # 確立を更新。

        step += 1

def ask_answer(question_key: str) -> str:
    while True:
        ans = input(f"{question_key}? (yes / no / unknown): ").strip().lower()
        if ans in ("yes", "no", "unknown"):
            return ans
        print("⚠ yes / no / unknown のどれかで入力してください")



# 候補キャラクター
characters = [
    {
        "name": "Dora",
        "features": {
            "is_human": False,
            "can_fly": True,
        }
    },
    {
        "name": "Goku",
        "features": {
            "is_human": True,
            "can_fly": True,
        }
    },
    {
        "name": "Nobi",
        "features": {
            "is_human": True,
            "can_fly": False,
        }
    }
]


run_akinator(characters)

# # 初期確率
# prob = {c["name"]: 1 / len(characters) for c in characters}

# print("初期確率")
# for k, v in prob.items():
#     print(k, v)

# # 質問：「人間ですか？」→ yes
# prob = update_probabilities(
#     characters,
#     prob,
#     question_key="is_human",
#     answer="yes"
# )

# print("\n質問：人間ですか？ → yes")
# for k, v in prob.items():
#     print(k, round(v, 3))

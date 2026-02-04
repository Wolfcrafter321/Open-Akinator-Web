from pprint import pprint as pp

def match_factor(feature_value, answer: float) -> float:
    """
    feature_value : キャラが持つ特徴
    answer        : 'yes', 'no', 'unknown'
    """

    return 1.0 - abs(feature_value - answer)

    # if answer == "yes":
    #     return 1.0 if feature_value is True else 0.1

    # elif answer == "no":
    #     return 1.0 if feature_value is False else 0.1

    # elif answer == "unknown":
    #     return 1.0

    # raise ValueError("answer must be yes / no / unknown")


def update_probabilities(characters:dict, prob, question_key:str, answer: float) -> dict:
    # 重み更新
    new_prob = {}
    for c in characters:
        name = c["name"]
        feature_value = c["features"].get(question_key, None)

        if feature_value is None:
            k = 1.0
        else:
            k = match_factor(feature_value, answer)

        new_prob[name] = prob[name] * k

    # 正規化
    total = sum(new_prob.values())
    for name in new_prob:
        new_prob[name] /= total

    return new_prob


def choose_best_question(characters:list, remaining_keys:list) -> str:
    best_key = None
    best_diff = float("inf")

    for key in remaining_keys:
        p = sum(c["features"].get(key, 0) for c in characters) / len(characters)
        diff = abs(p - 0.5) # score が小さい質問を選ぶ

        if diff < best_diff:
            best_diff = diff
            best_key = key

    return best_key

def collect_all_features_key(characters):
    keys = set()
    for c in characters:
        keys.update(c["features"].keys())
    return list(keys)

def run_akinator(characters: list, threshold:float = 0.9, debug=False):
    prob = {c["name"]: 1 / len(characters) for c in characters}
    remaining_keys = collect_all_features_key(characters)

    step = 1
    while True:
        print(f"\n--- Step {step} ---")


        best_name = max(prob, key=prob.get)
        best_prob = prob[best_name]

        if(debug): print("現在の確率:")
        # pp(prob)
        for k, v in prob.items():
            if(debug): print(f"  {k}: {v:.3f}")

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


def ask_answer(question_key: str) -> float:
    while True:
        ans = input(f"{question_key}? (yes (y/1) / no (n/2) / unknown (u/3)): ").strip().lower()
        if ans in   ("yes",     "y", "1", "a", "z"): return 1.0
        elif ans in ("no",      "n", "2", "b", "x"): return 0.0
        elif ans in ("unknown", "u", "3", "c", "c"): return 0.5
        print("⚠ yes / no / unknown のどれかで入力してください")



# 候補キャラクター
characters = [
    {
        "name": "Dora",
        "features": {
            "is_human": 0.1,
            "can_fly": 0.9,
            "can_use_magic": 0.8,
            "is_robot": 1.0,
            "has_pocket": 1.0,
            "is_color_blue": 0.95,
            "is_weight_129.3kg": 1.0,
            "is_cat": 0.9,
            "is_boy": 1.0,
            "is_girl": 0.0,
        }
    },
    {
        "name": "Goku",
        "features": {
            "is_human": 1.0,
            "can_fly": 1.0,
            "can_use_magic": 0.7,
            "is_robot": 0.0,
            "is_weight_129.3kg": 0.0,
            "has_super_power": 1.0,
            "is_boy": 1.0,
            "is_girl": 0.0,
        }
    },
    {
        "name": "Nobi",
        "features": {
            "is_human": 1.0,
            "can_fly": 0.0,
            "can_use_magic": 0.0,
            "is_robot": 0.0,
            "is_weight_129.3kg": 0.0,
            "wearing_yellow_shirts": 1.0,
            "wearing_pink_shirts": 0.0,
            "has_glasses": 1.0,
            "has_super_power": 0.0,
            "is_boy": 1.0,
            "is_girl": 0.0,
        }
    },
    {
        "name": "Shizu",
        "features": {
            "is_human": 1.0,
            "can_fly": 0.0,
            "can_use_magic": 0.0,
            "is_robot": 0.0,
            "is_weight_129.3kg": 0.0,
            "wearing_yellow_shirts": 0.0,
            "wearing_pink_shirts": 1.0,
            "has_glasses": 0.0,
            "has_super_power": 0.0,
            "is_boy": 0.0,
            "is_girl": 1.0,
        }
    }
]

if __name__ == "__main__":
    run_akinator(characters, debug=1)

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


def update_probabilities(character:dict, prob, question_key:str, answer):
    # 重み更新
    new_prob = {}
    for c in characters:
        name = c["name"]
        # feature_value = c["features"][question_key]
        feature_value = c["features"].get(question_key, None)
        k = match_factor(feature_value, answer)
        new_prob[name] = prob[name] * k

    # 正規化
    total = sum(new_prob.values())
    for name in new_prob:
        new_prob[name] /= total

    return new_prob


def choose_best_question(characters:dict, remaining_keys:list) -> str:
    best_key = None
    best_diff = float("inf")

    for key in remaining_keys:
        trues = 0
        falses = 0
        # キャラが 10 人いるとし
        # いい質問をして絞れた数が小さい方をとる。
        # trues = sum(c["features"][key] for c in characters) # 全キャラで残ったキーの個数
        # falses = len(characters) - trues # キャラで消えたキーの個数
        for c in characters:
            v = c["features"].get(key, None) # 存在しないキーの場合は安全にNoneにする。
            if v is True: trues += 1
            elif v is False: falses += 1
        diff = abs(trues - falses) # 差分を計算

        # もし情報が意味のない場合、パス。(聞いても意味のない（誰も存在しない）ものなど。)
        if trues + falses == 0: continue

        if diff < best_diff:
            best_diff = diff
            best_key = key
            # 一番diffが小さいものを採択。

    return best_key

def collect_all_features_key(characters):
    keys = set()
    for c in characters:
        keys.update(c["features"].keys())
    return list(keys)

def run_akinator(characters: dict, threshold:float =0.9):
    prob = {c["name"]: 1 / len(characters) for c in characters}
    # remaining_keys = list(characters[0]["features"].keys())
    remaining_keys = collect_all_features_key(characters)

    step = 1
    while True:
        print(f"\n--- Step {step} ---")


        best_name = max(prob, key=prob.get)
        best_prob = prob[best_name]

        print("現在の確率:")
        # pp(prob)
        for k, v in prob.items():
            print(f"  {k}: {v:.3f}")

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
        ans = input(f"{question_key}? (yes (y/1) / no (n/2) / unknown (u/3)): ").strip().lower()
        if ans in ("yes", "no", "unknown"):
            return ans
        elif ans in ("y", "1"): return "yes"
        elif ans in ("n", "2"): return "no"
        elif ans in ("u", "3"): return "unknown"
        print("⚠ yes / no / unknown のどれかで入力してください")



# 候補キャラクター
characters = [
    {
        "name": "Dora",
        "features": {
            "is_human": False,
            "can_fly": True,
            "can_use_magic": True,
            "is_robot": True,
            "has_pocket": True,
            "is_color_blue": True,
        }
    },
    {
        "name": "Goku",
        "features": {
            "is_human": True,
            "can_fly": True,
            "can_use_magic": True,
            "is_robot": False,
        }
    },
    {
        "name": "Nobi",
        "features": {
            "is_human": True,
            "can_fly": False,
            "can_use_magic": False,
            "is_robot": False,
        }
    }
]

if __name__ == "__main__":
    run_akinator(characters)

import pickle


def test_to_files(filename: str) -> None:
    with open(f"data/{filename}", "w", encoding="utf-8") as file:
        file.write(str(filename))
    with open(f"data/{filename}.pkl", "wb") as f:
        pickle.dump(filename, f)

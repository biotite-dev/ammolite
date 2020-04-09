

def select(model_name, mask):
    index_selection = " or ".join(
        [f"index {i+1}" for i, is_selected in enumerate(mask) if is_selected]
    )
    complete_selection = f"model {model_name} and ({index_selection})"
    return complete_selection
def get_model_info(model_name):
    model_info_dict = {
        "llama3.2:3b":
        "Llama 3.2 3B: Um modelo menor e eficiente com 3 bilhões de parâmetros.",
        "llama3.1:8b":
        "Llama 3.1 8B: Um poderoso modelo de linguagem com 8 bilhões de parâmetros.",
        "llama3.3:70b":
        "Llama 3.3 70B: O maior modelo com 70 bilhões de parâmetros, oferecendo a maior precisão."
    }
    return model_info_dict.get(model_name,
                               "Informações do modelo não disponíveis.")

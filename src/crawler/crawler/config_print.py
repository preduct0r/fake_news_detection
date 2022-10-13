from dotenv import dotenv_values


def congif_print(adress):
    config = dotenv_values(adress)
    print(config)
from dotenv import dotenv_values

config = dotenv_values(".env")
token = config["Token"]

print(dotenv_values(".env")["Token"])
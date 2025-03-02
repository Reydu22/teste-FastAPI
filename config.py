from dotenv import load_dotenv
import os
load_dotenv()

DBU = os.getenv("DATABASE_URL")
SCK = os.getenv("SECRET_KEY")

print(DBU)
print(SCK)
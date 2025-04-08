from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://franklin:root@cluster0.l7g9j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URI)
collectionItem = client["laboratorio_ing_web"]
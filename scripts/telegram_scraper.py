import os
import csv
from dotenv import load_dotenv
from telethon import TelegramClient


load_dotenv()

class TelegramChannelScraper:
    

    def __init__(self, api_id, api_hash, session_name, media_dir='../data/photos', csv_file='../data/telegram_data.csv', channels=None):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_name = session_name
        self.media_dir = media_dir
        self.csv_file = csv_file
        self.channels = channels or []

      
        os.makedirs(self.media_dir, exist_ok=True)

    async def scrape_channel(self, client, channel_username, writer):
        
        entity = await client.get_entity(channel_username)
        channel_title = entity.title  

        print(f"Scraping all history from {channel_username}...") 

        async for message in client.iter_messages(entity, limit=None):
            media_path = await self.download_media(client, message, channel_username)
            
     
            writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])

        print(f"Successfully scraped all history from {channel_username}") 

   
    async def download_media(self, client, message, channel_username):
        
        if message.media and hasattr(message.media, 'photo'):
            filename = f"{channel_username}_{message.id}.jpg"
            media_path = os.path.join(self.media_dir, filename)
            await client.download_media(message.media, media_path)
            return media_path
        return None

    async def run(self):
      
        print("Starting the full history scraping process...") 
        async with TelegramClient(self.session_name, self.api_id, self.api_hash) as client:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])

                for channel in self.channels:
                    await self.scrape_channel(client, channel, writer)

if __name__ == "__main__":
    
    api_id = os.getenv('api_id')
    api_hash = os.getenv('api_hash')

 
    if not api_id or not api_hash:
        raise ValueError("Your API ID or Hash cannot be empty or None. Please check your .env file.")


    channels_to_scrape = [
        '@helloomarketethiopia',
      
    ]

  
    scraper = TelegramChannelScraper(api_id=api_id, api_hash=api_hash, session_name='../data/scraping_session', channels=channels_to_scrape)

    import asyncio
    asyncio.run(scraper.run())
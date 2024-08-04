from dadata import DadataAsync

from config_data.settings import get_settings

async def get_address(latitude, longitude):
    async with DadataAsync(token=get_settings().dadata.token) as connect:
        result = await connect.geolocate(name='address', lat=latitude, lon=longitude, radius_meters=100)
        return result[0]['value']
        
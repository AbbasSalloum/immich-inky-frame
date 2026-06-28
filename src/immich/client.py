import requests


class ImmichClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "x-api-key": api_key,
            "Accept": "application/json",
        }

    def _get(self, path: str):
        url = f"{self.base_url}{path}"

        response = requests.get(
            url,
            headers=self.headers,
            timeout=30,
        )

        response.raise_for_status()
        return response.json()

    def get_albums(self) -> list[dict]:
        return self._get("/albums")

    def find_album_by_name(self, album_name: str) -> dict | None:
        albums = self.get_albums()

        for album in albums:
            if album.get("albumName") == album_name:
                return album

        return None

    def get_album_assets(self, album_id: str) -> list[dict]:
        album = self._get(f"/albums/{album_id}")
        return album.get("assets", [])
    

    def download_asset(self, asset_id: str) -> bytes:
        url = f"{self.base_url}/assets/{asset_id}/original"

        response = requests.get(
            url,
            headers=self.headers,
            timeout=60,
        )

        response.raise_for_status()
        return response.content


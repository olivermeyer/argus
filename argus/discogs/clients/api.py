import requests

from argus.logger import logger


class DiscogsApiClient:
    base_url: str = "https://api.discogs.com"

    def _get(self, endpoint: str, token: str) -> dict:
        try:
            logger.info(f"GET {self.base_url}{endpoint}")
            response = requests.get(
                f"{self.base_url}{endpoint}",
                headers={"Authorization": f"Discogs token={token}"},
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to GET {self.base_url}{endpoint}: {e}")
            raise

    def get_username(self, token: str) -> str:
        return self._get("/oauth/identity", token)["username"]

    def get_wantlist_item_ids(self, token: str) -> list[int]:
        username = self.get_username(token)
        wantlist_items = self._get(f"/users/{username}/wants?per_page=100", token)[
            "wants"
        ]
        return [int(item["id"]) for item in wantlist_items]

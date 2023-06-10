from dataclasses import dataclass

from argus.clients.discogs.api.client import DiscogsApiClient


@dataclass
class FindNonMasterReleasesInListTask:
    """
    This task is used to find non-master releases in a user's lists.
    """
    discogs_api_client: DiscogsApiClient

    def execute(self):
        user = self.discogs_api_client.identity()
        for user_list in user.lists:
            print(user_list)
            for item in user_list.items:
                if item.type == "master":
                    continue
                if item.type == "release":
                    release = self.discogs_api_client.release(item.id)
                    if release.master:
                        print(f"  {release.url}")

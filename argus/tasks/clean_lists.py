from argus.tasks.abstract import AbstractTask


class CleanListsTask(AbstractTask):
    """
    This task is used to find non-master releases in a user's lists.
    """
    def execute(self):
        user = self.discogs_client.identity()
        for user_list in user.lists:
            print(user_list)
            for item in user_list.items:
                if item.type == "master":
                    continue
                if item.type == "release":
                    release = self.discogs_client.release(item.id)
                    if release.master:
                        print(f"  {release.url}")

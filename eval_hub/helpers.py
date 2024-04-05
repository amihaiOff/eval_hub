import dash_mantine_components as dmc


def create_user_avatar(size: str):
    return dmc.Avatar(
            src="https://avatars.githubusercontent.com/u/91216500?v=4",
            radius="xl",
            size=size,
        )

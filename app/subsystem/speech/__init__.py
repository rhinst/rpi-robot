from app.command import Command, Argument

commands = [
        Command(
            name="say",
            arguments=[
                Argument(
                    name="phrase",
                    type=str,
                    required=True
                )
            ]
        )
    ]

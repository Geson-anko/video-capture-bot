import asyncio
import logging
import os
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import discord
import ffmpeg
import tyro
from discord.flags import Intents
from dotenv import load_dotenv

from video_recording_bot.obs_client import ObsClient

logger = logging.getLogger(__name__)


@dataclass
class Args:

    # Message configurations
    post_message: str = ""
    """Message when posting to Discord."""
    date_format: str = "%Y/%m/%d %H:%M:%S"
    """Date string format"""

    # Obs websocket configurations
    obs_ws_host: str = "127.0.0.1"
    """Address of obs websocker server."""
    obs_ws_port: int = 4455
    """Port of obs websocket server."""
    # NOTE: Please write password to `.env` file if you set it.

    # Video Configurations.
    video_duration: float = 30  # [sec]
    """Length of video [seconds], default is 30 secs."""
    recording_interval: float = 45 * 60  # [sec]
    """Interval for next recording. default is 45 mins."""
    video_width: int = 1280
    """Width of video."""
    video_height: int = 720
    """Height of video."""
    video_bitrate: str = "1000k"
    """Bitrate of video."""


def convert_video(input_path: str, output_path: str, resolution: tuple[int, int], bitrate: str) -> None:
    (
        ffmpeg.input(input_path)
        .output(output_path, vf=f"scale={resolution[0]}:{resolution[1]}", video_bitrate=bitrate)
        .overwrite_output()
        .run()
    )


def get_temp_video_path() -> Path:
    temp_video_dir = Path(tempfile.TemporaryDirectory().name)
    temp_video_dir.mkdir()
    return temp_video_dir / "video.mp4"


class Bot(discord.Client):
    def __init__(self, args: Args, intents: Intents, **options: Any) -> None:
        super().__init__(intents=intents, **options)

        self.args = args
        self.obs_client = ObsClient(
            host=args.obs_ws_host, port=args.obs_ws_port, password=str(os.environ["OBS_WEB_SOCKET_PASSWORD"])
        )
        self.target_channel_id = int(os.environ["DISCORD_POST_CHANNEL_ID"])

    async def on_ready(self) -> None:
        logger.info(f"Logged on as {self.user}!")
        self.loop.create_task(self.main_loop())

    async def main_loop(self) -> None:
        logger.info("Start main loop!")

        video_path_for_post = str(get_temp_video_path())
        channel = self.get_channel(int(os.environ["DISCORD_POST_CHANNEL_ID"]))

        if channel is None:
            raise RuntimeError("Specified channel id does not exists!")

        while True:
            current_time = datetime.now().strftime(self.args.date_format)
            logger.info(f"Start recording...: {current_time}")
            video_path = await self.obs_client.record(self.args.video_duration)
            logger.info("End recording.")
            message = f"{args.post_message}\nRecording start time: {current_time}"

            convert_video(
                video_path,
                video_path_for_post,
                (self.args.video_width, self.args.video_height),
                self.args.video_bitrate,
            )

            await channel.send(message, file=discord.File(video_path_for_post))
            os.remove(video_path)
            logger.info(f"Removed: {video_path}")

            if (
                wait_time := (
                    self.args.recording_interval - self.obs_client.wait_time_after_stop - self.args.video_duration
                )
            ) > 0:
                await asyncio.sleep(wait_time)


if __name__ == "__main__":
    discord.utils.setup_logging()
    args = tyro.cli(Args)
    load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True
    bot = Bot(args, intents=intents)
    bot.run(str(os.environ["DISCORD_BOT_TOKEN"]))

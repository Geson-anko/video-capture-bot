import asyncio
import logging

import obsws_python as obs
from obsws_python.error import OBSSDKError, OBSSDKRequestError

logger = logging.getLogger(__name__)


class ObsClient(obs.ReqClient):
    def __init__(self, wait_time_after_stop: float = 3.0, **kwargs):
        super().__init__(**kwargs)
        self.wait_time_after_stop = wait_time_after_stop

    async def record(self, duration: float) -> str:
        """Recording video for `duration`.

        Args:
            duration: video length [seconds].

        Returns:
            recorded_video_path:
        """

        self.start_record()
        await asyncio.sleep(duration)
        video_path = self.stop_record().output_path
        await asyncio.sleep(self.wait_time_after_stop)
        return video_path

    def __del__(self):
        try:
            self.stop_record()
        except OBSSDKError:
            pass
        except OBSSDKRequestError:
            pass

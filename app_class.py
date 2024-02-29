# pylint: disable=unused-argument
import asyncio
import json

from ffmpeg import FFmpeg as sync_ffmpeg, Progress
from ffmpeg.asyncio import FFmpeg

from params import VideoInfo


class App:

    """
    App class implement main logic
    """

    def __init__(self) -> None:
        self.eventloop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.eventloop)
        self._duration = None

    def get_probe(self, path) -> VideoInfo:
        """Get probe"""
        ffmpeg = sync_ffmpeg(executable="ffprobe").input(
            path,
            print_format="json",
            show_streams=None,
        )

        media = json.loads(
            ffmpeg.execute()
        )

        result = VideoInfo(
            width=media['streams'][0]['width'],
            height=media['streams'][0]['height'],
            fps=int(media['streams'][0]['avg_frame_rate'].split('/')[0]),
            duration=int(media['streams'][0]['nb_frames']),
        )

        self._duration = result.duration

        return result

    async def _convert(self, params, on_update_callback):
        """Convert"""
        vcodec = "libx264" if params.gpu else "h264"
        ffmpeg_job = (
            FFmpeg()
            .option("y")
            .input(params.input_path)
            .output(
                params.output_path,
                vcodec=vcodec,
                vf=f"scale={params.width}:{params.height}",
                preset="veryslow",
                crf=params.fps,
            )
        )

        @ffmpeg_job.on("progress")
        def update_progress_bar(progress: Progress):
            on_update_callback(progress.frame, self._duration)

        await ffmpeg_job.execute()

    async def run_tk(self, window_updater):
        """Update UI"""
        while True:
            if window_updater():
                break
            await asyncio.sleep(0.01)


    def start_app_loop(self, window_updater):
        """Run"""
        self.eventloop.run_until_complete(
            self.run_tk(window_updater)
        )

    def convert(self, params, callback, on_update_callback):
        """Start conver coroutine"""
        asyncio.run_coroutine_threadsafe(
            self._convert(params, on_update_callback),
            self.eventloop
        ).add_done_callback(
            callback
        )

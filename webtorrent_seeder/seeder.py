"""
Module handles the seeding of a file.
"""

import subprocess
import threading
from typing import List, Optional


class SeederProcess:  # pylint: disable=too-few-public-methods
    """Seeder process."""

    def __init__(
        self,
        file_name: str,
        magnet_uri: str,
        process: subprocess.Popen,
        thread_stdout_drain: threading.Thread,
    ) -> None:
        self.file_name = file_name
        self.magnet_uri = magnet_uri
        self.process = process
        self.thread_stdout_drain = thread_stdout_drain

    def terminate(self) -> None:
        """Kill the seeder process."""
        self.process.kill()
        self.thread_stdout_drain.join()
        print(f"seeder killed for {self.file_name}.")

    def wait(self) -> None:
        """Waits for ctrl-c, sig-kill or terminate() to be called."""
        try:
            self.process.wait()
        except KeyboardInterrupt:
            self.terminate()
        except Exception as exc:  # pylint: disable=broad-except
            print(f"Exception happened while waiting: {exc}")
            self.terminate()


def seed_file(
    path: str,
    tracker_list: List[str],
    port: int = 80,
    verbose: bool = False,
    timeout: int = 15,
) -> SeederProcess:
    """Runs the command to seed the content."""
    assert os.path.exists(path), f"File {path} does not exist!"
    # Runner will be run on a different thread, to allow timeouts.
    def runner(
        path: str,
        tracker_list: List[str],
        port: int,
        verbose: bool,
        runner_output: List[SeederProcess],
    ) -> None:
        def _print(*args, **kwargs):
            if verbose:
                print(*args, **kwargs)

        trackers: str = ",".join(tracker_list)
        cmd = f"webtorrent-hybrid seed {path} --keep-seeding --announce {trackers} --port {port}"
        # Iterate through the lines of stdout
        # iterate read line
        _print(f"Running: {cmd}")
        process = subprocess.Popen(  # pylint: disable=consider-using-with
            cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True
        )
        magnet_uri: Optional[str] = None
        for line in iter(process.stdout.readline, ""):  # type: ignore
            _print(line, end="")
            if line.startswith("magnetURI: "):
                magnet_uri = line.split(" ")[1].strip()
                _print("Found magnetURI!")
                break
        if magnet_uri is None:
            rtn_code = process.poll()
            if rtn_code is not None and rtn_code != 0:
                _print(f"Process exited with non-zero exit code: {rtn_code}")
                raise OSError(f"Process exited with non-zero exit code: {rtn_code}")
            _print("Could not find magnetURI!")
            raise OSError(f"Process exited with non-zero exit code: {rtn_code}")

        # will freeze unless the stdout buffer is drained.
        def drain_stdout(process: subprocess.Popen) -> None:
            try:
                for _ in iter(process.stdout.readline, ""):  # type: ignore
                    continue  # just drain the stdout buffer
            except KeyboardInterrupt:
                return

        thread_stdout_drain = threading.Thread(target=drain_stdout, args=(process,), daemon=True)
        thread_stdout_drain.start()
        out = SeederProcess(
            file_name=path,
            magnet_uri=magnet_uri,
            process=process,
            thread_stdout_drain=thread_stdout_drain,
        )
        runner_output.append(out)

    # Setup the thread.
    runner_output: List[SeederProcess] = []
    # Run the runner in a thread
    thread = threading.Thread(
        target=runner,
        args=(path, tracker_list, port, verbose, runner_output),
        daemon=True,  # so that the main thread can exit normally
    )
    thread.start()
    thread.join(timeout=timeout)
    if thread.is_alive():
        print(f"Timeout reached, terminating seeder process for {path}")
        raise OSError(f"Timeout reached, terminating seeder process for {path}")
    seeder_process = runner_output[0]
    return seeder_process


def seed_magneturi(
    magnet_uri, verbose: bool = False, timeout: int = 5
) -> Optional[SeederProcess]:  # Never returns.
    """Runs the command to seed the content."""
    # Runner will be run on a different thread, to allow timeouts.
    def runner(
        magnet_uri: str,
        verbose: bool,
        runner_output: List[SeederProcess],
    ) -> None:
        def _print(*args, **kwargs):
            if verbose:
                print(*args, **kwargs)

        cmd = f"webtorrent-hybrid seed {magnet_uri} --keep-seeding"
        # Iterate through the lines of stdout
        # iterate read line
        _print(f"Running: {cmd}")
        process = subprocess.Popen(  # pylint: disable=consider-using-with
            cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True
        )
        started = False
        for line in iter(process.stdout.readline, ""):  # type: ignore
            _print(line, end="")
            if "fetching torrent metadata" in line:
                started = True
                break
        if not started:
            rtn_code = process.poll()
            if rtn_code is not None and rtn_code != 0:
                _print(f"Process exited with non-zero exit code: {rtn_code}")
                raise OSError(f"Process exited with non-zero exit code: {rtn_code}")
            _print("Could not find magnetURI!")
            raise OSError(f"Process exited with non-zero exit code: {rtn_code}")

        # will freeze unless the stdout buffer is drained.
        def drain_stdout(process: subprocess.Popen) -> None:
            try:
                for _ in iter(process.stdout.readline, ""):  # type: ignore
                    continue  # just drain the stdout buffer
            except KeyboardInterrupt:
                return

        thread_stdout_drain = threading.Thread(target=drain_stdout, args=(process,), daemon=True)
        thread_stdout_drain.start()
        out = SeederProcess(
            file_name="?",
            magnet_uri=magnet_uri,
            process=process,
            thread_stdout_drain=thread_stdout_drain,
        )
        runner_output.append(out)

    # Setup the thread.
    runner_output: List[SeederProcess] = []
    # Run the runner in a thread
    thread = threading.Thread(
        target=runner,
        args=(magnet_uri, verbose, runner_output),
        daemon=True,  # so that the main thread can exit normally
    )
    thread.start()
    thread.join(timeout=timeout)
    if thread.is_alive():
        print(f"Timeout reached, terminating seeder process for {magnet_uri}")
        raise OSError(f"Timeout reached, terminating seeder process for {magnet_uri}")
    seeder_process = runner_output[0] if len(runner_output) > 0 else None
    return seeder_process

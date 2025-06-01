# /// script
# dependencies = [
#  "numpy",
#  "pygame-ce"
# ]
# ///

from gui import GUI
import asyncio

async def main() -> None:
    gui: GUI = GUI()
    while gui.running:
        try:
            await gui.run()
        except Exception as e:
            print(e.with_traceback(None))
            gui.hard_reset()

asyncio.run(main())

import argparse
import asyncio
import sys

from gui import GUI

from algorithm.voronoi import Voronoi
from geometry.point import Point
import os

def parse_args(args):
    parser = argparse.ArgumentParser(description="Voronoi API (no GUI)")
    parser.add_argument("--no-gui", action="store_true")
    parser.add_argument("--zoom", type=float, default=1.0, help="Zoom factor (default 1.0)")
    parser.add_argument("--pan-x", type=float, default=0.0, help="Pan X (default 0.0)")
    parser.add_argument("--pan-y", type=float, default=0.0, help="Pan Y (default 0.0)")
    parser.add_argument("--delaunay", action="store_true", help="Show Delaunay triangulation")
    parser.add_argument("--largest-empty-circle", action="store_true", help="Show largest empty circle")
    parser.add_argument("--events", action="store_true", help="Show the next event (site/circle)")
    parser.add_argument("--sweepline", type=float, default=None, help="Set the y value of the sweepline (float, or omit for full diagram)")
    return parser.parse_args(args)

async def run_gui() -> None:
    gui: GUI = GUI()
    while gui.running:
        try:
            await gui.run()
        except Exception as e:
            print(e.with_traceback(None))
            gui.hard_reset()

def run_no_gui(args=None) -> None:
    """
    Protocol API: Reads commands from stdin, processes diagram interactively.
    Supports initial settings via args, then enters protocol mode.
    """
    from shlex import split

    HELP_TEXT = '\n'.join(map(lambda x: '    ' + x.strip(), """Available commands:
        ADD (x1,y1) (x2,y2) ...      Add one or more sites at coordinates
        REMOVE (x1,y1) (x2,y2) ...   Remove one or more sites at coordinates
        PAN X <dx>                   Pan X by <dx> units
        PAN Y <dy>                   Pan Y by <dy> units
        ZOOM <factor>                Set zoom factor
        DELAUNAY ON|OFF              Enable/disable Delaunay triangulation output
        LEC ON|OFF                   Enable/disable largest empty circle output
        EVENTS ON|OFF                Enable/disable next event output
        SWEEPLINE <y|OFF>            Set sweepline y-value (float/int) or OFF for full diagram
        RUN                          Compute and print the current diagram
        CLEAR                        Remove all sites
        HELP                         Show this help message
        EXIT                         Quit protocol mode
    """.split('\n'))).strip()

    # Parse initial args
    opts = parse_args(sys.argv[1:] if args is None else args)
    sites = []
    zoom = opts.zoom
    pan_x = opts.pan_x
    pan_y = opts.pan_y
    show_delaunay = opts.delaunay
    show_lec = opts.largest_empty_circle
    show_events = opts.events
    sweepline_y = opts.sweepline

    # Load points.txt if exists and not overridden by ADD commands
    points_file = 'points.txt'
    if os.path.exists(points_file):
        with open(points_file, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        x, y = eval(line.strip())
                        sites.append((float(x), float(y)))
                    except Exception:
                        pass

    print("Voronoi API protocol mode. Type commands (EXIT to quit).")
    print("Type HELP for a list of commands.")
    print("Initial settings:")
    print(f"  sites = {len(sites)}")
    print(f"  zoom = {zoom}")
    print(f"  pan_x = {pan_x}")
    print(f"  pan_y = {pan_y}")
    print(f"  delaunay = {show_delaunay}")
    print(f"  largest_empty_circle = {show_lec}")
    print(f"  events = {show_events}")
    print(f"  sweepline_y = {sweepline_y}")

    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            break
        if not line:
            continue
        cmd = split(line)
        if not cmd:
            continue
        op = cmd[0].upper()

        if op == "EXIT":
            break
        elif op == "HELP":
            print(HELP_TEXT)
        elif op == "ADD" and len(cmd) >= 2:
            added = 0
            for arg in cmd[1:]:
                try:
                    x, y = eval(arg)
                    sites.append((float(x), float(y)))
                    added += 1
                except Exception:
                    print(f"Invalid ADD argument: {arg}. Use: ADD (x,y) ...")
            print(f"Added {added} site(s).")
        elif op == "REMOVE" and len(cmd) >= 2:
            removed = 0
            for arg in cmd[1:]:
                try:
                    x, y = eval(arg)
                    before = len(sites)
                    sites = [pt for pt in sites if pt != (float(x), float(y))]
                    if len(sites) < before:
                        removed += 1
                    else:
                        print(f"Site ({x}, {y}) not found.")
                except Exception:
                    print(f"Invalid REMOVE argument: {arg}. Use: REMOVE (x,y) ...")
            print(f"Removed {removed} site(s).")
        elif op == "PAN" and len(cmd) == 3:
            axis = cmd[1].upper()
            try:
                val = float(cmd[2])
                if axis == "X":
                    pan_x += val
                    print(f"Pan X by {val}")
                elif axis == "Y":
                    pan_y += val
                    print(f"Pan Y by {val}")
                else:
                    print("PAN axis must be X or Y.")
            except Exception:
                print("Invalid PAN value.")
        elif op == "ZOOM" and len(cmd) == 2:
            try:
                zoom = float(cmd[1])
                print(f"Zoom set to {zoom}")
            except Exception:
                print("Invalid ZOOM value.")
        elif op == "DELAUNAY" and len(cmd) == 2:
            show_delaunay = cmd[1].upper() == "ON"
            print(f"Delaunay output {'enabled' if show_delaunay else 'disabled'}")
        elif op in ("LEC", "LARGEST_EMPTY_CIRCLE") and len(cmd) == 2:
            show_lec = cmd[1].upper() == "ON"
            print(f"Largest empty circle output {'enabled' if show_lec else 'disabled'}")
        elif op == "EVENTS" and len(cmd) == 2:
            show_events = cmd[1].upper() == "ON"
            print(f"Events output {'enabled' if show_events else 'disabled'}")
        elif op == "SWEEPLINE" and len(cmd) == 2:
            val = cmd[1]
            if val.upper() == "OFF":
                sweepline_y = None
                print("Sweepline y-value set to OFF (full diagram).")
            else:
                try:
                    sweepline_y = float(val)
                    print(f"Sweepline y-value set to {sweepline_y}")
                except Exception:
                    print("Invalid SWEEPLINE value. Use: SWEEPLINE <y|OFF>")
        elif op == "CLEAR":
            sites.clear()
            print("All sites cleared.")
        elif op == "RUN":
            if not sites:
                print("No sites to process.")
                continue
            point_objs = {
                Point(float(x) * zoom + pan_x, float(y) * zoom + pan_y)
                for x, y in sites
            }
            vor = Voronoi(point_objs)
            vor.voronoi(sweepline_y)
            print("Voronoi Edges:")
            for edge in vor.edges:
                a = (float(edge.a.x), float(edge.a.y))
                b = (float(edge.b.x), float(edge.b.y))
                print(f"{a} -> {b}")
            if show_delaunay:
                print("\nDelaunay Triangulation Edges:")
                for edge in vor.delaunay:
                    a = (float(edge.a.x), float(edge.a.y))
                    b = (float(edge.b.x), float(edge.b.y))
                    print(f"{a} -> {b}")
            if show_lec and vor.empty_circle:
                c = vor.empty_circle
                print(f"\nLargest Empty Circle: [({c.center.x}, {c.center.y}), {c.r}]")
            print(f"\nSweepline y-value: {sweepline_y}")
            if show_events:
                print("\nNext Event:")
                if vor.next_visible:
                    print(f"{vor.next_visible}")
                else:
                    print("No next event.")
        else:
            print("Unknown or malformed command.")

async def main() -> None:
    args = sys.argv[1:]
    if args and args[0] == "--no-gui":
        run_no_gui(args)
    else:
        await run_gui()

asyncio.run(main())

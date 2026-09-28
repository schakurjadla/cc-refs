#!/usr/bin/env python3
"""Kodak Warm Teal - apply the look to the current DaVinci Resolve timeline.

Run from inside Resolve:  Workspace > Scripts > Color > KodakWarmTeal_Apply
(or externally with Resolve Studio + scripting env vars set).

What it does:
  1. Takes the clip under the playhead on the Color page as the TEMPLATE clip.
  2. Puts the Kodak Warm Teal LUTs into the look nodes of its node tree.
  3. Copies that grade to every other video clip in the timeline.

Before running: build the 13-node tree on the template clip once
(see README.md) - the scripting API can fill nodes but cannot create them.
"""
import os
import sys

# ------------------------------------------------------------------ settings
# Folder inside Resolve's master LUT folder that holds the .cube files.
LUT_SUBFOLDER = "KodakWarmTeal"

# node index (1-based, as shown on the node) -> LUT file
NODE_LUTS = {
    8: "KWT_1_Hue.cube",
    9: "KWT_2_Split.cube",
    10: "KWT_3_Print.cube",
}
MIN_NODES = 13

# True = copy the whole template grade (expo/WB/contrast too) to all clips.
COPY_TO_ALL_CLIPS = True


# ------------------------------------------------------------------ helpers
def get_resolve():
    r = globals().get("resolve")
    if r:
        return r
    try:
        import DaVinciResolveScript as dvr  # external scripting (Studio)
        return dvr.scriptapp("Resolve")
    except ImportError:
        pass
    bmd_mod = globals().get("bmd")
    if bmd_mod:
        return bmd_mod.scriptapp("Resolve")
    return None


def lut_root_candidates():
    if sys.platform.startswith("win"):
        return [os.path.join(os.environ.get("PROGRAMDATA", r"C:\ProgramData"),
                             "Blackmagic Design", "DaVinci Resolve", "Support", "LUT")]
    if sys.platform == "darwin":
        return ["/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT",
                os.path.expanduser("~/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT")]
    return ["/opt/resolve/LUT", os.path.expanduser("~/.local/share/DaVinciResolve/LUT")]


def find_lut(name):
    for root in lut_root_candidates():
        path = os.path.join(root, LUT_SUBFOLDER, name)
        if os.path.isfile(path):
            return path
    return None


def num_nodes(item):
    graph = item.GetNodeGraph() if hasattr(item, "GetNodeGraph") else None
    if graph:
        return graph.GetNumNodes(), graph
    return item.GetNumNodes(), None


def set_lut(item, graph, node, path):
    rel = LUT_SUBFOLDER + "/" + os.path.basename(path)
    target = graph if graph else item
    # Resolve accepts an absolute path or one relative to the master LUT folder
    return bool(target.SetLUT(node, path) or target.SetLUT(node, rel))


def fail(msg):
    print("[KodakWarmTeal] FEHLER: " + msg)
    sys.exit(1)


# ------------------------------------------------------------------ main
def main():
    resolve = get_resolve()
    if not resolve:
        fail("Keine Verbindung zu Resolve. Skript ueber Workspace > Scripts starten.")

    project = resolve.GetProjectManager().GetCurrentProject()
    timeline = project.GetCurrentTimeline() if project else None
    if not timeline:
        fail("Kein Projekt/Timeline geoeffnet.")

    resolve.OpenPage("color")
    if hasattr(project, "RefreshLUTList"):
        project.RefreshLUTList()

    luts = {}
    for node, name in NODE_LUTS.items():
        path = find_lut(name)
        if not path:
            fail("LUT '%s' nicht gefunden. Kopiere die .cube-Dateien nach <Resolve LUT-Ordner>/%s "
                 "und klicke im LUT-Browser auf 'Refresh'." % (name, LUT_SUBFOLDER))
        luts[node] = path

    template = timeline.GetCurrentVideoItem()
    if not template:
        fail("Playhead steht auf keinem Clip.")

    count, graph = num_nodes(template)
    if count < MIN_NODES:
        fail("Template-Clip '%s' hat %d Nodes, gebraucht werden %d. "
             "Node-Tree laut README bauen (Alt+S) und Skript erneut starten."
             % (template.GetName(), count, MIN_NODES))

    for node, path in sorted(luts.items()):
        ok = set_lut(template, graph, node, path)
        print("[KodakWarmTeal] Node %2d <- %s  %s" % (node, os.path.basename(path), "OK" if ok else "FEHLGESCHLAGEN"))

    if not COPY_TO_ALL_CLIPS:
        print("[KodakWarmTeal] Fertig (nur Template-Clip).")
        return

    targets = []
    for track in range(1, timeline.GetTrackCount("video") + 1):
        for item in timeline.GetItemListInTrack("video", track) or []:
            if item.GetUniqueId() != template.GetUniqueId():
                targets.append(item)

    if targets:
        ok = template.CopyGrades(targets)
        print("[KodakWarmTeal] Grade auf %d Clips kopiert: %s" % (len(targets), "OK" if ok else "FEHLGESCHLAGEN"))
    print("[KodakWarmTeal] Fertig. Jetzt pro Clip Node 02 EXPO / 03 WB feinjustieren.")


main()

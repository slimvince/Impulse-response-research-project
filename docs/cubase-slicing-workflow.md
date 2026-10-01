# Cubase Slicing Workflow (Candidate Event Generation)

**Status: CONFIRMED ONCE / PENDING CLEAN RE-TEST.** This workflow has been completed successfully once in the actual Cubase Pro 15 installation, but has not yet been independently re-tested end-to-end from a completely clean starting state. Do not replace it with an alternative workflow without a documented reason; if a step turns out to be wrong, correct this doc rather than silently deviating.

See `docs/decisions.md` ("Cubase Hitpoints as a fast candidate-event generator, not ground truth") for why Cubase is used here and what it is not: Cubase produces candidate slices, not validated events. Our own validator performs quality evaluation downstream of this workflow.

## Purpose

Turn one unsplit audio file, imported onto an audio track in Cubase Pro 15, into separate physical audio files on disk — one file per selected slice/region — using Cubase's Hitpoint detection as a fast candidate generator.

## Critical prerequisite: two different Audio menus

Cubase has two separate menus both named "Audio" that matter for this workflow. Confusing them is the most common way to get stuck.

- **Main Project-window Audio menu**: used for `Dissolve Part`, `Advanced → Event or Range as Region`, `Find Selected in Pool`.
- **Pool-window Audio menu** (only visible with the Pool window focused): used for `Bounce Selection`.

`Bounce Selection` is in the Pool window's Audio menu, not the main Project window's Audio menu.

## Exact workflow

Starting condition: one unsplit audio file imported onto an audio track, nothing else done yet.

1. Open the imported audio event in the Sample Editor.
2. Open the Hitpoints section.
3. Adjust/verify the detected hitpoints as necessary.
4. `Hitpoints → Create → Slices` — must be **Create Slices**, not Create Regions.
5. Return to the main Project window.
6. Select the Audio Part containing the slices.
7. Main Project-window Audio menu: `Audio → Dissolve Part`. This leaves the individual slice sections as independent audio events.
8. Select the individual audio events to export.
9. Main Project-window Audio menu: `Audio → Advanced → Event or Range as Region`. This creates regions matching the boundaries of the selected events inside the underlying audio clip.
10. Select one of the resulting audio events.
11. Main Project-window Audio menu: `Audio → Find Selected in Pool`. This locates/highlights the underlying source clip in the Pool.
12. In the Pool window, locate the highlighted source clip.
13. Expand that clip. The regions created in step 9 appear underneath it.
14. Select the regions to export.
15. **Pool-window's own Audio menu** (not the main Project-window one): `Audio → Bounce Selection`.
16. Choose the destination folder and confirm.
17. Verify the result: one physical audio file per exported region/slice.

## Operations that look similar but are NOT part of this workflow

Do not substitute these in just because they appear to offer similar functionality:

- Create Regions (at the Hitpoints stage) — we use Create Slices instead.
- `Audio → Advanced → Events from Regions` — this is the opposite direction from what we need (regions → events, not events → regions → files).
- Render in Place / Range Selection → Render in Place.
- Bounce Selection applied to the adjacent timeline events (rather than to Pool regions).
- `File → Export → Selected Events` — inconsistent/problematic in this Cubase Pro 15 installation; not part of the established procedure.
- Manually hunting through the entire Pool for the source clip instead of using `Find Selected in Pool`.

## Downstream role

Cubase-generated slices are candidate events only. They feed into our own validator (accept / reject / uncertain), which performs quality evaluation before slices enter feature extraction or corpus analysis. See `docs/decisions.md` for the validator's design principles (explicit quality tests preferred over an opaque classifier; optimize for trustworthy composition, not slice count).

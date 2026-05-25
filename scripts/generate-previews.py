#!/usr/bin/env python3
"""Generate per-state GIF previews from Codex pet spritesheets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont


CELL_WIDTH = 192
CELL_HEIGHT = 208
COLUMNS = 8
STATES = [
    ("idle", "idle"),
    ("running-right", "running-right"),
    ("running-left", "running-left"),
    ("waving", "waving"),
    ("jumping", "jumping"),
    ("failed", "failed"),
    ("waiting", "waiting"),
    ("running", "running"),
    ("review", "review"),
]
EXPECTED_SIZE = (CELL_WIDTH * COLUMNS, CELL_HEIGHT * len(STATES))


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def pet_dirs(root: Path) -> list[Path]:
    pets_root = root / "pets"
    return sorted(path for path in pets_root.iterdir() if path.is_dir())


def load_pet_manifest(pet_dir: Path) -> dict:
    with (pet_dir / "pet.json").open("r", encoding="utf-8") as f:
        return json.load(f)


def checkerboard(size: tuple[int, int], block: int = 16) -> Image.Image:
    image = Image.new("RGBA", size, "#ffffff")
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], block):
        for x in range(0, size[0], block):
            if (x // block + y // block) % 2:
                draw.rectangle((x, y, x + block - 1, y + block - 1), fill="#eef2f7")
    return image


def flatten_on_background(frame: Image.Image, background: Image.Image | tuple[int, int, int]) -> Image.Image:
    if isinstance(background, Image.Image):
        canvas = background.copy()
    else:
        canvas = Image.new("RGBA", frame.size, (*background, 255))
    canvas.alpha_composite(frame)
    return canvas.convert("RGB")


def to_gif_frame(frame: Image.Image, scale: int, background: str | tuple[int, int, int]) -> Image.Image:
    frame = frame.resize((frame.width * scale, frame.height * scale), Image.Resampling.NEAREST)
    if background == "checkerboard":
        matte: Image.Image | tuple[int, int, int] = checkerboard(frame.size, block=max(8, 8 * scale))
    else:
        matte = background
    return flatten_on_background(frame, matte).convert("P", palette=Image.Palette.ADAPTIVE, colors=256)


def crop_state_frames(sheet: Image.Image, row_index: int) -> list[Image.Image]:
    top = row_index * CELL_HEIGHT
    frames = []
    for column in range(COLUMNS):
        left = column * CELL_WIDTH
        frames.append(sheet.crop((left, top, left + CELL_WIDTH, top + CELL_HEIGHT)))
    return frames


def is_visible_frame(frame: Image.Image) -> bool:
    return frame.getchannel("A").getbbox() is not None


def visible_frames(frames: list[Image.Image]) -> list[Image.Image]:
    return [frame for frame in frames if is_visible_frame(frame)]


def save_state_gif(
    frames: list[Image.Image],
    out_path: Path,
    scale: int,
    duration: int,
    background: str | tuple[int, int, int],
) -> None:
    frames = visible_frames(frames)
    if not frames:
        raise ValueError(f"{out_path}: cannot generate GIF from an empty row")

    gif_frames = [to_gif_frame(frame, scale, background) for frame in frames]
    gif_frames[0].save(
        out_path,
        save_all=True,
        append_images=gif_frames[1:],
        duration=duration,
        loop=0,
        disposal=2,
        optimize=False,
    )


def save_contact_sheet(sheet: Image.Image, out_path: Path, scale: int) -> None:
    row_height = CELL_HEIGHT * scale
    frame_width = CELL_WIDTH * scale
    label_width = frame_width
    width = (COLUMNS + 1) * frame_width
    height = len(STATES) * row_height
    contact = checkerboard((width, height), block=16)
    draw = ImageDraw.Draw(contact)
    font = ImageFont.load_default()

    for row_index, (state, label) in enumerate(STATES):
        y = row_index * row_height
        draw.rectangle((0, y, label_width - 1, y + row_height - 1), fill="#f8fafc")
        draw.text((12, y + 12), label, fill="#111827", font=font)
        for column, frame in enumerate(crop_state_frames(sheet, row_index)):
            scaled = frame.resize((frame_width, row_height), Image.Resampling.NEAREST)
            contact.alpha_composite(scaled, (label_width + column * frame_width, y))

    contact.save(out_path)


def generate_for_pet(
    root: Path,
    pet_dir: Path,
    scale: int,
    duration: int,
    background: str | tuple[int, int, int],
) -> None:
    manifest = load_pet_manifest(pet_dir)
    pet_id = manifest["id"]
    spritesheet = pet_dir / manifest.get("spritesheetPath", "spritesheet.webp")
    if not spritesheet.exists():
        raise FileNotFoundError(f"{pet_id}: missing spritesheet at {spritesheet}")

    sheet = Image.open(spritesheet).convert("RGBA")
    if sheet.size != EXPECTED_SIZE:
        raise ValueError(f"{pet_id}: expected {EXPECTED_SIZE}, got {sheet.size}")

    out_dir = root / "assets" / "previews" / pet_id
    out_dir.mkdir(parents=True, exist_ok=True)
    for row_index, (state, _label) in enumerate(STATES):
        save_state_gif(crop_state_frames(sheet, row_index), out_dir / f"{state}.gif", scale, duration, background)
    save_contact_sheet(sheet, out_dir / "contact-sheet.png", scale=1)
    print(f"generated previews for {pet_id}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=1, help="GIF scale factor.")
    parser.add_argument("--duration", type=int, default=120, help="GIF frame duration in milliseconds.")
    parser.add_argument("--background", default="checkerboard", help="GIF matte background: checkerboard or a CSS color.")
    args = parser.parse_args()

    root = repo_root()
    background = "checkerboard" if args.background == "checkerboard" else ImageColor.getrgb(args.background)
    for pet_dir in pet_dirs(root):
        generate_for_pet(root, pet_dir, args.scale, args.duration, background)


if __name__ == "__main__":
    main()

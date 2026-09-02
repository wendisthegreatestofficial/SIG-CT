"""
SIG Config Tool v8
Visual configurator for SimpleItemGenerator Minecraft plugin.
Plugin DEV: Balerii (hes a good dev)
Made with Claude (ima new to coding dont jugde)
From: Turkiye
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import yaml
import json
import re
import os
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------------------------------------
#  DATA
# ---------------------------------------------

MATERIALS = [
    "DIAMOND_SWORD","NETHERITE_SWORD","IRON_SWORD","GOLDEN_SWORD","STONE_SWORD","WOODEN_SWORD",
    "DIAMOND_PICKAXE","NETHERITE_PICKAXE","IRON_PICKAXE","GOLDEN_PICKAXE","STONE_PICKAXE","WOODEN_PICKAXE",
    "DIAMOND_AXE","NETHERITE_AXE","IRON_AXE","GOLDEN_AXE","STONE_AXE","WOODEN_AXE",
    "DIAMOND_SHOVEL","NETHERITE_SHOVEL","IRON_SHOVEL","GOLDEN_SHOVEL","STONE_SHOVEL","WOODEN_SHOVEL",
    "DIAMOND_HOE","NETHERITE_HOE","IRON_HOE","GOLDEN_HOE","STONE_HOE","WOODEN_HOE",
    "DIAMOND_HELMET","NETHERITE_HELMET","IRON_HELMET","GOLDEN_HELMET","CHAINMAIL_HELMET","LEATHER_HELMET",
    "DIAMOND_CHESTPLATE","NETHERITE_CHESTPLATE","IRON_CHESTPLATE","GOLDEN_CHESTPLATE","CHAINMAIL_CHESTPLATE","LEATHER_CHESTPLATE",
    "DIAMOND_LEGGINGS","NETHERITE_LEGGINGS","IRON_LEGGINGS","GOLDEN_LEGGINGS","CHAINMAIL_LEGGINGS","LEATHER_LEGGINGS",
    "DIAMOND_BOOTS","NETHERITE_BOOTS","IRON_BOOTS","GOLDEN_BOOTS","CHAINMAIL_BOOTS","LEATHER_BOOTS",
    "BOW","CROSSBOW","TRIDENT","SHIELD","FISHING_ROD","FLINT_AND_STEEL",
    "STICK","BLAZE_ROD","BONE","FEATHER","ARROW",
    "APPLE","GOLDEN_APPLE","ENCHANTED_GOLDEN_APPLE","BREAD","COOKED_BEEF","COOKED_CHICKEN",
    "DIAMOND","EMERALD","AMETHYST_SHARD","NETHER_STAR","HEART_OF_THE_SEA","ECHO_SHARD",
    "BOOK","ENCHANTED_BOOK","WRITABLE_BOOK","KNOWLEDGE_BOOK",
    "POTION","SPLASH_POTION","LINGERING_POTION","TIPPED_ARROW",
    "PAPER","MAP","COMPASS","CLOCK","SPYGLASS","RECOVERY_COMPASS",
    "PLAYER_HEAD","SKELETON_SKULL","WITHER_SKELETON_SKULL","CREEPER_HEAD","ZOMBIE_HEAD",
    "CHEST","BARREL","SHULKER_BOX","ENDER_CHEST","TRAPPED_CHEST",
    "TNT","FIRE_CHARGE","FIREWORK_ROCKET",
    "STONE","COBBLESTONE","OAK_PLANKS","GLASS","OBSIDIAN","CRYING_OBSIDIAN",
    "TOTEM_OF_UNDYING","SADDLE","NAME_TAG","LEAD","IRON_INGOT","GOLD_INGOT","BLAZE_POWDER",
]

ENCHANTMENTS = [
    "minecraft:sharpness","minecraft:smite","minecraft:bane_of_arthropods",
    "minecraft:knockback","minecraft:fire_aspect","minecraft:looting","minecraft:sweeping_edge",
    "minecraft:unbreaking","minecraft:mending","minecraft:vanishing_curse",
    "minecraft:protection","minecraft:fire_protection","minecraft:blast_protection",
    "minecraft:projectile_protection","minecraft:thorns","minecraft:respiration",
    "minecraft:aqua_affinity","minecraft:depth_strider","minecraft:frost_walker",
    "minecraft:feather_falling","minecraft:soul_speed","minecraft:swift_sneak",
    "minecraft:efficiency","minecraft:silk_touch","minecraft:fortune",
    "minecraft:power","minecraft:punch","minecraft:flame","minecraft:infinity",
    "minecraft:luck_of_the_sea","minecraft:lure",
    "minecraft:channeling","minecraft:loyalty","minecraft:riptide","minecraft:impaling",
    "minecraft:multishot","minecraft:piercing","minecraft:quick_charge",
    "minecraft:binding_curse","minecraft:breach","minecraft:density","minecraft:wind_burst",
]

ITEM_FLAGS = [
    "HIDE_ATTRIBUTES","HIDE_DESTROYS","HIDE_DYE",
    "HIDE_ENCHANTS","HIDE_PLACED_ON","HIDE_POTION_EFFECTS","HIDE_UNBREAKABLE","HIDE_ARMOR_TRIM",
]

MINI_COLORS = {
    "White":       "white",
    "Yellow":      "yellow",
    "Gold":        "gold",
    "Red":         "red",
    "Dark Red":    "dark_red",
    "Green":       "green",
    "Dark Green":  "dark_green",
    "Blue":        "blue",
    "Dark Blue":   "dark_blue",
    "Aqua":        "aqua",
    "Dark Aqua":   "dark_aqua",
    "Purple":      "light_purple",
    "Dark Purple": "dark_purple",
    "Gray":        "gray",
    "Dark Gray":   "dark_gray",
    "Black":       "black",
}

ATTRIBUTE_TYPES = [
    "ATTACK_DAMAGE","MAX_HEALTH","FOLLOW_RANGE","KNOCKBACK_RESISTANCE","MOVEMENT_SPEED",
    "ATTACK_SPEED","ARMOR","ARMOR_TOUGHNESS","LUCK","FLYING_SPEED","ATTACK_KNOCKBACK",
    "MAX_ABSORPTION","SCALE","STEP_HEIGHT","GRAVITY","SAFE_FALL_DISTANCE",
    "BLOCK_BREAK_SPEED","BURNING_TIME","MINING_EFFICIENCY","SNEAKING_SPEED",
    "WATER_MOVEMENT_EFFICIENCY","OXYGEN_BONUS",
]

ATTRIBUTE_OPS = ["ADD_VALUE", "ADD_MULTIPLIED_BASE", "ADD_MULTIPLIED_TOTAL"]

ATTRIBUTE_SLOTS = ["ANY","MAINHAND","OFFHAND","HEAD","CHEST","LEGS","FEET","ARMOR","HAND"]

COOLDOWN_TYPES = ["PER_ITEM", "PER_PLAYER", "GLOBAL"]

# ---- TEMA ----
BG_ROOT   = "#0a0a0a"
BG_PANEL  = "#111111"
BG_HDR    = "#181818"
BG_CARD   = "#1c1c1c"
BG_ROW    = "#222222"
BORDER    = "#2e2e2e"
SEL_BG    = "#2a2a2a"

BTN       = "#2a2a2a"
BTN_H     = "#3e3e3e"
BTN_DEL   = "#3a1010"
BTN_DEL2  = "#5a1a1a"

TXT_MAIN  = "#e0e0e0"
TXT_SUB   = "#777777"
TXT_DIM   = "#3a3a3a"

SCROLL_FG  = "#181818"
SCROLL_BTN = "#383838"
SCROLL_HOV = "#525252"

YAML_TEXT  = "#cccccc"


# ---------------------------------------------
#  HELPERS
# ---------------------------------------------

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9_\-]", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_")


def make_neon_label(parent, text, font_size=18, bg=BG_ROOT):
    fw = font_size * len(text) + 60
    fh = font_size + 28
    c = tk.Canvas(parent, width=fw, height=fh, bg=bg, highlightthickness=0)
    cx, cy = fw // 2, fh // 2
    font_spec = ("Consolas", font_size, "bold")
    for off, col in [(4, "#1a1a1a"), (3, "#2e2e2e"), (2, "#4a4a4a"), (1, "#888888")]:
        c.create_text(cx+off, cy+off, text=text, font=font_spec, fill=col, anchor="center")
        c.create_text(cx-off, cy-off, text=text, font=font_spec, fill=col, anchor="center")
    c.create_text(cx, cy, text=text, font=font_spec, fill="#ffffff", anchor="center")
    return c


def mini(color_label: str, text: str) -> str:
    tag = MINI_COLORS.get(color_label, "white")
    return f"<{tag}>{text}</{tag}>"


# ---------------------------------------------
#  YAML BUILDER  (plugin-accurate format)
# ---------------------------------------------

def build_yaml_for_item(item: dict) -> dict:
    """
    Returns a dict matching SIG plugin format:
    {
      item: { material, name, lore, cmd, ... },
      usage: [...],
      is-ingredient: bool,
      ...
    }
    """
    inner = {}

    # material (required)
    inner["material"] = item.get("material", "STONE")

    # name
    name_text = item.get("name_text", "").strip()
    if name_text:
        inner["name"] = mini(item.get("name_color", "Gold"), name_text)

    # lore
    lore_lines = []
    for line_text, line_color in item.get("lore", []):
        t = line_text.strip()
        if t:
            lore_lines.append(mini(line_color, t))
    if lore_lines:
        inner["lore"] = lore_lines

    # cmd
    cmd_val = str(item.get("cmd", "")).strip()
    if cmd_val:
        try:
            inner["cmd"] = int(cmd_val)
        except ValueError:
            inner["cmd"] = cmd_val

    # amount
    try:
        amount = int(item.get("amount", 1))
        if amount != 1:
            inner["amount"] = amount
    except (ValueError, TypeError):
        pass

    # unbreakable
    if item.get("unbreakable", False):
        inner["unbreakable"] = True

    # durability
    dur_val = str(item.get("durability", "")).strip()
    if dur_val:
        try:
            inner["durability"] = int(dur_val)
        except ValueError:
            pass

    # enchantments
    enchs = {k: v for k, v in item.get("enchantments", {}).items() if v > 0}
    if enchs:
        inner["enchantments"] = enchs

    # item-flags
    flags = item.get("flags", [])
    if flags:
        inner["item-flags"] = flags

    # attributes
    attrs = item.get("attributes", [])
    if attrs:
        inner["attributes"] = attrs

    # color
    color_val = item.get("color", "").strip()
    if color_val:
        inner["color"] = color_val

    # head-texture
    head_val = item.get("head_texture", "").strip()
    if head_val:
        inner["head-texture"] = head_val

    # nbt
    nbt_val = item.get("nbt", "").strip()
    if nbt_val:
        inner["nbt"] = nbt_val

    # --- outer block ---
    block = {"item": inner}

    # is-ingredient
    if item.get("is_ingredient", False):
        block["is-ingredient"] = True

    # can-be-put-in-inventory
    if item.get("can_put_in_inventory", False):
        block["can-be-put-in-inventory"] = True

    # remove-on-death
    if item.get("remove_on_death", False):
        block["remove-on-death"] = True

    # is-plain
    if item.get("is_plain", False):
        block["is-plain"] = True

    # can-move
    if not item.get("can_move", True):
        block["can-move"] = False

    # usage
    usages = item.get("usage", [])
    if usages:
        usage_out = _build_usages(usages)
        if len(usage_out) == 1:
            block["usage"] = usage_out[0]
        elif usage_out:
            block["usage"] = usage_out

    return block


def _build_usages(usages: list) -> list:
    result = []
    for u in usages:
        cmds = u.get("commands", [])
        if not cmds:
            continue
        entry = {}

        # predicate — plugin format: "[button] right" or "[at] block"
        button  = u.get("button", "right")
        at_val  = u.get("at", "any")
        if at_val and at_val != "any":
            entry["predicate"] = f"[at] {at_val}"
        else:
            entry["predicate"] = f"[button] {button}"

        # cancel
        if not u.get("cancel", True):
            entry["cancel"] = False

        # cooldown
        cooldown = u.get("cooldown", "").strip()
        if cooldown:
            entry["cooldown"] = cooldown

        # cooldown-type
        cd_type = u.get("cooldown_type", "PER_ITEM")
        if cd_type != "PER_ITEM":
            entry["cooldown-type"] = cd_type

        # on-cooldown
        on_cd = u.get("on_cooldown", [])
        if on_cd:
            entry["on-cooldown"] = on_cd if len(on_cd) > 1 else on_cd[0]

        # freezetime
        ft = u.get("freezetime", "").strip()
        if ft:
            entry["freezetime"] = ft

        # consume
        consume = u.get("consume", 0)
        if consume:
            entry["consume"] = consume

        # commands
        if len(cmds) == 1:
            entry["commands"] = cmds[0]
        else:
            entry["commands"] = cmds

        result.append(entry)
    return result


# ---------------------------------------------
#  LORE EDITOR
# ---------------------------------------------

class LoreEditor(ctk.CTkFrame):
    def __init__(self, parent, on_change):
        super().__init__(parent, fg_color="transparent")
        self.on_change = on_change
        self.rows: list[tuple[tk.StringVar, tk.StringVar]] = []
        self._build()

    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text="Lore", font=("Consolas", 12, "bold"),
                     text_color=TXT_MAIN).pack(side="left")
        ctk.CTkButton(hdr, text="+ Line", width=80, height=26,
                      font=("Consolas", 11), fg_color=BTN, hover_color=BTN_H,
                      command=self.add_row).pack(side="right")
        self.container = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=4)
        self.container.pack(fill="x", pady=(4, 0))

    def add_row(self, text="", color="White"):
        color_var = tk.StringVar(value=color)
        text_var  = tk.StringVar(value=text)

        row_frame = ctk.CTkFrame(self.container, fg_color=BG_ROW, corner_radius=4)
        row_frame.pack(fill="x", pady=2, padx=4)

        ctk.CTkOptionMenu(row_frame, variable=color_var,
                          values=list(MINI_COLORS.keys()),
                          width=130, height=26, font=("Consolas", 10),
                          command=lambda _: self.on_change()
                          ).pack(side="left", padx=(6, 4), pady=4)

        entry = ctk.CTkEntry(row_frame, textvariable=text_var,
                             placeholder_text="lore text...",
                             height=26, font=("Consolas", 11))
        entry.pack(side="left", fill="x", expand=True, padx=4)
        text_var.trace_add("write", lambda *_: self.on_change())

        def remove():
            self.rows = [(tv, cv) for tv, cv in self.rows if tv is not text_var]
            row_frame.destroy()
            self.on_change()

        ctk.CTkButton(row_frame, text="X", width=26, height=26,
                      fg_color=BTN_DEL, hover_color=BTN_DEL2,
                      command=remove).pack(side="right", padx=6)

        self.rows.append((text_var, color_var))

    def get_data(self):
        return [(tv.get(), cv.get()) for tv, cv in self.rows]

    def load_data(self, data):
        for w in self.container.winfo_children():
            w.destroy()
        self.rows.clear()
        for text, color in data:
            self.add_row(text, color)


# ---------------------------------------------
#  ENCHANTMENT EDITOR
# ---------------------------------------------

class EnchantEditor(ctk.CTkFrame):
    def __init__(self, parent, on_change):
        super().__init__(parent, fg_color="transparent")
        self.on_change = on_change
        self.rows: list[tuple[tk.StringVar, tk.IntVar]] = []
        self._build()

    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text="Enchantments", font=("Consolas", 12, "bold"),
                     text_color=TXT_MAIN).pack(side="left")
        ctk.CTkButton(hdr, text="+ Enchant", width=90, height=26,
                      font=("Consolas", 11), fg_color=BTN, hover_color=BTN_H,
                      command=self.add_row).pack(side="right")
        self.container = ctk.CTkFrame(self, fg_color=BG_HDR, corner_radius=4)
        self.container.pack(fill="x", pady=(4, 0))

    def add_row(self, ench=None, level=1):
        ench = ench or ENCHANTMENTS[0]
        ench_var  = tk.StringVar(value=ench)
        level_var = tk.IntVar(value=level)

        row_frame = ctk.CTkFrame(self.container, fg_color=BG_ROW, corner_radius=4)
        row_frame.pack(fill="x", pady=2, padx=4)

        ctk.CTkOptionMenu(row_frame, variable=ench_var,
                          values=ENCHANTMENTS, width=240, height=26,
                          font=("Consolas", 10),
                          command=lambda _: self.on_change()
                          ).pack(side="left", padx=(6, 4), pady=4)

        ctk.CTkLabel(row_frame, text="Level:", font=("Consolas", 11)).pack(side="left")

        def inc():
            level_var.set(min(255, level_var.get() + 1))
            self.on_change()

        def dec():
            level_var.set(max(1, level_var.get() - 1))
            self.on_change()

        ctk.CTkButton(row_frame, text="-", width=26, height=26,
                      fg_color=BTN, hover_color=BTN_H, command=dec).pack(side="left", padx=2)
        ctk.CTkLabel(row_frame, textvariable=level_var,
                     font=("Consolas", 12, "bold"), width=30).pack(side="left")
        ctk.CTkButton(row_frame, text="+", width=26, height=26,
                      fg_color=BTN, hover_color=BTN_H, command=inc).pack(side="left", padx=2)

        def remove():
            self.rows = [(ev, lv) for ev, lv in self.rows if ev is not ench_var]
            row_frame.destroy()
            self.on_change()

        ctk.CTkButton(row_frame, text="X", width=26, height=26,
                      fg_color=BTN_DEL, hover_color=BTN_DEL2,
                      command=remove).pack(side="right", padx=6)

        self.rows.append((ench_var, level_var))

    def get_data(self) -> dict:
        return {ev.get(): lv.get() for ev, lv in self.rows}

    def load_data(self, data: dict):
        for w in self.container.winfo_children():
            w.destroy()
        self.rows.clear()
        for ench, level in data.items():
            self.add_row(ench, level)


# ---------------------------------------------
#  ATTRIBUTE EDITOR
# ---------------------------------------------

class AttributeEditor(ctk.CTkFrame):
    def __init__(self, parent, on_change):
        super().__init__(parent, fg_color="transparent")
        self.on_change = on_change
        self.rows: list[dict] = []
        self._build()

    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text="Attributes", font=("Consolas", 12, "bold"),
                     text_color=TXT_MAIN).pack(side="left")
        ctk.CTkButton(hdr, text="+ Attribute", width=100, height=26,
                      font=("Consolas", 11), fg_color=BTN, hover_color=BTN_H,
                      command=self.add_row).pack(side="right")
        self.container = ctk.CTkFrame(self, fg_color=BG_HDR, corner_radius=4)
        self.container.pack(fill="x", pady=(4, 0))

    def add_row(self, attr="ATTACK_DAMAGE", op="ADD_VALUE", amount=1.0, slot="MAINHAND", name=""):
        attr_var   = tk.StringVar(value=attr)
        op_var     = tk.StringVar(value=op)
        amount_var = tk.StringVar(value=str(amount))
        slot_var   = tk.StringVar(value=slot)
        name_var   = tk.StringVar(value=name)

        row_frame = ctk.CTkFrame(self.container, fg_color=BG_ROW, corner_radius=4)
        row_frame.pack(fill="x", pady=2, padx=4)

        r1 = ctk.CTkFrame(row_frame, fg_color="transparent")
        r1.pack(fill="x", padx=6, pady=(4, 2))

        ctk.CTkLabel(r1, text="Type:", font=("Consolas", 10), width=40).pack(side="left")
        ctk.CTkOptionMenu(r1, variable=attr_var, values=ATTRIBUTE_TYPES,
                          width=200, height=24, font=("Consolas", 10),
                          command=lambda _: self.on_change()).pack(side="left", padx=4)

        ctk.CTkLabel(r1, text="Op:", font=("Consolas", 10)).pack(side="left", padx=(8,2))
        ctk.CTkOptionMenu(r1, variable=op_var, values=ATTRIBUTE_OPS,
                          width=170, height=24, font=("Consolas", 10),
                          command=lambda _: self.on_change()).pack(side="left", padx=4)

        r2 = ctk.CTkFrame(row_frame, fg_color="transparent")
        r2.pack(fill="x", padx=6, pady=(0, 4))

        ctk.CTkLabel(r2, text="Amount:", font=("Consolas", 10), width=56).pack(side="left")
        ctk.CTkEntry(r2, textvariable=amount_var, width=70, height=24,
                     font=("Consolas", 10)).pack(side="left", padx=4)
        amount_var.trace_add("write", lambda *_: self.on_change())

        ctk.CTkLabel(r2, text="Slot:", font=("Consolas", 10)).pack(side="left", padx=(8,2))
        ctk.CTkOptionMenu(r2, variable=slot_var, values=ATTRIBUTE_SLOTS,
                          width=110, height=24, font=("Consolas", 10),
                          command=lambda _: self.on_change()).pack(side="left", padx=4)

        ctk.CTkLabel(r2, text="Name:", font=("Consolas", 10)).pack(side="left", padx=(8,2))
        ctk.CTkEntry(r2, textvariable=name_var, width=100, height=24,
                     placeholder_text="optional", font=("Consolas", 10)).pack(side="left", padx=4)
        name_var.trace_add("write", lambda *_: self.on_change())

        row_info = {"attr": attr_var, "op": op_var, "amount": amount_var,
                    "slot": slot_var, "name": name_var, "frame": row_frame}

        def remove():
            self.rows = [r for r in self.rows if r is not row_info]
            row_frame.destroy()
            self.on_change()

        ctk.CTkButton(r1, text="X", width=26, height=24,
                      fg_color=BTN_DEL, hover_color=BTN_DEL2,
                      command=remove).pack(side="right", padx=4)

        self.rows.append(row_info)

    def get_data(self) -> list:
        result = []
        for r in self.rows:
            try:
                amount = float(r["amount"].get())
            except ValueError:
                amount = 0.0
            entry = {
                "attribute": r["attr"].get(),
                "operation": r["op"].get(),
                "amount":    amount,
                "slot":      r["slot"].get(),
            }
            name = r["name"].get().strip()
            if name:
                entry["name"] = name
            result.append(entry)
        return result

    def load_data(self, data: list):
        for w in self.container.winfo_children():
            w.destroy()
        self.rows.clear()
        for entry in data:
            self.add_row(
                attr   = entry.get("attribute", "ATTACK_DAMAGE"),
                op     = entry.get("operation", "ADD_VALUE"),
                amount = entry.get("amount", 1.0),
                slot   = entry.get("slot", "MAINHAND"),
                name   = entry.get("name", ""),
            )


# ---------------------------------------------
#  USAGE EDITOR
# ---------------------------------------------

class UsageEditor(ctk.CTkFrame):
    def __init__(self, parent, on_change):
        super().__init__(parent, fg_color="transparent")
        self.on_change = on_change
        self.blocks: list[dict] = []
        self._build()

    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text="Usage / Commands", font=("Consolas", 12, "bold"),
                     text_color=TXT_MAIN).pack(side="left")
        ctk.CTkButton(hdr, text="+ Usage", width=90, height=26,
                      font=("Consolas", 11), fg_color=BTN, hover_color=BTN_H,
                      command=self.add_block).pack(side="right")
        self.container = ctk.CTkFrame(self, fg_color=BG_HDR, corner_radius=4)
        self.container.pack(fill="x", pady=(4, 0))

    def add_block(self, button="right", at="any", cancel=True,
                  cooldown="", cooldown_type="PER_ITEM", on_cooldown=None,
                  freezetime="", consume=0, cmds=None):
        cmds = cmds or []
        on_cooldown = on_cooldown or []

        block_frame = ctk.CTkFrame(self.container, fg_color=BG_ROW, corner_radius=4)
        block_frame.pack(fill="x", pady=4, padx=4)

        # -- Row 1: button, at, cancel
        r1 = ctk.CTkFrame(block_frame, fg_color="transparent")
        r1.pack(fill="x", padx=8, pady=(6, 2))

        ctk.CTkLabel(r1, text="Button:", font=("Consolas", 11)).pack(side="left")
        button_var = tk.StringVar(value=button)
        ctk.CTkOptionMenu(r1, variable=button_var,
                          values=["right", "left", "drop"],
                          width=80, height=26, font=("Consolas", 11),
                          command=lambda _: self.on_change()).pack(side="left", padx=6)

        ctk.CTkLabel(r1, text="At:", font=("Consolas", 11)).pack(side="left", padx=(8,2))
        at_var = tk.StringVar(value=at)
        ctk.CTkOptionMenu(r1, variable=at_var,
                          values=["any", "air", "block", "entity", "player"],
                          width=80, height=26, font=("Consolas", 11),
                          command=lambda _: self.on_change()).pack(side="left", padx=4)

        cancel_var = tk.BooleanVar(value=cancel)
        ctk.CTkCheckBox(r1, text="Cancel interaction", variable=cancel_var,
                        font=("Consolas", 11),
                        command=self.on_change).pack(side="left", padx=12)

        # -- Row 2: cooldown, cooldown-type, freezetime, consume
        r2 = ctk.CTkFrame(block_frame, fg_color="transparent")
        r2.pack(fill="x", padx=8, pady=2)

        ctk.CTkLabel(r2, text="Cooldown:", font=("Consolas", 11)).pack(side="left")
        cooldown_var = tk.StringVar(value=cooldown)
        ctk.CTkEntry(r2, textvariable=cooldown_var, width=80, height=24,
                     placeholder_text="e.g: 5s", font=("Consolas", 10)).pack(side="left", padx=4)
        cooldown_var.trace_add("write", lambda *_: self.on_change())

        ctk.CTkLabel(r2, text="Type:", font=("Consolas", 11)).pack(side="left", padx=(8,2))
        cd_type_var = tk.StringVar(value=cooldown_type)
        ctk.CTkOptionMenu(r2, variable=cd_type_var, values=COOLDOWN_TYPES,
                          width=110, height=24, font=("Consolas", 10),
                          command=lambda _: self.on_change()).pack(side="left", padx=4)

        ctk.CTkLabel(r2, text="Freezetime:", font=("Consolas", 11)).pack(side="left", padx=(8,2))
        ft_var = tk.StringVar(value=freezetime)
        ctk.CTkEntry(r2, textvariable=ft_var, width=70, height=24,
                     placeholder_text="e.g: 500", font=("Consolas", 10)).pack(side="left", padx=4)
        ft_var.trace_add("write", lambda *_: self.on_change())

        ctk.CTkLabel(r2, text="Consume:", font=("Consolas", 11)).pack(side="left", padx=(8,2))
        consume_var = tk.StringVar(value=str(consume) if consume else "")
        ctk.CTkEntry(r2, textvariable=consume_var, width=55, height=24,
                     placeholder_text="0", font=("Consolas", 10)).pack(side="left", padx=4)
        consume_var.trace_add("write", lambda *_: self.on_change())

        # -- On-cooldown commands
        on_cd_container = ctk.CTkFrame(block_frame, fg_color="transparent")
        on_cd_container.pack(fill="x", padx=8, pady=2)

        ctk.CTkLabel(on_cd_container, text="On-cooldown cmd:",
                     font=("Consolas", 10), text_color=TXT_SUB).pack(anchor="w")
        on_cd_var = tk.StringVar(value=on_cooldown[0] if len(on_cooldown) == 1 else
                                 "\n".join(on_cooldown) if on_cooldown else "")
        on_cd_entry = ctk.CTkEntry(on_cd_container, textvariable=on_cd_var,
                                   placeholder_text="[console] msg %player% On cooldown!",
                                   height=24, font=("Consolas", 10))
        on_cd_entry.pack(fill="x")
        on_cd_var.trace_add("write", lambda *_: self.on_change())

        # -- Commands
        cmd_container = ctk.CTkFrame(block_frame, fg_color="transparent")
        cmd_container.pack(fill="x", padx=8, pady=(4, 2))
        ctk.CTkLabel(cmd_container, text="Commands:", font=("Consolas", 10),
                     text_color=TXT_SUB).pack(anchor="w")

        block_info = {
            "frame":       block_frame,
            "button":      button_var,
            "at":          at_var,
            "cancel":      cancel_var,
            "cooldown":    cooldown_var,
            "cd_type":     cd_type_var,
            "on_cooldown": on_cd_var,
            "freezetime":  ft_var,
            "consume":     consume_var,
            "cmd_rows":    [],
        }

        def add_cmd(ctype="[console]", ctext=""):
            cmd_row = ctk.CTkFrame(cmd_container, fg_color="transparent")
            cmd_row.pack(fill="x", pady=1)
            type_var = tk.StringVar(value=ctype)
            text_var = tk.StringVar(value=ctext)
            ctk.CTkOptionMenu(cmd_row, variable=type_var,
                              values=["[console]", "[player]"],
                              width=90, height=24, font=("Consolas", 10),
                              command=lambda _: self.on_change()).pack(side="left", padx=(0,4))
            e = ctk.CTkEntry(cmd_row, textvariable=text_var,
                             placeholder_text="command...",
                             height=24, font=("Consolas", 10))
            e.pack(side="left", fill="x", expand=True)
            text_var.trace_add("write", lambda *_: self.on_change())

            def rm_cmd():
                block_info["cmd_rows"] = [r for r in block_info["cmd_rows"]
                                           if r[0] is not type_var]
                cmd_row.destroy()
                self.on_change()

            ctk.CTkButton(cmd_row, text="X", width=24, height=24,
                          fg_color=BTN_DEL, hover_color=BTN_DEL2,
                          command=rm_cmd).pack(side="right", padx=4)
            block_info["cmd_rows"].append((type_var, text_var))

        btn_row = ctk.CTkFrame(block_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=8, pady=(0, 6))
        ctk.CTkButton(btn_row, text="+ Command", width=95, height=24,
                      fg_color=BTN, hover_color=BTN_H, font=("Consolas", 10),
                      command=add_cmd).pack(side="left")

        def remove_block():
            self.blocks = [b for b in self.blocks if b is not block_info]
            block_frame.destroy()
            self.on_change()

        ctk.CTkButton(btn_row, text="Remove Usage", width=110, height=24,
                      fg_color=BTN_DEL, hover_color=BTN_DEL2, font=("Consolas", 10),
                      command=remove_block).pack(side="right")

        for ctype, ctext in cmds:
            add_cmd(ctype, ctext)

        self.blocks.append(block_info)

    def get_data(self) -> list:
        result = []
        for b in self.blocks:
            cmds = []
            for type_var, text_var in b["cmd_rows"]:
                t = text_var.get().strip()
                if t:
                    cmds.append(f"{type_var.get()} {t}")
            if not cmds:
                continue

            try:
                consume = int(b["consume"].get())
            except (ValueError, TypeError):
                consume = 0

            on_cd_raw = b["on_cooldown"].get().strip()
            on_cd = [l.strip() for l in on_cd_raw.splitlines() if l.strip()] if on_cd_raw else []

            entry = {
                "button":       b["button"].get(),
                "at":           b["at"].get(),
                "cancel":       b["cancel"].get(),
                "cooldown":     b["cooldown"].get().strip(),
                "cooldown_type":b["cd_type"].get(),
                "on_cooldown":  on_cd,
                "freezetime":   b["freezetime"].get().strip(),
                "consume":      consume,
                "commands":     cmds,
            }
            result.append(entry)
        return result

    def load_data(self, data: list):
        for b in list(self.blocks):
            try:
                b["frame"].destroy()
            except Exception:
                pass
        self.blocks.clear()
        for entry in data:
            cmds_raw = entry.get("commands", [])
            cmds = []
            for c in cmds_raw:
                parts = c.split(" ", 1)
                if len(parts) == 2 and parts[0] in ("[console]", "[player]"):
                    cmds.append((parts[0], parts[1]))
                else:
                    cmds.append(("[console]", c))
            self.add_block(
                button       = entry.get("button", "right"),
                at           = entry.get("at", "any"),
                cancel       = entry.get("cancel", True),
                cooldown     = entry.get("cooldown", ""),
                cooldown_type= entry.get("cooldown_type", "PER_ITEM"),
                on_cooldown  = entry.get("on_cooldown", []),
                freezetime   = entry.get("freezetime", ""),
                consume      = entry.get("consume", 0),
                cmds         = cmds,
            )


# ---------------------------------------------
#  ITEM EDITOR
# ---------------------------------------------

class ItemEditor(ctk.CTkFrame):
    def __init__(self, parent, on_change):
        super().__init__(parent, fg_color=BG_PANEL)
        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color=BG_PANEL,
            scrollbar_fg_color=SCROLL_FG,
            scrollbar_button_color=SCROLL_BTN,
            scrollbar_button_hover_color=SCROLL_HOV,
        )
        self._scroll.pack(fill="both", expand=True)
        self.on_change = on_change
        self._build()

    def _build(self):
        P = {"padx": 14, "pady": 5}

        # --- Basic Info ---
        self._section("Basic Info")

        r = self._row()
        ctk.CTkLabel(r, text="Item Key:", width=115, anchor="w",
                     font=("Consolas", 12)).pack(side="left")
        self.key_var = tk.StringVar()
        ctk.CTkEntry(r, textvariable=self.key_var, placeholder_text="e.g: dragon_sword",
                     font=("Consolas", 12)).pack(side="left", fill="x", expand=True)
        self.key_var.trace_add("write", lambda *_: self.on_change())

        r = self._row()
        ctk.CTkLabel(r, text="Material:", width=115, anchor="w",
                     font=("Consolas", 12)).pack(side="left")
        self.mat_var = tk.StringVar(value="DIAMOND_SWORD")
        ctk.CTkOptionMenu(r, variable=self.mat_var, values=MATERIALS,
                          width=260, height=32, font=("Consolas", 11),
                          command=lambda _: self.on_change()).pack(side="left")

        r = self._row()
        ctk.CTkLabel(r, text="CMD:", width=115, anchor="w",
                     font=("Consolas", 12)).pack(side="left")
        self.cmd_var = tk.StringVar()
        ctk.CTkEntry(r, textvariable=self.cmd_var, placeholder_text="e.g: 1001  (optional)",
                     width=180, font=("Consolas", 12)).pack(side="left")
        self.cmd_var.trace_add("write", lambda *_: self.on_change())

        r = self._row()
        ctk.CTkLabel(r, text="Display Name:", width=115, anchor="w",
                     font=("Consolas", 12)).pack(side="left")
        self.name_color_var = tk.StringVar(value="Gold")
        ctk.CTkOptionMenu(r, variable=self.name_color_var,
                          values=list(MINI_COLORS.keys()),
                          width=110, height=32, font=("Consolas", 11),
                          command=lambda _: self.on_change()).pack(side="left", padx=(0, 6))
        self.name_var = tk.StringVar()
        ctk.CTkEntry(r, textvariable=self.name_var, placeholder_text="item name...",
                     font=("Consolas", 12)).pack(side="left", fill="x", expand=True)
        self.name_var.trace_add("write", lambda *_: self.on_change())

        r = self._row()
        ctk.CTkLabel(r, text="Amount:", width=115, anchor="w",
                     font=("Consolas", 12)).pack(side="left")
        self.amount_var = tk.StringVar(value="1")
        ctk.CTkEntry(r, textvariable=self.amount_var, width=55,
                     font=("Consolas", 12)).pack(side="left", padx=(0, 20))
        self.amount_var.trace_add("write", lambda *_: self.on_change())

        self.unbreakable_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(r, text="Unbreakable", variable=self.unbreakable_var,
                        font=("Consolas", 12), command=self.on_change).pack(side="left")

        r = self._row()
        ctk.CTkLabel(r, text="Durability:", width=115, anchor="w",
                     font=("Consolas", 12)).pack(side="left")
        self.durability_var = tk.StringVar()
        ctk.CTkEntry(r, textvariable=self.durability_var,
                     placeholder_text="optional (requires SIG 1.9.0+)",
                     font=("Consolas", 12)).pack(side="left", fill="x", expand=True)
        self.durability_var.trace_add("write", lambda *_: self.on_change())

        # --- Item Properties ---
        self._sep()
        self._section("Item Properties")

        r = self._row()
        self.is_ingredient_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(r, text="is-ingredient  (can be used in crafting recipes)",
                        variable=self.is_ingredient_var, font=("Consolas", 12),
                        command=self.on_change).pack(side="left")

        r = self._row()
        self.can_put_inventory_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(r, text="can-be-put-in-inventory",
                        variable=self.can_put_inventory_var, font=("Consolas", 12),
                        command=self.on_change).pack(side="left")

        r = self._row()
        self.remove_on_death_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(r, text="remove-on-death  (item won't drop on death)",
                        variable=self.remove_on_death_var, font=("Consolas", 12),
                        command=self.on_change).pack(side="left")

        r = self._row()
        self.is_plain_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(r, text="is-plain  (behaves like normal item, overrides other flags)",
                        variable=self.is_plain_var, font=("Consolas", 12),
                        command=self.on_change).pack(side="left")

        r = self._row()
        self.can_move_var = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(r, text="can-move  (player can move item in inventory)",
                        variable=self.can_move_var, font=("Consolas", 12),
                        command=self.on_change).pack(side="left")

        # --- Color & Head Texture ---
        self._sep()
        self._section("Color & Head Texture")

        r = self._row()
        ctk.CTkLabel(r, text="Color:", width=115, anchor="w",
                     font=("Consolas", 12)).pack(side="left")
        self.color_var = tk.StringVar()
        ctk.CTkEntry(r, textvariable=self.color_var,
                     placeholder_text="e.g: [hex] #ff00ff  or  [dye] RED  (leather/potion only)",
                     font=("Consolas", 11)).pack(side="left", fill="x", expand=True)
        self.color_var.trace_add("write", lambda *_: self.on_change())

        r = self._row()
        ctk.CTkLabel(r, text="Head Texture:", width=115, anchor="w",
                     font=("Consolas", 12)).pack(side="left")
        self.head_var = tk.StringVar()
        ctk.CTkEntry(r, textvariable=self.head_var,
                     placeholder_text="e.g: [nickname] Steve  or  [url] https://...  or  [base64] ...",
                     font=("Consolas", 11)).pack(side="left", fill="x", expand=True)
        self.head_var.trace_add("write", lambda *_: self.on_change())

        # --- Lore ---
        self._sep()
        self.lore_editor = LoreEditor(self._scroll, self.on_change)
        self.lore_editor.pack(fill="x", **P)

        # --- Enchantments ---
        self._sep()
        self.ench_editor = EnchantEditor(self._scroll, self.on_change)
        self.ench_editor.pack(fill="x", **P)

        # --- Attributes ---
        self._sep()
        self.attr_editor = AttributeEditor(self._scroll, self.on_change)
        self.attr_editor.pack(fill="x", **P)

        # --- Item Flags ---
        self._sep()
        self._section("Item Flags")
        flags_frame = ctk.CTkFrame(self._scroll, fg_color=BG_HDR, corner_radius=4)
        flags_frame.pack(fill="x", **P)
        self.flag_vars: dict[str, tk.BooleanVar] = {}
        grid = ctk.CTkFrame(flags_frame, fg_color="transparent")
        grid.pack(padx=10, pady=8)
        for i, flag in enumerate(ITEM_FLAGS):
            v = tk.BooleanVar(value=False)
            self.flag_vars[flag] = v
            ctk.CTkCheckBox(grid, text=flag, variable=v,
                            font=("Consolas", 11),
                            command=self.on_change
                            ).grid(row=i // 2, column=i % 2, sticky="w", padx=14, pady=3)

        # --- NBT ---
        self._sep()
        self._section("NBT (raw)")
        r = self._row()
        self.nbt_var = tk.StringVar()
        ctk.CTkEntry(r, textvariable=self.nbt_var,
                     placeholder_text='{CustomTag: "value"}  — advanced use only',
                     font=("Consolas", 11)).pack(fill="x", expand=True)
        self.nbt_var.trace_add("write", lambda *_: self.on_change())

        # --- Usage ---
        self._sep()
        self.usage_editor = UsageEditor(self._scroll, self.on_change)
        self.usage_editor.pack(fill="x", **P)

        self._sep()

    def _section(self, title):
        ctk.CTkLabel(self._scroll, text=title,
                     font=("Consolas", 13, "bold"),
                     text_color=TXT_MAIN).pack(anchor="w", padx=14, pady=(10, 2))

    def _row(self):
        f = ctk.CTkFrame(self._scroll, fg_color="transparent")
        f.pack(fill="x", padx=14, pady=4)
        return f

    def _sep(self):
        ctk.CTkFrame(self._scroll, fg_color=BORDER, height=1).pack(fill="x", pady=6)

    def get_item_data(self) -> dict:
        try:
            amount = int(self.amount_var.get())
        except (ValueError, TypeError):
            amount = 1
        return {
            "key":               slugify(self.key_var.get()) or "item",
            "material":          self.mat_var.get(),
            "cmd":               self.cmd_var.get(),
            "name_text":         self.name_var.get(),
            "name_color":        self.name_color_var.get(),
            "amount":            amount,
            "unbreakable":       self.unbreakable_var.get(),
            "durability":        self.durability_var.get(),
            "lore":              self.lore_editor.get_data(),
            "enchantments":      self.ench_editor.get_data(),
            "attributes":        self.attr_editor.get_data(),
            "flags":             [f for f, v in self.flag_vars.items() if v.get()],
            "color":             self.color_var.get(),
            "head_texture":      self.head_var.get(),
            "nbt":               self.nbt_var.get(),
            "is_ingredient":     self.is_ingredient_var.get(),
            "can_put_in_inventory": self.can_put_inventory_var.get(),
            "remove_on_death":   self.remove_on_death_var.get(),
            "is_plain":          self.is_plain_var.get(),
            "can_move":          self.can_move_var.get(),
            "usage":             self.usage_editor.get_data(),
        }

    def load_item_data(self, data: dict):
        self.key_var.set(data.get("key", ""))
        self.mat_var.set(data.get("material", "DIAMOND_SWORD"))
        self.cmd_var.set(data.get("cmd", ""))
        self.name_var.set(data.get("name_text", ""))
        self.name_color_var.set(data.get("name_color", "Gold"))
        self.amount_var.set(str(data.get("amount", 1)))
        self.unbreakable_var.set(data.get("unbreakable", False))
        self.durability_var.set(str(data.get("durability", "")))
        self.lore_editor.load_data(data.get("lore", []))
        self.ench_editor.load_data(data.get("enchantments", {}))
        self.attr_editor.load_data(data.get("attributes", []))
        for flag, v in self.flag_vars.items():
            v.set(flag in data.get("flags", []))
        self.color_var.set(data.get("color", ""))
        self.head_var.set(data.get("head_texture", ""))
        self.nbt_var.set(data.get("nbt", ""))
        self.is_ingredient_var.set(data.get("is_ingredient", False))
        self.can_put_inventory_var.set(data.get("can_put_in_inventory", False))
        self.remove_on_death_var.set(data.get("remove_on_death", False))
        self.is_plain_var.set(data.get("is_plain", False))
        self.can_move_var.set(data.get("can_move", True))
        self.usage_editor.load_data(data.get("usage", []))


# ---------------------------------------------
#  MAIN APP
# ---------------------------------------------

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SIG Config Tool")
        self.geometry("1350x880")
        self.minsize(1100, 700)
        self.configure(fg_color=BG_ROOT)

        # Pencere ikonu
        try:
            base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
            ico_path = os.path.join(base, "sword-template.ico")
            if os.path.exists(ico_path):
                self.iconbitmap(ico_path)
            else:
                from PIL import Image, ImageTk
                img = Image.open(os.path.join(base, "eh.png")).resize((32, 32), Image.NEAREST)
                icon_img = ImageTk.PhotoImage(img)
                self.iconphoto(True, icon_img)
                self._icon_img = icon_img
        except Exception:
            pass

        self.project_name = ""
        self.items: list[dict] = []
        self.selected_idx: int | None = None
        self.unsaved = False
        self.item_editor = None

        self._build_header()
        self._build_welcome()

    # -----------------------------------------------

    def _build_header(self):
        hdr = ctk.CTkFrame(self, fg_color=BG_PANEL, height=52, corner_radius=0)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        self.back_btn = ctk.CTkButton(hdr, text="<", width=36, height=34,
                                      font=("Consolas", 14, "bold"),
                                      fg_color=BTN, hover_color=BTN_H,
                                      command=self._go_home)
        self.back_btn.pack(side="left", padx=(6, 0), pady=9)
        self.back_btn.pack_forget()

        neon = make_neon_label(hdr, "SIG Config Tool", font_size=16, bg="#111111")
        neon.pack(side="left", padx=18)

        self.project_label = ctk.CTkLabel(hdr, text="",
                                          font=("Consolas", 13, "bold"),
                                          text_color=TXT_MAIN)
        self.project_label.pack(side="left", padx=20)

        for txt, cmd in [
            ("💾 Save",        self._save_project),
            ("📂 Open",        self._load_project),
            ("📋 YAML Export", self._export_yaml),
        ]:
            ctk.CTkButton(hdr, text=txt, command=cmd, height=34, width=130,
                          font=("Consolas", 12),
                          fg_color=BTN, hover_color=BTN_H,
                          ).pack(side="right", padx=6, pady=9)

    def _build_welcome(self):
        self.welcome_frame = ctk.CTkFrame(self, fg_color=BG_ROOT)
        self.welcome_frame.pack(fill="both", expand=True)

        center = ctk.CTkFrame(self.welcome_frame, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        inner = ctk.CTkFrame(center, fg_color="transparent")
        inner.pack()

        img_label = ctk.CTkLabel(inner, text="")
        img_label.pack(side="left", padx=(0, 40))

        try:
            base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
            src_img = tk.PhotoImage(file=os.path.join(base, "eh.png"))
            expanded_img = src_img.zoom(13, 13)
            img_label.configure(image=expanded_img)
            img_label.image = expanded_img
        except Exception:
            img_label.configure(text="[ eh.png not found ]", font=("Consolas", 12), text_color="#cc4444")

        right = ctk.CTkFrame(inner, fg_color="transparent")
        right.pack(side="left")

        neon2 = make_neon_label(right, "SIG Config Tool", font_size=24, bg="#0a0a0a")
        neon2.pack(anchor="w")
        ctk.CTkLabel(right, text="Visual configurator for SimpleItemGenerator",
                     font=("Consolas", 12), text_color=TXT_DIM).pack(anchor="w", pady=(4, 32))

        ctk.CTkButton(right, text="New Project", height=50, width=280,
                      font=("Consolas", 15, "bold"),
                      fg_color=BTN, hover_color=BTN_H, corner_radius=4,
                      command=self._new_project).pack(pady=(0, 10))
        ctk.CTkButton(right, text="Open Project", height=44, width=280,
                      font=("Consolas", 13),
                      fg_color=BTN, hover_color=BTN, corner_radius=4,
                      border_width=1, border_color=BORDER,
                      command=self._load_project).pack()

        ctk.CTkLabel(right, text="v8.0  --  SimpleItemGenerator Config Tool",
                     font=("Consolas", 10), text_color=TXT_DIM).pack(anchor="w", pady=(28, 0))

        sig_label = ctk.CTkLabel(self.welcome_frame, text="by Goko0023",
                                 font=("Consolas", 11), text_color="#3a3a3a")
        sig_label.place(relx=0.0, rely=1.0, anchor="sw", x=14, y=-12)

    def _build_main_layout(self):
        if hasattr(self, "welcome_frame"):
            self.welcome_frame.destroy()

        self.back_btn.pack(side="left", padx=(6, 0), pady=9)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.left_panel = ctk.CTkFrame(self.main_frame, fg_color=BG_PANEL, corner_radius=4)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 6))

        self.right_panel = ctk.CTkFrame(self.main_frame, fg_color=BG_PANEL,
                                        corner_radius=4, width=420)
        self.right_panel.pack(side="right", fill="both")
        self.right_panel.pack_propagate(False)

        self._build_left_panel()
        self._build_right_panel()

    def _build_left_panel(self):
        list_hdr = ctk.CTkFrame(self.left_panel, fg_color=BG_HDR, height=40, corner_radius=0)
        list_hdr.pack(fill="x")
        list_hdr.pack_propagate(False)
        ctk.CTkLabel(list_hdr, text="Items", font=("Consolas", 13, "bold"),
                     text_color="#ffffff").pack(side="left", padx=12)
        ctk.CTkButton(list_hdr, text="+ New Item", height=28, width=110,
                      font=("Consolas", 12), fg_color=BTN, hover_color=BTN_H,
                      command=self._add_item).pack(side="right", padx=8, pady=6)

        self.item_list_frame = ctk.CTkScrollableFrame(
            self.left_panel, height=140, fg_color=BG_PANEL,
            scrollbar_fg_color=SCROLL_FG,
            scrollbar_button_color=SCROLL_BTN,
            scrollbar_button_hover_color=SCROLL_HOV,
        )
        self.item_list_frame.pack(fill="x", padx=6, pady=4)

        ctk.CTkFrame(self.left_panel, fg_color=BORDER, height=1).pack(fill="x")

        self.editor_container = ctk.CTkFrame(self.left_panel, fg_color=BG_PANEL)
        self.editor_container.pack(fill="both", expand=True)

        self.editor_label = ctk.CTkLabel(
            self.editor_container,
            text="Select an item or add a new one",
            font=("Consolas", 12), text_color=TXT_SUB,
        )
        self.editor_label.pack(pady=20)

    def _build_right_panel(self):
        top = ctk.CTkFrame(self.right_panel, fg_color=BG_HDR, height=40, corner_radius=0)
        top.pack(fill="x")
        top.pack_propagate(False)
        ctk.CTkLabel(top, text="Live YAML Preview", font=("Consolas", 13, "bold"),
                     text_color="#ffffff").pack(side="left", padx=12, pady=10)
        ctk.CTkButton(top, text="Copy", height=26, width=80,
                      font=("Consolas", 11), fg_color=BTN, hover_color=BTN_H,
                      command=self._copy_yaml).pack(side="right", padx=8, pady=7)

        self.yaml_box = ctk.CTkTextbox(
            self.right_panel, font=("Consolas", 11),
            fg_color=BG_ROOT, text_color=YAML_TEXT,
            wrap="none", state="disabled",
        )
        self.yaml_box.pack(fill="both", expand=True, padx=8, pady=8)

    # -- PROJECT OPS ---------------------------

    def _go_home(self):
        if self.unsaved and self.items:
            if not messagebox.askyesno("Go Home", "You have unsaved changes. Go to home screen anyway?"):
                return
        if hasattr(self, "main_frame"):
            self.main_frame.destroy()
        self.project_name = ""
        self.items.clear()
        self.selected_idx = None
        self.unsaved = False
        if self.item_editor is not None:
            try:
                self.item_editor.destroy()
            except Exception:
                pass
            self.item_editor = None
        self.project_label.configure(text="")
        self.back_btn.pack_forget()
        self._build_welcome()

    def _new_project(self):
        name = simpledialog.askstring("New Project", "Enter project name:", initialvalue="MyServer")
        if not name:
            return
        self.project_name = name.strip()
        self.items.clear()
        self.selected_idx = None
        self.unsaved = False
        if self.item_editor is not None:
            try:
                self.item_editor.destroy()
            except Exception:
                pass
            self.item_editor = None
        self.project_label.configure(text=f"[ {self.project_name} ]")
        self._build_main_layout()
        self._refresh_yaml()

    def _save_project(self):
        if not self.project_name:
            messagebox.showwarning("Warning", "Create a project first!")
            return
        self._flush_editor()
        path = filedialog.asksaveasfilename(
            defaultextension=".sigproj",
            filetypes=[("SIG Project", "*.sigproj"), ("JSON", "*.json")],
            initialfile=f"{self.project_name}.sigproj",
            title="Save Project",
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"project": self.project_name, "items": self.items},
                          f, ensure_ascii=False, indent=2)
        except OSError as e:
            messagebox.showerror("Error", f"Could not save:\n{e}")
            return
        self.unsaved = False
        messagebox.showinfo("Saved", f"Project saved:\n{path}")

    def _load_project(self):
        path = filedialog.askopenfilename(
            filetypes=[("SIG Project", "*.sigproj"), ("JSON", "*.json")],
            title="Open Project",
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            messagebox.showerror("Error", f"Could not load project:\n{e}")
            return
        self.project_name = data.get("project", "Project")
        self.items = data.get("items", [])
        self.selected_idx = None
        if self.item_editor is not None:
            try:
                self.item_editor.destroy()
            except Exception:
                pass
            self.item_editor = None
        self.project_label.configure(text=f"[ {self.project_name} ]")
        if hasattr(self, "welcome_frame"):
            self._build_main_layout()
        else:
            self._rebuild_item_list()
        self._refresh_yaml()

    def _export_yaml(self):
        if not self.items:
            messagebox.showwarning("Warning", "No items in project!")
            return
        self._flush_editor()
        path = filedialog.asksaveasfilename(
            defaultextension=".yml",
            filetypes=[("YAML", "*.yml")],
            initialfile="items.yml",
            title="YAML Export",
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self._build_full_yaml())
        except OSError as e:
            messagebox.showerror("Error", f"Could not export:\n{e}")
            return
        messagebox.showinfo("Export", f"YAML exported:\n{path}")

    # -- ITEM OPS ------------------------------

    def _add_item(self):
        self._flush_editor()
        new_idx = len(self.items)
        self.items.append({
            "key":              f"item_{new_idx + 1}",
            "material":         "DIAMOND_SWORD",
            "cmd":              "",
            "name_text":        "",
            "name_color":       "Gold",
            "amount":           1,
            "unbreakable":      False,
            "durability":       "",
            "lore":             [],
            "enchantments":     {},
            "attributes":       [],
            "flags":            [],
            "color":            "",
            "head_texture":     "",
            "nbt":              "",
            "is_ingredient":    False,
            "can_put_in_inventory": False,
            "remove_on_death":  False,
            "is_plain":         False,
            "can_move":         True,
            "usage":            [],
        })
        self.unsaved = True
        self._select_item(new_idx)

    def _select_item(self, idx: int):
        if self.selected_idx is not None and self.selected_idx != idx:
            self._flush_editor()
        self.selected_idx = idx

        if self.item_editor is not None:
            try:
                self.item_editor.destroy()
            except Exception:
                pass
            self.item_editor = None

        if hasattr(self, "editor_label"):
            try:
                if self.editor_label.winfo_exists():
                    self.editor_label.destroy()
            except Exception:
                pass

        self.item_editor = ItemEditor(self.editor_container, self._on_editor_change)
        self.item_editor.pack(fill="both", expand=True)
        self.item_editor.load_item_data(self.items[idx])

        self._rebuild_item_list()
        self._refresh_yaml()

    def _delete_item(self, idx: int):
        if not messagebox.askyesno("Delete", f"Delete '{self.items[idx].get('key', '?')}'?"):
            return
        self.items.pop(idx)
        if self.selected_idx == idx:
            self.selected_idx = None
            if self.item_editor is not None:
                try:
                    self.item_editor.destroy()
                except Exception:
                    pass
                self.item_editor = None
            self.editor_label = ctk.CTkLabel(
                self.editor_container,
                text="Select an item or add a new one",
                font=("Consolas", 12), text_color=TXT_SUB,
            )
            self.editor_label.pack(pady=20)
        elif self.selected_idx is not None and self.selected_idx > idx:
            self.selected_idx -= 1
        self._rebuild_item_list()
        self._refresh_yaml()

    def _rebuild_item_list(self):
        for w in self.item_list_frame.winfo_children():
            w.destroy()

        if not self.items:
            ctk.CTkLabel(self.item_list_frame,
                         text="No items yet  --  click + New Item",
                         font=("Consolas", 11), text_color=TXT_SUB).pack(pady=10)
            return

        for i, item in enumerate(self.items):
            is_sel = (i == self.selected_idx)
            row = ctk.CTkFrame(self.item_list_frame,
                               fg_color=SEL_BG if is_sel else BG_HDR,
                               corner_radius=4)
            row.pack(fill="x", pady=2, padx=4)

            ctk.CTkLabel(row,
                         text=(">> " if is_sel else "   ") + item.get("key", "?"),
                         font=("Consolas", 12, "bold" if is_sel else "normal"),
                         text_color="#ffffff" if is_sel else TXT_SUB,
                         anchor="w").pack(side="left", padx=10, pady=6, fill="x", expand=True)

            ctk.CTkLabel(row, text=item.get("material", ""),
                         font=("Consolas", 10), text_color=TXT_SUB).pack(side="left", padx=6)

            ctk.CTkButton(row, text="X", width=26, height=26,
                          fg_color=BTN_DEL, hover_color=BTN_DEL2,
                          command=lambda i=i: self._delete_item(i)
                          ).pack(side="right", padx=6, pady=4)
            ctk.CTkButton(row, text="Select", width=60, height=26,
                          fg_color=BTN_H if is_sel else BTN, hover_color=BTN_H,
                          font=("Consolas", 11),
                          command=lambda i=i: self._select_item(i)
                          ).pack(side="right", padx=4, pady=4)

    # -- YAML ----------------------------------

    def _flush_editor(self):
        if self.item_editor is not None and self.selected_idx is not None:
            try:
                data = self.item_editor.get_item_data()
                if 0 <= self.selected_idx < len(self.items):
                    self.items[self.selected_idx] = data
            except Exception:
                pass

    def _on_editor_change(self):
        self._flush_editor()
        if self.selected_idx is not None:
            self._rebuild_item_list()
        self._refresh_yaml()

    def _build_full_yaml(self) -> str:
        # SIG plugin format: items: root key
        all_items = {}
        for item in self.items:
            key = item.get("key") or "item"
            all_items[key] = build_yaml_for_item(item)
        root = {"items": all_items}
        return yaml.dump(root, allow_unicode=True,
                         default_flow_style=False, sort_keys=False, indent=2)

    def _refresh_yaml(self):
        if not hasattr(self, "yaml_box"):
            return
        try:
            text = self._build_full_yaml() if self.items else "# No items yet\n"
        except Exception as e:
            text = f"# Error building YAML: {e}\n"
        self.yaml_box.configure(state="normal")
        self.yaml_box.delete("1.0", "end")
        self.yaml_box.insert("1.0", text)
        self.yaml_box.configure(state="disabled")

    def _copy_yaml(self):
        self.yaml_box.configure(state="normal")
        content = self.yaml_box.get("1.0", "end")
        self.yaml_box.configure(state="disabled")
        self.clipboard_clear()
        self.clipboard_append(content)
        messagebox.showinfo("Copied", "YAML copied to clipboard!")

    def on_close(self):
        self._flush_editor()
        if self.unsaved and self.items:
            if messagebox.askyesno("Exit", "You have unsaved changes. Exit anyway?"):
                self.quit()
                self.destroy()
        else:
            self.quit()
            self.destroy()


# ---------------------------------------------
#  ENTRY POINT
# ---------------------------------------------

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()

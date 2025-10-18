from endstone.plugin import Plugin
from endstone.event import event_handler, PlayerInteractActorEvent
from endstone.form import ActionForm
from endstone import ColorFormat


class BuilderShopPlugin(Plugin):
    """Plugin that provides all obtainable items through NPC interactions"""

    api_version = "0.10"

    # Comprehensive list of ALL items excluding tools, armor, bedrock, arrows, potions, enchanted books, and give-only items
    BUILDING_MATERIALS = {
        "Stone & Rock Blocks": [
            "stone", "cobblestone", "mossy_cobblestone", "smooth_stone",
            "stone_bricks", "mossy_stone_bricks", "cracked_stone_bricks",
            "chiseled_stone_bricks", "infested_stone", "infested_cobblestone",
            "infested_stone_bricks", "infested_mossy_stone_bricks",
            "infested_cracked_stone_bricks", "infested_chiseled_stone_bricks",
            "granite", "polished_granite", "diorite", "polished_diorite",
            "andesite", "polished_andesite", "calcite", "tuff",
            "deepslate", "cobbled_deepslate", "polished_deepslate",
            "deepslate_bricks", "cracked_deepslate_bricks",
            "deepslate_tiles", "cracked_deepslate_tiles",
            "chiseled_deepslate", "reinforced_deepslate"
        ],
        "Wood Blocks & Logs": [
            "oak_planks", "spruce_planks", "birch_planks", "jungle_planks",
            "acacia_planks", "dark_oak_planks", "mangrove_planks",
            "cherry_planks", "bamboo_planks", "bamboo_mosaic",
            "crimson_planks", "warped_planks",
            "oak_log", "spruce_log", "birch_log", "jungle_log",
            "acacia_log", "dark_oak_log", "mangrove_log", "cherry_log",
            "stripped_oak_log", "stripped_spruce_log", "stripped_birch_log",
            "stripped_jungle_log", "stripped_acacia_log", "stripped_dark_oak_log",
            "stripped_mangrove_log", "stripped_cherry_log",
            "oak_wood", "spruce_wood", "birch_wood", "jungle_wood",
            "acacia_wood", "dark_oak_wood", "mangrove_wood", "cherry_wood",
            "stripped_oak_wood", "stripped_spruce_wood", "stripped_birch_wood",
            "stripped_jungle_wood", "stripped_acacia_wood", "stripped_dark_oak_wood",
            "stripped_mangrove_wood", "stripped_cherry_wood",
            "crimson_stem", "warped_stem", "stripped_crimson_stem", "stripped_warped_stem",
            "crimson_hyphae", "warped_hyphae", "stripped_crimson_hyphae", "stripped_warped_hyphae",
            "bamboo_block", "stripped_bamboo_block"
        ],
        "Stone Stairs": [
            "stone_stairs", "cobblestone_stairs", "mossy_cobblestone_stairs",
            "stone_brick_stairs", "mossy_stone_brick_stairs",
            "granite_stairs", "polished_granite_stairs",
            "diorite_stairs", "polished_diorite_stairs",
            "andesite_stairs", "polished_andesite_stairs",
            "cobbled_deepslate_stairs", "polished_deepslate_stairs",
            "deepslate_brick_stairs", "deepslate_tile_stairs",
            "sandstone_stairs", "smooth_sandstone_stairs",
            "red_sandstone_stairs", "smooth_red_sandstone_stairs",
            "prismarine_stairs", "prismarine_brick_stairs", "dark_prismarine_stairs",
            "brick_stairs", "nether_brick_stairs", "red_nether_brick_stairs",
            "end_stone_brick_stairs", "purpur_stairs",
            "quartz_stairs", "smooth_quartz_stairs",
            "blackstone_stairs", "polished_blackstone_stairs",
            "polished_blackstone_brick_stairs", "mud_brick_stairs"
        ],
        "Wood Stairs": [
            "oak_stairs", "spruce_stairs", "birch_stairs", "jungle_stairs",
            "acacia_stairs", "dark_oak_stairs", "mangrove_stairs",
            "cherry_stairs", "bamboo_stairs", "bamboo_mosaic_stairs",
            "crimson_stairs", "warped_stairs"
        ],
        "Stone Slabs": [
            "stone_slab", "smooth_stone_slab", "cobblestone_slab",
            "mossy_cobblestone_slab", "stone_brick_slab", "mossy_stone_brick_slab",
            "granite_slab", "polished_granite_slab", "diorite_slab",
            "polished_diorite_slab", "andesite_slab", "polished_andesite_slab",
            "cobbled_deepslate_slab", "polished_deepslate_slab",
            "deepslate_brick_slab", "deepslate_tile_slab",
            "sandstone_slab", "smooth_sandstone_slab", "cut_sandstone_slab",
            "red_sandstone_slab", "smooth_red_sandstone_slab", "cut_red_sandstone_slab",
            "prismarine_slab", "prismarine_brick_slab", "dark_prismarine_slab",
            "brick_slab", "nether_brick_slab", "red_nether_brick_slab",
            "end_stone_brick_slab", "purpur_slab",
            "quartz_slab", "smooth_quartz_slab",
            "blackstone_slab", "polished_blackstone_slab",
            "polished_blackstone_brick_slab", "mud_brick_slab"
        ],
        "Wood Slabs": [
            "oak_slab", "spruce_slab", "birch_slab", "jungle_slab",
            "acacia_slab", "dark_oak_slab", "mangrove_slab",
            "cherry_slab", "bamboo_slab", "bamboo_mosaic_slab",
            "crimson_slab", "warped_slab"
        ],
        "Walls": [
            "cobblestone_wall", "mossy_cobblestone_wall",
            "stone_brick_wall", "mossy_stone_brick_wall",
            "granite_wall", "diorite_wall", "andesite_wall",
            "cobbled_deepslate_wall", "polished_deepslate_wall",
            "deepslate_brick_wall", "deepslate_tile_wall",
            "sandstone_wall", "red_sandstone_wall",
            "brick_wall", "prismarine_wall", "red_nether_brick_wall",
            "nether_brick_wall", "blackstone_wall", "polished_blackstone_wall",
            "polished_blackstone_brick_wall", "end_stone_brick_wall",
            "mud_brick_wall"
        ],
        "Fences & Gates": [
            "oak_fence", "spruce_fence", "birch_fence", "jungle_fence",
            "acacia_fence", "dark_oak_fence", "mangrove_fence",
            "cherry_fence", "bamboo_fence", "crimson_fence", "warped_fence",
            "oak_fence_gate", "spruce_fence_gate", "birch_fence_gate",
            "jungle_fence_gate", "acacia_fence_gate", "dark_oak_fence_gate",
            "mangrove_fence_gate", "cherry_fence_gate", "bamboo_fence_gate",
            "crimson_fence_gate", "warped_fence_gate", "nether_brick_fence"
        ],
        "Nether Blocks": [
            "netherrack", "nether_bricks", "red_nether_bricks",
            "chiseled_nether_bricks", "cracked_nether_bricks",
            "nether_wart_block", "warped_wart_block",
            "soul_sand", "soul_soil", "basalt", "smooth_basalt",
            "polished_basalt", "blackstone", "gilded_blackstone",
            "polished_blackstone", "chiseled_polished_blackstone",
            "polished_blackstone_bricks", "cracked_polished_blackstone_bricks",
            "glowstone", "shroomlight", "crying_obsidian",
            "ancient_debris", "netherite_block",
            "magma_block", "nether_quartz_ore", "nether_gold_ore"
        ],
        "End Blocks": [
            "end_stone", "end_stone_bricks", "purpur_block",
            "purpur_pillar", "chorus_plant", "chorus_flower",
            "dragon_egg"
        ],
        "Ores & Minerals": [
            "coal_ore", "deepslate_coal_ore", "coal_block",
            "iron_ore", "deepslate_iron_ore", "raw_iron_block", "iron_block",
            "copper_ore", "deepslate_copper_ore", "raw_copper_block",
            "gold_ore", "deepslate_gold_ore", "raw_gold_block", "gold_block",
            "redstone_ore", "deepslate_redstone_ore", "redstone_block",
            "emerald_ore", "deepslate_emerald_ore", "emerald_block",
            "lapis_ore", "deepslate_lapis_ore", "lapis_block",
            "diamond_ore", "deepslate_diamond_ore", "diamond_block",
            "amethyst_block", "budding_amethyst",
            "small_amethyst_bud", "medium_amethyst_bud", "large_amethyst_bud", "amethyst_cluster"
        ],
        "Copper Blocks": [
            "copper_block", "exposed_copper", "weathered_copper", "oxidized_copper",
            "waxed_copper_block", "waxed_exposed_copper", "waxed_weathered_copper", "waxed_oxidized_copper",
            "cut_copper", "exposed_cut_copper", "weathered_cut_copper", "oxidized_cut_copper",
            "waxed_cut_copper", "waxed_exposed_cut_copper", "waxed_weathered_cut_copper", "waxed_oxidized_cut_copper",
            "cut_copper_stairs", "exposed_cut_copper_stairs", "weathered_cut_copper_stairs",
            "oxidized_cut_copper_stairs",
            "waxed_cut_copper_stairs", "waxed_exposed_cut_copper_stairs", "waxed_weathered_cut_copper_stairs",
            "waxed_oxidized_cut_copper_stairs",
            "cut_copper_slab", "exposed_cut_copper_slab", "weathered_cut_copper_slab", "oxidized_cut_copper_slab",
            "waxed_cut_copper_slab", "waxed_exposed_cut_copper_slab", "waxed_weathered_cut_copper_slab",
            "waxed_oxidized_cut_copper_slab",
            "lightning_rod", "copper_bulb", "exposed_copper_bulb", "weathered_copper_bulb", "oxidized_copper_bulb",
            "waxed_copper_bulb", "waxed_exposed_copper_bulb", "waxed_weathered_copper_bulb",
            "waxed_oxidized_copper_bulb",
            "copper_door", "exposed_copper_door", "weathered_copper_door", "oxidized_copper_door",
            "waxed_copper_door", "waxed_exposed_copper_door", "waxed_weathered_copper_door",
            "waxed_oxidized_copper_door",
            "copper_trapdoor", "exposed_copper_trapdoor", "weathered_copper_trapdoor", "oxidized_copper_trapdoor",
            "waxed_copper_trapdoor", "waxed_exposed_copper_trapdoor", "waxed_weathered_copper_trapdoor",
            "waxed_oxidized_copper_trapdoor",
            "copper_grate", "exposed_copper_grate", "weathered_copper_grate", "oxidized_copper_grate",
            "waxed_copper_grate", "waxed_exposed_copper_grate", "waxed_weathered_copper_grate",
            "waxed_oxidized_copper_grate"
        ],
        "Decoration Blocks": [
            "bricks", "packed_mud", "mud_bricks",
            "prismarine", "prismarine_bricks", "dark_prismarine",
            "sea_lantern", "conduit",
            "quartz_block", "smooth_quartz", "quartz_bricks",
            "chiseled_quartz_block", "quartz_pillar",
            "obsidian", "respawn_anchor", "lodestone",
            "tinted_glass", "hay_block", "dried_kelp_block",
            "honeycomb_block", "honey_block", "slime_block",
            "bone_block", "target", "scaffolding"
        ],
        "Glass & Stained Glass": [
            "glass", "tinted_glass",
            "white_stained_glass", "light_gray_stained_glass", "gray_stained_glass",
            "black_stained_glass", "brown_stained_glass", "red_stained_glass",
            "orange_stained_glass", "yellow_stained_glass", "lime_stained_glass",
            "green_stained_glass", "cyan_stained_glass", "light_blue_stained_glass",
            "blue_stained_glass", "purple_stained_glass", "magenta_stained_glass",
            "pink_stained_glass",
            "glass_pane", "white_stained_glass_pane", "light_gray_stained_glass_pane",
            "gray_stained_glass_pane", "black_stained_glass_pane", "brown_stained_glass_pane",
            "red_stained_glass_pane", "orange_stained_glass_pane", "yellow_stained_glass_pane",
            "lime_stained_glass_pane", "green_stained_glass_pane", "cyan_stained_glass_pane",
            "light_blue_stained_glass_pane", "blue_stained_glass_pane", "purple_stained_glass_pane",
            "magenta_stained_glass_pane", "pink_stained_glass_pane"
        ],
        "Terracotta": [
            "terracotta", "white_terracotta", "light_gray_terracotta", "gray_terracotta",
            "black_terracotta", "brown_terracotta", "red_terracotta", "orange_terracotta",
            "yellow_terracotta", "lime_terracotta", "green_terracotta", "cyan_terracotta",
            "light_blue_terracotta", "blue_terracotta", "purple_terracotta",
            "magenta_terracotta", "pink_terracotta",
            "white_glazed_terracotta", "light_gray_glazed_terracotta", "gray_glazed_terracotta",
            "black_glazed_terracotta", "brown_glazed_terracotta", "red_glazed_terracotta",
            "orange_glazed_terracotta", "yellow_glazed_terracotta", "lime_glazed_terracotta",
            "green_glazed_terracotta", "cyan_glazed_terracotta", "light_blue_glazed_terracotta",
            "blue_glazed_terracotta", "purple_glazed_terracotta", "magenta_glazed_terracotta",
            "pink_glazed_terracotta"
        ],
        "Concrete & Powder": [
            "white_concrete", "light_gray_concrete", "gray_concrete", "black_concrete",
            "brown_concrete", "red_concrete", "orange_concrete", "yellow_concrete",
            "lime_concrete", "green_concrete", "cyan_concrete", "light_blue_concrete",
            "blue_concrete", "purple_concrete", "magenta_concrete", "pink_concrete",
            "white_concrete_powder", "light_gray_concrete_powder", "gray_concrete_powder",
            "black_concrete_powder", "brown_concrete_powder", "red_concrete_powder",
            "orange_concrete_powder", "yellow_concrete_powder", "lime_concrete_powder",
            "green_concrete_powder", "cyan_concrete_powder", "light_blue_concrete_powder",
            "blue_concrete_powder", "purple_concrete_powder", "magenta_concrete_powder",
            "pink_concrete_powder"
        ],
        "Wool": [
            "white_wool", "light_gray_wool", "gray_wool", "black_wool",
            "brown_wool", "red_wool", "orange_wool", "yellow_wool",
            "lime_wool", "green_wool", "cyan_wool", "light_blue_wool",
            "blue_wool", "purple_wool", "magenta_wool", "pink_wool"
        ],
        "Carpet": [
            "white_carpet", "light_gray_carpet", "gray_carpet", "black_carpet",
            "brown_carpet", "red_carpet", "orange_carpet", "yellow_carpet",
            "lime_carpet", "green_carpet", "cyan_carpet", "light_blue_carpet",
            "blue_carpet", "purple_carpet", "magenta_carpet", "pink_carpet",
            "moss_carpet"
        ],
        "Sand & Sandstone": [
            "sand", "red_sand", "gravel", "suspicious_sand", "suspicious_gravel",
            "sandstone", "chiseled_sandstone", "cut_sandstone", "smooth_sandstone",
            "red_sandstone", "chiseled_red_sandstone", "cut_red_sandstone", "smooth_red_sandstone"
        ],
        "Soil & Nature": [
            "dirt", "coarse_dirt", "rooted_dirt", "mud", "clay",
            "podzol", "mycelium", "grass_block", "moss_block",
            "farmland", "dirt_path", "muddy_mangrove_roots",
            "snow", "snow_block", "ice", "packed_ice", "blue_ice",
            "powder_snow"
        ],
        "Doors & Trapdoors": [
            "oak_door", "spruce_door", "birch_door", "jungle_door",
            "acacia_door", "dark_oak_door", "mangrove_door", "cherry_door",
            "bamboo_door", "crimson_door", "warped_door", "iron_door",
            "oak_trapdoor", "spruce_trapdoor", "birch_trapdoor", "jungle_trapdoor",
            "acacia_trapdoor", "dark_oak_trapdoor", "mangrove_trapdoor",
            "cherry_trapdoor", "bamboo_trapdoor", "crimson_trapdoor",
            "warped_trapdoor", "iron_trapdoor"
        ],
        "Lighting": [
            "torch", "soul_torch", "redstone_torch",
            "lantern", "soul_lantern",
            "campfire", "soul_campfire",
            "redstone_lamp", "sea_lantern", "glowstone", "shroomlight",
            "end_rod", "froglight", "ochre_froglight", "verdant_froglight", "pearlescent_froglight",
            "glow_lichen", "sculk", "sculk_vein"
        ],
        "Redstone Components": [
            "redstone_block", "redstone_torch", "redstone_lamp",
            "repeater", "comparator", "observer", "piston", "sticky_piston",
            "lever", "tripwire_hook", "trapped_chest",
            "stone_button", "oak_button", "spruce_button", "birch_button",
            "jungle_button", "acacia_button", "dark_oak_button", "mangrove_button",
            "cherry_button", "bamboo_button", "crimson_button", "warped_button",
            "polished_blackstone_button",
            "stone_pressure_plate", "oak_pressure_plate", "spruce_pressure_plate",
            "birch_pressure_plate", "jungle_pressure_plate", "acacia_pressure_plate",
            "dark_oak_pressure_plate", "mangrove_pressure_plate", "cherry_pressure_plate",
            "bamboo_pressure_plate", "crimson_pressure_plate", "warped_pressure_plate",
            "light_weighted_pressure_plate", "heavy_weighted_pressure_plate",
            "polished_blackstone_pressure_plate",
            "dispenser", "dropper", "hopper", "tnt", "note_block",
            "daylight_detector", "target", "lightning_rod",
            "lectern", "crafter"
        ],
        "Rails": [
            "rail", "powered_rail", "detector_rail", "activator_rail"
        ],
        "Plants & Crops": [
            "oak_sapling", "spruce_sapling", "birch_sapling", "jungle_sapling",
            "acacia_sapling", "dark_oak_sapling", "mangrove_propagule", "cherry_sapling",
            "azalea", "flowering_azalea",
            "dead_bush", "grass", "fern", "dandelion", "poppy", "blue_orchid",
            "allium", "azure_bluet", "red_tulip", "orange_tulip", "white_tulip",
            "pink_tulip", "oxeye_daisy", "cornflower", "lily_of_the_valley",
            "wither_rose", "torchflower", "pitcher_plant", "spore_blossom",
            "sunflower", "lilac", "rose_bush", "peony", "tall_grass", "large_fern",
            "bamboo", "sugar_cane", "cactus", "kelp", "dried_kelp_block",
            "vine", "glow_lichen", "weeping_vines", "twisting_vines",
            "crimson_roots", "warped_roots", "nether_sprouts",
            "crimson_fungus", "warped_fungus",
            "brown_mushroom", "red_mushroom", "brown_mushroom_block", "red_mushroom_block",
            "mushroom_stem",
            "wheat_seeds", "beetroot_seeds", "melon_seeds", "pumpkin_seeds",
            "torchflower_seeds", "pitcher_pod",
            "carrot", "potato", "beetroot", "wheat", "melon", "pumpkin",
            "carved_pumpkin", "jack_o_lantern",
            "sweet_berries", "glow_berries", "cocoa_beans",
            "chorus_fruit", "chorus_flower",
            "sea_pickle", "lily_pad", "big_dripleaf", "small_dripleaf",
            "hanging_roots", "mangrove_roots"
        ],
        "Functional Blocks": [
            "crafting_table", "furnace", "blast_furnace", "smoker",
            "cartography_table", "fletching_table", "smithing_table",
            "grindstone", "loom", "stonecutter", "composter",
            "barrel", "chest", "trapped_chest", "ender_chest",
            "anvil", "chipped_anvil", "damaged_anvil",
            "brewing_stand", "cauldron", "water_cauldron", "lava_cauldron",
            "powder_snow_cauldron",
            "enchanting_table", "bookshelf", "chiseled_bookshelf",
            "lectern", "bell", "beacon", "conduit",
            "jukebox", "note_block",
            "lodestone", "respawn_anchor"
        ],
        "Storage & Utility": [
            "chest", "trapped_chest", "barrel", "ender_chest",
            "hopper", "dropper", "dispenser",
            "furnace", "blast_furnace", "smoker",
            "shulker_box"
        ],
        "Banners": [
            "white_banner", "light_gray_banner", "gray_banner", "black_banner",
            "brown_banner", "red_banner", "orange_banner", "yellow_banner",
            "lime_banner", "green_banner", "cyan_banner", "light_blue_banner",
            "blue_banner", "purple_banner", "magenta_banner", "pink_banner"
        ],
        "Beds": [
            "white_bed", "light_gray_bed", "gray_bed", "black_bed",
            "brown_bed", "red_bed", "orange_bed", "yellow_bed",
            "lime_bed", "green_bed", "cyan_bed", "light_blue_bed",
            "blue_bed", "purple_bed", "magenta_bed", "pink_bed"
        ],
        "Candles": [
            "candle", "white_candle", "light_gray_candle", "gray_candle",
            "black_candle", "brown_candle", "red_candle", "orange_candle",
            "yellow_candle", "lime_candle", "green_candle", "cyan_candle",
            "light_blue_candle", "blue_candle", "purple_candle",
            "magenta_candle", "pink_candle"
        ],
        "Mob Heads": [
            "skeleton_skull", "wither_skeleton_skull", "zombie_head",
            "player_head", "creeper_head", "dragon_head", "piglin_head"
        ],
        "Misc Decorations": [
            "painting", "item_frame", "glow_item_frame",
            "flower_pot", "armor_stand",
            "ladder", "chain",
            "sign", "hanging_sign",
            "oak_sign", "spruce_sign", "birch_sign", "jungle_sign",
            "acacia_sign", "dark_oak_sign", "mangrove_sign", "cherry_sign",
            "bamboo_sign", "crimson_sign", "warped_sign",
            "oak_hanging_sign", "spruce_hanging_sign", "birch_hanging_sign",
            "jungle_hanging_sign", "acacia_hanging_sign", "dark_oak_hanging_sign",
            "mangrove_hanging_sign", "cherry_hanging_sign", "bamboo_hanging_sign",
            "crimson_hanging_sign", "warped_hanging_sign"
        ],
        "Food Items": [
            "apple", "golden_apple", "melon_slice", "sweet_berries", "glow_berries",
            "chorus_fruit", "carrot", "golden_carrot", "potato", "baked_potato",
            "poisonous_potato", "beetroot", "dried_kelp",
            "bread", "cookie", "cake", "pumpkin_pie",
            "mushroom_stew", "rabbit_stew", "suspicious_stew",
            "beetroot_soup",
            "beef", "cooked_beef", "porkchop", "cooked_porkchop",
            "mutton", "cooked_mutton", "chicken", "cooked_chicken",
            "rabbit", "cooked_rabbit", "cod", "cooked_cod",
            "salmon", "cooked_salmon", "tropical_fish", "pufferfish",
            "rotten_flesh", "spider_eye", "honey_bottle", "milk_bucket"
        ],
        "Raw Materials": [
            "stick", "coal", "charcoal", "raw_iron", "iron_ingot", "iron_nugget",
            "raw_copper", "copper_ingot", "raw_gold", "gold_ingot", "gold_nugget",
            "diamond", "emerald", "lapis_lazuli", "redstone", "quartz",
            "netherite_scrap", "netherite_ingot",
            "amethyst_shard", "echo_shard", "disc_fragment_5",
            "flint", "clay_ball", "brick", "nether_brick",
            "prismarine_shard", "prismarine_crystals",
            "wheat", "string", "feather", "leather",
            "rabbit_hide", "honeycomb", "slime_ball",
            "ender_pearl", "blaze_rod", "blaze_powder",
            "magma_cream", "ghast_tear", "nether_star",
            "bone", "bone_meal", "ink_sac", "glow_ink_sac",
            "scute", "phantom_membrane", "nautilus_shell", "heart_of_the_sea",
            "turtle_egg", "sniffer_egg", "frogspawn",
            "gunpowder", "glowstone_dust", "sugar",
            "paper", "book", "writable_book", "written_book",
            "map", "filled_map", "compass", "recovery_compass", "clock",
            "spyglass", "brush", "shears", "flint_and_steel",
            "fire_charge", "lead", "name_tag", "saddle",
            "bucket", "water_bucket", "lava_bucket", "milk_bucket",
            "powder_snow_bucket", "cod_bucket", "salmon_bucket",
            "tropical_fish_bucket", "pufferfish_bucket", "axolotl_bucket",
            "tadpole_bucket",
            "minecart", "chest_minecart", "furnace_minecart",
            "tnt_minecart", "hopper_minecart",
            "oak_boat", "spruce_boat", "birch_boat", "jungle_boat",
            "acacia_boat", "dark_oak_boat", "mangrove_boat", "cherry_boat",
            "bamboo_raft",
            "oak_chest_boat", "spruce_chest_boat", "birch_chest_boat",
            "jungle_chest_boat", "acacia_chest_boat", "dark_oak_chest_boat",
            "mangrove_chest_boat", "cherry_chest_boat", "bamboo_chest_raft"
        ],
        "Music Discs": [
            "music_disc_13", "music_disc_cat", "music_disc_blocks",
            "music_disc_chirp", "music_disc_far", "music_disc_mall",
            "music_disc_mellohi", "music_disc_stal", "music_disc_strad",
            "music_disc_ward", "music_disc_11", "music_disc_wait",
            "music_disc_otherside", "music_disc_5", "music_disc_pigstep",
            "music_disc_relic", "music_disc_creator", "music_disc_creator_music_box",
            "music_disc_precipice"
        ],
        "Dyes": [
            "white_dye", "light_gray_dye", "gray_dye", "black_dye",
            "brown_dye", "red_dye", "orange_dye", "yellow_dye",
            "lime_dye", "green_dye", "cyan_dye", "light_blue_dye",
            "blue_dye", "purple_dye", "magenta_dye", "pink_dye"
        ],
        "Pottery & Smithing": [
            "pottery_shard_angler", "pottery_shard_archer", "pottery_shard_arms_up",
            "pottery_shard_blade", "pottery_shard_brewer", "pottery_shard_burn",
            "pottery_shard_danger", "pottery_shard_explorer", "pottery_shard_friend",
            "pottery_shard_heart", "pottery_shard_heartbreak", "pottery_shard_howl",
            "pottery_shard_miner", "pottery_shard_mourner", "pottery_shard_plenty",
            "pottery_shard_prize", "pottery_shard_sheaf", "pottery_shard_shelter",
            "pottery_shard_skull", "pottery_shard_snort",
            "netherite_upgrade_smithing_template",
            "sentry_armor_trim_smithing_template", "vex_armor_trim_smithing_template",
            "wild_armor_trim_smithing_template", "coast_armor_trim_smithing_template",
            "dune_armor_trim_smithing_template", "wayfinder_armor_trim_smithing_template",
            "raiser_armor_trim_smithing_template", "shaper_armor_trim_smithing_template",
            "host_armor_trim_smithing_template", "ward_armor_trim_smithing_template",
            "silence_armor_trim_smithing_template", "tide_armor_trim_smithing_template",
            "snout_armor_trim_smithing_template", "rib_armor_trim_smithing_template",
            "eye_armor_trim_smithing_template", "spire_armor_trim_smithing_template",
            "flow_armor_trim_smithing_template", "bolt_armor_trim_smithing_template"
        ],
        "Mob Drops": [
            "rotten_flesh", "bone", "spider_eye", "string", "slime_ball",
            "ender_pearl", "blaze_rod", "ghast_tear", "magma_cream",
            "phantom_membrane", "rabbit_hide", "rabbit_foot",
            "leather", "feather", "egg", "wool",
            "ink_sac", "glow_ink_sac", "prismarine_shard", "prismarine_crystals",
            "nautilus_shell", "scute", "gunpowder", "nether_star"
        ],
        "Spawn Eggs": [
            "axolotl_spawn_egg", "bat_spawn_egg", "bee_spawn_egg", "blaze_spawn_egg",
            "cat_spawn_egg", "cave_spider_spawn_egg", "chicken_spawn_egg",
            "cod_spawn_egg", "cow_spawn_egg", "creeper_spawn_egg",
            "dolphin_spawn_egg", "donkey_spawn_egg", "drowned_spawn_egg",
            "elder_guardian_spawn_egg", "enderman_spawn_egg", "endermite_spawn_egg",
            "evoker_spawn_egg", "fox_spawn_egg", "frog_spawn_egg",
            "ghast_spawn_egg", "glow_squid_spawn_egg", "goat_spawn_egg",
            "guardian_spawn_egg", "hoglin_spawn_egg", "horse_spawn_egg",
            "husk_spawn_egg", "llama_spawn_egg", "magma_cube_spawn_egg",
            "mooshroom_spawn_egg", "mule_spawn_egg", "ocelot_spawn_egg",
            "panda_spawn_egg", "parrot_spawn_egg", "phantom_spawn_egg",
            "pig_spawn_egg", "piglin_spawn_egg", "piglin_brute_spawn_egg",
            "pillager_spawn_egg", "polar_bear_spawn_egg", "pufferfish_spawn_egg",
            "rabbit_spawn_egg", "ravager_spawn_egg", "salmon_spawn_egg",
            "sheep_spawn_egg", "shulker_spawn_egg", "silverfish_spawn_egg",
            "skeleton_spawn_egg", "skeleton_horse_spawn_egg", "slime_spawn_egg",
            "sniffer_spawn_egg", "snow_golem_spawn_egg", "spider_spawn_egg",
            "squid_spawn_egg", "stray_spawn_egg", "strider_spawn_egg",
            "tadpole_spawn_egg", "trader_llama_spawn_egg", "tropical_fish_spawn_egg",
            "turtle_spawn_egg", "vex_spawn_egg", "villager_spawn_egg",
            "vindicator_spawn_egg", "wandering_trader_spawn_egg", "warden_spawn_egg",
            "witch_spawn_egg", "wither_skeleton_spawn_egg", "wolf_spawn_egg",
            "zoglin_spawn_egg", "zombie_spawn_egg", "zombie_horse_spawn_egg",
            "zombie_villager_spawn_egg", "zombified_piglin_spawn_egg",
            "allay_spawn_egg", "camel_spawn_egg", "iron_golem_spawn_egg"
        ],
        "Misc Items": [
            "totem_of_undying", "elytra", "firework_rocket", "firework_star",
            "dragon_breath", "experience_bottle", "end_crystal",
            "goat_horn", "trial_key", "ominous_trial_key",
            "bundle", "mace", "wind_charge", "breeze_rod",
            "armadillo_scute", "wolf_armor", "honeycomb"
        ],
        "Coral & Ocean": [
            "tube_coral", "brain_coral", "bubble_coral", "fire_coral", "horn_coral",
            "tube_coral_fan", "brain_coral_fan", "bubble_coral_fan",
            "fire_coral_fan", "horn_coral_fan",
            "tube_coral_block", "brain_coral_block", "bubble_coral_block",
            "fire_coral_block", "horn_coral_block",
            "dead_tube_coral", "dead_brain_coral", "dead_bubble_coral",
            "dead_fire_coral", "dead_horn_coral",
            "dead_tube_coral_fan", "dead_brain_coral_fan", "dead_bubble_coral_fan",
            "dead_fire_coral_fan", "dead_horn_coral_fan",
            "dead_tube_coral_block", "dead_brain_coral_block", "dead_bubble_coral_block",
            "dead_fire_coral_block", "dead_horn_coral_block",
            "sponge", "wet_sponge", "kelp", "seagrass", "sea_pickle",
            "turtle_egg", "heart_of_the_sea", "conduit", "nautilus_shell"
        ],
        "Sculk Blocks": [
            "sculk", "sculk_vein", "sculk_catalyst", "sculk_sensor",
            "calibrated_sculk_sensor", "sculk_shrieker"
        ]
    }

    def on_enable(self):
        """Called when the plugin is enabled"""
        self.logger.info(f"{ColorFormat.GREEN}Builder Shop Plugin enabled!")
        self.register_events(self)
        self.logger.info(f"{ColorFormat.YELLOW}Interact with NPCs tagged 'builder' to open the shop")

    def on_disable(self):
        """Called when the plugin is disabled"""
        self.logger.info(f"{ColorFormat.RED}Builder Shop Plugin disabled!")

    @event_handler
    def on_player_interact_actor(self, event: PlayerInteractActorEvent):
        """Handle player interaction with NPCs"""
        actor = event.actor
        player = event.player

        # Check if the actor has the "builder" tag
        if "builder" in actor.scoreboard_tags:
            event.cancel()  # Prevent default interaction
            self.show_category_menu(player)

    def show_category_menu(self, player):
        """Show the main category selection form"""
        form = ActionForm(
            title=f"{ColorFormat.GOLD}{ColorFormat.BOLD}Builder Shop",
            content=f"{ColorFormat.GRAY}Select a category to browse items.\n{ColorFormat.YELLOW}Each item gives you 128 (or max stack)!"
        )

        # Add a button for each category
        for category in self.BUILDING_MATERIALS.keys():
            form.add_button(
                text=category,
                on_click=lambda p, cat=category: self.show_items_menu(p, cat)
            )

        player.send_form(form)

    def show_items_menu(self, player, category: str):
        """Show items in the selected category"""
        items = self.BUILDING_MATERIALS.get(category, [])

        form = ActionForm(
            title=f"{ColorFormat.GOLD}{ColorFormat.BOLD}{category}",
            content=f"{ColorFormat.GRAY}Click an item to receive it"
        )

        # Add button for each item in category
        for item_id in items:
            # Format the display name (replace underscores with spaces and title case)
            display_name = item_id.replace("_", " ").title()
            form.add_button(
                text=display_name,
                on_click=lambda p, item=item_id: self.give_item(p, item, category)
            )

        # Add back button
        form.add_button(
            text=f"{ColorFormat.RED}← Back to Categories",
            on_click=lambda p: self.show_category_menu(p)
        )

        player.send_form(form)

    def give_item(self, player, item_id: str, category: str):
        """Give the player 128 of the selected item (or max stack size)"""
        try:
            # For most items give 128, but some have smaller stack sizes
            # Items like tools, buckets, etc. stack to 1 or 16
            # Most blocks stack to 64, but we give 128 for convenience
            amount = 128

            # Items that stack to 16 or less
            if any(x in item_id for x in ["bucket", "sign", "banner", "egg", "boat", "minecart", "stew", "soup"]):
                amount = 16
            elif any(x in item_id for x in
                     ["bed", "cake", "armor_stand", "painting", "item_frame", "saddle", "totem", "elytra"]):
                amount = 1
            elif "music_disc" in item_id or item_id in ["dragon_egg", "nether_star", "end_crystal"]:
                amount = 1

            # Use the give command to add items with quoted player name to handle spaces
            command = f'give "{player.name}" {item_id} {amount}'
            self.server.dispatch_command(self.server.command_sender, command)

            # Format display name
            display_name = item_id.replace("_", " ").title()

            # Send success message
            player.send_message(
                f"{ColorFormat.GREEN}✓ You received {ColorFormat.YELLOW}{amount}x {display_name}"
            )

            # Log the transaction
            self.logger.info(
                f"{player.name} received {amount}x {item_id} from Builder Shop"
            )

            # Show the items menu again for convenience
            self.show_items_menu(player, category)

        except Exception as e:
            player.send_error_message(
                f"{ColorFormat.RED}Failed to give item: {str(e)}"
            )
            self.logger.error(f"Error giving item to {player.name}: {str(e)}")
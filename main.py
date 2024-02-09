# sprites
red = sprites.create(assets.image("red player"), SpriteKind.player)
blue = sprites.create(assets.image("blue player"), SpriteKind.enemy)
green = sprites.create(assets.image("green player"), SpriteKind.enemy)
sprites.set_data_image(red, "tile", assets.tile("red"))
sprites.set_data_image(blue, "tile", assets.tile("blue"))
sprites.set_data_image(green, "tile", assets.tile("green"))

# variables
opponent_speed = 75

# setup
info.start_countdown(120)
controller.move_sprite(red)

def setup_map():
    scene.set_tile_map_level(assets.tilemap("level"))
    scene.camera_follow_sprite(red)
    tiles.place_on_random_tile(red, assets.tile("spawn"))
    tiles.set_tile_at(red.tilemap_location(), assets.tile("red"))
    for opponent in sprites.all_of_kind(SpriteKind.enemy):
        tiles.place_on_random_tile(opponent, assets.tile("spawn"))
        tile_image = sprites.read_data_image(opponent, "tile")
        tiles.set_tile_at(opponent.tilemap_location(), tile_image)
        change_opponent_dir(opponent)
setup_map()

def time_up():
    reds = len(tiles.get_tiles_by_type(assets.tile("red")))
    blues = len(tiles.get_tiles_by_type(assets.tile("blue")))
    greens = len(tiles.get_tiles_by_type(assets.tile("green")))
    if reds > blues and reds > greens:
        game.over(True)
    else: 
        game.over(False)
info.on_countdown_end(time_up)

def change_opponent_dir(opponent: Sprite):
    if opponent.vx != 0:
        y_vel = (randint(0, 1) * opponent_speed * 2) - opponent_speed
        opponent.set_velocity(0, y_vel)
    else:
        x_vel = (randint(0, 1) * opponent_speed * 2) - opponent_speed
        opponent.set_velocity(x_vel, 0)

def opponent_hit_wall(opponent, location):
    change_opponent_dir(opponent)
scene.on_hit_wall(SpriteKind.enemy, opponent_hit_wall)

def target_tile_not_owned(opponent: Sprite):
    start = opponent.tilemap_location()
    targets = tilesAdvanced.get_all_tiles_where_wall_is(False)
    tile_image = sprites.read_data_image(opponent, "tile")
    owned_tiles = tiles.get_tiles_by_type(tile_image)
    for target in targets:
        if tilesAdvanced.tile_is_in_list(target, owned_tiles):
            targets.remove_element(target)
    sorted_targets = tilesAdvanced.sort_list_of_tiles_by_distance(start, targets)
    path = scene.a_star(start, sorted_targets[0])
    scene.follow_path(opponent, path, opponent_speed)

def on_path_completion(sprite, location):
    change_opponent_dir(sprite)
scene.on_path_completion(SpriteKind.enemy, on_path_completion)

def opponent_behaviour(opponent: Sprite):
    tile_image = sprites.read_data_image(opponent, "tile")
    tiles.set_tile_at(opponent.tilemap_location(), tile_image)
    if randint(1, 50) == 1:
        change_opponent_dir(opponent)
    elif randint(1, 50) == 1:
        target_tile_not_owned(opponent)

def tick():
    for opponent in sprites.all_of_kind(SpriteKind.enemy):
        opponent_behaviour(opponent)
    tiles.set_tile_at(red.tilemap_location(), assets.tile("red"))
game.on_update(tick)


# stun mechanic
# paint bomb
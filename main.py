# sprites
red = sprites.create(assets.image("red player"), SpriteKind.player)
blue = sprites.create(assets.image("blue player"), SpriteKind.enemy)
green = sprites.create(assets.image("green player"), SpriteKind.enemy)
sprites.set_data_image(red, "tile", assets.tile("red"))
sprites.set_data_image(blue, "tile", assets.tile("blue"))
sprites.set_data_image(green, "tile", assets.tile("green"))
sprites.set_data_number(red, "colour", 3)
sprites.set_data_number(blue, "colour", 6)
sprites.set_data_number(green, "colour", 9)

# variables
opponent_speed = 75
last_vx = 100
last_vy = 0

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
        change_opponent_dir(blue)
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

def fire(sprite: Sprite):
    proj = sprites.create(image.create(4, 4), SpriteKind.projectile)
    colour = sprites.read_data_number(sprite, "colour")
    proj.image.fill(colour)
    proj.set_flag(SpriteFlag.DESTROY_ON_WALL, True)
    proj.set_position(sprite.x, sprite.y)
    proj.lifespan = 5000
    return proj

def player_fire():
    fire(red).set_velocity(last_vx, last_vy)
controller.A.on_event(ControllerButtonEvent.PRESSED, player_fire)

def hit(player, proj):
    if proj.image.get_pixel(0, 0) == sprites.read_data_number(player, "colour"):
        return
    player.say_text("!", 1000)
    for i in range(100):
        tiles.place_on_tile(player, player.tilemap_location())
        pause(10)
    proj.destroy()
sprites.on_overlap(SpriteKind.player, SpriteKind.projectile, hit)
sprites.on_overlap(SpriteKind.enemy, SpriteKind.projectile, hit)

#
def collect_star(player, star):
    tile_image = sprites.read_data_image(player, "tile")
    target_tiles = tilesAdvanced.get_adjacent_tiles(Shapes.SQUARE, star.tilemap_location(), 2)
    for tile in target_tiles:
        if not tiles.tile_at_location_is_wall(tile):
            tiles.set_tile_at(tile, tile_image)
    star.destroy()
sprites.on_overlap(SpriteKind.player, SpriteKind.food, collect_star)
sprites.on_overlap(SpriteKind.enemy, SpriteKind.food, collect_star)
#

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
    if randint(1, 150) == 1:
        proj = fire(opponent)
        proj.set_velocity(opponent.vx * 2, opponent.vy * 2)

#
def spawn_star():
    star = sprites.create(assets.image("star"), SpriteKind.food)
    star.lifespan = 7500
    random_tile = tilesAdvanced.get_all_tiles_where_wall_is(False)._pick_random()
    tiles.place_on_tile(star, random_tile)
    for opponent in sprites.all_of_kind(SpriteKind.enemy):
        if randint(1, 5) == 1:
            path = scene.a_star(opponent.tilemap_location(), star.tilemap_location())
            scene.follow_path(opponent, path, opponent_speed)
game.on_update_interval(10000, spawn_star)
#

def tick():
    global last_vx, last_vy
    if red.vx != 0 or red.vy != 0:
        last_vx = red.vx
        last_vy = red.vy
    for opponent in sprites.all_of_kind(SpriteKind.enemy):
        opponent_behaviour(opponent)
    tiles.set_tile_at(red.tilemap_location(), assets.tile("red"))
game.on_update(tick)

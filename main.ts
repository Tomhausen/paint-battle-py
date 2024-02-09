//  sprites
let red = sprites.create(assets.image`red player`, SpriteKind.Player)
let blue = sprites.create(assets.image`blue player`, SpriteKind.Enemy)
let green = sprites.create(assets.image`green player`, SpriteKind.Enemy)
sprites.setDataImage(red, "tile", assets.tile`red`)
sprites.setDataImage(blue, "tile", assets.tile`blue`)
sprites.setDataImage(green, "tile", assets.tile`green`)
// 
sprites.setDataNumber(red, "colour", 3)
sprites.setDataNumber(blue, "colour", 6)
sprites.setDataNumber(green, "colour", 9)
// 
//  variables
let opponent_speed = 75
// 
let last_vx = 100
let last_vy = 0
// 
//  setup
info.startCountdown(120)
controller.moveSprite(red)
function setup_map() {
    let tile_image: Image;
    scene.setTileMapLevel(assets.tilemap`level`)
    scene.cameraFollowSprite(red)
    tiles.placeOnRandomTile(red, assets.tile`spawn`)
    tiles.setTileAt(red.tilemapLocation(), assets.tile`red`)
    for (let opponent of sprites.allOfKind(SpriteKind.Enemy)) {
        tiles.placeOnRandomTile(opponent, assets.tile`spawn`)
        tile_image = sprites.readDataImage(opponent, "tile")
        tiles.setTileAt(opponent.tilemapLocation(), tile_image)
        change_opponent_dir(blue)
    }
}

setup_map()
info.onCountdownEnd(function time_up() {
    let reds = tiles.getTilesByType(assets.tile`red`).length
    let blues = tiles.getTilesByType(assets.tile`blue`).length
    let greens = tiles.getTilesByType(assets.tile`green`).length
    if (reds > blues && reds > greens) {
        game.over(true)
    } else {
        game.over(false)
    }
    
})
// 
function fire(sprite: Sprite): Sprite {
    let proj = sprites.create(image.create(4, 4), SpriteKind.Projectile)
    let colour = sprites.readDataNumber(sprite, "colour")
    proj.image.fill(colour)
    proj.setFlag(SpriteFlag.DestroyOnWall, true)
    proj.setPosition(sprite.x, sprite.y)
    return proj
}

controller.A.onEvent(ControllerButtonEvent.Pressed, function player_fire() {
    fire(red).setVelocity(last_vx, last_vy)
})
function hit(player: Sprite, proj: Sprite) {
    if (proj.image.getPixel(0, 0) == sprites.readDataNumber(player, "colour")) {
        return
    }
    
    player.sayText("!", 1000)
    for (let i = 0; i < 100; i++) {
        tiles.placeOnTile(player, player.tilemapLocation())
        pause(10)
    }
    proj.destroy()
}

sprites.onOverlap(SpriteKind.Player, SpriteKind.Projectile, hit)
sprites.onOverlap(SpriteKind.Enemy, SpriteKind.Projectile, hit)
// 
function change_opponent_dir(opponent: Sprite) {
    let y_vel: number;
    let x_vel: number;
    if (opponent.vx != 0) {
        y_vel = randint(0, 1) * opponent_speed * 2 - opponent_speed
        opponent.setVelocity(0, y_vel)
    } else {
        x_vel = randint(0, 1) * opponent_speed * 2 - opponent_speed
        opponent.setVelocity(x_vel, 0)
    }
    
}

scene.onHitWall(SpriteKind.Enemy, function opponent_hit_wall(opponent: Sprite, location: tiles.Location) {
    change_opponent_dir(opponent)
})
function target_tile_not_owned(opponent: Sprite) {
    let start = opponent.tilemapLocation()
    let targets = tilesAdvanced.getAllTilesWhereWallIs(false)
    let tile_image = sprites.readDataImage(opponent, "tile")
    let owned_tiles = tiles.getTilesByType(tile_image)
    for (let target of targets) {
        if (tilesAdvanced.tileIsInList(target, owned_tiles)) {
            targets.removeElement(target)
        }
        
    }
    let sorted_targets = tilesAdvanced.sortListOfTilesByDistance(start, targets)
    let path = scene.aStar(start, sorted_targets[0])
    scene.followPath(opponent, path, opponent_speed)
}

scene.onPathCompletion(SpriteKind.Enemy, function on_path_completion(sprite: Sprite, location: tiles.Location) {
    change_opponent_dir(sprite)
})
function opponent_behaviour(opponent: Sprite) {
    let proj: Sprite;
    let tile_image = sprites.readDataImage(opponent, "tile")
    tiles.setTileAt(opponent.tilemapLocation(), tile_image)
    if (randint(1, 50) == 1) {
        change_opponent_dir(opponent)
    } else if (randint(1, 50) == 1) {
        target_tile_not_owned(opponent)
    }
    
    // 
    if (randint(1, 150) == 1) {
        proj = fire(opponent)
        proj.setVelocity(opponent.vx * 2, opponent.vy * 2)
    }
    
}

// 
game.onUpdate(function tick() {
    // 
    
    if (red.vx != 0 || red.vy != 0) {
        last_vx = red.vx
        last_vy = red.vy
    }
    
    // 
    for (let opponent of sprites.allOfKind(SpriteKind.Enemy)) {
        opponent_behaviour(opponent)
    }
    tiles.setTileAt(red.tilemapLocation(), assets.tile`red`)
})

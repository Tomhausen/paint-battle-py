// Auto-generated code. Do not edit.
namespace myTiles {
    //% fixedInstance jres blockIdentity=images._tile
    export const transparency16 = image.ofBuffer(hex``);
    //% fixedInstance jres blockIdentity=images._tile
    export const tile1 = image.ofBuffer(hex``);
    //% fixedInstance jres blockIdentity=images._tile
    export const tile3 = image.ofBuffer(hex``);
    //% fixedInstance jres blockIdentity=images._tile
    export const tile4 = image.ofBuffer(hex``);
    //% fixedInstance jres blockIdentity=images._tile
    export const tile2 = image.ofBuffer(hex``);
    //% fixedInstance jres blockIdentity=images._tile
    export const tile5 = image.ofBuffer(hex``);

    helpers._registerFactory("tilemap", function(name: string) {
        switch(helpers.stringTrim(name)) {
            case "level":
            case "level1":return tiles.createTilemap(hex`18001800010101010101010101010101010101010101010101010101010203030303030303030303010303030303030303030301010303030303030303030303010303030303030303030301010303030303030303030303010303030303030303030301010303030101010103030101010103030101010303030301010303030103030303030303030303030303030303030301010303030103030303030303030303030303030303030301010303030103030101030303010101030303010303030301010303030103030301030303010101030303010303030301010303030303030301030303030303030303010303030301010303030303030301010303030303030303010103030301010303030103030303030303020103030303030303030301010303030103030303030303030103030303030303030301010303030103030303030303030103030303030301010101010101010101010101030301010101010303030303030301010303030303030303030303030303010303030303030301010303030303030303030303030303030303030301030301010303030303030303030303030303030303030301030301010303030103030301010101010103030303030301030301010303030103030301030303030303030301010101030301010303030101030101030303030303030301030303030301010303030303030303030303010103030303030303030301010303030303030303030301010101030303030303030201010101010101010101010101010101010101010101010101`, img`
222222222222222222222222
2...........2..........2
2...........2..........2
2...........2..........2
2...2222..2222..222....2
2...2..................2
2...2..................2
2...2..22...222...2....2
2...2...2...222...2....2
2.......2.........2....2
2.......22........22...2
2...2........2.........2
2...2........2.........2
2...2........2......2222
222222222..22222.......2
2..............2.......2
2...................2..2
2...................2..2
2...2...222222......2..2
2...2...2........2222..2
2...22.22........2.....2
2...........22.........2
2..........2222........2
222222222222222222222222
`, [myTiles.transparency16,sprites.builtin.brick,myTiles.tile1,myTiles.tile2], TileScale.Sixteen);
        }
        return null;
    })

    helpers._registerFactory("tile", function(name: string) {
        switch(helpers.stringTrim(name)) {
            case "transparency16":return transparency16;
            case "spawn":
            case "tile1":return tile1;
            case "red":
            case "tile3":return tile3;
            case "blue":
            case "tile4":return tile4;
            case "blank":
            case "tile2":return tile2;
            case "green":
            case "tile5":return tile5;
        }
        return null;
    })

}
// Auto-generated code. Do not edit.

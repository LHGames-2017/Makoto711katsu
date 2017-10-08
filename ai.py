from flask import Flask, request
from structs import *
import json
import numpy

app = Flask(__name__)

def create_action(action_type, target):
    actionContent = ActionContent(action_type, target.__dict__)
    return json.dumps(actionContent.__dict__)

def create_move_action(target):
    return create_action("MoveAction", target)

def create_attack_action(target):
    return create_action("AttackAction", target)

def create_collect_action(target):
    return create_action("CollectAction", target)

def create_steal_action(target):
    return create_action("StealAction", target)

def create_heal_action():
    return create_action("HealAction", "")

def create_purchase_action(item):
    return create_action("PurchaseAction", item)

def deserialize_map(serialized_map):
    """
    Fonction utilitaire pour comprendre la map
    """
    serialized_map = serialized_map[1:]
    rows = serialized_map.split('[')
    column = rows[0].split('{')
    deserialized_map = [[Tile() for x in range(40)] for y in range(40)]
    for i in range(len(rows) - 1):
        column = rows[i + 1].split('{')

        for j in range(len(column) - 1):
            infos = column[j + 1].split(',')
            end_index = infos[2].find('}')
            content = int(infos[0])
            x = int(infos[1])
            y = int(infos[2][:end_index])
            deserialized_map[i][j] = Tile(content, x, y)

    return deserialized_map

def bot():
    """
    Main de votre bot.
    """
    map_json = request.form["map"]

    # Player info

    encoded_map = map_json.encode()
    map_json = json.loads(encoded_map)
    p = map_json["Player"]
    pos = p["Position"]
    x = pos["X"]
    y = pos["Y"]
    house = p["HouseLocation"]
    player = Player(p["Health"], p["MaxHealth"], Point(x,y),
                    Point(house["X"], house["Y"]), p["Score"],
                    p["CarriedResources"], p["CarryingCapacity"])

    # Map
    serialized_map = map_json["CustomSerializedMap"]
    deserialized_map = deserialize_map(serialized_map)
    print(deserialized_map[28][35].Content)
    otherPlayers = []

    for players in map_json["OtherPlayers"]:
        player_info = players["Value"]
        p_pos = player_info["Position"]
        player_info = PlayerInfo(player_info["Health"],
                                     player_info["MaxHealth"],
                                     Point(p_pos["X"], p_pos["Y"]))

        otherPlayers.append(player_info)
    displayMap(deserialized_map, x, y)

    print("Player: hp = " + repr(player.Health) + ", carried resources = " + repr(player.CarriedRessources) + ")")

    nodes = findNodes(deserialized_map)

    nodesPos = []

    for i in range(0, nodes.__len__()):
        nodesPos.append(Point(nodes[i].X, nodes[i].Y))



    print(player.CarryingCapacity == player.CarriedRessources)

    print(player.HouseLocation.X)
    print(player.HouseLocation.Y)


    if player.CarriedRessources == player.CarryingCapacity:
        decision = moveTo(Point(x, y), player.HouseLocation, deserialized_map)
    else:
        nearestNode = getNearestPoint(Point(x, y), nodesPos)
        decision = moveTo(Point(x, y), nearestNode, deserialized_map)

    print(deserialized_map[28][35].Content)

    print(decision)

    # return decision
    return decision

def moveTo(playerPos, destination, map):

    newX = int(destination.X - playerPos.X)
    newY = int(destination.Y - playerPos.Y)

    #distance plus courte sur l'axe des x
    if abs((newX) - abs(newY) < 0 or newY == 0) and newX != 0:
        newX = int(newX / abs(newX))
        newPos = Point(playerPos.X + newX, playerPos.Y)

        print(map[newPos.X][newPos.Y].Content)
        if map[newPos.X][newPos.Y].Content == TileContent.Wall:
            return create_attack_action(newPos)
        elif map[newPos.X][newPos.Y].Content == TileContent.Resource:
            return create_collect_action(newPos)
        else:
            return create_move_action(newPos)

    #distance plus courte sur l'axe des y
    elif abs(newX) - abs(newY) < 0 and newY != 0:
        newY = int(newY / abs(newY))
        newPos = Point(playerPos.X, playerPos.Y + newY)

        print(map[newPos.X][newPos.Y].Content)

        if map[newPos.X][newPos.Y].Content == TileContent.Wall:
            return create_attack_action(newPos)
        elif map[newPos.X][newPos.Y].Content == TileContent.Resource:
            create_collect_action(newPos)
        else:
            return create_move_action(newPos)

    else:
        return create_move_action(Point(playerPos.X, playerPos.Y))

def displayMap(deserialized_map, x, y):

    for i in range(0, 19):
        if i is 0:
            print(end="   ")

        if deserialized_map[i][0].X is 0:
            print(end=" X ")
        elif (deserialized_map[i][0].X / 10) < 1:
            print(end=" ")
            print(deserialized_map[i][0].X, end=" ")
        else:
            print(deserialized_map[i][0].X, end=" ")
    print()

    for i in range(0, 19):
        for j in range(0, 19):
            if j is 0:
                if deserialized_map[i][j].Y is 0:
                    print(end=" X ")
                elif deserialized_map[j][i].Y / 10 < 1:
                    print(end=" ")
                    print(deserialized_map[j][i].Y, end=" ")
                else:
                    print(deserialized_map[j][i].Y, end=" ")
            if deserialized_map[j][i].X == x and deserialized_map[j][i].Y == y:
                print(end=" M ")
            elif deserialized_map[j][i].Content is None:
                    print(end=" - ")
            else:
                print(end=" ")
                if deserialized_map[j][i].Content is 0:
                    print(" ", end=" ")
                elif deserialized_map[j][i].Content is 1:
                    print("+", end=" ")
                elif deserialized_map[j][i].Content is 2:
                    print("H", end=" ")
                elif deserialized_map[j][i].Content is 3:
                    print("_", end=" ")
                elif deserialized_map[j][i].Content is 4:
                    print("R", end=" ")
                elif deserialized_map[j][i].Content is 5:
                    print("S", end=" ")
                elif deserialized_map[j][i].Content is 6:
                    print("P", end=" ")

        print(end="\n")

def findNodes(map):

    nodes = []

    for row in range(0, map.__len__()):
        for col in range(0, map[row].__len__()):
            if(map[row][col].Content is TileContent.Resource):
                nodes.append(map[row][col])

    return nodes

def getNearestPoint(point, points):

    min = Point.Distance(point, points[0])
    minPos = 0

    for i in range(0, points.__len__()):
        currentDistance = Point.Distance(point, points[i])
        if currentDistance < min:
            min = currentDistance
            minPos = i

    return points[minPos]

@app.route("/", methods=["POST"])
def reponse():
    """
    Point d'entree appelle par le GameServer
    """
    return bot()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

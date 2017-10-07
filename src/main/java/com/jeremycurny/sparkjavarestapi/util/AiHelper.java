package com.jeremycurny.sparkjavarestapi.util;

import java.util.ArrayList;
import java.util.List;

public class AiHelper {

    public static String CreateStealAction(Point position) {
        return CreateAction("StealAction", position);
    }

    public static String CreateAttackAction(Point position) {
        return CreateAction("AttackAction", position);
    }

    public static String CreateCollectAction(Point position) {
        return CreateAction("CollectAction", position);
    }

    public static String CreateMoveAction(Point newPosition) {
        return CreateAction("MoveAction", newPosition);
    }

    public static String CreateUpgradeAction(UpgradeType upgrade) {
        return (new ActionContent("UpgradeAction", upgrade)).toJson();
    }

    public static String CreatePurchaseAction(PurchasableItem item) {
        return (new ActionContent("PurchaseAction", item)).toJson();
    }

    public static String CreateHealAction() {
        return (new ActionContent("HealAction")).toJson();
    }

    private static String CreateAction(String name, Point target) {
        return (new ActionContent(name, target)).toJson();
    }

    public static List<List<Tile>> deserializeMap(String serializedMap) {
        serializedMap = serializedMap.substring(1, serializedMap.length() - 1);
        String[] rows = serializedMap.split("\\[");
        List<List<Tile>> map = new ArrayList<>();
        for (int i = 0; i < rows.length; ++i) {
            map.add(new ArrayList<>());
        }

        String[] column;
        for (int i = 0; i < rows.length - 1; i++) {
            column = rows[i + 1].split("\\{");
            for (int j = 0; j < column.length - 1; j++)
            {
                String[] infos = column[j + 1].split(",");
                map.get(j).add(
                        new Tile(
                                Integer.parseInt(infos[0]),
                                Integer.parseInt(infos[1]),
                                Integer.parseInt((infos[2].substring(0, infos[2].indexOf('}'))))));
            }
        }
        return map;
    }
}

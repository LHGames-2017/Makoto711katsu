package com.jeremycurny.sparkjavarestapi.util;

import org.json.simple.JSONObject;

public class ActionContent {
    public String ActionName;
    public String Content;

    public ActionContent(String name, Point content) {
        ActionName = name;
        Content = content.toJson();
    }

    public ActionContent(String name, UpgradeType content) {
        ActionName = name;
        Content = content.toString();
    }

    public ActionContent(String name, PurchasableItem content) {
        ActionName = name;
        Content = content.toString();
    }

    public ActionContent(String name) {
        ActionName = name;
        Content = "";
    }

    public String toJson() {
        JSONObject obj = new JSONObject();

        obj.put("ActionName", ActionName);
        if (!Content.isEmpty()) {
            obj.put("Content", Content);
        }

        return obj.toJSONString();
    }
}

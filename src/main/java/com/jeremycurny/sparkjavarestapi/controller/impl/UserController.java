package com.jeremycurny.sparkjavarestapi.controller.impl;

import com.jeremycurny.sparkjavarestapi.controller.RestController;
import com.jeremycurny.sparkjavarestapi.util.*;

import java.net.URLDecoder;
import java.util.List;

import spark.Request;
import spark.Response;

public class UserController extends RestController {

	@Override
	public Object bot(Request req, Response res) {
		String s = URLDecoder.decode(req.body()).substring(4);
		GameInfo gameInfo = new GameInfo();
		gameInfo.fromJson(s);

		// AI IMPLEMENTATION HERE.

		List<List<Tile>> map = gameInfo.map;
		System.out.println("Player:" + gameInfo.player.Position.x + ", " + gameInfo.player.Position.y);

		for(int row = 0; row < map.size(); row++) {

			for(int col = 0; col < map.get(row).size(); col++) {

				int content = map.get(row).get(col).Content;

				System.out.print(content + ", ");

			}

			System.out.println();

		}

		System.out.println("House:" + gameInfo.player.HouseLocation.x + ", " + gameInfo.player.HouseLocation.y);

		AiHelper.CreateMoveAction(new Point(25+-1,27));

		String action = AiHelper.CreateMoveAction(gameInfo.player.Position);
	    return super.resJson(req, res, 200, action);
	}
}

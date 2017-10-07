package com.jeremycurny.sparkjavarestapi.controller;

import spark.Request;
import spark.Response;

abstract public class RestController {

	public abstract Object bot(Request req, Response res);

	protected String resJson(Request req, Response res, int httpStatus, String action) {
		res.type("application/json");
		res.status(httpStatus);
		return action;
	}

}

package com.jeremycurny.sparkjavarestapi.app;

import static spark.Spark.*;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.jeremycurny.sparkjavarestapi.controller.impl.UserController;

import spark.Spark;

public class App {

	public static void main(String[] args) {

		UserController userController = new UserController();

		port(3000);

		before((req, res) -> {
			res.header("Access-Control-Allow-Headers", "Authorization, Content-Type");
			res.header("Access-Control-Allow-Methods", "POST");
			res.header("Access-Control-Allow-Origin", "*");
		});

		post("/", (req, res) -> userController.bot(req, res));

		exception(Exception.class, (e, req, res) -> {
			String message = e.getClass().getName() + ": " + e.getMessage();
			res.type("application/json");
			res.status(500);
			res.body(message);
		});
	}
}

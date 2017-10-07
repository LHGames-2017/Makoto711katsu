FROM polyhx/java-seed

ADD . .

EXPOSE 3000

RUN mvn clean package

CMD ["java", "-jar", "target/lhgames-java-server-1.0.0.jar"]
